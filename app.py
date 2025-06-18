import os
import logging
from flask import Flask, render_template, request, jsonify
from flask.logging import default_handler
import requests
import base64
import json
from datetime import datetime
from api import VirtualTAAPI
from scraper import DiscourseScraperTDS
from data_store import DataStore
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
CORS(app)

# Initialize components
data_store = DataStore()
scraper = DiscourseScraperTDS()
virtual_ta = VirtualTAAPI()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            if not request.is_json:
                return jsonify({"error": "Content-Type must be application/json"}), 400

            data = request.get_json()
            if not data or 'question' not in data:
                return jsonify({"error": "Question is required"}), 400

            question = data.get('question', '').strip()
            image_base64 = data.get('image', '')

            if not question:
                return jsonify({"error": "Question cannot be empty"}), 400

            app.logger.info(f"Received question (via root POST): {question[:100]}...")
            response = virtual_ta.process_question(question, image_base64)
            return jsonify(response)

        except Exception as e:
            app.logger.error(f"Root POST error: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500

    # If GET, show UI
    return render_template('index.html')

@app.route('/api/', methods=['GET','POST'])
def api_endpoint():
    """Main API endpoint for Virtual TA"""
    try:
        # Validate request
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({"error": "Question is required"}), 400
        
        question = data.get('question', '').strip()
        image_base64 = data.get('image', '')
        
        if not question:
            return jsonify({"error": "Question cannot be empty"}), 400
        
        # Log the request
        app.logger.info(f"Received question: {question[:100]}...")
        
        # Process the question
        response = virtual_ta.process_question(question, image_base64)
        
        return jsonify(response)
        
    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/scrape', methods=['GET','POST'])
def scrape_endpoint():
    """Endpoint to trigger scraping of Discourse posts"""
    try:
        data = request.get_json()
        start_date = data.get('start_date', '2025-01-01')
        end_date = data.get('end_date', '2025-04-14')
        
        # Scrape discourse posts
        posts = scraper.scrape_posts(start_date, end_date)
        
        # Store in data store
        data_store.add_discourse_posts(posts)
        
        return jsonify({
            "message": f"Successfully scraped {len(posts)} posts",
            "posts_count": len(posts)
        })
        
    except Exception as e:
        app.logger.error(f"Error scraping posts: {str(e)}")
        return jsonify({"error": "Failed to scrape posts"}), 500

@app.route('/health',  methods=['GET','POST'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
