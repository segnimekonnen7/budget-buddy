# 🚀 Internship Application Assistant

A comprehensive tool to streamline your internship search and application process. Built with FastAPI and modern web technologies.

## ✨ Features

### 📋 Application Tracking
- **Database Management**: Track all your applications with status updates
- **Progress Monitoring**: Visual dashboard with application statistics
- **Follow-up Reminders**: Never miss important follow-up dates
- **Status Updates**: Track applications from Applied → Interview → Accepted/Rejected

### 🔍 Job Discovery
- **Multi-Source Scraping**: Search Indeed, LinkedIn, and other job boards
- **Smart Filtering**: Filter by keywords, location, and date posted
- **One-Click Application**: Add discovered jobs directly to your application tracker
- **Real-time Search**: Get fresh job postings instantly

### 📝 Document Generation
- **AI-Powered Cover Letters**: Generate personalized cover letters using templates
- **Resume Customization**: Adapt your resume for different roles
- **Template Library**: Pre-built templates for different industries
- **Export Options**: Save documents in multiple formats

### 📊 Analytics & Insights
- **Application Statistics**: Track success rates and response times
- **Company Research**: Store notes about companies and interview processes
- **Performance Metrics**: Monitor your application efficiency
- **Trend Analysis**: Identify patterns in successful applications

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM)
- **SQLite**: Lightweight database for local development
- **BeautifulSoup4**: Web scraping library
- **Jinja2**: Template engine for document generation

### Frontend
- **Vanilla HTML/CSS/JavaScript**: Clean, responsive interface
- **Modern CSS Grid**: Responsive layout system
- **Fetch API**: Asynchronous data loading
- **Modal System**: Interactive application management

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd internship-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Open your browser**
   - Backend API: `http://localhost:8003`
   - Frontend Interface: `http://localhost:8003` (serves the HTML file)

### Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t internship-assistant .
   ```

2. **Run the container**
   ```bash
   docker run -p 8003:8003 internship-assistant
   ```

## 📖 API Documentation

### Application Management
- `POST /applications/` - Create new application
- `GET /applications/` - List all applications
- `GET /applications/{id}` - Get specific application
- `PUT /applications/{id}` - Update application
- `DELETE /applications/{id}` - Delete application

### Job Discovery
- `GET /jobs/scrape` - Scrape job postings
- `GET /jobs/` - List saved job postings

### Document Generation
- `POST /cover-letter/generate` - Generate cover letter

### Analytics
- `GET /analytics/dashboard` - Get dashboard statistics
- `GET /analytics/follow-ups` - Get follow-up reminders

## 🎯 Usage Guide

### 1. Track Applications
1. Click "Add New" in the Application Tracker
2. Fill in company details, position, and requirements
3. Set follow-up dates and add notes
4. Monitor status updates and progress

### 2. Discover Jobs
1. Enter keywords and location in Job Discovery
2. Click "Search Jobs" to find opportunities
3. Review results and add interesting positions to applications
4. One-click application creation from job listings

### 3. Generate Cover Letters
1. Fill in company and position details
2. Add your skills and experience
3. Explain why you're interested
4. Generate and copy personalized cover letter

### 4. Monitor Progress
1. View dashboard statistics
2. Check follow-up reminders
3. Update application statuses
4. Track success rates and trends

## 🔧 Configuration

### Environment Variables
- `DATABASE_URL`: Database connection string
- `SCRAPING_DELAY`: Delay between scraping requests (default: 1 second)
- `MAX_RESULTS`: Maximum job results per search (default: 50)

### Customization
- **Templates**: Modify cover letter templates in `main.py`
- **Scraping**: Add new job sources in scraping functions
- **Styling**: Customize the frontend in `index.html`

## ⚠️ Important Notes

### Legal & Ethical Considerations
- **Respect robots.txt**: Always check website scraping policies
- **Rate Limiting**: Implement delays to avoid overwhelming servers
- **Terms of Service**: Ensure compliance with job board terms
- **Personal Use**: This tool is for personal internship search only

### Limitations
- **Manual Submission**: You must submit applications manually
- **Authentication**: Cannot handle login-protected job boards
- **Dynamic Content**: May not work with JavaScript-heavy sites
- **Rate Limits**: Some sites may block automated requests

## 🚀 Deployment

### Render.com
1. Connect your GitHub repository
2. Use the provided `render.yaml` configuration
3. Deploy with automatic builds

### Other Platforms
- **Heroku**: Use the included `Dockerfile`
- **AWS**: Deploy using Elastic Beanstalk or ECS
- **DigitalOcean**: Use App Platform or Droplets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions or issues:
1. Check the documentation
2. Review the API endpoints
3. Open an issue on GitHub
4. Contact the development team

---

**Happy job hunting! 🎯**

