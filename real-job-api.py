from flask import Flask, request, jsonify
from flask_cors import CORS
from real_job_scraper import RealJobScraper
import json

app = Flask(__name__)
CORS(app)

scraper = RealJobScraper()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Real Job Scraper API is running',
        'endpoints': [
            '/api/search',
            '/api/health'
        ]
    })

@app.route('/api/search', methods=['POST'])
def search_jobs():
    try:
        data = request.get_json()
        keyword = data.get('keyword', 'software engineer')
        location = data.get('location', 'United States')
        job_type = data.get('jobType', 'internship')
        
        print(f"Searching for: {keyword} in {location}")
        
        # Search for internships
        results = scraper.search_internships(keyword, location)
        
        return jsonify({
            'success': True,
            'count': len(results),
            'jobs': results,
            'search_params': {
                'keyword': keyword,
                'location': location,
                'jobType': job_type
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'jobs': []
        }), 500

@app.route('/api/search', methods=['GET'])
def search_jobs_get():
    try:
        keyword = request.args.get('keyword', 'software engineer')
        location = request.args.get('location', 'United States')
        job_type = request.args.get('jobType', 'internship')
        
        print(f"Searching for: {keyword} in {location}")
        
        # Search for internships
        results = scraper.search_internships(keyword, location)
        
        return jsonify({
            'success': True,
            'count': len(results),
            'jobs': results,
            'search_params': {
                'keyword': keyword,
                'location': location,
                'jobType': job_type
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'jobs': []
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Real Job Scraper API...")
    print("📡 API will be available at: http://localhost:5003")
    print("🔍 Endpoints:")
    print("   GET  /api/health - Health check")
    print("   GET  /api/search?keyword=...&location=... - Search jobs")
    print("   POST /api/search - Search jobs with JSON body")
    app.run(debug=True, host='0.0.0.0', port=5003) 