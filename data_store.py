import json
import os
import logging
from datetime import datetime

class DataStore:
    """In-memory data store for TDS content and discourse posts"""
    
    def __init__(self):
        self.course_content = self._load_course_content()
        self.discourse_posts = []
        self.logger = logging.getLogger(__name__)
        # Load sample discourse posts automatically
        self._load_sample_discourse_posts()
        
    def _load_course_content(self):
        """Load TDS course content"""
        return {
            "python_basics": {
                "title": "Python Programming Basics",
                "content": "Python is a high-level programming language. Key concepts include variables, data types, functions, classes, and modules. Use proper naming conventions and follow PEP 8 style guide.",
                "keywords": ["python", "programming", "variables", "functions", "classes", "pep8"]
            },
            "data_structures": {
                "title": "Data Structures in Python",
                "content": "Important data structures include lists, tuples, dictionaries, and sets. Lists are mutable and ordered, tuples are immutable, dictionaries store key-value pairs, sets contain unique elements.",
                "keywords": ["list", "tuple", "dictionary", "set", "data structures", "mutable", "immutable"]
            },
            "pandas": {
                "title": "Data Manipulation with Pandas",
                "content": "Pandas provides DataFrame and Series objects for data manipulation. Key operations include filtering with df[condition], grouping with df.groupby(), merging with pd.merge(), and reading CSV files with pd.read_csv().",
                "keywords": ["pandas", "dataframe", "series", "data manipulation", "csv", "groupby", "merge"]
            },
            "numpy": {
                "title": "Numerical Computing with NumPy",
                "content": "NumPy provides efficient array operations and mathematical functions. Create arrays with np.array(), perform element-wise operations, use broadcasting for different sized arrays.",
                "keywords": ["numpy", "array", "numerical", "mathematical", "scientific computing", "broadcasting"]
            },
            "matplotlib": {
                "title": "Data Visualization with Matplotlib",
                "content": "Matplotlib is used for creating static, animated, and interactive visualizations. Use plt.plot() for line plots, plt.scatter() for scatter plots, plt.bar() for bar charts. Always add labels and titles.",
                "keywords": ["matplotlib", "visualization", "plot", "chart", "graph", "scatter", "bar"]
            },
            "git": {
                "title": "Version Control with Git",
                "content": "Git is a distributed version control system. Essential commands include git add (stage changes), git commit (save changes), git push (upload to remote), git pull (download from remote), git clone (copy repository).",
                "keywords": ["git", "version control", "repository", "commit", "branch", "clone", "push", "pull"]
            },
            "jupyter": {
                "title": "Jupyter Notebooks",
                "content": "Jupyter notebooks provide an interactive computing environment for data science and research. Install with 'pip install jupyter', start with 'jupyter notebook'. Use markdown cells for documentation.",
                "keywords": ["jupyter", "notebook", "interactive", "data science", "research", "markdown", "kernel"]
            },
            "machine_learning": {
                "title": "Introduction to Machine Learning",
                "content": "Machine learning involves algorithms that learn patterns from data. Supervised learning uses labeled data, unsupervised learning finds patterns in unlabeled data, reinforcement learning learns through rewards.",
                "keywords": ["machine learning", "supervised", "unsupervised", "algorithm", "model", "reinforcement"]
            },
            "virtual_environment": {
                "title": "Python Virtual Environments",
                "content": "Virtual environments isolate Python projects and their dependencies. Use 'python -m venv myenv' to create, 'source myenv/bin/activate' (Linux/Mac) or 'myenv\\Scripts\\activate' (Windows) to activate. Install packages with pip after activation.",
                "keywords": ["virtual environment", "venv", "python", "dependencies", "pip", "activate", "isolate"]
            },
            "api_development": {
                "title": "API Development with Flask",
                "content": "APIs (Application Programming Interfaces) allow different software systems to communicate. Flask is used to create REST APIs with endpoints that handle HTTP requests (GET, POST, PUT, DELETE). Use @app.route decorators to define endpoints and return JSON responses.",
                "keywords": ["api", "flask", "rest", "endpoint", "http", "route", "json", "post", "get"]
            },
            "data_preprocessing": {
                "title": "Data Preprocessing Techniques",
                "content": "Data preprocessing involves cleaning and preparing raw data for analysis. Key steps include handling missing values with fillna() or dropna(), removing duplicates with drop_duplicates(), data type conversion with astype(), normalization, and feature scaling using sklearn.",
                "keywords": ["preprocessing", "cleaning", "missing values", "duplicates", "normalization", "scaling", "fillna", "dropna"]
            }
        }
    
    def _load_sample_discourse_posts(self):
        """Load sample discourse posts automatically"""
        sample_posts = [
            {
                "id": "155939",
                "title": "GA5 Question 8 Clarification",
                "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939",
                "content": "Use the model that's mentioned in the question. My understanding is that you just have to use a tokenizer, similar to what Prof. Anand used, to get the number of tokens and multiply that by the given rate.",
                "date": "2025-04-10",
                "category": "assignments",
                "tags": ["gpt", "tokenizer", "assignment"]
            },
            {
                "id": "155940",
                "title": "Python Environment Setup Issues",
                "url": "https://discourse.onlinedegree.iitm.ac.in/t/python-environment-setup-issues/155940",
                "content": "For setting up Python environment, make sure to use conda or venv. Install required packages using pip install -r requirements.txt. Create virtual environment with 'python -m venv myenv' and activate with 'source myenv/bin/activate'",
                "date": "2025-04-08",
                "category": "technical-help",
                "tags": ["python", "setup", "environment", "venv", "conda"]
            },
            {
                "id": "155941",
                "title": "Data Preprocessing Best Practices",
                "url": "https://discourse.onlinedegree.iitm.ac.in/t/data-preprocessing-best-practices/155941",
                "content": "When preprocessing data, always check for missing values, outliers, and data types. Use pandas for data manipulation and sklearn for preprocessing. Handle missing data with fillna() or dropna(), detect outliers using IQR method.",
                "date": "2025-04-05",
                "category": "general",
                "tags": ["preprocessing", "pandas", "sklearn", "missing values", "outliers"]
            },
            {
                "id": "155942",
                "title": "Git and Version Control",
                "url": "https://discourse.onlinedegree.iitm.ac.in/t/git-and-version-control/155942",
                "content": "Use git for version control. Essential commands: git add, git commit, git push, git pull. Create meaningful commit messages. Use branches for feature development. Clone repositories with git clone <url>.",
                "date": "2025-03-28",
                "category": "tools",
                "tags": ["git", "version-control", "github", "commit", "branch"]
            },
            {
                "id": "155943",
                "title": "Jupyter Notebook Tips",
                "url": "https://discourse.onlinedegree.iitm.ac.in/t/jupyter-notebook-tips/155943",
                "content": "Use Jupyter notebooks for data exploration. Remember to restart kernel when needed. Use markdown cells for documentation. Install with 'pip install jupyter' and start with 'jupyter notebook'.",
                "date": "2025-03-25",
                "category": "tools",
                "tags": ["jupyter", "notebook", "data-science", "kernel", "markdown"]
            },
            {
                "id": "155944",
                "title": "Flask API Development Tutorial",
                "url": "https://discourse.onlinedegree.iitm.ac.in/t/flask-api-development-tutorial/155944",
                "content": "Creating APIs with Flask is straightforward. Use @app.route('/api/', methods=['POST']) for POST endpoints. Handle JSON data with request.get_json(). Return JSON responses with jsonify(). Always validate input data.",
                "date": "2025-03-20",
                "category": "programming",
                "tags": ["flask", "api", "json", "route", "endpoint", "post"]
            },
            {
                "id": "155945",
                "title": "Pandas DataFrame Operations",
                "url": "https://discourse.onlinedegree.iitm.ac.in/t/pandas-dataframe-operations/155945",
                "content": "DataFrames are the core of pandas. Create with pd.DataFrame(), read CSV with pd.read_csv(). Filter data with df[df['column'] > value]. Group data with df.groupby(). Merge DataFrames with pd.merge().",
                "date": "2025-03-15",
                "category": "data-analysis",
                "tags": ["pandas", "dataframe", "csv", "filter", "groupby", "merge"]
            }
        ]
        self.discourse_posts.extend(sample_posts)
        self.logger.info(f"Loaded {len(sample_posts)} sample discourse posts")
    
    def add_discourse_posts(self, posts):
        """Add discourse posts to the data store"""
        self.discourse_posts.extend(posts)
        self.logger.info(f"Added {len(posts)} discourse posts to data store")
    
    def search_content(self, query):
        """Search for relevant content based on query"""
        query_lower = query.lower()
        query_words = [word.strip() for word in query_lower.split() if len(word.strip()) > 2]
        
        # Search course content with scoring
        relevant_course_content = []
        course_scores = {}
        
        for topic_id, topic_data in self.course_content.items():
            score = 0
            
            # Check exact keyword matches (higher score)
            for keyword in topic_data['keywords']:
                if keyword.lower() in query_lower:
                    score += 10
            
            # Check word matches in content and title (medium score)
            for word in query_words:
                if word in topic_data['content'].lower():
                    score += 3
                if word in topic_data['title'].lower():
                    score += 5
            
            # Check partial matches (lower score)
            for word in query_words:
                for keyword in topic_data['keywords']:
                    if word in keyword.lower() or keyword.lower() in word:
                        score += 2
            
            if score > 0:
                course_scores[topic_id] = score
        
        # Sort by score and take top results
        sorted_topics = sorted(course_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        
        for topic_id, score in sorted_topics:
            topic_data = self.course_content[topic_id]
            relevant_course_content.append(f"**{topic_data['title']}**: {topic_data['content']}")
        
        # Search discourse posts with scoring
        relevant_discourse_posts = []
        relevant_discourse_posts_detailed = []
        post_scores = {}
        
        for i, post in enumerate(self.discourse_posts):
            score = 0
            
            # Check matches in title (high score)
            for word in query_words:
                if word in post['title'].lower():
                    score += 8
            
            # Check matches in content (medium score)
            for word in query_words:
                if word in post['content'].lower():
                    score += 4
            
            # Check matches in tags (high score)
            for tag in post.get('tags', []):
                for word in query_words:
                    if word in tag.lower() or tag.lower() in word:
                        score += 6
            
            # Check exact phrase matches (very high score)
            if any(phrase in post['title'].lower() or phrase in post['content'].lower() 
                   for phrase in [query_lower]):
                score += 15
            
            if score > 0:
                post_scores[i] = score
        
        # Sort by score and take top results
        sorted_posts = sorted(post_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        
        for post_idx, score in sorted_posts:
            post = self.discourse_posts[post_idx]
            relevant_discourse_posts.append(f"**{post['title']}**: {post['content']}")
            relevant_discourse_posts_detailed.append(post)
        
        return {
            'course_content': '\n\n'.join(relevant_course_content) if relevant_course_content else "No specific course content found for this query.",
            'discourse_posts': '\n\n'.join(relevant_discourse_posts) if relevant_discourse_posts else "No relevant discourse posts found for this query.",
            'discourse_posts_detailed': relevant_discourse_posts_detailed,
            'query_matched': len(relevant_course_content) > 0 or len(relevant_discourse_posts) > 0
        }
    
    def get_all_posts(self):
        """Get all discourse posts"""
        return self.discourse_posts
    
    def get_course_topics(self):
        """Get all course topics"""
        return list(self.course_content.keys())