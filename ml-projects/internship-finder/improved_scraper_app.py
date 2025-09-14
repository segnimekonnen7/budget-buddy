from flask import Flask, render_template, request, jsonify
from improved_scraper import ImprovedInternshipScraper
import json
import threading
import time

app = Flask(__name__)

# Global variable to store search results
search_results = []
search_in_progress = False

@app.route('/')
def index():
    return render_template('enhanced_search_interface.html')

@app.route('/api/categories')
def get_categories():
    """Get available job categories"""
    scraper = ImprovedInternshipScraper()
    categories = scraper.get_job_categories()
    return jsonify({'categories': categories})

@app.route('/api/locations')
def get_locations():
    """Get popular locations"""
    scraper = ImprovedInternshipScraper()
    locations = scraper.get_popular_locations()
    return jsonify({'locations': locations})

@app.route('/api/search', methods=['POST'])
def search_internships():
    global search_results, search_in_progress
    
    if search_in_progress:
        return jsonify({'error': 'Search already in progress'})
    
    data = request.json
    keywords = data.get('keywords', '')
    location = data.get('location', '')
    job_type = data.get('job_type', '')
    experience = data.get('experience', '')
    sources = data.get('sources', ['indeed', 'linkedin', 'glassdoor'])
    
    # Start search in background thread
    search_in_progress = True
    thread = threading.Thread(target=perform_improved_search, args=(keywords, location, job_type, experience, sources))
    thread.start()
    
    return jsonify({'message': 'Improved search started', 'status': 'searching'})

@app.route('/api/results')
def get_results():
    global search_results, search_in_progress
    
    return jsonify({
        'results': search_results,
        'in_progress': search_in_progress,
        'count': len(search_results)
    })

def perform_improved_search(keywords, location, job_type, experience, sources):
    global search_results, search_in_progress
    
    try:
        scraper = ImprovedInternshipScraper()
        results = scraper.search_all_sources_improved(
            keywords=keywords,
            location=location,
            job_type=job_type,
            experience=experience,
            sources=sources
        )
        
        # Convert results to the format expected by the frontend
        formatted_results = []
        for job in results:
            formatted_job = {
                'id': len(formatted_results) + 1,
                'company': job['company'],
                'position': job['title'],
                'location': job['location'],
                'type': 'Remote' if 'remote' in job_type.lower() else 'On-site',
                'duration': '12 months',
                'salary': '$75,000',  # Default salary
                'deadline': '2024-04-01',
                'description': f"Internship opportunity at {job['company']} in {job['category']}",
                'requirements': 'Python, Machine Learning, Data Science',
                'matchScore': 85,
                'logo': job['logo'],
                'source': job['source'],
                'applyLink': job['url'],
                'category': job['category'],
                'status': None
            }
            formatted_results.append(formatted_job)
        
        search_results = formatted_results
        
    except Exception as e:
        print(f"Improved search error: {e}")
        search_results = []
    
    finally:
        search_in_progress = False

if __name__ == '__main__':
    app.run(debug=True, port=5003) 