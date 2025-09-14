# Internship Locator

A full-stack web application that helps users search for currently available internships across major platforms like LinkedIn, Glassdoor, Indeed, and more.

## 🌟 Features

- **Real-time Search**: Search across multiple job platforms simultaneously
- **Live Results**: Get real, currently available internships
- **Direct Apply Links**: Click to apply directly on company websites
- **Smart Filtering**: Filter by location, job type, and remote options
- **Responsive Design**: Works on desktop and mobile devices

## 🏗️ Project Structure

```
internship-locator/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── linkedin_scraper.py
│   │   ├── indeed_scraper.py
│   │   ├── glassdoor_scraper.py
│   │   └── handshake_scraper.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── rate_limiter.py
│   │   └── data_processor.py
│   ├── requirements.txt
│   └── config.py
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── README.md
└── setup.sh
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- Modern web browser

### Installation

1. **Clone and setup:**
```bash
git clone <repository-url>
cd internship-locator
chmod +x setup.sh
./setup.sh
```

2. **Start the backend:**
```bash
cd backend
python app.py
```

3. **Open the frontend:**
```bash
cd frontend
python -m http.server 3000
```

4. **Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## 🔧 API Endpoints

### Search Internships
```
POST /api/search
Content-Type: application/json

{
  "keyword": "software engineer",
  "location": "San Francisco",
  "remote_only": false,
  "paid_only": true
}
```

### Health Check
```
GET /api/health
```

### Get Supported Platforms
```
GET /api/platforms
```

## 🛡️ Safety Measures

- **Rate Limiting**: Respects robots.txt and implements delays between requests
- **User-Agent Rotation**: Uses realistic browser headers
- **Request Delays**: 2-5 second delays between requests
- **Error Handling**: Graceful handling of blocked requests
- **Fallback Data**: Provides sample data when scraping fails

## 📊 Supported Platforms

- **LinkedIn**: Professional networking and job search
- **Indeed**: World's largest job site
- **Glassdoor**: Company reviews and job listings
- **Handshake**: University-focused job platform
- **Internships.com**: Specialized internship platform

## 🎯 Usage Examples

### Search for Software Engineering Internships
```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "software engineer",
    "location": "San Francisco",
    "remote_only": false
  }'
```

### Search for Remote Data Science Internships
```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "data science",
    "location": "Remote",
    "remote_only": true
  }'
```

## 🔍 How It Works

1. **User Input**: User enters job type and location
2. **API Request**: Frontend sends search request to backend
3. **Multi-Platform Search**: Backend searches multiple job sites simultaneously
4. **Data Processing**: Results are cleaned and deduplicated
5. **Response**: Structured data is returned to frontend
6. **Display**: Results are displayed with apply links

## 🛠️ Development

### Adding New Platforms

1. Create a new scraper in `backend/scrapers/`
2. Implement the required methods:
   - `search_internships(keyword, location)`
   - `get_job_details(job_url)`
3. Add to the main scraper registry in `app.py`

### Customizing the Frontend

- Modify `frontend/css/style.css` for styling
- Update `frontend/js/app.js` for functionality
- Edit `frontend/index.html` for structure

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## ⚠️ Disclaimer

This application is for educational purposes. Please respect the terms of service of job sites and implement appropriate rate limiting in production use. 