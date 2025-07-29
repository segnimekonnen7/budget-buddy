#!/usr/bin/env python3
"""
Streamlit app for ML Internship Finder
Deployment-ready version
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from internship_finder import InternshipFinder
import json
from datetime import datetime

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
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_finder():
    """Load the internship finder"""
    finder = InternshipFinder()
    return finder

def main():
    # Header
    st.markdown('<h1 class="main-header">🎯 ML Internship Finder</h1>', unsafe_allow_html=True)
    
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
        
        # Search options
        col1, col2 = st.columns(2)
        
        with col1:
            search_keywords = st.text_input("Search Keywords", 
                                          placeholder="e.g., machine learning, python, data science")
            company_filter = st.text_input("Company Filter", 
                                         placeholder="e.g., Google, Microsoft")
        
        with col2:
            location_filter = st.text_input("Location Filter", 
                                          placeholder="e.g., San Francisco, Remote")
            sort_by = st.selectbox("Sort By", 
                                 ['Match Score', 'Salary', 'Company', 'Location'])
        
        # Filter options
        with st.expander("Advanced Filters"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                min_salary_filter = st.number_input("Min Salary ($/hour)", 
                                                  min_value=0, max_value=100, value=15)
                remote_only = st.checkbox("Remote Only")
            
            with col2:
                required_skills = st.text_input("Required Skills", 
                                              placeholder="e.g., python, tensorflow")
                experience_level = st.selectbox("Experience Level", 
                                              ['Any', 'Beginner', 'Intermediate', 'Advanced'])
            
            with col3:
                job_type = st.selectbox("Job Type", 
                                      ['Any', 'Full-time', 'Part-time', 'Contract'])
                duration = st.selectbox("Duration", 
                                      ['Any', '3 months', '6 months', '12 months'])
        
        # Search button
        if st.button("🔍 Search Internships", type="primary"):
            with st.spinner("Searching for internships..."):
                # Get jobs
                jobs = finder.scrape_jobs()
                
                # Apply filters
                filtered_jobs = finder.filter_jobs(
                    jobs,
                    keywords=search_keywords if search_keywords else None,
                    company=company_filter if company_filter else None,
                    location=location_filter if location_filter else None,
                    remote_only=remote_only,
                    min_salary=min_salary_filter,
                    required_skills=[s.strip() for s in required_skills.split(',')] if required_skills else [],
                    experience_level=experience_level if experience_level != 'Any' else None
                )
                
                # Calculate match scores
                for job in filtered_jobs:
                    job['match_score'] = finder.calculate_match_score(job)
                
                # Sort jobs
                if sort_by == 'Match Score':
                    filtered_jobs.sort(key=lambda x: x['match_score'], reverse=True)
                elif sort_by == 'Salary':
                    filtered_jobs.sort(key=lambda x: x.get('salary', 0), reverse=True)
                elif sort_by == 'Company':
                    filtered_jobs.sort(key=lambda x: x.get('company', ''))
                elif sort_by == 'Location':
                    filtered_jobs.sort(key=lambda x: x.get('location', ''))
                
                st.session_state.filtered_jobs = filtered_jobs
        
        # Display results
        if 'filtered_jobs' in st.session_state and st.session_state.filtered_jobs:
            jobs = st.session_state.filtered_jobs
            
            st.subheader(f"Found {len(jobs)} internships")
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                avg_salary = sum(j.get('salary', 0) for j in jobs) / len(jobs)
                st.metric("Avg Salary", f"${avg_salary:.1f}/hr")
            with col2:
                avg_match = sum(j['match_score'] for j in jobs) / len(jobs)
                st.metric("Avg Match", f"{avg_match:.1f}%")
            with col3:
                remote_count = sum(1 for j in jobs if j.get('remote', False))
                st.metric("Remote Jobs", remote_count)
            with col4:
                top_companies = pd.Series([j.get('company', '') for j in jobs]).value_counts().head(1)
                st.metric("Top Company", top_companies.index[0] if len(top_companies) > 0 else "N/A")
            
            # Display jobs
            for i, job in enumerate(jobs):
                with st.container():
                    st.markdown('<div class="job-card">', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.subheader(f"🎯 {job['title']}")
                        st.write(f"**Company:** {job['company']}")
                        st.write(f"**Location:** {job['location']}")
                        st.write(f"**Salary:** ${job.get('salary', 'N/A')}/hour")
                        
                        if job.get('description'):
                            with st.expander("Job Description"):
                                st.write(job['description'][:500] + "..." if len(job['description']) > 500 else job['description'])
                        
                        if job.get('requirements'):
                            with st.expander("Requirements"):
                                for req in job['requirements']:
                                    st.write(f"• {req}")
                    
                    with col2:
                        match_score = job['match_score']
                        if match_score >= 80:
                            color = "green"
                        elif match_score >= 60:
                            color = "orange"
                        else:
                            color = "red"
                        
                        st.markdown(f'<div class="match-score" style="background-color: {color}; color: white;">{match_score:.0f}% Match</div>', unsafe_allow_html=True)
                        
                        if st.button(f"Apply", key=f"apply_{i}"):
                            finder.track_application(job)
                            st.success("Application tracked!")
                        
                        if st.button(f"Save", key=f"save_{i}"):
                            finder.save_job(job)
                            st.success("Job saved!")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        elif 'filtered_jobs' in st.session_state:
            st.info("No internships found matching your criteria. Try adjusting your filters.")
    
    with tab2:
        st.header("📊 Analytics")
        
        # Get analytics data
        applications = finder.get_applications()
        saved_jobs = finder.get_saved_jobs()
        
        if applications or saved_jobs:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Application Analytics")
                
                if applications:
                    # Application status
                    status_counts = pd.Series([app['status'] for app in applications]).value_counts()
                    fig_status = px.pie(values=status_counts.values, names=status_counts.index,
                                       title="Application Status")
                    st.plotly_chart(fig_status, use_container_width=True)
                    
                    # Applications over time
                    dates = [app['date'] for app in applications]
                    date_counts = pd.Series(dates).value_counts().sort_index()
                    fig_timeline = px.line(x=date_counts.index, y=date_counts.values,
                                         title="Applications Over Time")
                    st.plotly_chart(fig_timeline, use_container_width=True)
                else:
                    st.info("No applications yet.")
            
            with col2:
                st.subheader("Job Analytics")
                
                if saved_jobs:
                    # Company distribution
                    company_counts = pd.Series([job['company'] for job in saved_jobs]).value_counts().head(10)
                    fig_companies = px.bar(x=company_counts.values, y=company_counts.index,
                                         orientation='h', title="Top Companies")
                    st.plotly_chart(fig_companies, use_container_width=True)
                    
                    # Salary distribution
                    salaries = [job.get('salary', 0) for job in saved_jobs if job.get('salary', 0) > 0]
                    if salaries:
                        fig_salary = px.histogram(x=salaries, title="Salary Distribution",
                                                labels={'x': 'Salary ($/hour)', 'y': 'Count'})
                        st.plotly_chart(fig_salary, use_container_width=True)
                else:
                    st.info("No saved jobs yet.")
        else:
            st.info("Start applying to jobs to see analytics!")
    
    with tab3:
        st.header("📝 Application Tracker")
        
        applications = finder.get_applications()
        
        if applications:
            # Application table
            app_data = []
            for app in applications:
                app_data.append({
                    'Company': app['company'],
                    'Position': app['title'],
                    'Date': app['date'],
                    'Status': app['status'],
                    'Notes': app.get('notes', '')
                })
            
            df_apps = pd.DataFrame(app_data)
            st.dataframe(df_apps, use_container_width=True)
            
            # Download applications
            csv = df_apps.to_csv(index=False)
            st.download_button(
                label="Download Applications CSV",
                data=csv,
                file_name="applications.csv",
                mime="text/csv"
            )
        else:
            st.info("No applications tracked yet. Start applying to jobs!")
    
    with tab4:
        st.header("💡 Application Tips")
        
        tips = [
            "🎯 **Customize your resume** for each application",
            "📝 **Write a compelling cover letter** explaining your interest",
            "🔗 **Network** - reach out to employees at target companies",
            "📚 **Showcase projects** - include GitHub links and demos",
            "⏰ **Apply early** - many positions fill quickly",
            "📞 **Follow up** - send thank you emails after interviews",
            "📊 **Track everything** - use this app to stay organized",
            "🎓 **Highlight relevant coursework** and certifications"
        ]
        
        for tip in tips:
            st.write(tip)
        
        st.subheader("📈 Success Metrics")
        
        metrics = {
            'Metric': ['Applications Sent', 'Response Rate', 'Interview Rate', 'Offer Rate'],
            'Target': ['50+', '10-15%', '5-10%', '2-5%'],
            'Tips': [
                'Apply to 5-10 jobs per week',
                'Customize each application',
                'Practice technical interviews',
                'Negotiate salary and benefits'
            ]
        }
        
        df_metrics = pd.DataFrame(metrics)
        st.dataframe(df_metrics, use_container_width=True)

if __name__ == "__main__":
    main() 