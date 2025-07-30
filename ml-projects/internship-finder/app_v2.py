import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime
import random

# Page configuration
st.set_page_config(
    page_title="🎯 Enhanced ML Internship Finder v2.0",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .job-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .search-box {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

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

@st.cache_resource
def load_finder():
    """Load the internship finder"""
    return EnhancedInternshipFinder()

def create_application_chart(stats):
    """Create application statistics chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=stats['application_rate'],
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Weekly Application Rate"},
        delta={'reference': 20},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 20], 'color': "lightgray"},
                {'range': [20, 50], 'color': "yellow"},
                {'range': [50, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    return fig

def main():
    st.markdown('<h1 class="main-header">🎯 Enhanced ML Internship Finder v2.0</h1>', unsafe_allow_html=True)
    st.markdown("### AI-powered internship matching and application tracking")
    
    # Initialize finder
    finder = load_finder()
    
    # Sidebar for user profile
    with st.sidebar:
        st.header("👤 Your Profile")
        
        # Skills input
        skills_input = st.text_area(
            "Your Skills (comma-separated):",
            placeholder="Python, Machine Learning, TensorFlow, Data Analysis...",
            help="Enter your technical skills to get better job matches"
        )
        
        if skills_input:
            skills = [skill.strip() for skill in skills_input.split(',') if skill.strip()]
            finder.set_user_profile({'skills': skills})
        
        # Experience level
        experience = st.selectbox(
            "Experience Level:",
            ["Beginner", "Intermediate", "Advanced", "Expert"]
        )
        
        # Preferred location
        preferred_location = st.selectbox(
            "Preferred Location:",
            ["Any", "Remote", "On-site", "Hybrid"]
        )
        
        # Salary expectations
        min_salary = st.slider(
            "Minimum Salary ($/hr):",
            min_value=20,
            max_value=60,
            value=30,
            step=5
        )
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Find Jobs", "📊 Analytics", "📝 Applications", "💡 Tips"])
    
    with tab1:
        st.header("🔍 Find ML Internships")
        
        # Search and filters
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            search_query = st.text_input(
                "Search jobs:",
                placeholder="Enter keywords like 'computer vision', 'NLP', 'research'..."
            )
        
        with col2:
            location_filter = st.selectbox(
                "Location:",
                ["All", "Remote", "On-site", "Hybrid"]
            )
        
        with col3:
            job_type_filter = st.selectbox(
                "Job Type:",
                ["All", "Research", "Engineering", "Analytics"]
            )
        
        # Apply filters
        filters = {
            'location': location_filter if location_filter != "All" else None,
            'job_type': job_type_filter if job_type_filter != "All" else None,
            'min_salary': min_salary
        }
        
        # Find matching jobs
        matching_jobs = finder.find_matching_jobs(search_query, filters)
        
        # Sort options
        sort_by = st.selectbox(
            "Sort by:",
            ["Match Score", "Salary", "Company", "Location"]
        )
        
        if sort_by == "Salary":
            matching_jobs.sort(key=lambda x: x['salary'], reverse=True)
        elif sort_by == "Company":
            matching_jobs.sort(key=lambda x: x['company'])
        elif sort_by == "Location":
            matching_jobs.sort(key=lambda x: x['location'])
        
        # Display results
        st.markdown(f"**Found {len(matching_jobs)} matching internships**")
        
        for job in matching_jobs:
            with st.container():
                st.markdown(f"""
                <div class="job-card">
                    <h3>{job['title']}</h3>
                    <p><strong>Company:</strong> {job['company']}</p>
                    <p><strong>Location:</strong> {job['location']} ({job['remote']})</p>
                    <p><strong>Salary:</strong> ${job['salary']}/hour</p>
                    <p><strong>Skills:</strong> {', '.join(job['skills'])}</p>
                    <p><strong>Description:</strong> {job['description']}</p>
                    <p><strong>Job Type:</strong> {job['job_type']} | <strong>Duration:</strong> {job['duration']}</p>
                    <p><strong>Requirements:</strong> {job['requirements']}</p>
                    <p><strong>Match Score:</strong> {job['match_score']}%</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button(f"Apply to {job['title']}", key=f"apply_{job['title']}"):
                        finder.apply_to_job(job['title'])
                        st.success(f"Applied to {job['title']}!")
                        st.rerun()
                
                with col2:
                    if st.button(f"Save {job['title']}", key=f"save_{job['title']}"):
                        st.info(f"Saved {job['title']} to your list!")
                
                st.divider()
    
    with tab2:
        st.header("📊 Analytics Dashboard")
        
        # Application statistics
        stats = finder.get_application_stats()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Applications", stats['total_applications'])
        
        with col2:
            st.metric("Recent Applications (7 days)", stats['recent_applications'])
        
        with col3:
            st.metric("Weekly Application Rate", f"{stats['application_rate']:.1f}%")
        
        # Application rate chart
        st.plotly_chart(create_application_chart(stats), use_container_width=True)
        
        # Job distribution by company
        if matching_jobs:
            company_counts = {}
            for job in matching_jobs:
                company = job['company']
                company_counts[company] = company_counts.get(company, 0) + 1
            
            fig = px.bar(
                x=list(company_counts.keys()),
                y=list(company_counts.values()),
                title="Job Distribution by Company",
                labels={'x': 'Company', 'y': 'Number of Jobs'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.header("📝 Your Applications")
        
        if not finder.applications:
            st.info("You haven't applied to any jobs yet. Start applying to track your progress!")
        else:
            for app in reversed(finder.applications):
                st.markdown(f"""
                - **{app['job_title']}** - Applied on {app['date']} - Status: {app['status']}
                """)
    
    with tab4:
        st.header("💡 Application Tips")
        
        st.markdown("""
        ### 🎯 **How to Get the Best ML Internships:**
        
        **1. Build a Strong Portfolio**
        - Create ML projects on GitHub
        - Participate in Kaggle competitions
        - Write technical blog posts
        
        **2. Network Effectively**
        - Attend ML conferences and meetups
        - Connect with professionals on LinkedIn
        - Join ML communities and forums
        
        **3. Prepare for Interviews**
        - Practice coding problems on LeetCode
        - Review ML fundamentals and algorithms
        - Prepare for behavioral questions
        
        **4. Customize Your Applications**
        - Tailor your resume for each position
        - Write personalized cover letters
        - Highlight relevant projects and skills
        
        **5. Follow Up**
        - Send thank-you emails after interviews
        - Follow up on applications after 1-2 weeks
        - Stay connected with recruiters
        """)

if __name__ == "__main__":
    main() 