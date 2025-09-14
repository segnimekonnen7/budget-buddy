#!/usr/bin/env python3
"""
Internship Locator - Flask API Server
Main backend server that handles internship search requests and coordinates scrapers.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import time
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import scrapers
from scrapers.linkedin_scraper import LinkedInScraper
from scrapers.indeed_scraper import IndeedScraper
from scrapers.glassdoor_scraper import GlassdoorScraper
from scrapers.handshake_scraper import HandshakeScraper

# Import utilities
from utils.rate_limiter import RateLimiter
from utils.data_processor import DataProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize components
rate_limiter = RateLimiter()
data_processor = DataProcessor()

# Initialize scrapers
scrapers = {
    'linkedin': LinkedInScraper(),
    'indeed': IndeedScraper(),
    'glassdoor': GlassdoorScraper(),
    'handshake': HandshakeScraper()
}

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'message': 'Internship Locator API is running'
    })

@app.route('/api/platforms', methods=['GET'])
def get_platforms():
    """Get list of supported platforms"""
    return jsonify({
        'platforms': [
            {
                'name': 'LinkedIn',
                'id': 'linkedin',
                'description': 'Professional networking and job search',
                'status': 'active'
            },
            {
                'name': 'Indeed',
                'id': 'indeed',
                'description': 'World\'s largest job site',
                'status': 'active'
            },
            {
                'name': 'Glassdoor',
                'id': 'glassdoor',
                'description': 'Company reviews and job listings',
                'status': 'active'
            },
            {
                'name': 'Handshake',
                'id': 'handshake',
                'description': 'University-focused job platform',
                'status': 'active'
            }
        ]
    })

@app.route('/api/search', methods=['POST'])
def search_internships():
    """
    Main search endpoint that coordinates multiple scrapers
    """
    try:
        # Parse request data
        data = request.get_json()
        keyword = data.get('keyword', '').strip()
        location = data.get('location', '').strip()
        remote_only = data.get('remote_only', False)
        paid_only = data.get('paid_only', False)
        platforms = data.get('platforms', ['linkedin', 'indeed', 'glassdoor'])
        
        # Validate input
        if not keyword:
            return jsonify({
                'success': False,
                'error': 'Keyword is required'
            }), 400
        
        if not location:
            return jsonify({
                'success': False,
                'error': 'Location is required'
            }), 400
        
        logger.info(f"Search request: {keyword} in {location}")
        
        # Search across platforms
        all_results = []
        search_start_time = time.time()
        
        # Use ThreadPoolExecutor for concurrent scraping
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Submit search tasks
            future_to_platform = {}
            for platform in platforms:
                if platform in scrapers:
                    future = executor.submit(
                        search_platform,
                        platform,
                        keyword,
                        location,
                        remote_only,
                        paid_only
                    )
                    future_to_platform[future] = platform
            
            # Collect results
            for future in as_completed(future_to_platform):
                platform = future_to_platform[future]
                try:
                    results = future.result()
                    all_results.extend(results)
                    logger.info(f"✅ {platform}: Found {len(results)} internships")
                except Exception as e:
                    logger.error(f"❌ {platform}: Error - {str(e)}")
        
        # Process and deduplicate results
        processed_results = data_processor.process_results(all_results)
        
        # Apply filters
        if remote_only:
            processed_results = [r for r in processed_results if r.get('remote', False)]
        
        if paid_only:
            processed_results = [r for r in processed_results if r.get('paid', True)]
        
        search_time = time.time() - search_start_time
        
        return jsonify({
            'success': True,
            'results': processed_results,
            'total_count': len(processed_results),
            'search_time': round(search_time, 2),
            'search_params': {
                'keyword': keyword,
                'location': location,
                'remote_only': remote_only,
                'paid_only': paid_only,
                'platforms': platforms
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'An error occurred while searching for internships'
        }), 500

def search_platform(platform_name, keyword, location, remote_only, paid_only):
    """
    Search a specific platform for internships
    """
    try:
        scraper = scrapers[platform_name]
        
        # Apply rate limiting
        rate_limiter.wait_if_needed(platform_name)
        
        # Search the platform
        results = scraper.search_internships(keyword, location)
        
        # Add platform metadata
        for result in results:
            result['platform'] = platform_name
            result['scraped_at'] = datetime.now().isoformat()
        
        return results
        
    except Exception as e:
        logger.error(f"Error searching {platform_name}: {str(e)}")
        return []

@app.route('/api/search', methods=['GET'])
def search_internships_get():
    """
    GET endpoint for simple searches
    """
    try:
        keyword = request.args.get('keyword', '').strip()
        location = request.args.get('location', '').strip()
        remote_only = request.args.get('remote_only', 'false').lower() == 'true'
        paid_only = request.args.get('paid_only', 'false').lower() == 'true'
        
        if not keyword or not location:
            return jsonify({
                'success': False,
                'error': 'Both keyword and location are required'
            }), 400
        
        # Convert to POST format and call the main search function
        data = {
            'keyword': keyword,
            'location': location,
            'remote_only': remote_only,
            'paid_only': paid_only
        }
        
        # Create a mock request object
        class MockRequest:
            def __init__(self, data):
                self.json = lambda: data
        
        request._json = data
        return search_internships()
        
    except Exception as e:
        logger.error(f"GET search error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/test', methods=['GET'])
def test_scrapers():
    """
    Test endpoint to verify scrapers are working
    """
    try:
        test_results = {}
        
        for platform_name, scraper in scrapers.items():
            try:
                # Test with a simple search
                results = scraper.search_internships("software engineer", "San Francisco")
                test_results[platform_name] = {
                    'status': 'success',
                    'count': len(results),
                    'sample_results': results[:2] if results else []
                }
            except Exception as e:
                test_results[platform_name] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        return jsonify({
            'success': True,
            'test_results': test_results,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    print("🚀 Starting Internship Locator API Server...")
    print("📡 API will be available at: http://localhost:5001")
    print("🔍 Endpoints:")
    print("   GET  /api/health - Health check")
    print("   GET  /api/platforms - Get supported platforms")
    print("   GET  /api/test - Test scrapers")
    print("   GET  /api/search?keyword=...&location=... - Search internships")
    print("   POST /api/search - Search internships with JSON body")
    print("🌐 Supported platforms:")
    for platform in scrapers.keys():
        print(f"   - {platform.title()}")
    print("✅ Ready to search for internships!")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5001) 