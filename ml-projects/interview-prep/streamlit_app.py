#!/usr/bin/env python3
"""
Streamlit app for ML Interview Preparation
Deployment-ready version
"""

import streamlit as st
import json
import random
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="ML Interview Prep",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .question-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Sample ML interview questions database
ML_QUESTIONS = {
    "Machine Learning Fundamentals": [
        {
            "question": "What is the difference between supervised and unsupervised learning?",
            "answer": "Supervised learning uses labeled data to train models, while unsupervised learning finds patterns in unlabeled data.",
            "difficulty": "Easy",
            "category": "Fundamentals"
        },
        {
            "question": "Explain overfitting and how to prevent it.",
            "answer": "Overfitting occurs when a model learns noise in training data. Prevention: regularization, cross-validation, more data, simpler models.",
            "difficulty": "Medium",
            "category": "Fundamentals"
        },
        {
            "question": "What is cross-validation and why is it important?",
            "answer": "Cross-validation splits data into multiple folds to evaluate model performance more reliably and prevent overfitting.",
            "difficulty": "Medium",
            "category": "Fundamentals"
        }
    ],
    "Deep Learning": [
        {
            "question": "What is backpropagation?",
            "answer": "Backpropagation is an algorithm that calculates gradients of loss with respect to weights by applying the chain rule of calculus.",
            "difficulty": "Hard",
            "category": "Deep Learning"
        },
        {
            "question": "Explain the difference between CNN and RNN.",
            "answer": "CNNs are for spatial data (images), RNNs are for sequential data (text, time series). CNNs use convolutional layers, RNNs use recurrent connections.",
            "difficulty": "Medium",
            "category": "Deep Learning"
        }
    ],
    "Natural Language Processing": [
        {
            "question": "What is TF-IDF?",
            "answer": "Term Frequency-Inverse Document Frequency measures word importance by considering frequency in document vs. rarity across corpus.",
            "difficulty": "Medium",
            "category": "NLP"
        },
        {
            "question": "Explain word embeddings.",
            "answer": "Word embeddings represent words as dense vectors in continuous space, capturing semantic relationships (Word2Vec, GloVe, BERT).",
            "difficulty": "Medium",
            "category": "NLP"
        }
    ],
    "Computer Vision": [
        {
            "question": "What are the main components of a CNN?",
            "answer": "Convolutional layers, pooling layers, activation functions, and fully connected layers.",
            "difficulty": "Easy",
            "category": "Computer Vision"
        },
        {
            "question": "Explain data augmentation in computer vision.",
            "answer": "Data augmentation creates variations of training images (rotation, scaling, flipping) to improve model generalization.",
            "difficulty": "Easy",
            "category": "Computer Vision"
        }
    ]
}

def load_user_progress():
    """Load user progress from session state or create new"""
    if 'user_progress' not in st.session_state:
        st.session_state.user_progress = {
            'total_questions': 0,
            'correct_answers': 0,
            'practice_sessions': 0,
            'mock_interviews': 0,
            'last_session': None,
            'category_scores': {},
            'difficulty_scores': {}
        }
    return st.session_state.user_progress

def save_progress():
    """Save progress to session state"""
    st.session_state.user_progress = load_user_progress()

def get_random_question(category=None, difficulty=None):
    """Get a random question based on filters"""
    all_questions = []
    for cat, questions in ML_QUESTIONS.items():
        if category is None or cat == category:
            for q in questions:
                if difficulty is None or q['difficulty'] == difficulty:
                    all_questions.append(q)
    
    if all_questions:
        return random.choice(all_questions)
    return None

def evaluate_answer(user_answer, correct_answer):
    """Simple keyword-based evaluation"""
    if not user_answer.strip():
        return 0
    
    user_words = set(user_answer.lower().split())
    correct_words = set(correct_answer.lower().split())
    
    # Calculate similarity
    if len(correct_words) == 0:
        return 0
    
    common_words = user_words.intersection(correct_words)
    similarity = len(common_words) / len(correct_words)
    
    # Boost score for longer answers
    length_boost = min(len(user_answer.split()) / 10, 0.3)
    
    return min(similarity + length_boost, 1.0)

def main():
    # Header
    st.markdown('<h1 class="main-header">🧠 ML Interview Preparation</h1>', unsafe_allow_html=True)
    
    # Load user progress
    progress = load_user_progress()
    
    # Sidebar
    st.sidebar.title("📊 Progress Dashboard")
    
    # Progress metrics
    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        st.metric("Questions", progress['total_questions'])
    with col2:
        st.metric("Accuracy", f"{progress['correct_answers']/max(progress['total_questions'], 1)*100:.1f}%")
    with col3:
        st.metric("Sessions", progress['practice_sessions'])
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Practice Session", "📝 Mock Interview", "📈 Analytics", "📚 Study Resources"])
    
    with tab1:
        st.header("🎯 Practice Session")
        
        # Session options
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Select Category", ["All"] + list(ML_QUESTIONS.keys()))
        with col2:
            difficulty = st.selectbox("Select Difficulty", ["All", "Easy", "Medium", "Hard"])
        
        if st.button("🎲 Get Random Question", type="primary"):
            selected_category = None if category == "All" else category
            selected_difficulty = None if difficulty == "All" else difficulty
            
            question = get_random_question(selected_category, selected_difficulty)
            if question:
                st.session_state.current_question = question
                st.session_state.show_answer = False
                st.session_state.user_answer = ""
        
        # Display current question
        if 'current_question' in st.session_state:
            question = st.session_state.current_question
            
            st.markdown('<div class="question-card">', unsafe_allow_html=True)
            st.subheader(f"Question ({question['difficulty']} - {question['category']})")
            st.write(question['question'])
            
            # User answer input
            user_answer = st.text_area("Your Answer:", value=st.session_state.get('user_answer', ''), height=150)
            st.session_state.user_answer = user_answer
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Submit Answer"):
                    if user_answer.strip():
                        score = evaluate_answer(user_answer, question['answer'])
                        progress['total_questions'] += 1
                        if score > 0.5:
                            progress['correct_answers'] += 1
                        
                        # Update category and difficulty scores
                        cat = question['category']
                        diff = question['difficulty']
                        
                        if cat not in progress['category_scores']:
                            progress['category_scores'][cat] = {'total': 0, 'correct': 0}
                        if diff not in progress['difficulty_scores']:
                            progress['difficulty_scores'][diff] = {'total': 0, 'correct': 0}
                        
                        progress['category_scores'][cat]['total'] += 1
                        progress['difficulty_scores'][diff]['total'] += 1
                        
                        if score > 0.5:
                            progress['category_scores'][cat]['correct'] += 1
                            progress['difficulty_scores'][diff]['correct'] += 1
                        
                        progress['last_session'] = datetime.now().isoformat()
                        save_progress()
                        
                        st.success(f"Score: {score:.1%}")
                        st.session_state.show_answer = True
                    else:
                        st.error("Please provide an answer!")
            
            with col2:
                if st.button("👁️ Show Answer"):
                    st.session_state.show_answer = True
            
            if st.session_state.get('show_answer', False):
                st.markdown("**Correct Answer:**")
                st.info(question['answer'])
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.header("📝 Mock Interview")
        
        if st.button("🎬 Start Mock Interview", type="primary"):
            progress['mock_interviews'] += 1
            save_progress()
            
            # Generate mock interview questions
            interview_questions = []
            for category in ML_QUESTIONS.keys():
                cat_questions = ML_QUESTIONS[category]
                interview_questions.extend(random.sample(cat_questions, min(2, len(cat_questions))))
            
            st.session_state.interview_questions = random.sample(interview_questions, min(5, len(interview_questions)))
            st.session_state.current_interview_q = 0
            st.session_state.interview_answers = []
        
        if 'interview_questions' in st.session_state:
            questions = st.session_state.interview_questions
            current_q = st.session_state.current_interview_q
            
            if current_q < len(questions):
                question = questions[current_q]
                
                st.markdown(f"**Question {current_q + 1} of {len(questions)}**")
                st.markdown(f"*{question['category']} - {question['difficulty']}*")
                st.write(question['question'])
                
                answer = st.text_area("Your Answer:", key=f"interview_{current_q}", height=150)
                
                if st.button("Next Question"):
                    st.session_state.interview_answers.append(answer)
                    st.session_state.current_interview_q += 1
                    st.rerun()
            
            else:
                st.success("🎉 Mock Interview Complete!")
                
                # Calculate results
                total_score = 0
                for i, (question, answer) in enumerate(zip(questions, st.session_state.interview_answers)):
                    score = evaluate_answer(answer, question['answer'])
                    total_score += score
                
                avg_score = total_score / len(questions)
                st.metric("Interview Score", f"{avg_score:.1%}")
                
                if st.button("📊 View Detailed Results"):
                    for i, (question, answer) in enumerate(zip(questions, st.session_state.interview_answers)):
                        score = evaluate_answer(answer, question['answer'])
                        st.write(f"**Q{i+1}:** {question['question']}")
                        st.write(f"**Your Answer:** {answer}")
                        st.write(f"**Score:** {score:.1%}")
                        st.write("---")
    
    with tab3:
        st.header("📈 Analytics")
        
        if progress['total_questions'] > 0:
            # Category performance
            if progress['category_scores']:
                st.subheader("Performance by Category")
                cat_data = []
                for cat, scores in progress['category_scores'].items():
                    accuracy = scores['correct'] / scores['total'] * 100
                    cat_data.append({'Category': cat, 'Accuracy': accuracy, 'Questions': scores['total']})
                
                df_cat = pd.DataFrame(cat_data)
                fig_cat = px.bar(df_cat, x='Category', y='Accuracy', 
                               title='Accuracy by Category',
                               color='Questions', color_continuous_scale='viridis')
                st.plotly_chart(fig_cat, use_container_width=True)
            
            # Difficulty performance
            if progress['difficulty_scores']:
                st.subheader("Performance by Difficulty")
                diff_data = []
                for diff, scores in progress['difficulty_scores'].items():
                    accuracy = scores['correct'] / scores['total'] * 100
                    diff_data.append({'Difficulty': diff, 'Accuracy': accuracy, 'Questions': scores['total']})
                
                df_diff = pd.DataFrame(diff_data)
                fig_diff = px.bar(df_diff, x='Difficulty', y='Accuracy',
                                title='Accuracy by Difficulty',
                                color='Questions', color_continuous_scale='plasma')
                st.plotly_chart(fig_diff, use_container_width=True)
            
            # Progress over time
            st.subheader("Overall Progress")
            col1, col2 = st.columns(2)
            with col1:
                fig_progress = go.Figure()
                fig_progress.add_trace(go.Indicator(
                    mode="gauge+number+delta",
                    value=progress['correct_answers']/progress['total_questions']*100,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Overall Accuracy"},
                    delta={'reference': 50},
                    gauge={'axis': {'range': [None, 100]},
                           'bar': {'color': "darkblue"},
                           'steps': [{'range': [0, 50], 'color': "lightgray"},
                                    {'range': [50, 80], 'color': "yellow"},
                                    {'range': [80, 100], 'color': "green"}]}))
                st.plotly_chart(fig_progress, use_container_width=True)
            
            with col2:
                st.metric("Total Questions", progress['total_questions'])
                st.metric("Correct Answers", progress['correct_answers'])
                st.metric("Practice Sessions", progress['practice_sessions'])
                st.metric("Mock Interviews", progress['mock_interviews'])
        else:
            st.info("Complete some practice sessions to see your analytics!")
    
    with tab4:
        st.header("📚 Study Resources")
        
        st.subheader("📖 Recommended Topics")
        
        # Get weak areas
        weak_areas = []
        if progress['category_scores']:
            for cat, scores in progress['category_scores'].items():
                accuracy = scores['correct'] / scores['total']
                if accuracy < 0.7:
                    weak_areas.append(cat)
        
        if weak_areas:
            st.warning(f"Focus on these areas: {', '.join(weak_areas)}")
        else:
            st.success("Great job! Keep practicing to maintain your skills.")
        
        st.subheader("🔗 Learning Resources")
        
        resources = {
            "Machine Learning Fundamentals": [
                "📚 'Hands-On Machine Learning' by Aurélien Géron",
                "🎥 Andrew Ng's Machine Learning Course (Coursera)",
                "📖 'Pattern Recognition and Machine Learning' by Bishop"
            ],
            "Deep Learning": [
                "📚 'Deep Learning' by Ian Goodfellow",
                "🎥 CS231n: Convolutional Neural Networks (Stanford)",
                "📖 'Neural Networks and Deep Learning' by Michael Nielsen"
            ],
            "Natural Language Processing": [
                "📚 'Speech and Language Processing' by Jurafsky & Martin",
                "🎥 CS224n: Natural Language Processing (Stanford)",
                "📖 'Natural Language Processing with Python' by Bird et al."
            ],
            "Computer Vision": [
                "📚 'Computer Vision: Algorithms and Applications' by Szeliski",
                "🎥 CS231n: Computer Vision (Stanford)",
                "📖 'Learning OpenCV' by Bradski & Kaehler"
            ]
        }
        
        for category, resource_list in resources.items():
            with st.expander(f"📚 {category}"):
                for resource in resource_list:
                    st.write(resource)
        
        st.subheader("💡 Interview Tips")
        tips = [
            "🎯 Practice explaining concepts in simple terms",
            "📝 Write code on a whiteboard or paper",
            "🤔 Think out loud during problem-solving",
            "❓ Ask clarifying questions before starting",
            "📊 Know your algorithms' time/space complexity",
            "🧪 Be ready to discuss trade-offs and alternatives"
        ]
        
        for tip in tips:
            st.write(tip)

if __name__ == "__main__":
    main() 