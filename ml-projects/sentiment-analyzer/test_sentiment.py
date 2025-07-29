#!/usr/bin/env python3
"""
Comprehensive test script for sentiment analyzer
"""

from sentiment_model import SentimentAnalyzer

def test_sentiment_analyzer():
    # Initialize analyzer
    analyzer = SentimentAnalyzer()
    
    # Train model
    print("Training sentiment analysis model...")
    results = analyzer.train_model()
    print(f"Model accuracy: {results['accuracy']:.2f}")
    
    # Test cases with different types of text
    test_cases = [
        # Positive cases
        ("I love this movie! It's absolutely fantastic!", "positive"),
        ("Great service and amazing quality!", "positive"),
        ("This is the best thing I've ever bought!", "positive"),
        ("Wonderful experience, highly recommend!", "positive"),
        ("Excellent product with outstanding features!", "positive"),
        
        # Negative cases
        ("I hate this product. It's terrible!", "negative"),
        ("Worst experience ever. Don't buy this!", "negative"),
        ("This is awful and a complete waste of money!", "negative"),
        ("Terrible quality and poor service!", "negative"),
        ("Disappointing and frustrating experience!", "negative"),
        
        # Neutral cases
        ("The product is okay, nothing special.", "neutral"),
        ("It works fine, meets basic expectations.", "neutral"),
        ("Average quality, standard features.", "neutral"),
        ("The service is acceptable but not outstanding.", "neutral"),
        ("It's fine for what it is, nothing more.", "neutral"),
        
        # Edge cases
        ("", "neutral"),  # Empty text
        ("12345", "neutral"),  # Numbers only
        ("!@#$%", "neutral"),  # Special characters only
        ("The", "neutral"),  # Single word
        ("This product has both good and bad aspects.", "neutral"),  # Mixed sentiment
    ]
    
    print("\n" + "="*60)
    print("COMPREHENSIVE TESTING")
    print("="*60)
    
    correct_predictions = 0
    total_tests = len(test_cases)
    
    for i, (text, expected) in enumerate(test_cases, 1):
        try:
            result = analyzer.predict_sentiment(text)
            predicted = result['sentiment']
            confidence = result['confidence']
            
            is_correct = predicted == expected
            if is_correct:
                correct_predictions += 1
            
            status = "✓" if is_correct else "✗"
            
            print(f"{i:2d}. {status} Text: '{text[:50]}{'...' if len(text) > 50 else ''}'")
            print(f"    Expected: {expected}, Predicted: {predicted}, Confidence: {confidence:.2f}")
            print()
            
        except Exception as e:
            print(f"{i:2d}. ✗ Error: {e}")
            print()
    
    accuracy = (correct_predictions / total_tests) * 100
    print(f"Overall Accuracy: {accuracy:.1f}% ({correct_predictions}/{total_tests})")
    
    # Test batch analysis
    print("\n" + "="*60)
    print("BATCH ANALYSIS TEST")
    print("="*60)
    
    batch_texts = [
        "I love this!",
        "This is terrible!",
        "It's okay.",
        "Amazing product!",
        "Worst ever!"
    ]
    
    batch_results = analyzer.analyze_batch(batch_texts)
    
    for i, (text, result) in enumerate(zip(batch_texts, batch_results)):
        print(f"{i+1}. '{text}' -> {result['sentiment']} (confidence: {result['confidence']:.2f})")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    test_sentiment_analyzer() 