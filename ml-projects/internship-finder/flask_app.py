from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
from datetime import datetime
import os

app = Flask(__name__)

class EnhancedInternshipFinder:
    def __init__(self):
        self.jobs = self._generate_comprehensive_jobs()
        self.user_profile = {}
        self.applications = []
        self.load_data()
    
    def _generate_comprehensive_jobs(self):
        """Generate 12 comprehensive ML internship opportunities"""
        return [
            {
                "title": "Machine Learning Intern",
                "company": "Google AI",
                "location": "Mountain View, CA",
                "remote": "Hybrid",
                "salary": 45,
                "skills": ["Python", "TensorFlow", "Machine Learning", "Deep Learning", "Research"],
                "description": "Work on cutting-edge ML research projects with Google's AI team. Contribute to publications and real-world applications.",
                "job_type": "Research",
                "duration": "3-6 months",
                "requirements": "Strong ML fundamentals, research experience preferred"
            },
            {
                "title": "ML Research Intern",
                "company": "OpenAI",
                "location": "San Francisco, CA",
                "remote": "On-site",
                "salary": 50,
                "skills": ["Python", "PyTorch", "Deep Learning", "NLP", "Research"],
                "description": "Contribute to breakthrough AI research. Work on large language models and advanced AI systems.",
                "job_type": "Research",
                "duration": "3-6 months",
                "requirements": "Strong research background, publications preferred"
            },
            {
                "title": "Computer Vision Intern",
                "company": "Tesla",
                "location": "Palo Alto, CA",
                "remote": "On-site",
                "salary": 40,
                "skills": ["Python", "OpenCV", "Computer Vision", "CNN", "Autonomous Driving"],
                "description": "Develop computer vision algorithms for Tesla's autonomous driving systems.",
                "job_type": "Engineering",
                "duration": "3-6 months",
                "requirements": "Computer vision experience, C++ knowledge helpful"
            },
            {
                "title": "NLP Intern",
                "company": "Microsoft",
                "location": "Redmond, WA",
                "remote": "Hybrid",
                "salary": 42,
                "skills": ["Python", "NLTK", "NLP", "Transformers", "Azure"],
                "description": "Build natural language processing models for Microsoft's AI services.",
                "job_type": "Engineering",
                "duration": "3-6 months",
                "requirements": "NLP experience, cloud computing knowledge"
            },
            {
                "title": "Data Science Intern",
                "company": "Netflix",
                "location": "Los Gatos, CA",
                "remote": "Hybrid",
                "salary": 38,
                "skills": ["Python", "Pandas", "SQL", "Statistics", "Recommendation Systems"],
                "description": "Analyze user behavior data and build recommendation algorithms for Netflix.",
                "job_type": "Analytics",
                "duration": "3-6 months",
                "requirements": "Statistics background, big data experience"
            },
            {
                "title": "ML Engineering Intern",
                "company": "Amazon",
                "location": "Seattle, WA",
                "remote": "On-site",
                "salary": 44,
                "skills": ["Python", "MLOps", "Docker", "AWS", "Machine Learning"],
                "description": "Deploy and maintain ML models in production environments at Amazon.",
                "job_type": "Engineering",
                "duration": "3-6 months",
                "requirements": "Software engineering skills, cloud experience"
            },
            {
                "title": "AI Research Intern",
                "company": "Meta AI",
                "location": "Menlo Park, CA",
                "remote": "Hybrid",
                "salary": 46,
                "skills": ["Python", "PyTorch", "Deep Learning", "Research", "Social AI"],
                "description": "Research AI applications for social media and virtual reality.",
                "job_type": "Research",
                "duration": "3-6 months",
                "requirements": "Research experience, social computing interest"
            },
            {
                "title": "Robotics ML Intern",
                "company": "Boston Dynamics",
                "location": "Waltham, MA",
                "remote": "On-site",
                "salary": 43,
                "skills": ["Python", "ROS", "Robotics", "Machine Learning", "Control Systems"],
                "description": "Develop ML algorithms for robot learning and control systems.",
                "job_type": "Engineering",
                "duration": "3-6 months",
                "requirements": "Robotics experience, control theory knowledge"
            },
            {
                "title": "Healthcare AI Intern",
                "company": "Johnson & Johnson",
                "location": "New Brunswick, NJ",
                "remote": "Hybrid",
                "salary": 36,
                "skills": ["Python", "Medical AI", "Deep Learning", "Healthcare", "Data Analysis"],
                "description": "Apply AI to healthcare challenges and medical device development.",
                "job_type": "Research",
                "duration": "3-6 months",
                "requirements": "Healthcare interest, medical data experience"
            },
            {
                "title": "Financial ML Intern",
                "company": "Goldman Sachs",
                "location": "New York, NY",
                "remote": "On-site",
                "salary": 48,
                "skills": ["Python", "Quantitative Finance", "Machine Learning", "Statistics", "Risk Models"],
                "description": "Develop ML models for financial risk assessment and trading strategies.",
                "job_type": "Analytics",
                "duration": "3-6 months",
                "requirements": "Finance knowledge, quantitative skills"
            },
            {
                "title": "Computer Vision Intern",
                "company": "NVIDIA",
                "location": "Santa Clara, CA",
                "remote": "Hybrid",
                "salary": 45,
                "skills": ["Python", "CUDA", "Computer Vision", "GPU Computing", "Deep Learning"],
                "description": "Optimize computer vision algorithms for GPU acceleration.",
                "job_type": "Engineering",
                "duration": "3-6 months",
                "requirements": "GPU programming experience, computer vision skills"
            },
            {
                "title": "ML Infrastructure Intern",
                "company": "Uber",
                "location": "San Francisco, CA",
                "remote": "Hybrid",
                "salary": 41,
                "skills": ["Python", "Distributed Systems", "MLOps", "Kubernetes", "Machine Learning"],
                "description": "Build scalable ML infrastructure for Uber's platform.",
                "job_type": "Engineering",
                "duration": "3-6 months",
                "requirements": "Distributed systems experience, cloud computing"
            }
        ]
    
    def set_user_profile(self, profile):
        """Set user profile for matching"""
        self.user_profile = profile
    
    def search_jobs(self, search_query, filters=None):
        """Search jobs based on query and filters"""
        if not search_query and not filters:
            return self.jobs
        
        filtered_jobs = []
        search_terms = search_query.lower().split() if search_query else []
        
        for job in self.jobs:
            # Text search
            job_text = f"{job['title']} {job['company']} {job['description']} {' '.join(job['skills'])}".lower()
            text_match = all(term in job_text for term in search_terms) if search_terms else True
            
            # Filter matching
            filter_match = True
            if filters:
                if filters.get('location') and filters['location'] != 'All':
                    if filters['location'] == 'Remote' and job['remote'] != 'Remote':
                        filter_match = False
                    elif filters['location'] == 'On-site' and job['remote'] == 'Remote':
                        filter_match = False
                
                if filters.get('job_type') and filters['job_type'] != 'All':
                    if job['job_type'] != filters['job_type']:
                        filter_match = False
                
                if filters.get('min_salary'):
                    if job['salary'] < filters['min_salary']:
                        filter_match = False
            
            if text_match and filter_match:
                filtered_jobs.append(job)
        
        return filtered_jobs
    
    def calculate_match_score(self, job, user_skills):
        """Calculate match score based on user skills"""
        if not user_skills:
            return 30  # Default score
        
        job_skills = set(skill.lower() for skill in job['skills'])
        user_skill_set = set(skill.lower() for skill in user_skills)
        
        if not job_skills:
            return 30
        
        # Calculate skill overlap
        overlap = len(job_skills.intersection(user_skill_set))
        total_skills = len(job_skills)
        
        # Base score + skill match bonus
        base_score = 30
        skill_bonus = (overlap / total_skills) * 70
        
        return min(100, int(base_score + skill_bonus))
    
    def find_matching_jobs(self, search_query="", filters=None):
        """Find jobs matching user profile and search criteria"""
        matching_jobs = self.search_jobs(search_query, filters)
        
        # Calculate match scores
        for job in matching_jobs:
            user_skills = self.user_profile.get('skills', [])
            job['match_score'] = self.calculate_match_score(job, user_skills)
        
        # Sort by match score (descending)
        matching_jobs.sort(key=lambda x: x['match_score'], reverse=True)
        
        return matching_jobs
    
    def apply_to_job(self, job_title):
        """Apply to a job"""
        application = {
            'job_title': job_title,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'status': 'Applied'
        }
        self.applications.append(application)
        self.save_data()
    
    def get_application_stats(self):
        """Get application statistics"""
        if not self.applications:
            return {
                'total_applications': 0,
                'recent_applications': 0,
                'application_rate': 0
            }
        
        total = len(self.applications)
        recent = len([app for app in self.applications 
                     if (datetime.now() - datetime.strptime(app['date'], '%Y-%m-%d %H:%M')).days <= 7])
        
        return {
            'total_applications': total,
            'recent_applications': recent,
            'application_rate': min(100, (recent / 7) * 100)  # Applications per week
        }
    
    def load_data(self):
        """Load saved data"""
        try:
            with open('internship_data.json', 'r') as f:
                data = json.load(f)
                self.applications = data.get('applications', [])
        except FileNotFoundError:
            self.applications = []
    
    def save_data(self):
        """Save data to file"""
        data = {
            'applications': self.applications
        }
        with open('internship_data.json', 'w') as f:
            json.dump(data, f)

# Initialize the finder
finder = EnhancedInternshipFinder()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/jobs')
def get_jobs():
    """API endpoint to get jobs"""
    search_query = request.args.get('search', '')
    location_filter = request.args.get('location', 'All')
    job_type_filter = request.args.get('job_type', 'All')
    min_salary = request.args.get('min_salary', 0, type=int)
    
    filters = {
        'location': location_filter if location_filter != "All" else None,
        'job_type': job_type_filter if job_type_filter != "All" else None,
        'min_salary': min_salary if min_salary > 0 else None
    }
    
    jobs = finder.find_matching_jobs(search_query, filters)
    return jsonify(jobs)

@app.route('/api/apply', methods=['POST'])
def apply_to_job():
    """API endpoint to apply to a job"""
    data = request.get_json()
    job_title = data.get('job_title')
    
    if job_title:
        finder.apply_to_job(job_title)
        return jsonify({'success': True, 'message': f'Applied to {job_title}!'})
    
    return jsonify({'success': False, 'message': 'Job title required'})

@app.route('/api/stats')
def get_stats():
    """API endpoint to get application statistics"""
    stats = finder.get_application_stats()
    return jsonify(stats)

@app.route('/api/profile', methods=['POST'])
def update_profile():
    """API endpoint to update user profile"""
    data = request.get_json()
    skills = data.get('skills', [])
    
    finder.set_user_profile({'skills': skills})
    return jsonify({'success': True, 'message': 'Profile updated!'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 