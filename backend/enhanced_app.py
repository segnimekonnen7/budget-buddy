from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random
from datetime import datetime
import re

app = Flask(__name__)
CORS(app)

# Enhanced location matching
US_STATE_TO_ABBR = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR", "california": "CA", "colorado": "CO",
    "connecticut": "CT", "delaware": "DE", "florida": "FL", "georgia": "GA", "hawaii": "HI", "idaho": "ID",
    "illinois": "IL", "indiana": "IN", "iowa": "IA", "kansas": "KS", "kentucky": "KY", "louisiana": "LA",
    "maine": "ME", "maryland": "MD", "massachusetts": "MA", "michigan": "MI", "minnesota": "MN", "mississippi": "MS",
    "missouri": "MO", "montana": "MT", "nebraska": "NE", "nevada": "NV", "new hampshire": "NH", "new jersey": "NJ",
    "new mexico": "NM", "new york": "NY", "north carolina": "NC", "north dakota": "ND", "ohio": "OH",
    "oklahoma": "OK", "oregon": "OR", "pennsylvania": "PA", "rhode island": "RI", "south carolina": "SC",
    "south dakota": "SD", "tennessee": "TN", "texas": "TX", "utah": "UT", "vermont": "VT", "virginia": "VA",
    "washington": "WA", "west virginia": "WV", "wisconsin": "WI", "wyoming": "WY", "district of columbia": "DC",
    "washington dc": "DC", "dc": "DC"
}

def expand_location_terms(raw):
    """Expand location terms with state abbreviations"""
    if not raw:
        return []
    terms = []
    for chunk in raw.replace("|", ",").split(","):
        term = chunk.strip().lower()
        if term:
            terms.append(term)
            # Add state abbreviation if it's a state name
            abbr = US_STATE_TO_ABBR.get(term)
            if abbr:
                terms.append(abbr.lower())
    return terms

# Enhanced internship data with more companies and locations
ENHANCED_INTERNSHIPS = [
    {
        "id": 1,
        "title": "Software Engineering Intern",
        "company": "Google",
        "location": "Mountain View, CA",
        "type": "Summer 2024",
        "duration": "12 weeks",
        "salary": "$8,000 - $12,000/month",
        "description": "Join Google's engineering team and work on real projects that impact millions of users worldwide. Learn from experienced engineers and contribute to innovative solutions.",
        "category": "software-engineering",
        "applyUrl": "https://careers.google.com/students/",
        "source": "Google Careers"
    },
    {
        "id": 2,
        "title": "Backend Engineering Intern",
        "company": "Microsoft",
        "location": "Seattle, WA",
        "type": "Summer 2024",
        "duration": "10 weeks",
        "salary": "$7,500 - $11,000/month",
        "description": "Build scalable backend systems using Azure cloud technologies. Work on real-world problems and learn from industry experts.",
        "category": "backend",
        "applyUrl": "https://careers.microsoft.com/students/us/en/internship",
        "source": "Microsoft Careers"
    },
    {
        "id": 3,
        "title": "Full Stack Developer Intern",
        "company": "Amazon",
        "location": "Seattle, WA",
        "type": "Summer 2024",
        "duration": "12 weeks",
        "salary": "$8,500 - $12,500/month",
        "description": "Develop full-stack applications using AWS services. Work on projects that serve millions of customers globally.",
        "category": "software-engineering",
        "applyUrl": "https://www.amazon.jobs/en/teams/internships-for-students",
        "source": "Amazon Jobs"
    },
    {
        "id": 4,
        "title": "Machine Learning Intern",
        "company": "Meta",
        "location": "Menlo Park, CA",
        "type": "Summer 2024",
        "duration": "12 weeks",
        "salary": "$9,000 - $13,000/month",
        "description": "Work on cutting-edge AI and machine learning projects. Contribute to research that shapes the future of technology.",
        "category": "machine-learning",
        "applyUrl": "https://www.metacareers.com/students-and-grads/",
        "source": "Meta Careers"
    },
    {
        "id": 5,
        "title": "Data Science Intern",
        "company": "Netflix",
        "location": "Los Gatos, CA",
        "type": "Summer 2024",
        "duration": "10 weeks",
        "salary": "$8,000 - $12,000/month",
        "description": "Analyze big data to improve user experience and content recommendations. Work with real streaming data.",
        "category": "data-science",
        "applyUrl": "https://jobs.netflix.com/teams/internships",
        "source": "Netflix Jobs"
    },
    {
        "id": 6,
        "title": "Frontend Engineering Intern",
        "company": "Airbnb",
        "location": "San Francisco, CA",
        "type": "Summer 2024",
        "duration": "12 weeks",
        "salary": "$7,500 - $11,500/month",
        "description": "Build beautiful user interfaces using React and modern web technologies. Focus on user experience and performance.",
        "category": "frontend",
        "applyUrl": "https://careers.airbnb.com/teams/internships",
        "source": "Airbnb Careers"
    },
    {
        "id": 7,
        "title": "Software Engineering Intern",
        "company": "Apple",
        "location": "Cupertino, CA",
        "type": "Summer 2024",
        "duration": "12 weeks",
        "salary": "$8,500 - $12,500/month",
        "description": "Develop software for iOS, macOS, and other Apple platforms. Work on products used by millions worldwide.",
        "category": "software-engineering",
        "applyUrl": "https://jobs.apple.com/en-us/search?job=intern",
        "source": "Apple Jobs"
    },
    {
        "id": 8,
        "title": "Backend Developer Intern",
        "company": "Twitter",
        "location": "San Francisco, CA",
        "type": "Summer 2024",
        "duration": "12 weeks",
        "salary": "$7,500 - $11,500/month",
        "description": "Build scalable backend services that handle millions of tweets. Work with real-time data processing.",
        "category": "backend",
        "applyUrl": "https://careers.twitter.com/en/teams/internships.html",
        "source": "Twitter Careers"
    },
    {
        "id": 9,
        "title": "Full Stack Engineering Intern",
        "company": "LinkedIn",
        "location": "Sunnyvale, CA",
        "type": "Summer 2024",
        "duration": "12 weeks",
        "salary": "$8,000 - $12,000/month",
        "description": "Develop features for the world's largest professional network. Work on both frontend and backend systems.",
        "category": "software-engineering",
        "applyUrl": "https://careers.linkedin.com/reach/student",
        "source": "LinkedIn Careers"
    },
    {
        "id": 10,
        "title": "Software Engineering Intern",
        "company": "Salesforce",
        "location": "San Francisco, CA",
        "type": "Summer 2024",
        "duration": "12 weeks",
        "salary": "$7,500 - $11,500/month",
        "description": "Build cloud-based applications and learn about enterprise software development.",
        "category": "software-engineering",
        "applyUrl": "https://salesforce.wd1.myworkdayjobs.com/External_Career_Site/0/refreshFacet/318c8bb6f553100021d223d9780d30be",
        "source": "Salesforce Careers"
    },
    {
        "id": 11,
        "title": "Machine Learning Intern",
        "company": "OpenAI",
        "location": "San Francisco, CA",
        "type": "Summer 2024",
        "duration": "12 weeks",
        "salary": "$9,000 - $13,000/month",
        "description": "Work on cutting-edge AI research and development. Contribute to the future of artificial intelligence.",
        "category": "machine-learning",
        "applyUrl": "https://openai.com/careers",
        "source": "OpenAI Careers"
    },
    {
        "id": 12,
        "title": "Data Engineering Intern",
        "company": "Palantir",
        "location": "Palo Alto, CA",
        "type": "Summer 2024",
        "duration": "12 weeks",
        "salary": "$8,500 - $12,500/month",
        "description": "Build data pipelines and work with large-scale data processing systems.",
        "category": "data-science",
        "applyUrl": "https://jobs.lever.co/palantir",
        "source": "Palantir Careers"
    },
    {
        "id": 13,
        "title": "Software Engineering Intern",
        "company": "Stripe",
        "location": "San Francisco, CA",
        "type": "Summer 2024",
        "duration": "12 weeks",
        "salary": "$8,000 - $12,000/month",
        "description": "Build payment infrastructure that powers the internet economy.",
        "category": "software-engineering",
        "applyUrl": "https://stripe.com/jobs/search?teams%5B%5D=University",
        "source": "Stripe Careers"
    },
    {
        "id": 14,
        "title": "Backend Engineering Intern",
        "company": "Square",
        "location": "San Francisco, CA",
        "type": "Summer 2024",
        "duration": "12 weeks",
        "salary": "$7,500 - $11,500/month",
        "description": "Develop backend services for financial technology applications.",
        "category": "backend",
        "applyUrl": "https://careers.squareup.com/us/en/teams/internships",
        "source": "Square Careers"
    },
    {
        "id": 15,
        "title": "Software Engineering Intern",
        "company": "Uber",
        "location": "San Francisco, CA",
        "type": "Summer 2024",
        "duration": "12 weeks",
        "salary": "$8,000 - $12,000/month",
        "description": "Build transportation technology that moves the world. Work on real-time systems and mobile applications.",
        "category": "software-engineering",
        "applyUrl": "https://www.uber.com/us/en/careers/teams/university/",
        "source": "Uber Careers"
    },
    {
        "id": 16,
        "title": "Frontend Developer Intern",
        "company": "Shopify",
        "location": "Ottawa, ON",
        "type": "Summer 2024",
        "duration": "12 weeks",
        "salary": "$7,000 - $10,000/month",
        "description": "Build e-commerce solutions that help merchants succeed online. Work with React and modern web technologies.",
        "category": "frontend",
        "applyUrl": "https://www.shopify.com/careers/teams/engineering",
        "source": "Shopify Careers"
    },
    {
        "id": 17,
        "title": "Software Engineering Intern",
        "company": "Spotify",
        "location": "New York, NY",
        "type": "Summer 2024",
        "duration": "12 weeks",
        "salary": "$7,500 - $11,000/month",
        "description": "Build music streaming technology that connects artists and listeners worldwide.",
        "category": "software-engineering",
        "applyUrl": "https://www.lifeatspotify.com/jobs/student",
        "source": "Spotify Careers"
    },
    {
        "id": 18,
        "title": "Data Science Intern",
        "company": "Pinterest",
        "location": "San Francisco, CA",
        "type": "Summer 2024",
        "duration": "12 weeks",
        "salary": "$8,000 - $12,000/month",
        "description": "Analyze user behavior and content to improve discovery and recommendations.",
        "category": "data-science",
        "applyUrl": "https://www.pinterestcareers.com/jobs/",
        "source": "Pinterest Careers"
    },
    {
        "id": 19,
        "title": "Software Engineering Intern",
        "company": "Snapchat",
        "location": "Los Angeles, CA",
        "type": "Summer 2024",
        "duration": "12 weeks",
        "salary": "$8,000 - $12,000/month",
        "description": "Build creative tools and camera technology that brings people together.",
        "category": "software-engineering",
        "applyUrl": "https://careers.snap.com/",
        "source": "Snapchat Careers"
    },
    {
        "id": 20,
        "title": "Machine Learning Intern",
        "company": "Tesla",
        "location": "Palo Alto, CA",
        "type": "Summer 2024",
        "duration": "12 weeks",
        "salary": "$8,500 - $12,500/month",
        "description": "Work on autonomous driving technology and energy solutions for a sustainable future.",
        "category": "machine-learning",
        "applyUrl": "https://www.tesla.com/careers",
        "source": "Tesla Careers"
    }
]

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Enhanced Internship Finder API is running',
        'features': ['location_search', 'state_abbreviations', 'enhanced_matching'],
        'endpoints': [
            '/api/search',
            '/api/health',
            '/api/jobs/search'
        ]
    })

@app.route('/api/search', methods=['POST'])
def search_jobs():
    try:
        data = request.get_json()
        keyword = data.get('keyword', 'software engineer').lower()
        location = data.get('location', 'United States').lower()
        job_type = data.get('jobType', 'internship').lower()
        
        print(f"🔍 Enhanced search: {keyword} in {location}")
        
        # Enhanced location matching
        location_terms = expand_location_terms(location)
        
        # Filter internships with enhanced matching
        filtered_jobs = []
        
        for job in ENHANCED_INTERNSHIPS:
            # Check keyword match
            keyword_match = (
                keyword in job['title'].lower() or
                keyword in job['description'].lower() or
                keyword in job['category'].lower() or
                keyword in job['company'].lower()
            )
            
            # Enhanced location matching
            location_match = False
            if not location_terms or location == 'united states' or location == '':
                location_match = True
            else:
                job_location = job['location'].lower()
                for term in location_terms:
                    if term in job_location:
                        location_match = True
                        break
            
            # Check job type match
            type_match = (
                job_type in job['type'].lower() or
                job_type == '' or
                job_type == 'internship'
            )
            
            if keyword_match and location_match and type_match:
                filtered_jobs.append(job)
        
        # If no exact matches, return some relevant results
        if not filtered_jobs:
            filtered_jobs = random.sample(ENHANCED_INTERNSHIPS, min(8, len(ENHANCED_INTERNSHIPS)))
        
        return jsonify({
            'success': True,
            'count': len(filtered_jobs),
            'jobs': filtered_jobs,
            'search_params': {
                'keyword': keyword,
                'location': location,
                'jobType': job_type,
                'location_terms': location_terms
            },
            'message': f'Found {len(filtered_jobs)} internships with enhanced location matching'
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
        keyword = request.args.get('keyword', 'software engineer').lower()
        location = request.args.get('location', 'United States').lower()
        job_type = request.args.get('jobType', 'internship').lower()
        
        print(f"🔍 Enhanced GET search: {keyword} in {location}")
        
        # Enhanced location matching
        location_terms = expand_location_terms(location)
        
        # Filter internships with enhanced matching
        filtered_jobs = []
        
        for job in ENHANCED_INTERNSHIPS:
            # Check keyword match
            keyword_match = (
                keyword in job['title'].lower() or
                keyword in job['description'].lower() or
                keyword in job['category'].lower() or
                keyword in job['company'].lower()
            )
            
            # Enhanced location matching
            location_match = False
            if not location_terms or location == 'united states' or location == '':
                location_match = True
            else:
                job_location = job['location'].lower()
                for term in location_terms:
                    if term in job_location:
                        location_match = True
                        break
            
            # Check job type match
            type_match = (
                job_type in job['type'].lower() or
                job_type == '' or
                job_type == 'internship'
            )
            
            if keyword_match and location_match and type_match:
                filtered_jobs.append(job)
        
        # If no exact matches, return some relevant results
        if not filtered_jobs:
            filtered_jobs = random.sample(ENHANCED_INTERNSHIPS, min(8, len(ENHANCED_INTERNSHIPS)))
        
        return jsonify({
            'success': True,
            'count': len(filtered_jobs),
            'jobs': filtered_jobs,
            'search_params': {
                'keyword': keyword,
                'location': location,
                'jobType': job_type,
                'location_terms': location_terms
            },
            'message': f'Found {len(filtered_jobs)} internships with enhanced location matching'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'jobs': []
        }), 500

# New FastAPI-style endpoint for compatibility
@app.route('/api/jobs/search', methods=['GET'])
def jobs_search():
    """FastAPI-compatible search endpoint"""
    try:
        query = request.args.get('query', '')
        loc = request.args.get('loc', '')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        # Use the enhanced search logic
        location_terms = expand_location_terms(loc) if loc else []
        
        filtered_jobs = []
        for job in ENHANCED_INTERNSHIPS:
            # Keyword matching
            keyword_match = True
            if query:
                keyword_match = (
                    query.lower() in job['title'].lower() or
                    query.lower() in job['description'].lower() or
                    query.lower() in job['category'].lower() or
                    query.lower() in job['company'].lower()
                )
            
            # Location matching
            location_match = True
            if location_terms:
                job_location = job['location'].lower()
                location_match = any(term in job_location for term in location_terms)
            
            if keyword_match and location_match:
                filtered_jobs.append(job)
        
        # Pagination
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_jobs = filtered_jobs[start_idx:end_idx]
        
        return jsonify({
            'total': len(filtered_jobs),
            'page': page,
            'per_page': per_page,
            'items': paginated_jobs
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'total': 0,
            'page': 1,
            'per_page': 20,
            'items': []
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Enhanced Internship Finder API...")
    print("📡 API will be available at: http://localhost:5003")
    print("🔍 Enhanced Features:")
    print("   - Smart location matching with state abbreviations")
    print("   - Expanded internship database (20+ companies)")
    print("   - Better search algorithms")
    print("   - FastAPI-compatible endpoints")
    print(f"📊 Total internships available: {len(ENHANCED_INTERNSHIPS)}")
    app.run(debug=True, host='0.0.0.0', port=5003)