#!/usr/bin/env python3
"""
Streamlit app for Plant Disease Classification
Deployment-ready version
"""

import streamlit as st
import numpy as np
import cv2
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from plant_classifier import PlantDiseaseClassifier
import os
import pandas as pd

# Set page config
st.set_page_config(
    page_title="Plant Disease Classifier",
    page_icon="🌱",
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
    .result-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .confidence-bar {
        background-color: #f0f2f6;
        border-radius: 0.5rem;
        padding: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_classifier():
    """Load the plant disease classifier"""
    classifier = PlantDiseaseClassifier()
    
    # Check if model exists, if not train it
    if not os.path.exists('plant_disease_model.h5'):
        with st.spinner("Training model for the first time..."):
            history = classifier.train_model(epochs=5)
            classifier.save_model()
    else:
        classifier.load_model()
    
    return classifier

def create_sample_images():
    """Create sample images for demonstration"""
    sample_images = {}
    
    # Create Healthy sample
    healthy_img = np.zeros((224, 224, 3), dtype=np.uint8)
    cv2.ellipse(healthy_img, (112, 112), (80, 50), 0, 0, 360, (0, 128, 0), -1)
    for _ in range(50):
        x = np.random.randint(50, 174)
        y = np.random.randint(50, 174)
        cv2.circle(healthy_img, (x, y), 1, (50, 205, 50), -1)
    sample_images['Healthy'] = Image.fromarray(healthy_img)
    
    # Create Bacterial Blight sample
    blight_img = np.zeros((224, 224, 3), dtype=np.uint8)
    cv2.ellipse(blight_img, (112, 112), (80, 50), 0, 0, 360, (139, 69, 19), -1)
    for _ in range(15):
        x = np.random.randint(50, 174)
        y = np.random.randint(50, 174)
        radius = np.random.randint(5, 12)
        cv2.circle(blight_img, (x, y), radius, (160, 82, 45), -1)
    sample_images['Bacterial Blight'] = Image.fromarray(blight_img)
    
    # Create Brown Spot sample
    spot_img = np.zeros((224, 224, 3), dtype=np.uint8)
    cv2.ellipse(spot_img, (112, 112), (80, 50), 0, 0, 360, (128, 128, 128), -1)
    for _ in range(40):
        x = np.random.randint(50, 174)
        y = np.random.randint(50, 174)
        radius = np.random.randint(1, 3)
        cv2.circle(spot_img, (x, y), radius, (105, 105, 105), -1)
    sample_images['Brown Spot'] = Image.fromarray(spot_img)
    
    # Create Leaf Blast sample
    blast_img = np.zeros((224, 224, 3), dtype=np.uint8)
    cv2.ellipse(blast_img, (112, 112), (80, 50), 0, 0, 360, (255, 0, 0), -1)
    for _ in range(15):
        x = np.random.randint(50, 174)
        y = np.random.randint(50, 174)
        size = np.random.randint(8, 18)
        pts = np.array([[x-size, y], [x, y-size], [x+size, y], [x, y+size]], np.int32)
        cv2.fillPoly(blast_img, [pts], (220, 20, 60))
    sample_images['Leaf Blast'] = Image.fromarray(blast_img)
    
    return sample_images

def main():
    # Header
    st.markdown('<h1 class="main-header">🌱 Plant Disease Classifier</h1>', unsafe_allow_html=True)
    
    # Load classifier
    classifier = load_classifier()
    
    # Sidebar
    st.sidebar.title("📊 Model Information")
    
    # Model stats
    st.sidebar.metric("Model Type", "CNN")
    st.sidebar.metric("Classes", "4")
    st.sidebar.metric("Input Size", "224x224")
    
    # Disease information
    st.sidebar.subheader("🌿 Disease Types")
    diseases = {
        "Healthy": "No disease detected",
        "Bacterial Blight": "Caused by Xanthomonas oryzae",
        "Brown Spot": "Caused by Cochliobolus miyabeanus", 
        "Leaf Blast": "Caused by Magnaporthe oryzae"
    }
    
    for disease, description in diseases.items():
        with st.sidebar.expander(disease):
            st.write(description)
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["🔍 Upload Image", "🎲 Try Samples", "📈 Analytics"])
    
    with tab1:
        st.header("🔍 Upload Plant Image")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg']
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Uploaded Image")
                st.image(image, caption="Uploaded Image", use_column_width=True)
            
            with col2:
                # Make prediction
                with st.spinner("Analyzing image..."):
                    result = classifier.predict_image(image)
                
                st.subheader("Classification Results")
                
                # Display prediction
                predicted_class = result['class']
                confidence = result['confidence']
                
                if predicted_class == 'Healthy':
                    st.success(f"🌿 {predicted_class}")
                else:
                    st.error(f"⚠️ {predicted_class}")
                
                st.metric("Confidence", f"{confidence:.1%}")
                
                # Show probabilities
                st.subheader("Class Probabilities")
                
                prob_data = {
                    'Disease': result['class_names'],
                    'Probability': result['probabilities']
                }
                
                df_probs = pd.DataFrame(prob_data)
                
                fig = px.bar(df_probs, x='Disease', y='Probability',
                           color='Probability', color_continuous_scale='RdYlGn',
                           title='Disease Classification Probabilities')
                st.plotly_chart(fig, use_container_width=True)
                
                # Treatment recommendations
                st.subheader("💡 Treatment Recommendations")
                
                treatments = {
                    "Healthy": "Continue regular care and monitoring",
                    "Bacterial Blight": "Remove infected plants, use copper-based fungicides",
                    "Brown Spot": "Improve air circulation, apply fungicides",
                    "Leaf Blast": "Use resistant varieties, apply systemic fungicides"
                }
                
                treatment = treatments.get(predicted_class, "Consult with a plant expert")
                st.info(treatment)
    
    with tab2:
        st.header("🎲 Try Sample Images")
        
        st.write("Click on a sample image to see how the classifier works:")
        
        # Create sample images
        sample_images = create_sample_images()
        
        # Display sample images in a grid
        cols = st.columns(2)
        
        for i, (disease, image) in enumerate(sample_images.items()):
            with cols[i % 2]:
                st.subheader(disease)
                st.image(image, caption=disease, use_column_width=True)
                
                if st.button(f"Analyze {disease}", key=f"sample_{i}"):
                    with st.spinner("Analyzing..."):
                        result = classifier.predict_image(image)
                    
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    
                    predicted = result['class']
                    confidence = result['confidence']
                    
                    if predicted == disease:
                        st.success(f"✅ Correctly identified as {predicted}")
                    else:
                        st.error(f"❌ Predicted as {predicted} (Expected: {disease})")
                    
                    st.metric("Confidence", f"{confidence:.1%}")
                    
                    # Show all probabilities
                    for class_name, prob in zip(result['class_names'], result['probabilities']):
                        color = "green" if class_name == predicted else "gray"
                        st.markdown(f'<div class="confidence-bar" style="background-color: {color}; color: white;">{class_name}: {prob:.1%}</div>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.header("📈 Analytics & Insights")
        
        # Model performance
        st.subheader("Model Performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Accuracy gauge
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=25,  # Current accuracy
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Current Accuracy"},
                delta={'reference': 80},
                gauge={'axis': {'range': [None, 100]},
                       'bar': {'color': "darkblue"},
                       'steps': [{'range': [0, 50], 'color': "lightgray"},
                                {'range': [50, 80], 'color': "yellow"},
                                {'range': [80, 100], 'color': "green"}]}))
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with col2:
            st.metric("Training Images", "800")
            st.metric("Validation Images", "200")
            st.metric("Model Architecture", "CNN")
        
        # Disease distribution
        st.subheader("Disease Distribution in Training Data")
        
        disease_counts = {
            'Healthy': 200,
            'Bacterial Blight': 200,
            'Brown Spot': 200,
            'Leaf Blast': 200
        }
        
        fig_dist = px.pie(values=list(disease_counts.values()), 
                         names=list(disease_counts.keys()),
                         title="Training Data Distribution")
        st.plotly_chart(fig_dist, use_container_width=True)
        
        # Usage tips
        st.subheader("💡 Usage Tips")
        
        tips = [
            "📸 **Clear images** work best - ensure good lighting",
            "🌿 **Focus on leaves** - most diseases appear on leaf surfaces",
            "📏 **Multiple angles** - try different views of the same plant",
            "🔍 **Close-up shots** - capture disease symptoms clearly",
            "⏰ **Early detection** - check plants regularly for best results"
        ]
        
        for tip in tips:
            st.write(tip)
        
        # Technical details
        st.subheader("🔧 Technical Details")
        
        tech_info = {
            'Feature': ['Model Type', 'Input Size', 'Classes', 'Training Data', 'Framework'],
            'Value': ['Convolutional Neural Network', '224x224x3', '4', '800 images', 'TensorFlow/Keras']
        }
        
        df_tech = pd.DataFrame(tech_info)
        st.dataframe(df_tech, use_container_width=True)

if __name__ == "__main__":
    main() 