import os
import requests
import json
import base64
import logging
from data_store import DataStore

class VirtualTAAPI:
    """Virtual Teaching Assistant API handler"""
    
    def __init__(self):
        self.aipipe_token = os.environ.get("AIPIPE_TOKEN", "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIyZjMwMDExMzVAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.SxLN3zTAfCsfLBKi2wpFR6-YdKRNPGDpVAzlAxNO48I")
        self.data_store = DataStore()
        self.logger = logging.getLogger(__name__)
        
    def process_question(self, question, image_base64=None):
        """Process student question and return structured response"""
        try:
            # Search for relevant content
            relevant_content = self.data_store.search_content(question)
            
            # Prepare context for AI
            context = self._prepare_context(question, relevant_content, image_base64)
            
            # Get AI response
            ai_response = self._get_ai_response(context)
            
            # Extract answer and find relevant links
            answer = self._extract_answer(ai_response)
            links = self._find_relevant_links(question, relevant_content)
            
            return {
                "answer": answer,
                "links": links
            }
            
        except Exception as e:
            self.logger.error(f"Error processing question: {str(e)}")
            return {
                "answer": "I apologize, but I'm having trouble processing your question right now. Please try again later.",
                "links": []
            }
    
    def _prepare_context(self, question, relevant_content, image_base64=None):
        """Prepare context for AI model"""
        # Determine if we have specific relevant content
        has_relevant_content = relevant_content.get('query_matched', False)
        
        if has_relevant_content:
            context = f"""You are a Virtual Teaching Assistant for the Tools in Data Science (TDS) course at IIT Madras Online Degree Program.

Student Question: {question}

RELEVANT COURSE MATERIAL:
{relevant_content.get('course_content', '')}

RELEVANT DISCOURSE DISCUSSIONS:
{relevant_content.get('discourse_posts', '')}

Instructions:
1. Answer the student's specific question directly and clearly
2. Use the provided course material and discourse discussions to give accurate, contextual information
3. If the question relates to programming, provide practical examples
4. If the question is about tools or concepts, explain them step-by-step
5. Keep your answer focused on the TDS course context
6. Be specific and avoid generic responses"""
        else:
            # For questions without specific matches, provide general TDS guidance
            context = f"""You are a Virtual Teaching Assistant for the Tools in Data Science (TDS) course at IIT Madras Online Degree Program.

Student Question: {question}

The question doesn't match specific course content in our database, but you should still provide helpful guidance based on your knowledge of:
- Python programming fundamentals
- Data science tools (pandas, numpy, matplotlib, jupyter)
- Version control with Git
- Data analysis and visualization
- Machine learning basics
- Best practices in data science workflows

Instructions:
1. Answer the student's question as it relates to the TDS course
2. Provide practical, actionable advice
3. Include specific examples or code snippets when relevant
4. Suggest relevant tools or approaches commonly used in data science
5. Keep the answer educational and appropriate for a data science student"""

        if image_base64:
            context += f"\n\nNOTE: The student has provided an image attachment. Please analyze it and incorporate any relevant visual information into your response."
        
        return context
    
    def _get_ai_response(self, context):
        """Get response from AI Pipe"""
        try:
            headers = {
                "Authorization": f"Bearer {self.aipipe_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert Teaching Assistant for the Tools in Data Science (TDS) course at IIT Madras. Your responses should be educational, practical, and specific to each question. Always provide concrete examples and actionable advice."
                    },
                    {
                        "role": "user",
                        "content": context
                    }
                ],
                "max_tokens": 1500,
                "temperature": 0.3
            }
            
            response = requests.post(
                "https://aipipe.org/openrouter/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                self.logger.error(f"AI API error: {response.status_code} - {response.text}")
                return "I'm having trouble connecting to the AI service. Please try again later."
                
        except Exception as e:
            self.logger.error(f"Error calling AI API: {str(e)}")
            return "I'm currently experiencing technical difficulties. Please try again later."
    
    def _extract_answer(self, ai_response):
        """Extract and format the answer from AI response"""
        if not ai_response:
            return "I apologize, but I couldn't generate a response. Please try rephrasing your question."
        
        return ai_response.strip()
    
    def _find_relevant_links(self, question, relevant_content):
        """Find relevant discourse links based on question and content"""
        links = []
        
        # Get discourse posts from relevant content
        discourse_posts = relevant_content.get('discourse_posts_detailed', [])
        
        # Score and select most relevant posts
        for post in discourse_posts[:3]:  # Limit to top 3 most relevant
            links.append({
                "url": post.get('url', '#'),
                "text": post.get('title', 'Relevant Discussion')
            })
        
        return links