#!/usr/bin/env python3
"""
Streamlit web application for ML Interview Preparation
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from interview_prep import InterviewPrep
import json
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="ML Interview Prep",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize interview prep
@st.cache_resource
def get_interview_prep():
    return InterviewPrep()

prep = get_interview_prep()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
    .question-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .feedback-good {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #28a745;
    }
    .feedback-improve {
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🧪 ML Interview Prep")
st.sidebar.markdown("---")

# User ID (in real app, would use authentication)
user_id = st.sidebar.text_input("Enter your user ID:", value="user_001")

# Navigation
page = st.sidebar.selectbox(
    "Choose a section:",
    ["🏠 Dashboard", "📚 Practice Sessions", "🎯 Mock Interviews", "📊 Progress Analytics", "📖 Study Resources"]
)

# Main content
if page == "🏠 Dashboard":
    st.markdown('<div class="main-header"><h1>🧪 ML Interview Preparation Dashboard</h1><p>Master your ML interview skills with personalized practice</p></div>', unsafe_allow_html=True)
    
    # Get user progress
    progress = prep.get_user_progress(user_id)
    stats = progress.get('stats', {})
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{stats.get('total_sessions', 0)}</h3>
            <p>Practice Sessions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{stats.get('total_questions', 0)}</h3>
            <p>Questions Answered</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        accuracy = stats.get('overall_accuracy', 0)
        st.markdown(f"""
        <div class="metric-card">
            <h3>{accuracy:.1f}%</h3>
            <p>Overall Accuracy</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_score = stats.get('average_score', 0)
        st.markdown(f"""
        <div class="metric-card">
            <h3>{avg_score:.1f}%</h3>
            <p>Average Score</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick actions
    st.subheader("🚀 Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📚 Start Practice Session", use_container_width=True):
            st.session_state.page = "practice"
            st.rerun()
    
    with col2:
        if st.button("🎯 Take Mock Interview", use_container_width=True):
            st.session_state.page = "mock"
            st.rerun()
    
    with col3:
        if st.button("📊 View Analytics", use_container_width=True):
            st.session_state.page = "analytics"
            st.rerun()
    
    # Recent activity
    if progress.get('sessions'):
        st.subheader("📈 Recent Activity")
        recent_sessions = progress['sessions'][-5:]  # Last 5 sessions
        
        for session in reversed(recent_sessions):
            with st.expander(f"Session {session['session_id']} - {session['date'][:10]}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Questions", session['total_questions'])
                with col2:
                    st.metric("Correct", session['correct_answers'])
                with col3:
                    st.metric("Score", f"{session['average_score']:.1f}%")
    
    # Study recommendations
    recommendations = prep.get_study_recommendations(user_id)
    if recommendations:
        st.subheader("💡 Study Recommendations")
        for rec in recommendations:
            st.info(rec)

elif page == "📚 Practice Sessions":
    st.title("📚 Practice Sessions")
    
    # Session configuration
    st.subheader("Configure Your Practice Session")
    
    col1, col2 = st.columns(2)
    
    with col1:
        categories = st.multiselect(
            "Select categories:",
            options=list(prep.categories['technical'].keys()) + list(prep.categories['behavioral'].keys()),
            default=['machine_learning', 'python']
        )
        
        difficulty = st.selectbox(
            "Difficulty level:",
            options=['easy', 'medium', 'hard', 'mixed']
        )
    
    with col2:
        question_count = st.slider("Number of questions:", 5, 20, 10)
        
        if st.button("🎯 Start Practice Session", use_container_width=True):
            if categories:
                session = prep.get_practice_session(categories, difficulty, question_count)
                st.session_state.current_session = session
                st.session_state.current_question = 0
                st.session_state.answers = []
                st.rerun()
            else:
                st.error("Please select at least one category.")
    
    # Practice session
    if 'current_session' in st.session_state and st.session_state.current_session:
        session = st.session_state.current_session
        
        st.subheader(f"Practice Session - {session['id']}")
        st.progress((st.session_state.current_question) / len(session['questions']))
        
        if st.session_state.current_question < len(session['questions']):
            question = session['questions'][st.session_state.current_question]
            
            st.markdown(f"""
            <div class="question-card">
                <h4>Question {st.session_state.current_question + 1} of {len(session['questions'])}</h4>
                <p><strong>Category:</strong> {', '.join(session['categories'])}</p>
                <p><strong>Difficulty:</strong> {question['difficulty']}</p>
                <hr>
                <h5>{question['question']}</h5>
            </div>
            """, unsafe_allow_html=True)
            
            # Answer input
            user_answer = st.text_area(
                "Your answer:",
                height=200,
                placeholder="Type your answer here..."
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("⏭️ Skip Question"):
                    st.session_state.answers.append({
                        'question': question,
                        'answer': '',
                        'score': 0,
                        'skipped': True
                    })
                    st.session_state.current_question += 1
                    st.rerun()
            
            with col2:
                if st.button("✅ Submit Answer") and user_answer.strip():
                    # Evaluate answer
                    evaluation = prep.evaluate_answer(question, user_answer)
                    
                    st.session_state.answers.append({
                        'question': question,
                        'answer': user_answer,
                        'score': evaluation['score'],
                        'feedback': evaluation['feedback'],
                        'suggestions': evaluation['suggested_improvements']
                    })
                    
                    st.session_state.current_question += 1
                    st.rerun()
        
        else:
            # Session completed
            st.success("🎉 Practice session completed!")
            
            # Calculate results
            total_score = sum(answer['score'] for answer in st.session_state.answers if not answer.get('skipped'))
            avg_score = total_score / len([a for a in st.session_state.answers if not a.get('skipped')]) if st.session_state.answers else 0
            
            st.metric("Average Score", f"{avg_score:.1f}%")
            
            # Show results
            st.subheader("📊 Session Results")
            
            for i, answer in enumerate(st.session_state.answers):
                with st.expander(f"Question {i+1}: {answer['question']['question'][:50]}..."):
                    st.write(f"**Your answer:** {answer['answer']}")
                    st.write(f"**Score:** {answer['score']:.1f}%")
                    
                    if answer['score'] >= 70:
                        st.markdown(f'<div class="feedback-good">{answer["feedback"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="feedback-improve">{answer["feedback"]}</div>', unsafe_allow_html=True)
                    
                    if answer['suggestions']:
                        st.write("**Suggestions for improvement:**")
                        for suggestion in answer['suggestions']:
                            st.write(f"• {suggestion}")
            
            # Save progress
            if st.button("💾 Save Progress"):
                prep.track_progress(user_id, session['id'], st.session_state.answers)
                st.success("Progress saved successfully!")
                
                # Clear session
                del st.session_state.current_session
                del st.session_state.current_question
                del st.session_state.answers
                st.rerun()

elif page == "🎯 Mock Interviews":
    st.title("🎯 Mock Interviews")
    
    st.subheader("Simulate Real Interview Conditions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        duration = st.selectbox(
            "Interview duration:",
            options=[30, 45, 60, 90],
            format_func=lambda x: f"{x} minutes"
        )
    
    with col2:
        if st.button("🎯 Start Mock Interview", use_container_width=True):
            mock_interview = prep.generate_mock_interview(user_id, duration)
            st.session_state.mock_interview = mock_interview
            st.session_state.mock_question = 0
            st.rerun()
    
    if 'mock_interview' in st.session_state:
        interview = st.session_state.mock_interview
        
        st.subheader(f"Mock Interview - {interview['id']}")
        st.write(f"**Duration:** {interview['duration']} minutes")
        st.write(f"**Focus Areas:** {', '.join(interview['focus_areas'])}")
        
        st.info("**Instructions:**")
        for instruction in interview['instructions']:
            st.write(f"• {instruction}")
        
        st.progress((st.session_state.mock_question) / len(interview['questions']))
        
        if st.session_state.mock_question < len(interview['questions']):
            question = interview['questions'][st.session_state.mock_question]
            
            st.markdown(f"""
            <div class="question-card">
                <h4>Question {st.session_state.mock_question + 1} of {len(interview['questions'])}</h4>
                <h5>{question['question']}</h5>
            </div>
            """, unsafe_allow_html=True)
            
            # Timer (simplified)
            if 'start_time' not in st.session_state:
                st.session_state.start_time = time.time()
            
            elapsed = time.time() - st.session_state.start_time
            remaining = (interview['duration'] * 60) - elapsed
            
            if remaining > 0:
                st.metric("Time Remaining", f"{int(remaining // 60)}:{int(remaining % 60):02d}")
            else:
                st.warning("Time's up!")
            
            # Answer input
            user_answer = st.text_area(
                "Your answer:",
                height=200,
                placeholder="Type your answer here..."
            )
            
            if st.button("⏭️ Next Question") and user_answer.strip():
                st.session_state.mock_question += 1
                st.session_state.start_time = time.time()  # Reset timer
                st.rerun()
        
        else:
            st.success("🎉 Mock interview completed!")
            st.balloons()

elif page == "📊 Progress Analytics":
    st.title("📊 Progress Analytics")
    
    progress = prep.get_user_progress(user_id)
    stats = progress.get('stats', {})
    
    if not stats:
        st.info("Complete some practice sessions to see your analytics!")
    else:
        # Performance over time
        st.subheader("📈 Performance Trends")
        
        if progress.get('sessions'):
            sessions_data = []
            for session in progress['sessions']:
                sessions_data.append({
                    'Date': session['date'][:10],
                    'Score': session['average_score'],
                    'Questions': session['total_questions']
                })
            
            df = pd.DataFrame(sessions_data)
            
            fig = px.line(df, x='Date', y='Score', title='Score Progression Over Time')
            st.plotly_chart(fig, use_container_width=True)
        
        # Category performance
        st.subheader("🎯 Category Performance")
        
        category_performance = stats.get('category_performance', {})
        if category_performance:
            categories = list(category_performance.keys())
            scores = list(category_performance.values())
            
            fig = px.bar(
                x=categories,
                y=scores,
                title='Performance by Category',
                labels={'x': 'Category', 'y': 'Average Score (%)'}
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed statistics
        st.subheader("📋 Detailed Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Overall Performance**")
            st.metric("Total Sessions", stats.get('total_sessions', 0))
            st.metric("Total Questions", stats.get('total_questions', 0))
            st.metric("Correct Answers", stats.get('total_correct', 0))
        
        with col2:
            st.write("**Accuracy Metrics**")
            st.metric("Overall Accuracy", f"{stats.get('overall_accuracy', 0):.1f}%")
            st.metric("Average Score", f"{stats.get('average_score', 0):.1f}%")
            st.metric("Last Session", stats.get('last_session', 'Never')[:10])

elif page == "📖 Study Resources":
    st.title("📖 Study Resources")
    
    st.subheader("🎯 Personalized Study Plan")
    
    recommendations = prep.get_study_recommendations(user_id)
    
    if recommendations:
        st.write("**Based on your performance, here are your study priorities:**")
        for i, rec in enumerate(recommendations, 1):
            st.write(f"{i}. {rec}")
    else:
        st.info("Complete some practice sessions to get personalized recommendations!")
    
    st.subheader("📚 Learning Resources")
    
    # ML Fundamentals
    with st.expander("🤖 Machine Learning Fundamentals"):
        st.write("**Key Topics:**")
        st.write("• Supervised vs Unsupervised Learning")
        st.write("• Overfitting and Regularization")
        st.write("• Cross-validation")
        st.write("• Model Evaluation Metrics")
        st.write("**Resources:**")
        st.write("• [Coursera ML Course](https://www.coursera.org/learn/machine-learning)")
        st.write("• [Scikit-learn Documentation](https://scikit-learn.org/)")
    
    # Deep Learning
    with st.expander("🧠 Deep Learning"):
        st.write("**Key Topics:**")
        st.write("• Neural Network Architectures")
        st.write("• Backpropagation")
        st.write("• CNNs, RNNs, Transformers")
        st.write("• Optimization Techniques")
        st.write("**Resources:**")
        st.write("• [Deep Learning Book](https://www.deeplearningbook.org/)")
        st.write("• [TensorFlow Tutorials](https://www.tensorflow.org/tutorials)")
    
    # Python Programming
    with st.expander("🐍 Python Programming"):
        st.write("**Key Topics:**")
        st.write("• Data Structures")
        st.write("• Algorithms")
        st.write("• Performance Optimization")
        st.write("• Libraries: NumPy, Pandas, Matplotlib")
        st.write("**Resources:**")
        st.write("• [Python Documentation](https://docs.python.org/)")
        st.write("• [LeetCode Python Problems](https://leetcode.com/)")
    
    # Statistics
    with st.expander("📊 Statistics & Probability"):
        st.write("**Key Topics:**")
        st.write("• Probability Distributions")
        st.write("• Hypothesis Testing")
        st.write("• Correlation vs Causation")
        st.write("• Statistical Significance")
        st.write("**Resources:**")
        st.write("• [Khan Academy Statistics](https://www.khanacademy.org/math/statistics-probability)")
        st.write("• [Statistics for Data Science](https://www.statlearning.com/)")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>🧪 ML Interview Prep Tool | Built for ML Students</p>
    </div>
    """,
    unsafe_allow_html=True
) 