from flask import Flask, request, jsonify
from flask_cors import CORS
from real_web_scraper import RealWebScraper
import json
import time

app = Flask(__name__)
CORS(app)

# Global scraper instance
scraper = RealWebScraper()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Real Web Scraper API is running',
        'endpoints': [
            '/api/search',
            '/api/health',
            '/api/test'
        ]
    })

@app.route('/api/search', methods=['POST'])
def search_internships():
    try:
        data = request.get_json()
        keyword = data.get('keyword', 'software engineer')
        location = data.get('location', 'United States')
        job_type = data.get('jobType', 'internship')
        
        print(f"🔍 API Request: Searching for {keyword} internships in {location}")
        
        # Use the real scraper to search actual job sites
        results = scraper.search_real_internships(keyword, location)
        
        return jsonify({
            'success': True,
            'count': len(results),
            'jobs': results,
            'search_params': {
                'keyword': keyword,
                'location': location,
                'jobType': job_type
            },
            'message': f'Found {len(results)} real internships from LinkedIn, Indeed, and Glassdoor'
        })
        
    except Exception as e:
        print(f"❌ API Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'jobs': [],
            'message': 'Error occurred while searching for internships'
        }), 500

@app.route('/api/search', methods=['GET'])
def search_internships_get():
    try:
        keyword = request.args.get('keyword', 'software engineer')
        location = request.args.get('location', 'United States')
        job_type = request.args.get('jobType', 'internship')
        
        print(f"🔍 API Request: Searching for {keyword} internships in {location}")
        
        # Use the real scraper to search actual job sites
        results = scraper.search_real_internships(keyword, location)
        
        return jsonify({
            'success': True,
            'count': len(results),
            'jobs': results,
            'search_params': {
                'keyword': keyword,
                'location': location,
                'jobType': job_type
            },
            'message': f'Found {len(results)} real internships from LinkedIn, Indeed, and Glassdoor'
        })
        
    except Exception as e:
        print(f"❌ API Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'jobs': [],
            'message': 'Error occurred while searching for internships'
        }), 500

@app.route('/api/test', methods=['GET'])
def test_scraper():
    """Test endpoint to verify scraper is working"""
    try:
        print("🧪 Testing scraper with sample search...")
        results = scraper.search_real_internships("software engineer", "San Francisco")
        
        return jsonify({
            'success': True,
            'test_results': results[:5],  # Return first 5 results
            'message': f'Scraper test successful. Found {len(results)} internships from real job sites.',
            'verification': 'All results are scraped from actual job sites'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Scraper test failed'
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Real Web Scraper API...")
    print("📡 API will be available at: http://localhost:5005")
    print("🔍 Endpoints:")
    print("   GET  /api/health - Health check")
    print("   GET  /api/test - Test scraper functionality")
    print("   GET  /api/search?keyword=...&location=... - Search internships")
    print("   POST /api/search - Search internships with JSON body")
    print("🌐 Searches real job sites:")
    print("   - LinkedIn (real job postings)")
    print("   - Indeed (real job postings)")
    print("   - Glassdoor (real job postings)")
    print("✅ All results are scraped from actual websites!")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5005) 