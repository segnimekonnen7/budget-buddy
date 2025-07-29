#!/usr/bin/env python3
"""
Test script to test Flask API endpoints
"""

import requests
import json

def test_api():
    base_url = "http://localhost:5002"
    
    # Test single sentiment analysis
    test_texts = [
        "I love this product! It's amazing!",
        "This is terrible, I hate it!",
        "The weather is okay today."
    ]
    
    print("Testing single sentiment analysis:")
    print("=" * 50)
    
    for text in test_texts:
        try:
            response = requests.post(
                f"{base_url}/api/analyze",
                json={"text": text},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    result = data['result']
                    print(f"\nText: {text}")
                    print(f"Sentiment: {result['sentiment']}")
                    print(f"Confidence: {result['confidence']:.3f}")
                    print(f"Probabilities: {result['probabilities']}")
                else:
                    print(f"Error: {data.get('error', 'Unknown error')}")
            else:
                print(f"HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"Request failed: {e}")
        
        print("-" * 30)
    
    # Test batch analysis
    print("\n\nTesting batch sentiment analysis:")
    print("=" * 50)
    
    try:
        response = requests.post(
            f"{base_url}/api/analyze-batch",
            json={"texts": test_texts},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"Batch results:")
                for i, result in enumerate(data['results']):
                    print(f"Text {i+1}: {result['sentiment']} (confidence: {result['confidence']:.3f})")
                print(f"\nStatistics: {data['statistics']}")
            else:
                print(f"Error: {data.get('error', 'Unknown error')}")
        else:
            print(f"HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_api() 