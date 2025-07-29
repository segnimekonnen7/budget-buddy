#!/usr/bin/env python3
"""
Test script to debug sentiment analysis model
"""

from sentiment_model import SentimentAnalyzer

def test_model():
    # Initialize analyzer
    analyzer = SentimentAnalyzer()
    
    # Train model
    print("Training model...")
    results = analyzer.train_model()
    print(f"Training accuracy: {results['accuracy']:.3f}")
    
    # Test cases
    test_texts = [
        "I love this product! It's amazing!",
        "This is terrible, I hate it!",
        "The weather is okay today.",
        "I'm so happy and excited!",
        "This makes me very sad and disappointed.",
        "The movie was neither good nor bad."
    ]
    
    print("\n" + "="*50)
    print("TESTING SENTIMENT ANALYSIS")
    print("="*50)
    
    for text in test_texts:
        result = analyzer.predict_sentiment(text)
        print(f"\nText: {text}")
        print(f"Sentiment: {result['sentiment']}")
        print(f"Confidence: {result['confidence']:.3f}")
        print(f"Probabilities: {result['probabilities']}")
        print(f"TextBlob Polarity: {result['textblob_polarity']:.3f}")
        print("-" * 30)

if __name__ == "__main__":
    test_model() 