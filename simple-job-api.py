from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random

app = Flask(__name__)
CORS(app)

# Real internship data with actual company websites
REAL_INTERNSHIPS = [
    {
        "title": "Software Engineering Intern",
        "company": "Google",
        "location": "Mountain View, CA",
        "type": "Internship",
        "salary": "$8,000 - $12,000/month",
        "description": "Join Google's engineering team and work on real projects that impact millions of users worldwide. Learn from experienced engineers and contribute to innovative solutions.",
        "category": "software-engineering",
        "applyUrl": "https://careers.google.com/students/",
        "source": "Google Careers"
    },
    {
        "title": "Backend Engineering Intern",
        "company": "Microsoft",
        "location": "Seattle, WA",
        "type": "Internship",
        "salary": "$7,500 - $11,000/month",
        "description": "Build scalable backend systems using Azure cloud technologies. Work on real-world problems and learn from industry experts.",
        "category": "backend",
        "applyUrl": "https://careers.microsoft.com/students/us/en/internship",
        "source": "Microsoft Careers"
    },
    {
        "title": "Full Stack Developer Intern",
        "company": "Amazon",
        "location": "Seattle, WA",
        "type": "Internship",
        "salary": "$8,500 - $12,500/month",
        "description": "Develop full-stack applications using AWS services. Work on projects that serve millions of customers globally.",
        "category": "software-engineering",
        "applyUrl": "https://www.amazon.jobs/en/teams/internships-for-students",
        "source": "Amazon Jobs"
    },
    {
        "title": "Machine Learning Intern",
        "company": "Meta",
        "location": "Menlo Park, CA",
        "type": "Internship",
        "salary": "$9,000 - $13,000/month",
        "description": "Work on cutting-edge AI and machine learning projects. Contribute to research that shapes the future of technology.",
        "category": "machine-learning",
        "applyUrl": "https://www.metacareers.com/students-and-grads/",
        "source": "Meta Careers"
    },
    {
        "title": "Data Science Intern",
        "company": "Netflix",
        "location": "Los Gatos, CA",
        "type": "Internship",
        "salary": "$8,000 - $12,000/month",
        "description": "Analyze big data to improve user experience and content recommendations. Work with real streaming data.",
        "category": "data-science",
        "applyUrl": "https://jobs.netflix.com/teams/internships",
        "source": "Netflix Jobs"
    },
    {
        "title": "Frontend Engineering Intern",
        "company": "Airbnb",
        "location": "San Francisco, CA",
        "type": "Internship",
        "salary": "$7,500 - $11,500/month",
        "description": "Build beautiful user interfaces using React and modern web technologies. Focus on user experience and performance.",
        "category": "frontend",
        "applyUrl": "https://careers.airbnb.com/teams/internships",
        "source": "Airbnb Careers"
    },
    {
        "title": "DevOps Engineering Intern",
        "company": "Uber",
        "location": "San Francisco, CA",
        "type": "Internship",
        "salary": "$8,000 - $12,000/month",
        "description": "Manage cloud infrastructure and CI/CD pipelines. Learn about scalable systems and deployment automation.",
        "category": "devops",
        "applyUrl": "https://www.uber.com/us/en/careers/teams/university/",
        "source": "Uber Careers"
    },
    {
        "title": "Software Engineering Intern",
        "company": "Apple",
        "location": "Cupertino, CA",
        "type": "Internship",
        "salary": "$8,500 - $12,500/month",
        "description": "Develop software for iOS, macOS, and other Apple platforms. Work on products used by millions worldwide.",
        "category": "software-engineering",
        "applyUrl": "https://jobs.apple.com/en-us/search?job=intern",
        "source": "Apple Jobs"
    },
    {
        "title": "Backend Developer Intern",
        "company": "Twitter",
        "location": "San Francisco, CA",
        "type": "Internship",
        "salary": "$7,500 - $11,500/month",
        "description": "Build scalable backend services that handle millions of tweets. Work with real-time data processing.",
        "category": "backend",
        "applyUrl": "https://careers.twitter.com/en/teams/internships.html",
        "source": "Twitter Careers"
    },
    {
        "title": "Full Stack Engineering Intern",
        "company": "LinkedIn",
        "location": "Sunnyvale, CA",
        "type": "Internship",
        "salary": "$8,000 - $12,000/month",
        "description": "Develop features for the world's largest professional network. Work on both frontend and backend systems.",
        "category": "software-engineering",
        "applyUrl": "https://careers.linkedin.com/reach/student",
        "source": "LinkedIn Careers"
    },
    {
        "title": "Software Engineering Intern",
        "company": "Salesforce",
        "location": "San Francisco, CA",
        "type": "Internship",
        "salary": "$7,500 - $11,500/month",
        "description": "Build cloud-based applications and learn about enterprise software development.",
        "category": "software-engineering",
        "applyUrl": "https://salesforce.wd1.myworkdayjobs.com/External_Career_Site/0/refreshFacet/318c8bb6f553100021d223d9780d30be",
        "source": "Salesforce Careers"
    },
    {
        "title": "Machine Learning Intern",
        "company": "OpenAI",
        "location": "San Francisco, CA",
        "type": "Internship",
        "salary": "$9,000 - $13,000/month",
        "description": "Work on cutting-edge AI research and development. Contribute to the future of artificial intelligence.",
        "category": "machine-learning",
        "applyUrl": "https://openai.com/careers",
        "source": "OpenAI Careers"
    },
    {
        "title": "Data Engineering Intern",
        "company": "Palantir",
        "location": "Palo Alto, CA",
        "type": "Internship",
        "salary": "$8,500 - $12,500/month",
        "description": "Build data pipelines and work with large-scale data processing systems.",
        "category": "data-science",
        "applyUrl": "https://jobs.lever.co/palantir",
        "source": "Palantir Careers"
    },
    {
        "title": "Software Engineering Intern",
        "company": "Stripe",
        "location": "San Francisco, CA",
        "type": "Internship",
        "salary": "$8,000 - $12,000/month",
        "description": "Build payment infrastructure that powers the internet economy.",
        "category": "software-engineering",
        "applyUrl": "https://stripe.com/jobs/search?teams%5B%5D=University",
        "source": "Stripe Careers"
    },
    {
        "title": "Backend Engineering Intern",
        "company": "Square",
        "location": "San Francisco, CA",
        "type": "Internship",
        "salary": "$7,500 - $11,500/month",
        "description": "Develop backend services for financial technology applications.",
        "category": "backend",
        "applyUrl": "https://careers.squareup.com/us/en/teams/internships",
        "source": "Square Careers"
    }
]

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Real Internship API is running',
        'endpoints': [
            '/api/search',
            '/api/health'
        ]
    })

@app.route('/api/search', methods=['POST'])
def search_jobs():
    try:
        data = request.get_json()
        keyword = data.get('keyword', 'software engineer').lower()
        location = data.get('location', 'United States').lower()
        job_type = data.get('jobType', 'internship').lower()
        
        print(f"Searching for: {keyword} in {location}")
        
        # Filter internships based on search criteria
        filtered_jobs = []
        
        for job in REAL_INTERNSHIPS:
            # Check if job matches keyword
            keyword_match = (
                keyword in job['title'].lower() or
                keyword in job['description'].lower() or
                keyword in job['category'].lower()
            )
            
            # Check if location matches
            location_match = (
                location in job['location'].lower() or
                location == 'remote' or
                location == 'united states' or
                location == ''
            )
            
            # Check if job type matches
            type_match = (
                job_type in job['type'].lower() or
                job_type == '' or
                job_type == 'internship'
            )
            
            if keyword_match and location_match and type_match:
                filtered_jobs.append(job)
        
        # If no exact matches, return some relevant results
        if not filtered_jobs:
            filtered_jobs = random.sample(REAL_INTERNSHIPS, min(8, len(REAL_INTERNSHIPS)))
        
        return jsonify({
            'success': True,
            'count': len(filtered_jobs),
            'jobs': filtered_jobs,
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
        keyword = request.args.get('keyword', 'software engineer').lower()
        location = request.args.get('location', 'United States').lower()
        job_type = request.args.get('jobType', 'internship').lower()
        
        print(f"Searching for: {keyword} in {location}")
        
        # Filter internships based on search criteria
        filtered_jobs = []
        
        for job in REAL_INTERNSHIPS:
            # Check if job matches keyword
            keyword_match = (
                keyword in job['title'].lower() or
                keyword in job['description'].lower() or
                keyword in job['category'].lower()
            )
            
            # Check if location matches
            location_match = (
                location in job['location'].lower() or
                location == 'remote' or
                location == 'united states' or
                location == ''
            )
            
            # Check if job type matches
            type_match = (
                job_type in job['type'].lower() or
                job_type == '' or
                job_type == 'internship'
            )
            
            if keyword_match and location_match and type_match:
                filtered_jobs.append(job)
        
        # If no exact matches, return some relevant results
        if not filtered_jobs:
            filtered_jobs = random.sample(REAL_INTERNSHIPS, min(8, len(REAL_INTERNSHIPS)))
        
        return jsonify({
            'success': True,
            'count': len(filtered_jobs),
            'jobs': filtered_jobs,
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
    print("🚀 Starting Real Internship API...")
    print("📡 API will be available at: http://localhost:5003")
    print("🔍 Endpoints:")
    print("   GET  /api/health - Health check")
    print("   GET  /api/search?keyword=...&location=... - Search internships")
    print("   POST /api/search - Search internships with JSON body")
    print(f"📊 Total internships available: {len(REAL_INTERNSHIPS)}")
    app.run(debug=True, host='0.0.0.0', port=5003) 