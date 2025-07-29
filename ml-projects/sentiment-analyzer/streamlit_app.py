#!/usr/bin/env python3
"""
Streamlit app for Sentiment Analysis
Deployment-ready version
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sentiment_model import SentimentAnalyzer
import json

# Set page config
st.set_page_config(
    page_title="Sentiment Analyzer",
    page_icon="😊",
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
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .result-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_analyzer():
    """Load the sentiment analyzer model"""
    analyzer = SentimentAnalyzer()
    try:
        analyzer.load_model()
    except:
        st.info("Training model for the first time...")
        analyzer.train_model()
        analyzer.save_model()
    return analyzer

def main():
    # Header
    st.markdown('<h1 class="main-header">😊 Sentiment Analysis</h1>', unsafe_allow_html=True)
    
    # Load model
    analyzer = load_analyzer()
    
    # Sidebar
    st.sidebar.title("📊 Model Statistics")
    
    # Get model stats
    stats = analyzer.get_model_stats()
    
    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        st.metric("Accuracy", f"{stats['accuracy']:.1f}%")
    with col2:
        st.metric("Training Samples", stats['training_samples'])
    with col3:
        st.metric("Vocabulary Size", stats['vocabulary_size'])
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["🔍 Single Analysis", "📋 Batch Analysis", "📈 Analytics"])
    
    with tab1:
        st.header("🔍 Single Text Analysis")
        
        # Text input
        text_input = st.text_area(
            "Enter text to analyze:",
            placeholder="Type your text here...",
            height=150
        )
        
        if st.button("Analyze Sentiment", type="primary"):
            if text_input.strip():
                with st.spinner("Analyzing..."):
                    result = analyzer.predict_sentiment(text_input)
                
                # Display results
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    sentiment = result['sentiment']
                    if sentiment == 'positive':
                        st.success("😊 Positive")
                    elif sentiment == 'negative':
                        st.error("😞 Negative")
                    else:
                        st.info("😐 Neutral")
                
                with col2:
                    confidence = result['confidence']
                    st.metric("Confidence", f"{confidence:.1%}")
                
                with col3:
                    st.metric("Text Length", len(text_input))
                
                # Show probabilities
                st.subheader("Sentiment Probabilities")
                prob_data = {
                    'Sentiment': ['Positive', 'Negative', 'Neutral'],
                    'Probability': [
                        result['probabilities'][0],
                        result['probabilities'][1], 
                        result['probabilities'][2]
                    ]
                }
                df_probs = pd.DataFrame(prob_data)
                
                fig = px.bar(df_probs, x='Sentiment', y='Probability',
                           color='Probability', color_continuous_scale='RdYlGn',
                           title='Sentiment Distribution')
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("Please enter some text to analyze!")
    
    with tab2:
        st.header("📋 Batch Analysis")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload CSV file with 'text' column",
            type=['csv']
        )
        
        # Manual batch input
        st.subheader("Or enter multiple texts manually:")
        batch_texts = st.text_area(
            "Enter texts (one per line):",
            placeholder="Text 1\nText 2\nText 3\n...",
            height=200
        )
        
        if st.button("Analyze Batch", type="primary"):
            texts_to_analyze = []
            
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
                if 'text' in df.columns:
                    texts_to_analyze = df['text'].tolist()
                else:
                    st.error("CSV file must have a 'text' column!")
                    return
            elif batch_texts.strip():
                texts_to_analyze = [text.strip() for text in batch_texts.split('\n') if text.strip()]
            else:
                st.error("Please provide texts to analyze!")
                return
            
            if texts_to_analyze:
                with st.spinner(f"Analyzing {len(texts_to_analyze)} texts..."):
                    results = analyzer.analyze_batch(texts_to_analyze)
                
                # Create results dataframe
                results_data = []
                for i, (text, result) in enumerate(zip(texts_to_analyze, results)):
                    results_data.append({
                        'Text': text[:100] + '...' if len(text) > 100 else text,
                        'Sentiment': result['sentiment'],
                        'Confidence': f"{result['confidence']:.1%}",
                        'Positive': f"{result['probabilities'][0]:.1%}",
                        'Negative': f"{result['probabilities'][1]:.1%}",
                        'Neutral': f"{result['probabilities'][2]:.1%}"
                    })
                
                df_results = pd.DataFrame(results_data)
                st.dataframe(df_results, use_container_width=True)
                
                # Download results
                csv = df_results.to_csv(index=False)
                st.download_button(
                    label="Download Results CSV",
                    data=csv,
                    file_name="sentiment_analysis_results.csv",
                    mime="text/csv"
                )
                
                # Summary statistics
                st.subheader("📊 Batch Analysis Summary")
                
                sentiment_counts = df_results['Sentiment'].value_counts()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_pie = px.pie(
                        values=sentiment_counts.values,
                        names=sentiment_counts.index,
                        title="Sentiment Distribution"
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                with col2:
                    avg_confidence = df_results['Confidence'].str.rstrip('%').astype(float).mean()
                    st.metric("Average Confidence", f"{avg_confidence:.1f}%")
                    st.metric("Total Texts", len(texts_to_analyze))
                    st.metric("Most Common", sentiment_counts.index[0])
    
    with tab3:
        st.header("📈 Analytics & Insights")
        
        # Model performance
        st.subheader("Model Performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Accuracy gauge
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=stats['accuracy'],
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Model Accuracy"},
                delta={'reference': 80},
                gauge={'axis': {'range': [None, 100]},
                       'bar': {'color': "darkblue"},
                       'steps': [{'range': [0, 60], 'color': "lightgray"},
                                {'range': [60, 80], 'color': "yellow"},
                                {'range': [80, 100], 'color': "green"}]}))
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with col2:
            st.metric("Training Samples", stats['training_samples'])
            st.metric("Vocabulary Size", stats['vocabulary_size'])
            st.metric("Model Type", "Logistic Regression")
        
        # Feature importance (if available)
        st.subheader("Model Information")
        
        info_data = {
            'Metric': ['Model Type', 'Vectorizer', 'Training Samples', 'Vocabulary Size', 'Accuracy'],
            'Value': [
                'Logistic Regression',
                'TF-IDF',
                str(stats['training_samples']),
                str(stats['vocabulary_size']),
                f"{stats['accuracy']:.1f}%"
            ]
        }
        
        df_info = pd.DataFrame(info_data)
        st.dataframe(df_info, use_container_width=True)
        
        # Usage tips
        st.subheader("💡 Usage Tips")
        
        tips = [
            "📝 **Longer texts** generally provide more accurate results",
            "🎯 **Clear language** works better than slang or abbreviations", 
            "📊 **Batch analysis** is great for processing multiple texts efficiently",
            "🔍 **Review results** - confidence scores help assess reliability",
            "📈 **Monitor trends** - use batch analysis to track sentiment over time"
        ]
        
        for tip in tips:
            st.write(tip)

if __name__ == "__main__":
    main() 