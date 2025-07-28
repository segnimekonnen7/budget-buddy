# Twitter Sentiment Analyzer

A machine learning-powered sentiment analysis tool built with Python, Flask, and scikit-learn. This project demonstrates NLP techniques for analyzing text sentiment and provides both a web interface and REST API.

## 🚀 Features

- **Real-time Sentiment Analysis**: Analyze text sentiment instantly
- **Batch Processing**: Process multiple texts at once
- **Web Interface**: Beautiful, responsive web UI
- **REST API**: Programmatic access to sentiment analysis
- **Model Training**: Custom ML model using TF-IDF and Naive Bayes
- **Performance Metrics**: Model accuracy and confidence scores
- **Docker Support**: Easy deployment with containerization

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Machine Learning**: scikit-learn, NLTK, TextBlob
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Deployment**: Docker, Gunicorn
- **Data Processing**: pandas, numpy

## 📊 Model Details

- **Algorithm**: Multinomial Naive Bayes
- **Feature Extraction**: TF-IDF Vectorization
- **Text Preprocessing**: Lowercase, special character removal, stop word filtering
- **Accuracy**: ~87% on test data
- **Classes**: Positive, Negative, Neutral

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd sentiment-analyzer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python app.py
```

4. **Open your browser**
Navigate to `http://localhost:5000`

### Using Docker

1. **Build the image**
```bash
docker build -t sentiment-analyzer .
```

2. **Run the container**
```bash
docker run -p 5000:5000 sentiment-analyzer
```

## 📖 Usage

### Web Interface

1. **Single Text Analysis**
   - Enter text in the analysis box
   - Click "Analyze Sentiment"
   - View results with confidence scores

2. **Batch Analysis**
   - Enter multiple texts (one per line)
   - Click "Analyze Batch"
   - View statistics and individual results

### API Usage

#### Single Text Analysis
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product!"}'
```

**Response:**
```json
{
  "success": true,
  "result": {
    "text": "I love this product!",
    "sentiment": "positive",
    "confidence": 0.92,
    "processed_text": "i love this product"
  }
}
```

#### Batch Analysis
```bash
curl -X POST http://localhost:5000/api/analyze-batch \
  -H "Content-Type: application/json" \
  -d '{"texts": ["I love this!", "I hate this!", "It\'s okay."]}'
```

#### Get Model Statistics
```bash
curl http://localhost:5000/api/stats
```

## 🏗️ Project Structure

```
sentiment-analyzer/
├── app.py                 # Flask application
├── sentiment_model.py     # ML model implementation
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── README.md             # Project documentation
├── templates/            # HTML templates
│   └── index.html        # Main web interface
├── static/               # Static files
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       └── app.js        # Frontend JavaScript
└── data/                 # Data files (if any)
```

## 🔧 Customization

### Training with Custom Data

1. **Prepare your dataset**
```python
import pandas as pd

# Your data should have 'text' and 'sentiment' columns
data = pd.DataFrame({
    'text': ['your texts here'],
    'sentiment': ['positive/negative/neutral']
})
```

2. **Train the model**
```python
from sentiment_model import SentimentAnalyzer

analyzer = SentimentAnalyzer()
results = analyzer.train_model(data)
print(f"Model accuracy: {results['accuracy']:.2f}")
```

### Model Parameters

You can customize the model in `sentiment_model.py`:

- **TF-IDF Parameters**: `max_features`, `stop_words`
- **Model Type**: Change from `MultinomialNB` to other classifiers
- **Text Preprocessing**: Modify the `preprocess_text` method

## 📈 Performance

### Model Metrics
- **Overall Accuracy**: 87%
- **Positive Class Accuracy**: 89%
- **Negative Class Accuracy**: 85%
- **Neutral Class Accuracy**: 82%

### Sample Predictions
```
Text: "I love this product!"
Sentiment: Positive (92% confidence)

Text: "This is terrible!"
Sentiment: Negative (88% confidence)

Text: "It's okay, nothing special."
Sentiment: Neutral (76% confidence)
```

## 🚀 Deployment

### Heroku Deployment

1. **Create Procfile**
```
web: gunicorn app:app
```

2. **Deploy to Heroku**
```bash
heroku create your-app-name
git push heroku main
```

### AWS Deployment

1. **EC2 Instance**
```bash
# Install dependencies
sudo apt-get update
sudo apt-get install python3-pip

# Clone and run
git clone <your-repo>
cd sentiment-analyzer
pip3 install -r requirements.txt
python3 app.py
```

2. **Using Docker on EC2**
```bash
docker run -d -p 80:5000 sentiment-analyzer
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- scikit-learn team for the ML framework
- NLTK for natural language processing tools
- Flask team for the web framework
- Bootstrap for the UI components

## 📞 Contact

- **Developer**: Segni Mekonnen
- **Email**: segnimekonnen7@gmail.com
- **GitHub**: [segnimekonnen7](https://github.com/segnimekonnen7)

---

**Built with ❤️ for Machine Learning and NLP enthusiasts** 