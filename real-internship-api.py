from flask import Flask, request, jsonify
from flask_cors import CORS
from real_internship_scraper import RealInternshipScraper
import json
import threading
import time

app = Flask(__name__)
CORS(app)

# Global scraper instance
scraper = RealInternshipScraper()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Real Internship Scraper API is running',
        'endpoints': [
            '/api/search',
            '/api/health'
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
            'message': f'Found {len(results)} real internships from LinkedIn, Indeed, Glassdoor, and Internships.com'
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
            'message': f'Found {len(results)} real internships from LinkedIn, Indeed, Glassdoor, and Internships.com'
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
            'message': f'Scraper test successful. Found {len(results)} internships.'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Scraper test failed'
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Real Internship Scraper API...")
    print("📡 API will be available at: http://localhost:5003")
    print("🔍 Endpoints:")
    print("   GET  /api/health - Health check")
    print("   GET  /api/test - Test scraper functionality")
    print("   GET  /api/search?keyword=...&location=... - Search internships")
    print("   POST /api/search - Search internships with JSON body")
    print("🌐 Searches real job sites:")
    print("   - LinkedIn")
    print("   - Indeed")
    print("   - Glassdoor")
    print("   - Internships.com")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5003) 