# TDS Virtual Teaching Assistant

A Flask-based Virtual Teaching Assistant API that answers student questions about the Tools in Data Science course using AI integration.

## Features

- **REST API**: Accept POST requests with student questions and optional image attachments
- **AI Integration**: Uses AI Pipe for intelligent responses
- **Content Search**: Searches through course content and discourse posts
- **Web Interface**: Simple HTML interface for testing the API
- **Discourse Scraping**: Capability to scrape TDS discourse posts
- **Easy Deployment**: Designed for simple deployment on various platforms

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd tds-virtual-ta
   ```

2. **Install dependencies**
   ```bash
   pip install flask requests trafilatura python-dotenv gunicorn
   ```

3. **Set environment variables**
   ```bash
   export AIPIPE_TOKEN="your-aipipe-token"
   export SESSION_SECRET="your-secret-key"
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Access the application**
   - Web interface: http://localhost:5000
   - API endpoint: http://localhost:5000/api/

### API Usage

**Endpoint:** `POST /api/`

**Request Format:**
```json
{
  "question": "How do I use pandas DataFrames?",
  "image": "base64-encoded-image-data (optional)"
}
```

**Response Format:**
```json
{
  "answer": "DataFrames are the core of pandas. They provide a 2-dimensional labeled data structure...",
  "links": [
    {
      "url": "https://discourse.onlinedegree.iitm.ac.in/t/pandas-dataframe-operations/155945",
      "text": "Pandas DataFrame Operations"
    }
  ]
}
```

**Example cURL Request:**
```bash
curl -X POST "http://localhost:5000/api/" \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I use pandas DataFrames?"}'
```

## Deployment

### Production Deployment

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**
   ```bash
   export AIPIPE_TOKEN="your-production-aipipe-token"
   export SESSION_SECRET="your-production-secret-key"
   ```

3. **Run with Gunicorn**
   ```bash
   gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
   ```

### Platform-Specific Deployment

**Replit:**
- Upload all files to Replit
- Set environment variables in Secrets tab
- Use the "Run" button

**Heroku:**
- Create `Procfile` with: `web: gunicorn main:app`
- Set environment variables in Heroku dashboard
- Deploy via Git

**Railway/Render:**
- Connect GitHub repository
- Set environment variables in platform settings
- Deploy automatically

## Project Structure

```
tds-virtual-ta/
├── main.py                 # Application entry point
├── app.py                  # Flask application setup
├── api.py                  # Virtual TA API logic
├── data_store.py           # Data storage and search functionality
├── scraper.py              # Discourse scraper
├── requirements.txt        # Python dependencies
├── LICENSE                 # MIT License
├── README.md               # Project documentation
├── templates/
│   └── index.html          # Web interface
└── static/
    ├── style.css           # Stylesheet
    └── script.js           # Frontend JavaScript
```

## Configuration

### Environment Variables

- `AIPIPE_TOKEN`: Your AI Pipe API token (required)
- `SESSION_SECRET`: Flask session secret key (required)

### AI Pipe Setup

1. Sign up at https://aipipe.org
2. Get your API token
3. Set the `AIPIPE_TOKEN` environment variable

## Features

### Dynamic Response System

The application provides contextual responses based on:
- Course content matching
- Discourse post relevance
- Question-specific context

### Supported Topics

- Python programming basics
- Data structures (lists, tuples, dictionaries, sets)
- Pandas for data manipulation
- NumPy for numerical computing
- Matplotlib for visualization
- Git version control
- Jupyter notebooks
- Machine learning basics
- Virtual environments
- API development with Flask
- Data preprocessing techniques

### Web Interface

- Clean, responsive design with Bootstrap
- Real-time question processing
- Image upload support
- API documentation
- Error handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed information

## Acknowledgments

- IIT Madras Online Degree Program
- Tools in Data Science course
- AI Pipe for AI integration
- Bootstrap for UI components