import requests
import json
import logging
from datetime import datetime, timedelta
import trafilatura
from urllib.parse import urljoin
import time

class DiscourseScraperTDS:
    """Scraper for TDS Discourse posts"""
    
    def __init__(self):
        self.base_url = "https://discourse.onlinedegree.iitm.ac.in"
        self.logger = logging.getLogger(__name__)
        
    def scrape_posts(self, start_date, end_date):
        """Scrape discourse posts between given dates"""
        try:
            # Convert string dates to datetime objects
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            
            posts = []
            
            # Since we can't actually scrape without authentication,
            # we'll create a mock scraper that returns sample data
            # In a real implementation, this would use the Discourse API
            
            sample_posts = self._get_sample_posts()
            
            # Filter posts by date range (in real implementation)
            for post in sample_posts:
                post_date = datetime.strptime(post['date'], '%Y-%m-%d')
                if start_dt <= post_date <= end_dt:
                    posts.append(post)
            
            self.logger.info(f"Scraped {len(posts)} posts from {start_date} to {end_date}")
            return posts
            
        except Exception as e:
            self.logger.error(f"Error scraping posts: {str(e)}")
            return []
    
    def _get_sample_posts(self):
        """Return sample TDS discourse posts for development"""
        return [
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
                "content": "For setting up Python environment, make sure to use conda or venv. Install required packages using pip install -r requirements.txt",
                "date": "2025-04-08",
                "category": "technical-help",
                "tags": ["python", "setup", "environment"]
            },
            {
                "id": "155941",
                "title": "Data Preprocessing Best Practices",
                "url": "https://discourse.onlinedegree.iitm.ac.in/t/data-preprocessing-best-practices/155941",
                "content": "When preprocessing data, always check for missing values, outliers, and data types. Use pandas for data manipulation and sklearn for preprocessing.",
                "date": "2025-04-05",
                "category": "general",
                "tags": ["preprocessing", "pandas", "sklearn"]
            },
            {
                "id": "155942",
                "title": "Git and Version Control",
                "url": "https://discourse.onlinedegree.iitm.ac.in/t/git-and-version-control/155942",
                "content": "Use git for version control. Essential commands: git add, git commit, git push, git pull. Create meaningful commit messages.",
                "date": "2025-03-28",
                "category": "tools",
                "tags": ["git", "version-control", "github"]
            },
            {
                "id": "155943",
                "title": "Jupyter Notebook Tips",
                "url": "https://discourse.onlinedegree.iitm.ac.in/t/jupyter-notebook-tips/155943",
                "content": "Use Jupyter notebooks for data exploration. Remember to restart kernel when needed. Use markdown cells for documentation.",
                "date": "2025-03-25",
                "category": "tools",
                "tags": ["jupyter", "notebook", "data-science"]
            }
        ]
    
    def scrape_specific_post(self, post_url):
        """Scrape content from a specific discourse post"""
        try:
            # Use trafilatura to extract text content
            downloaded = trafilatura.fetch_url(post_url)
            if downloaded:
                text = trafilatura.extract(downloaded)
                return text
            return None
            
        except Exception as e:
            self.logger.error(f"Error scraping post {post_url}: {str(e)}")
            return None