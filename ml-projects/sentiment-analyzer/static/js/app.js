// Sentiment Analyzer JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Load model statistics on page load
    loadModelStats();
    
    // Form submissions
    document.getElementById('sentimentForm').addEventListener('submit', handleSentimentAnalysis);
    document.getElementById('batchForm').addEventListener('submit', handleBatchAnalysis);
});

// Handle single sentiment analysis
async function handleSentimentAnalysis(e) {
    e.preventDefault();
    
    const textInput = document.getElementById('textInput');
    const text = textInput.value.trim();
    
    if (!text) {
        showAlert('Please enter some text to analyze.', 'warning');
        return;
    }
    
    // Show loading state
    const submitBtn = e.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<span class="loading"></span> Analyzing...';
    submitBtn.disabled = true;
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displaySentimentResult(data.result);
        } else {
            showAlert(data.error || 'Analysis failed.', 'danger');
        }
    } catch (error) {
        showAlert('Network error. Please try again.', 'danger');
        console.error('Error:', error);
    } finally {
        // Reset button
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
}

// Handle batch sentiment analysis
async function handleBatchAnalysis(e) {
    e.preventDefault();
    
    const batchInput = document.getElementById('batchInput');
    const texts = batchInput.value.trim().split('\n').filter(text => text.trim());
    
    if (texts.length === 0) {
        showAlert('Please enter some texts to analyze.', 'warning');
        return;
    }
    
    // Show loading state
    const submitBtn = e.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<span class="loading"></span> Analyzing...';
    submitBtn.disabled = true;
    
    try {
        const response = await fetch('/api/analyze-batch', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ texts: texts })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayBatchResults(data.results, data.statistics);
        } else {
            showAlert(data.error || 'Batch analysis failed.', 'danger');
        }
    } catch (error) {
        showAlert('Network error. Please try again.', 'danger');
        console.error('Error:', error);
    } finally {
        // Reset button
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
}

// Display single sentiment result
function displaySentimentResult(result) {
    const resultsDiv = document.getElementById('results');
    const sentimentIcon = document.getElementById('sentimentIcon');
    const sentimentLabel = document.getElementById('sentimentLabel');
    const confidenceValue = document.getElementById('confidenceValue');
    const processedText = document.getElementById('processedText');
    
    // Set sentiment icon and class
    sentimentIcon.className = 'sentiment-icon';
    if (result.sentiment === 'positive') {
        sentimentIcon.innerHTML = '<i class="fas fa-smile"></i>';
        sentimentIcon.classList.add('sentiment-positive');
        sentimentLabel.textContent = 'Positive';
        sentimentLabel.className = 'mb-1 text-success';
    } else if (result.sentiment === 'negative') {
        sentimentIcon.innerHTML = '<i class="fas fa-frown"></i>';
        sentimentIcon.classList.add('sentiment-negative');
        sentimentLabel.textContent = 'Negative';
        sentimentLabel.className = 'mb-1 text-danger';
    } else {
        sentimentIcon.innerHTML = '<i class="fas fa-meh"></i>';
        sentimentIcon.classList.add('sentiment-neutral');
        sentimentLabel.textContent = 'Neutral';
        sentimentLabel.className = 'mb-1 text-secondary';
    }
    
    // Set confidence and processed text
    confidenceValue.textContent = `${(result.confidence * 100).toFixed(1)}%`;
    processedText.textContent = result.processed_text;
    
    // Show results with animation
    resultsDiv.style.display = 'block';
    resultsDiv.classList.add('fade-in');
    
    // Scroll to results
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Display batch analysis results
function displayBatchResults(results, stats) {
    const batchResultsDiv = document.getElementById('batchResults');
    const batchStatsDiv = document.getElementById('batchStats');
    const batchDetailsDiv = document.getElementById('batchDetails');
    
    // Display statistics
    batchStatsDiv.innerHTML = `
        <div class="col-md-3 text-center">
            <div class="stats-card">
                <div class="stats-number">${stats.total}</div>
                <div class="stats-label">Total Texts</div>
            </div>
        </div>
        <div class="col-md-3 text-center">
            <div class="stats-card" style="background: linear-gradient(135deg, #28a745, #20c997);">
                <div class="stats-number">${stats.positive}</div>
                <div class="stats-label">Positive (${stats.positive_percentage.toFixed(1)}%)</div>
            </div>
        </div>
        <div class="col-md-3 text-center">
            <div class="stats-card" style="background: linear-gradient(135deg, #dc3545, #fd7e14);">
                <div class="stats-number">${stats.negative}</div>
                <div class="stats-label">Negative (${stats.negative_percentage.toFixed(1)}%)</div>
            </div>
        </div>
        <div class="col-md-3 text-center">
            <div class="stats-card" style="background: linear-gradient(135deg, #6c757d, #adb5bd);">
                <div class="stats-number">${stats.neutral}</div>
                <div class="stats-label">Neutral (${stats.neutral_percentage.toFixed(1)}%)</div>
            </div>
        </div>
    `;
    
    // Display individual results
    batchDetailsDiv.innerHTML = '<h6 class="mb-3">Individual Results:</h6>';
    
    results.forEach((result, index) => {
        const sentimentClass = result.sentiment;
        const sentimentIcon = result.sentiment === 'positive' ? '😊' : 
                            result.sentiment === 'negative' ? '😞' : '😐';
        
        const resultHtml = `
            <div class="batch-item ${sentimentClass} fade-in">
                <div class="row align-items-center">
                    <div class="col-md-1 text-center">
                        <span style="font-size: 1.5rem;">${sentimentIcon}</span>
                    </div>
                    <div class="col-md-7">
                        <strong>Text ${index + 1}:</strong> ${result.text}
                    </div>
                    <div class="col-md-2 text-center">
                        <span class="badge bg-${result.sentiment === 'positive' ? 'success' : 
                                               result.sentiment === 'negative' ? 'danger' : 'secondary'}">
                            ${result.sentiment.charAt(0).toUpperCase() + result.sentiment.slice(1)}
                        </span>
                    </div>
                    <div class="col-md-2 text-center">
                        <small class="text-muted">${(result.confidence * 100).toFixed(1)}%</small>
                    </div>
                </div>
            </div>
        `;
        
        batchDetailsDiv.innerHTML += resultHtml;
    });
    
    // Show results with animation
    batchResultsDiv.style.display = 'block';
    batchResultsDiv.classList.add('fade-in');
    
    // Scroll to results
    batchResultsDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Load model statistics
async function loadModelStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        if (data.success) {
            const stats = data.stats;
            document.getElementById('totalAnalyses').textContent = stats.total_analyses.toLocaleString();
            document.getElementById('modelAccuracy').textContent = `${(stats.accuracy * 100).toFixed(1)}%`;
            document.getElementById('positiveAccuracy').textContent = `${(stats.positive_accuracy * 100).toFixed(1)}%`;
            document.getElementById('negativeAccuracy').textContent = `${(stats.negative_accuracy * 100).toFixed(1)}%`;
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Show alert message
function showAlert(message, type) {
    // Remove existing alerts
    const existingAlert = document.querySelector('.alert');
    if (existingAlert) {
        existingAlert.remove();
    }
    
    // Create new alert
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at top of container
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Add some sample texts for testing
function addSampleTexts() {
    const sampleTexts = [
        "I absolutely love this product! It's amazing and works perfectly.",
        "This is the worst thing I've ever bought. Terrible quality.",
        "The product works fine, nothing special but gets the job done.",
        "Amazing service and great quality! Highly recommend!",
        "Terrible experience, would not recommend to anyone."
    ];
    
    document.getElementById('batchInput').value = sampleTexts.join('\n');
}

// Add click handler for sample texts button (if you want to add one)
// document.getElementById('addSampleBtn').addEventListener('click', addSampleTexts); 