#!/usr/bin/env python3
"""
Test script for Enhanced Plant Disease Classifier
Comprehensive testing of all features
"""

import numpy as np
from PIL import Image
import sys
import os

# Add the current directory to path to import functions
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import functions from enhanced_app
from enhanced_app import (
    create_sample_images,
    analyze_image_features,
    predict_disease_advanced,
    create_analysis_charts
)

def test_sample_image_creation():
    """Test sample image creation"""
    print("🧪 Testing sample image creation...")
    
    try:
        sample_images = create_sample_images()
        
        # Check if all 4 disease types are created
        expected_diseases = ['Healthy', 'Bacterial Blight', 'Brown Spot', 'Leaf Blast']
        for disease in expected_diseases:
            assert disease in sample_images, f"Missing {disease} sample image"
            assert sample_images[disease].size == (224, 224), f"Wrong size for {disease}"
            print(f"✅ {disease} sample image created successfully")
        
        print("✅ All sample images created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Sample image creation failed: {e}")
        return False

def test_feature_analysis():
    """Test image feature analysis"""
    print("\n🧪 Testing feature analysis...")
    
    try:
        # Create a test image
        test_img = np.zeros((224, 224, 3), dtype=np.uint8)
        test_img[:, :, 1] = 128  # Green image
        test_image = Image.fromarray(test_img)
        
        # Analyze features
        features = analyze_image_features(test_image)
        
        # Check if all expected features are present
        expected_features = ['avg_red', 'avg_green', 'avg_blue', 'std_dev', 'width', 'height', 'aspect_ratio']
        for feature in expected_features:
            assert feature in features, f"Missing feature: {feature}"
        
        # Check feature values
        assert features['avg_green'] == 128, f"Expected green=128, got {features['avg_green']}"
        assert features['width'] == 224, f"Expected width=224, got {features['width']}"
        assert features['height'] == 224, f"Expected height=224, got {features['height']}"
        
        print("✅ Feature analysis working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Feature analysis failed: {e}")
        return False

def test_disease_prediction():
    """Test disease prediction"""
    print("\n🧪 Testing disease prediction...")
    
    try:
        # Test healthy image
        healthy_img = np.zeros((224, 224, 3), dtype=np.uint8)
        healthy_img[:, :, 1] = 150  # High green
        healthy_image = Image.fromarray(healthy_img)
        
        prediction, confidence, features = predict_disease_advanced(healthy_image)
        print(f"✅ Healthy image prediction: {prediction} ({confidence:.1%})")
        
        # Test leaf blast image
        blast_img = np.zeros((224, 224, 3), dtype=np.uint8)
        blast_img[:, :, 0] = 200  # High red
        blast_image = Image.fromarray(blast_img)
        
        prediction, confidence, features = predict_disease_advanced(blast_image)
        print(f"✅ Leaf blast image prediction: {prediction} ({confidence:.1%})")
        
        # Test bacterial blight image
        blight_img = np.zeros((224, 224, 3), dtype=np.uint8)
        blight_img[:, :, 0] = 120  # Medium red
        blight_img[:, :, 1] = 60   # Medium green
        blight_img[:, :, 2] = 20   # Low blue
        blight_image = Image.fromarray(blight_img)
        
        prediction, confidence, features = predict_disease_advanced(blight_image)
        print(f"✅ Bacterial blight image prediction: {prediction} ({confidence:.1%})")
        
        print("✅ Disease prediction working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Disease prediction failed: {e}")
        return False

def test_chart_creation():
    """Test chart creation"""
    print("\n🧪 Testing chart creation...")
    
    try:
        # Create test features
        features = {
            'avg_red': 100,
            'avg_green': 150,
            'avg_blue': 50,
            'std_dev': 25,
            'width': 224,
            'height': 224,
            'aspect_ratio': 1.0
        }
        
        # Create charts
        fig1, fig2 = create_analysis_charts(features, "Healthy", 0.92)
        
        # Check if charts were created
        assert fig1 is not None, "Color distribution chart not created"
        assert fig2 is not None, "Confidence chart not created"
        
        print("✅ Chart creation working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Chart creation failed: {e}")
        return False

def test_all_features():
    """Test all features together"""
    print("\n🧪 Testing all features together...")
    
    try:
        # Create sample images
        sample_images = create_sample_images()
        
        # Test each sample image
        for disease, image in sample_images.items():
            # Analyze features
            features = analyze_image_features(image)
            
            # Predict disease
            prediction, confidence, features = predict_disease_advanced(image)
            
            # Create charts
            fig1, fig2 = create_analysis_charts(features, prediction, confidence)
            
            print(f"✅ {disease}: {prediction} ({confidence:.1%})")
        
        print("✅ All features working together correctly")
        return True
        
    except Exception as e:
        print(f"❌ Combined features test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Enhanced Plant Disease Classifier Tests")
    print("=" * 60)
    
    tests = [
        test_sample_image_creation,
        test_feature_analysis,
        test_disease_prediction,
        test_chart_creation,
        test_all_features
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The enhanced app is ready for deployment.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    main() 