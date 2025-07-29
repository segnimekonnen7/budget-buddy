#!/usr/bin/env python3
"""
Enhanced Streamlit app for ML Internship Finder
Professional version with advanced search and filtering
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime
import random

# Set page config
st.set_page_config(
    page_title="ML Internship Finder",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .job-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .job-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .match-score {
        font-size: 1.5rem;
        font-weight: bold;
        text-align: center;
        padding: 0.5rem;
        border-radius: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .search-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

class EnhancedInternshipFinder:
    def __init__(self):
        self.user_profile = {
            'name': '',
            'skills': [],
            'experience_level': 'Beginner',
            'location': '',
            'remote_only': False,
            'min_salary': 15,
            'preferred_skills': []
        }
        self.applications = []
        self.jobs = self._generate_comprehensive_jobs()
    
    def _generate_comprehensive_jobs(self):
        """Generate comprehensive ML internship jobs"""
        comprehensive_jobs = [
            # Machine Learning Internships
            {
                'title': 'Machine Learning Intern',
                'company': 'Google AI',
                'location': 'Mountain View, CA',
                'remote': False,
                'salary': 45,
                'skills': ['Python', 'TensorFlow', 'Machine Learning', 'Deep Learning', 'Statistics'],
                'description': 'Work on cutting-edge ML projects with Google\'s AI research team. Develop and deploy machine learning models for real-world applications.',
                'requirements': 'Python, ML basics, strong analytical skills, coursework in ML/AI',
                'duration': '12 weeks',
                'type': 'Machine Learning'
            },
            {
                'title': 'ML Research Intern',
                'company': 'OpenAI',
                'location': 'San Francisco, CA',
                'remote': True,
                'salary': 50,
                'skills': ['Python', 'PyTorch', 'Research', 'NLP', 'Transformers'],
                'description': 'Contribute to breakthrough AI research. Work on large language models and advanced NLP techniques.',
                'requirements': 'Python, PyTorch, research experience, strong math background',
                'duration': '16 weeks',
                'type': 'Machine Learning'
            },
            {
                'title': 'Computer Vision Intern',
                'company': 'Tesla',
                'location': 'Palo Alto, CA',
                'remote': False,
                'salary': 40,
                'skills': ['Python', 'OpenCV', 'Computer Vision', 'CNN', 'Autonomous Driving'],
                'description': 'Develop computer vision algorithms for Tesla\'s autonomous driving systems.',
                'requirements': 'Python, OpenCV, computer vision, CNN, autonomous systems',
                'duration': '12 weeks',
                'type': 'Computer Vision'
            },
            {
                'title': 'NLP Intern',
                'company': 'Microsoft',
                'location': 'Redmond, WA',
                'remote': True,
                'salary': 42,
                'skills': ['Python', 'NLTK', 'NLP', 'Transformers', 'BERT'],
                'description': 'Build natural language processing models for Microsoft\'s AI services.',
                'requirements': 'Python, NLP, transformers, text processing, linguistics',
                'duration': '12 weeks',
                'type': 'NLP'
            },
            {
                'title': 'Data Science Intern',
                'company': 'Netflix',
                'location': 'Los Gatos, CA',
                'remote': False,
                'salary': 38,
                'skills': ['Python', 'Pandas', 'SQL', 'Statistics', 'Data Visualization'],
                'description': 'Analyze user behavior data and build recommendation systems for Netflix.',
                'requirements': 'Python, SQL, statistics, data visualization, recommendation systems',
                'duration': '12 weeks',
                'type': 'Data Science'
            },
            {
                'title': 'ML Engineering Intern',
                'company': 'Amazon',
                'location': 'Seattle, WA',
                'remote': True,
                'salary': 44,
                'skills': ['Python', 'MLOps', 'Docker', 'AWS', 'Kubernetes'],
                'description': 'Deploy and maintain ML models in production environments using AWS services.',
                'requirements': 'Python, MLOps, cloud platforms, deployment, AWS',
                'duration': '12 weeks',
                'type': 'ML Engineering'
            },
            {
                'title': 'AI Ethics Intern',
                'company': 'Anthropic',
                'location': 'San Francisco, CA',
                'remote': True,
                'salary': 35,
                'skills': ['Python', 'AI Ethics', 'Fairness', 'Bias Detection', 'Policy'],
                'description': 'Work on AI safety and ethics, ensuring responsible AI development.',
                'requirements': 'Python, AI ethics, fairness, policy, philosophy background',
                'duration': '12 weeks',
                'type': 'AI Ethics'
            },
            {
                'title': 'Robotics ML Intern',
                'company': 'Boston Dynamics',
                'location': 'Waltham, MA',
                'remote': False,
                'salary': 46,
                'skills': ['Python', 'Robotics', 'Control Systems', 'ML', 'ROS'],
                'description': 'Develop machine learning algorithms for robotic control and navigation.',
                'requirements': 'Python, robotics, control systems, ML, ROS',
                'duration': '16 weeks',
                'type': 'Robotics'
            },
            {
                'title': 'Healthcare AI Intern',
                'company': 'Johnson & Johnson',
                'location': 'New Brunswick, NJ',
                'remote': False,
                'salary': 36,
                'skills': ['Python', 'Healthcare', 'Medical Imaging', 'ML', 'Regulatory'],
                'description': 'Develop AI solutions for healthcare applications and medical imaging.',
                'requirements': 'Python, healthcare, medical imaging, ML, regulatory knowledge',
                'duration': '12 weeks',
                'type': 'Healthcare AI'
            },
            {
                'title': 'Financial ML Intern',
                'company': 'Goldman Sachs',
                'location': 'New York, NY',
                'remote': False,
                'salary': 48,
                'skills': ['Python', 'Finance', 'Risk Modeling', 'ML', 'Time Series'],
                'description': 'Build machine learning models for financial risk assessment and trading.',
                'requirements': 'Python, finance, risk modeling, ML, time series analysis',
                'duration': '12 weeks',
                'type': 'Financial ML'
            },
            {
                'title': 'Autonomous Systems Intern',
                'company': 'Waymo',
                'location': 'Mountain View, CA',
                'remote': False,
                'salary': 45,
                'skills': ['Python', 'Autonomous Driving', 'SLAM', 'ML', 'Sensor Fusion'],
                'description': 'Develop algorithms for autonomous vehicle perception and decision-making.',
                'requirements': 'Python, autonomous driving, SLAM, ML, sensor fusion',
                'duration': '16 weeks',
                'type': 'Autonomous Systems'
            },
            {
                'title': 'Quantum ML Intern',
                'company': 'IBM',
                'location': 'Yorktown Heights, NY',
                'remote': True,
                'salary': 40,
                'skills': ['Python', 'Quantum Computing', 'Qiskit', 'ML', 'Quantum Algorithms'],
                'description': 'Explore quantum machine learning algorithms and quantum computing applications.',
                'requirements': 'Python, quantum computing, Qiskit, ML, quantum algorithms',
                'duration': '12 weeks',
                'type': 'Quantum ML'
            }
        ]
        return comprehensive_jobs
    
    def set_user_profile(self, profile):
        """Set user profile"""
        self.user_profile.update(profile)
    
    def search_jobs(self, search_query, filters=None):
        """Search jobs based on query and filters"""
        if not search_query and not filters:
            return self.jobs
        
        filtered_jobs = []
        search_terms = search_query.lower().split() if search_query else []
        
        for job in self.jobs:
            # Text search
            job_text = f"{job['title']} {job['company']} {job['description']} {' '.join(job['skills'])}".lower()
            
            # Check if search terms match
            if search_terms:
                if not any(term in job_text for term in search_terms):
                    continue
            
            # Apply filters
            if filters:
                if filters.get('location') and filters['location'].lower() not in job['location'].lower():
                    continue
                if filters.get('remote_only') and not job['remote']:
                    continue
                if filters.get('min_salary') and job['salary'] < filters['min_salary']:
                    continue
                if filters.get('job_type') and job['type'] != filters['job_type']:
                    continue
            
            filtered_jobs.append(job)
        
        return filtered_jobs
    
    def calculate_match_score(self, job, user_skills):
        """Calculate match score between job and user"""
        if not user_skills:
            return 0.3
        
        # Count matching skills
        matching_skills = sum(1 for skill in user_skills if skill.lower() in [s.lower() for s in job['skills']])
        total_skills = len(job['skills'])
        
        # Base score from skill match
        skill_score = matching_skills / total_skills if total_skills > 0 else 0
        
        # Location preference
        location_score = 0.2 if not self.user_profile['remote_only'] or job['remote'] else 0
        
        # Salary preference
        salary_score = 0.1 if job['salary'] >= self.user_profile['min_salary'] else 0
        
        # Experience level bonus
        experience_bonus = 0.1 if self.user_profile['experience_level'] in ['Intermediate', 'Advanced'] else 0
        
        # Preferred skills bonus
        preferred_bonus = 0.1 if any(skill.lower() in [s.lower() for s in self.user_profile.get('preferred_skills', [])] for skill in job['skills']) else 0
        
        total_score = skill_score + location_score + salary_score + experience_bonus + preferred_bonus
        return min(total_score, 1.0)
    
    def find_matching_jobs(self, search_query="", filters=None):
        """Find jobs matching user profile and search criteria"""
        user_skills = self.user_profile['skills']
        matching_jobs = []
        
        # Search jobs
        searched_jobs = self.search_jobs(search_query, filters)
        
        for job in searched_jobs:
            match_score = self.calculate_match_score(job, user_skills)
            if match_score > 0.1:  # Show all jobs with some match
                job_copy = job.copy()
                job_copy['match_score'] = match_score
                matching_jobs.append(job_copy)
        
        # Sort by match score
        matching_jobs.sort(key=lambda x: x['match_score'], reverse=True)
        return matching_jobs
    
    def apply_to_job(self, job_title):
        """Apply to a job"""
        application = {
            'job_title': job_title,
            'date_applied': datetime.now().strftime('%Y-%m-%d'),
            'status': 'Applied',
            'company': next((job['company'] for job in self.jobs if job['title'] == job_title), 'Unknown')
        }
        self.applications.append(application)
    
    def get_application_stats(self):
        """Get application statistics"""
        if not self.applications:
            return {'total': 0, 'applied': 0, 'interviewed': 0, 'offered': 0}
        
        stats = {'total': len(self.applications)}
        for app in self.applications:
            status = app['status']
            if status == 'Applied':
                stats['applied'] = stats.get('applied', 0) + 1
            elif status == 'Interviewed':
                stats['interviewed'] = stats.get('interviewed', 0) + 1
            elif status == 'Offered':
                stats['offered'] = stats.get('offered', 0) + 1
        
        return stats

@st.cache_resource
def load_finder():
    """Load the internship finder"""
    return EnhancedInternshipFinder()

def create_application_chart(stats):
    """Create application status chart"""
    if stats['total'] == 0:
        return None
    
    data = {
        'Status': ['Applied', 'Interviewed', 'Offered'],
        'Count': [stats['applied'], stats['interviewed'], stats['offered']]
    }
    
    df = pd.DataFrame(data)
    fig = px.bar(df, x='Status', y='Count', 
                title="Application Status",
                color='Status',
                color_discrete_map={
                    'Applied': '#667eea',
                    'Interviewed': '#ff7f0e',
                    'Offered': '#2ca02c'
                })
    
    return fig

def main():
    # Header
    st.markdown('<h1 class="main-header">🎯 Enhanced ML Internship Finder</h1>', unsafe_allow_html=True)
    st.markdown("### AI-powered internship search with advanced filtering and matching")
    
    # Load finder
    finder = load_finder()
    
    # Sidebar
    st.sidebar.title("👤 User Profile")
    
    # User profile form
    with st.sidebar.form("user_profile"):
        st.subheader("Your Profile")
        
        name = st.text_input("Name", value=finder.user_profile.get('name', ''))
        skills = st.text_area("Skills (comma-separated)", 
                             value=', '.join(finder.user_profile.get('skills', [])))
        experience = st.selectbox("Experience Level", 
                                 ['Beginner', 'Intermediate', 'Advanced'],
                                 index=['Beginner', 'Intermediate', 'Advanced'].index(
                                     finder.user_profile.get('experience_level', 'Beginner')))
        location = st.text_input("Preferred Location", 
                                value=finder.user_profile.get('location', ''))
        remote_preference = st.checkbox("Remote Only", 
                                       value=finder.user_profile.get('remote_only', False))
        min_salary = st.number_input("Minimum Salary ($/hour)", 
                                    min_value=0, max_value=100, 
                                    value=finder.user_profile.get('min_salary', 15))
        preferred_skills = st.text_area("Preferred Skills (comma-separated)",
                                       value=', '.join(finder.user_profile.get('preferred_skills', [])))
        
        submitted = st.form_submit_button("Update Profile")
        
        if submitted:
            finder.set_user_profile({
                'name': name,
                'skills': [s.strip() for s in skills.split(',') if s.strip()],
                'experience_level': experience,
                'location': location,
                'remote_only': remote_preference,
                'min_salary': min_salary,
                'preferred_skills': [s.strip() for s in preferred_skills.split(',') if s.strip()]
            })
            st.success("Profile updated!")
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Search Jobs", "📊 Analytics", "📝 Applications", "💡 Tips"])
    
    with tab1:
        st.header("🔍 Search ML Internships")
        
        # Search and filter section
        st.markdown('<div class="search-box">', unsafe_allow_html=True)
        st.subheader("Search & Filters")
        
        col1, col2 = st.columns(2)
        with col1:
            search_query = st.text_input("Search jobs (title, company, skills, description):", 
                                       placeholder="e.g., machine learning, Google, Python")
        
        with col2:
            job_types = ['All'] + list(set(job['type'] for job in finder.jobs))
            selected_type = st.selectbox("Job Type", job_types)
        
        col3, col4, col5 = st.columns(3)
        with col3:
            location_filter = st.text_input("Location filter:", placeholder="e.g., California")
        with col4:
            remote_filter = st.checkbox("Remote only")
        with col5:
            min_salary_filter = st.number_input("Min salary ($/hr)", min_value=0, max_value=100, value=0)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Apply filters
        filters = {}
        if location_filter:
            filters['location'] = location_filter
        if remote_filter:
            filters['remote_only'] = True
        if min_salary_filter > 0:
            filters['min_salary'] = min_salary_filter
        if selected_type != 'All':
            filters['job_type'] = selected_type
        
        # Find matching jobs
        matching_jobs = finder.find_matching_jobs(search_query, filters)
        
        if matching_jobs:
            st.subheader(f"Found {len(matching_jobs)} matching internships")
            
            # Sort options
            sort_by = st.selectbox("Sort by:", ["Match Score", "Salary", "Company", "Location"])
            if sort_by == "Salary":
                matching_jobs.sort(key=lambda x: x['salary'], reverse=True)
            elif sort_by == "Company":
                matching_jobs.sort(key=lambda x: x['company'])
            elif sort_by == "Location":
                matching_jobs.sort(key=lambda x: x['location'])
            
            for job in matching_jobs:
                with st.container():
                    st.markdown('<div class="job-card">', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(job['title'])
                        st.write(f"**Company:** {job['company']}")
                        st.write(f"**Location:** {job['location']} {'(Remote)' if job['remote'] else ''}")
                        st.write(f"**Salary:** ${job['salary']}/hour")
                        st.write(f"**Duration:** {job['duration']}")
                        st.write(f"**Type:** {job['type']}")
                        st.write(f"**Skills:** {', '.join(job['skills'])}")
                        st.write(f"**Description:** {job['description']}")
                        st.write(f"**Requirements:** {job['requirements']}")
                    
                    with col2:
                        match_score = job['match_score']
                        if match_score > 0.7:
                            st.markdown(f'<div class="match-score" style="background-color: #4CAF50; color: white;">{match_score:.0%}</div>', unsafe_allow_html=True)
                        elif match_score > 0.4:
                            st.markdown(f'<div class="match-score" style="background-color: #FF9800; color: white;">{match_score:.0%}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="match-score" style="background-color: #f44336; color: white;">{match_score:.0%}</div>', unsafe_allow_html=True)
                        
                        if st.button(f"Apply", key=f"apply_{job['title']}"):
                            finder.apply_to_job(job['title'])
                            st.success(f"Applied to {job['title']}!")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No matching jobs found. Try adjusting your search criteria or updating your profile.")
    
    with tab2:
        st.header("📊 Analytics Dashboard")
        
        # Job market insights
        st.subheader("Job Market Insights")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Jobs", len(finder.jobs))
        with col2:
            avg_salary = sum(job['salary'] for job in finder.jobs) / len(finder.jobs)
            st.metric("Avg Salary", f"${avg_salary:.0f}/hr")
        with col3:
            remote_jobs = sum(1 for job in finder.jobs if job['remote'])
            st.metric("Remote Jobs", remote_jobs)
        with col4:
            matching_jobs = finder.find_matching_jobs()
            st.metric("Your Matches", len(matching_jobs))
        
        # Top skills chart
        st.subheader("Most Required Skills")
        all_skills = []
        for job in finder.jobs:
            all_skills.extend(job['skills'])
        
        skill_counts = pd.Series(all_skills).value_counts().head(10)
        fig = px.bar(x=skill_counts.values, y=skill_counts.index, 
                    title="Top Skills in Demand",
                    orientation='h')
        st.plotly_chart(fig, use_container_width=True)
        
        # Salary distribution
        st.subheader("Salary Distribution")
        salaries = [job['salary'] for job in finder.jobs]
        fig2 = px.histogram(x=salaries, title="Salary Distribution", nbins=10)
        st.plotly_chart(fig2, use_container_width=True)
        
        # Job types distribution
        st.subheader("Job Types Distribution")
        job_types = [job['type'] for job in finder.jobs]
        type_counts = pd.Series(job_types).value_counts()
        fig3 = px.pie(values=type_counts.values, names=type_counts.index, title="Job Types")
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab3:
        st.header("📝 Application Tracking")
        
        if finder.applications:
            st.subheader("Your Applications")
            
            # Display applications
            for app in finder.applications:
                with st.container():
                    st.markdown('<div class="job-card">', unsafe_allow_html=True)
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"**Job:** {app['job_title']}")
                        st.write(f"**Company:** {app['company']}")
                    with col2:
                        st.write(f"**Applied:** {app['date_applied']}")
                    with col3:
                        status = st.selectbox(
                            "Status",
                            ['Applied', 'Interviewed', 'Offered', 'Rejected'],
                            index=['Applied', 'Interviewed', 'Offered', 'Rejected'].index(app['status']),
                            key=f"status_{app['job_title']}"
                        )
                        app['status'] = status
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # Application statistics
            stats = finder.get_application_stats()
            chart = create_application_chart(stats)
            if chart:
                st.plotly_chart(chart, use_container_width=True)
        else:
            st.info("No applications yet. Apply to some jobs to track your progress!")
    
    with tab4:
        st.header("💡 Application Tips")
        
        tips = [
            {
                "title": "Resume Optimization",
                "content": "Tailor your resume to highlight ML skills, projects, and relevant coursework. Include specific technologies and frameworks you've used."
            },
            {
                "title": "Portfolio Projects",
                "content": "Build and showcase ML projects on GitHub. Include Jupyter notebooks, documentation, and live demos."
            },
            {
                "title": "Networking",
                "content": "Attend ML meetups, conferences, and connect with professionals on LinkedIn. Many internships come through networking."
            },
            {
                "title": "Interview Preparation",
                "content": "Practice coding problems, ML concepts, and be ready to discuss your projects in detail."
            },
            {
                "title": "Follow Up",
                "content": "Send thank-you emails after interviews and follow up on applications after 1-2 weeks."
            },
            {
                "title": "Skill Development",
                "content": "Focus on in-demand skills like Python, TensorFlow, PyTorch, and cloud platforms (AWS, GCP)."
            }
        ]
        
        for tip in tips:
            with st.expander(tip['title']):
                st.write(tip['content'])

if __name__ == "__main__":
    main() 