#!/usr/bin/env python3
"""
Simplified Streamlit app for ML Internship Finder
Deployment-ready version with minimal dependencies
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
</style>
""", unsafe_allow_html=True)

class SimpleInternshipFinder:
    def __init__(self):
        self.user_profile = {
            'name': '',
            'skills': [],
            'experience_level': 'Beginner',
            'location': '',
            'remote_only': False,
            'min_salary': 15
        }
        self.applications = []
        self.jobs = self._generate_sample_jobs()
    
    def _generate_sample_jobs(self):
        """Generate sample ML internship jobs"""
        sample_jobs = [
            {
                'title': 'Machine Learning Intern',
                'company': 'TechCorp AI',
                'location': 'San Francisco, CA',
                'remote': True,
                'salary': 25,
                'skills': ['Python', 'TensorFlow', 'Machine Learning'],
                'description': 'Work on cutting-edge ML projects with our AI team.',
                'requirements': 'Python, ML basics, strong analytical skills'
            },
            {
                'title': 'Data Science Intern',
                'company': 'DataFlow Analytics',
                'location': 'New York, NY',
                'remote': False,
                'salary': 30,
                'skills': ['Python', 'Pandas', 'SQL', 'Statistics'],
                'description': 'Analyze large datasets and build predictive models.',
                'requirements': 'Python, SQL, statistics, data visualization'
            },
            {
                'title': 'AI Research Intern',
                'company': 'InnovateAI Labs',
                'location': 'Boston, MA',
                'remote': True,
                'salary': 28,
                'skills': ['Python', 'PyTorch', 'Deep Learning', 'Research'],
                'description': 'Contribute to breakthrough AI research projects.',
                'requirements': 'Python, deep learning, research experience'
            },
            {
                'title': 'Computer Vision Intern',
                'company': 'VisionTech Solutions',
                'location': 'Seattle, WA',
                'remote': False,
                'salary': 32,
                'skills': ['Python', 'OpenCV', 'Computer Vision', 'CNN'],
                'description': 'Develop computer vision algorithms for real-world applications.',
                'requirements': 'Python, OpenCV, computer vision, CNN'
            },
            {
                'title': 'NLP Intern',
                'company': 'LanguageAI Systems',
                'location': 'Austin, TX',
                'remote': True,
                'salary': 26,
                'skills': ['Python', 'NLTK', 'NLP', 'Transformers'],
                'description': 'Build natural language processing models and applications.',
                'requirements': 'Python, NLP, transformers, text processing'
            },
            {
                'title': 'ML Engineering Intern',
                'company': 'MLOps Solutions',
                'location': 'Denver, CO',
                'remote': False,
                'salary': 35,
                'skills': ['Python', 'MLOps', 'Docker', 'AWS'],
                'description': 'Deploy and maintain ML models in production environments.',
                'requirements': 'Python, MLOps, cloud platforms, deployment'
            }
        ]
        return sample_jobs
    
    def set_user_profile(self, profile):
        """Set user profile"""
        self.user_profile.update(profile)
    
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
        
        total_score = skill_score + location_score + salary_score + experience_bonus
        return min(total_score, 1.0)
    
    def find_matching_jobs(self):
        """Find jobs matching user profile"""
        user_skills = self.user_profile['skills']
        matching_jobs = []
        
        for job in self.jobs:
            match_score = self.calculate_match_score(job, user_skills)
            if match_score > 0.2:  # Only show jobs with decent match
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
    return SimpleInternshipFinder()

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
    st.markdown('<h1 class="main-header">🎯 ML Internship Finder</h1>', unsafe_allow_html=True)
    st.markdown("### AI-powered internship matching and application tracking")
    
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
        
        submitted = st.form_submit_button("Update Profile")
        
        if submitted:
            finder.set_user_profile({
                'name': name,
                'skills': [s.strip() for s in skills.split(',') if s.strip()],
                'experience_level': experience,
                'location': location,
                'remote_only': remote_preference,
                'min_salary': min_salary
            })
            st.success("Profile updated!")
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Find Jobs", "📊 Analytics", "📝 Applications", "💡 Tips"])
    
    with tab1:
        st.header("🔍 Find ML Internships")
        
        # Find matching jobs
        matching_jobs = finder.find_matching_jobs()
        
        if matching_jobs:
            st.subheader(f"Found {len(matching_jobs)} matching internships")
            
            for job in matching_jobs:
                with st.container():
                    st.markdown('<div class="job-card">', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.subheader(job['title'])
                        st.write(f"**Company:** {job['company']}")
                        st.write(f"**Location:** {job['location']} {'(Remote)' if job['remote'] else ''}")
                        st.write(f"**Salary:** ${job['salary']}/hour")
                        st.write(f"**Skills:** {', '.join(job['skills'])}")
                        st.write(f"**Description:** {job['description']}")
                    
                    with col2:
                        match_score = job['match_score']
                        if match_score > 0.7:
                            st.markdown(f'<div class="match-score" style="background-color: #4CAF50; color: white;">{match_score:.0%}</div>', unsafe_allow_html=True)
                        elif match_score > 0.4:
                            st.markdown(f'<div class="match-score" style="background-color: #FF9800; color: white;">{match_score:.0%}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="match-score" style="background-color: #f44336; color: white;">{match_score:.0%}</div>', unsafe_allow_html=True)
                        
                        if st.button(f"Apply to {job['title']}", key=f"apply_{job['title']}"):
                            finder.apply_to_job(job['title'])
                            st.success(f"Applied to {job['title']}!")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No matching jobs found. Try updating your profile or skills.")
    
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
            }
        ]
        
        for tip in tips:
            with st.expander(tip['title']):
                st.write(tip['content'])

if __name__ == "__main__":
    main() 