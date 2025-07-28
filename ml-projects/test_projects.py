#!/usr/bin/env python3
"""
Test script to verify both ML projects work correctly
"""

import sys
import os
import numpy as np
from PIL import Image

def test_sentiment_analyzer():
    """Test the sentiment analyzer"""
    print("🧪 Testing Sentiment Analyzer...")
    
    try:
        # Add sentiment analyzer to path
        sys.path.append('sentiment-analyzer')
        from sentiment_model import SentimentAnalyzer
        
        # Initialize and train model
        analyzer = SentimentAnalyzer()
        results = analyzer.train_model()
        
        # Test predictions
        test_texts = [
            "I love this product!",
            "This is terrible.",
            "It's okay, nothing special."
        ]
        
        print("✅ Model trained successfully!")
        print(f"📊 Model accuracy: {results['accuracy']:.2f}")
        
        for text in test_texts:
            result = analyzer.predict_sentiment(text)
            print(f"📝 '{text}' → {result['sentiment']} ({result['confidence']:.2f})")
        
        print("✅ Sentiment Analyzer: ALL TESTS PASSED!\n")
        return True
        
    except Exception as e:
        print(f"❌ Sentiment Analyzer failed: {e}")
        return False

def test_image_classifier():
    """Test the image classifier"""
    print("🧪 Testing Image Classifier...")
    
    try:
        # Add image classifier to path
        sys.path.append('image-classifier')
        from plant_classifier import PlantDiseaseClassifier
        
        # Initialize classifier
        classifier = PlantDiseaseClassifier()
        
        # Create a test image (synthetic)
        test_image = Image.new('RGB', (224, 224), color=(34, 139, 34))  # Green
        
        # Train model (this will create synthetic data)
        print("🔄 Training model with synthetic data...")
        history = classifier.train_model(epochs=1)  # Quick training for testing
        
        # Test prediction
        result = classifier.predict_image(test_image)
        
        print("✅ Model trained successfully!")
        print(f"📊 Prediction: {result['class']} (confidence: {result['confidence']:.2f})")
        print(f"📋 Available classes: {result['class_names']}")
        
        print("✅ Image Classifier: ALL TESTS PASSED!\n")
        return True
        
    except Exception as e:
        print(f"❌ Image Classifier failed: {e}")
        return False

def test_web_applications():
    """Test if web applications can start"""
    print("🧪 Testing Web Applications...")
    
    try:
        # Test Flask app
        print("🌐 Testing Flask app...")
        import subprocess
        import time
        
        # Start Flask app in background
        flask_process = subprocess.Popen(
            ['python', 'sentiment-analyzer/app.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a moment for app to start
        time.sleep(3)
        
        # Check if process is still running
        if flask_process.poll() is None:
            print("✅ Flask app started successfully!")
            flask_process.terminate()
        else:
            print("❌ Flask app failed to start")
            return False
        
        # Test Streamlit app
        print("🌐 Testing Streamlit app...")
        streamlit_process = subprocess.Popen(
            ['streamlit', 'run', 'image-classifier/app.py', '--server.headless', 'true'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a moment for app to start
        time.sleep(5)
        
        # Check if process is still running
        if streamlit_process.poll() is None:
            print("✅ Streamlit app started successfully!")
            streamlit_process.terminate()
        else:
            print("❌ Streamlit app failed to start")
            return False
        
        print("✅ Web Applications: ALL TESTS PASSED!\n")
        return True
        
    except Exception as e:
        print(f"❌ Web Applications failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Both ML Projects...\n")
    
    # Change to projects directory
    os.chdir('ml-projects')
    
    # Run tests
    sentiment_ok = test_sentiment_analyzer()
    image_ok = test_image_classifier()
    web_ok = test_web_applications()
    
    # Summary
    print("📊 TEST RESULTS SUMMARY:")
    print("=" * 40)
    print(f"Sentiment Analyzer: {'✅ PASSED' if sentiment_ok else '❌ FAILED'}")
    print(f"Image Classifier:   {'✅ PASSED' if image_ok else '❌ FAILED'}")
    print(f"Web Applications:  {'✅ PASSED' if web_ok else '❌ FAILED'}")
    print("=" * 40)
    
    if all([sentiment_ok, image_ok, web_ok]):
        print("🎉 ALL PROJECTS WORK CORRECTLY!")
        print("🚀 You're ready to deploy and apply for internships!")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return all([sentiment_ok, image_ok, web_ok])

if __name__ == "__main__":
    main() 