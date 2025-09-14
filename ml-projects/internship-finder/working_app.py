from flask import Flask, render_template, request, jsonify
from working_scraper import WorkingInternshipScraper
import threading
import time

app = Flask(__name__)

# Global variables
search_results = []
search_in_progress = False

@app.route('/')
def index():
    return render_template('working_interface.html')

@app.route('/api/search', methods=['POST'])
def search_internships():
    global search_results, search_in_progress
    
    if search_in_progress:
        return jsonify({'error': 'Search already in progress'})
    
    data = request.json
    keywords = data.get('keywords', 'machine learning')
    location = data.get('location', 'San Francisco')
    sources = data.get('sources', ['indeed', 'linkedin', 'glassdoor'])
    
    # Start search in background thread
    search_in_progress = True
    thread = threading.Thread(target=perform_search, args=(keywords, location, sources))
    thread.start()
    
    return jsonify({'message': 'Search started', 'status': 'searching'})

@app.route('/api/results')
def get_results():
    global search_results, search_in_progress
    
    return jsonify({
        'results': search_results,
        'in_progress': search_in_progress,
        'count': len(search_results)
    })

def perform_search(keywords, location, sources):
    global search_results, search_in_progress
    
    try:
        scraper = WorkingInternshipScraper()
        results = scraper.search_all_sources(keywords, location, sources)
        
        # Convert to frontend format
        formatted_results = []
        for job in results:
            formatted_job = {
                'id': len(formatted_results) + 1,
                'company': job['company'],
                'position': job['title'],
                'location': job['location'],
                'type': 'Remote' if 'remote' in job['title'].lower() else 'On-site',
                'duration': '3-6 months',
                'salary': '$25-35/hour',
                'deadline': '2024-12-31',
                'description': f"Internship opportunity at {job['company']}",
                'requirements': 'Python, Programming, Teamwork',
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
        print(f"Search error: {e}")
        search_results = []
    
    finally:
        search_in_progress = False

if __name__ == '__main__':
    app.run(debug=True, port=5005, host='0.0.0.0') 