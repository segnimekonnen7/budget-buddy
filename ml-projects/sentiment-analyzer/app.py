from flask import Flask, render_template, request, jsonify
from sentiment_model import SentimentAnalyzer
import plotly.graph_objs as go
import plotly.utils
import json
import os

app = Flask(__name__)

# Initialize sentiment analyzer
analyzer = SentimentAnalyzer()

# Train model on startup
def train_model():
    print("Training sentiment analysis model...")
    results = analyzer.train_model()
    print(f"Model trained with accuracy: {results['accuracy']:.2f}")

# Train model when app starts
with app.app_context():
    train_model()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_sentiment():
    """API endpoint for sentiment analysis"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Analyze sentiment
        result = analyzer.predict_sentiment(text)
        
        return jsonify({
            'success': True,
            'result': result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-batch', methods=['POST'])
def analyze_batch():
    """API endpoint for batch sentiment analysis"""
    try:
        data = request.get_json()
        texts = data.get('texts', [])
        
        if not texts:
            return jsonify({'error': 'No texts provided'}), 400
        
        # Analyze sentiments
        results = analyzer.analyze_batch(texts)
        
        # Calculate statistics
        sentiments = [r['sentiment'] for r in results]
        positive_count = sentiments.count('positive')
        negative_count = sentiments.count('negative')
        neutral_count = sentiments.count('neutral')
        
        stats = {
            'total': len(texts),
            'positive': positive_count,
            'negative': negative_count,
            'neutral': neutral_count,
            'positive_percentage': (positive_count / len(texts)) * 100,
            'negative_percentage': (negative_count / len(texts)) * 100,
            'neutral_percentage': (neutral_count / len(texts)) * 100
        }
        
        return jsonify({
            'success': True,
            'results': results,
            'statistics': stats
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """Get model statistics"""
    try:
        # This would typically come from a database
        # For now, return sample statistics
        stats = {
            'total_analyses': 1250,
            'accuracy': 0.87,
            'positive_accuracy': 0.89,
            'negative_accuracy': 0.85,
            'neutral_accuracy': 0.82
        }
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/demo')
def demo():
    """Demo page with interactive examples"""
    return render_template('demo.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002) 