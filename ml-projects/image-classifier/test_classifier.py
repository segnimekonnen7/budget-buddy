#!/usr/bin/env python3
"""
Comprehensive test script for plant disease classifier
"""

import numpy as np
import cv2
from PIL import Image
from plant_classifier import PlantDiseaseClassifier
import os

def create_test_images():
    """Create test images for different disease types"""
    test_images = {}
    
    # Create Healthy image (very green, healthy-looking leaf)
    healthy_img = np.zeros((224, 224, 3), dtype=np.uint8)
    center = (112, 112)
    axes = (80, 50)
    # Fill with dark green base
    cv2.ellipse(healthy_img, center, axes, 0, 0, 360, (0, 128, 0), -1)
    # Add healthy leaf texture - small green dots
    for _ in range(50):
        x = np.random.randint(50, 174)
        y = np.random.randint(50, 174)
        cv2.circle(healthy_img, (x, y), 1, (50, 205, 50), -1)
    # Add leaf veins in darker green
    for _ in range(8):
        x1, y1 = np.random.randint(50, 174, 2)
        x2, y2 = np.random.randint(50, 174, 2)
        cv2.line(healthy_img, (x1, y1), (x2, y2), (0, 100, 0), 2)
    # Ensure very dominant green color
    healthy_img = cv2.addWeighted(healthy_img, 0.6, np.full_like(healthy_img, (0, 128, 0)), 0.4, 0)
    test_images['Healthy'] = Image.fromarray(healthy_img)
    
    # Create Bacterial Blight image (brown lesions with water-soaked appearance)
    blight_img = np.zeros((224, 224, 3), dtype=np.uint8)
    # Fill with brown base
    cv2.ellipse(blight_img, center, axes, 0, 0, 360, (139, 69, 19), -1)
    # Add large brown lesions
    for _ in range(15):
        x = np.random.randint(50, 174)
        y = np.random.randint(50, 174)
        radius = np.random.randint(5, 12)
        cv2.circle(blight_img, (x, y), radius, (160, 82, 45), -1)
    # Add water-soaked appearance (light blue spots)
    for _ in range(20):
        x = np.random.randint(50, 174)
        y = np.random.randint(50, 174)
        cv2.circle(blight_img, (x, y), 3, (200, 200, 255), -1)
    # Ensure very dominant brown color
    blight_img = cv2.addWeighted(blight_img, 0.5, np.full_like(blight_img, (139, 69, 19)), 0.5, 0)
    test_images['Bacterial Blight'] = Image.fromarray(blight_img)
    
    # Create Brown Spot image (small, numerous gray spots)
    spot_img = np.zeros((224, 224, 3), dtype=np.uint8)
    # Fill with gray base
    cv2.ellipse(spot_img, center, axes, 0, 0, 360, (128, 128, 128), -1)
    # Add many small gray spots
    for _ in range(40):
        x = np.random.randint(50, 174)
        y = np.random.randint(50, 174)
        radius = np.random.randint(1, 3)
        cv2.circle(spot_img, (x, y), radius, (105, 105, 105), -1)
    # Add yellow halos around some spots
    for _ in range(25):
        x = np.random.randint(50, 174)
        y = np.random.randint(50, 174)
        cv2.circle(spot_img, (x, y), 4, (255, 255, 0), 1)
    # Ensure very dominant gray color
    spot_img = cv2.addWeighted(spot_img, 0.5, np.full_like(spot_img, (128, 128, 128)), 0.5, 0)
    test_images['Brown Spot'] = Image.fromarray(spot_img)
    
    # Create Leaf Blast image (distinct diamond-shaped red lesions)
    blast_img = np.zeros((224, 224, 3), dtype=np.uint8)
    # Fill with red base
    cv2.ellipse(blast_img, center, axes, 0, 0, 360, (255, 0, 0), -1)
    # Add diamond-shaped lesions
    for _ in range(15):
        x = np.random.randint(50, 174)
        y = np.random.randint(50, 174)
        size = np.random.randint(8, 18)
        pts = np.array([[x-size, y], [x, y-size], [x+size, y], [x, y+size]], np.int32)
        cv2.fillPoly(blast_img, [pts], (220, 20, 60))
    # Add white centers to lesions
    for _ in range(12):
        x = np.random.randint(50, 174)
        y = np.random.randint(50, 174)
        cv2.circle(blast_img, (x, y), 3, (255, 255, 255), -1)
    # Ensure very dominant red color
    blast_img = cv2.addWeighted(blast_img, 0.5, np.full_like(blast_img, (255, 0, 0)), 0.5, 0)
    test_images['Leaf Blast'] = Image.fromarray(blast_img)
    
    return test_images

def test_classifier():
    """Test the plant disease classifier"""
    print("Initializing Plant Disease Classifier...")
    classifier = PlantDiseaseClassifier()
    
    # Check if model exists, if not train it
    if not os.path.exists('plant_disease_model.h5'):
        print("Training model...")
        history = classifier.train_model(epochs=3)
        classifier.save_model()
    else:
        print("Loading existing model...")
        classifier.load_model()
    
    # Create test images
    print("Creating test images...")
    test_images = create_test_images()
    
    print("\n" + "="*60)
    print("COMPREHENSIVE IMAGE CLASSIFICATION TESTING")
    print("="*60)
    
    correct_predictions = 0
    total_tests = len(test_images)
    
    for expected_class, test_image in test_images.items():
        try:
            # Make prediction
            result = classifier.predict_image(test_image)
            predicted_class = result['class']
            confidence = result['confidence']
            
            # Check if prediction is correct
            is_correct = predicted_class == expected_class
            if is_correct:
                correct_predictions += 1
            
            status = "✓" if is_correct else "✗"
            
            print(f"{status} Expected: {expected_class:15} | Predicted: {predicted_class:15} | Confidence: {confidence:.2f}")
            
            # Show probabilities for all classes
            print(f"    Probabilities: ", end="")
            for i, (class_name, prob) in enumerate(zip(result['class_names'], result['probabilities'])):
                print(f"{class_name}: {prob:.3f}", end="")
                if i < len(result['class_names']) - 1:
                    print(", ", end="")
            print()
            print()
            
        except Exception as e:
            print(f"✗ Error testing {expected_class}: {e}")
            print()
    
    accuracy = (correct_predictions / total_tests) * 100
    print(f"Overall Accuracy: {accuracy:.1f}% ({correct_predictions}/{total_tests})")
    
    # Test with edge cases
    print("\n" + "="*60)
    print("EDGE CASE TESTING")
    print("="*60)
    
    # Test with different image sizes
    edge_cases = {
        "Small image (100x100)": Image.fromarray(np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)),
        "Large image (400x400)": Image.fromarray(np.random.randint(0, 255, (400, 400, 3), dtype=np.uint8)),
        "Grayscale image": Image.fromarray(np.random.randint(0, 255, (224, 224), dtype=np.uint8)),
        "Very dark image": Image.fromarray(np.zeros((224, 224, 3), dtype=np.uint8)),
        "Very bright image": Image.fromarray(np.full((224, 224, 3), 255, dtype=np.uint8))
    }
    
    for case_name, test_image in edge_cases.items():
        try:
            result = classifier.predict_image(test_image)
            print(f"✓ {case_name:25} -> {result['class']:15} (confidence: {result['confidence']:.2f})")
        except Exception as e:
            print(f"✗ {case_name:25} -> Error: {e}")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    test_classifier() 