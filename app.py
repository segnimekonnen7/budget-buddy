#!/usr/bin/env python3
"""
AI Task Manager - Local AI Powered Task Management
Uses Ollama for local AI processing - completely free and private!
"""

from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta
import requests
import os
from dotenv import load_dotenv
import json
import re
from dateutil import parser
import spacy
import threading
import time
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Ollama (Local AI)
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Load spaCy model for NLP
try:
    nlp = spacy.load("en_core_web_sm")
except:
    nlp = None

# Database Models
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), default='General')
    priority = db.Column(db.String(20), default='Medium')
    status = db.Column(db.String(20), default='Pending')
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    ai_processed = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'priority': self.priority,
            'status': self.status,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'ai_processed': self.ai_processed
        }

# AI Processing Functions
def extract_entities(text):
    """Extract entities like dates, times, people from text using spaCy"""
    if not nlp:
        return {}
    
    doc = nlp(text)
    entities = {
        'dates': [],
        'times': [],
        'people': [],
        'locations': []
    }
    
    for ent in doc.ents:
        if ent.label_ == 'DATE':
            entities['dates'].append(ent.text)
        elif ent.label_ == 'TIME':
            entities['times'].append(ent.text)
        elif ent.label_ == 'PERSON':
            entities['people'].append(ent.text)
        elif ent.label_ == 'GPE':
            entities['locations'].append(ent.text)
    
    return entities

def analyze_task_with_ai(task_text):
    """Use Ollama (local AI) to analyze task and extract structured information"""
    # Try AI first, but always fallback to our improved time extraction
    try:
        prompt = f"""
        Analyze this task and extract the following information in JSON format:
        Task: "{task_text}"
        
        Return JSON with:
        - title: Short, clear task title
        - description: Detailed description
        - category: One of [Work, Personal, Health, Finance, Education, Shopping, Travel, Home]
        - priority: One of [Low, Medium, High, Urgent]
        - due_date: Extract date if mentioned (YYYY-MM-DD format)
        - estimated_duration: Estimated time in hours
        
        Only return valid JSON, no other text.
        """
        
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": "llama2:7b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "num_predict": 300
                }
            },
            timeout=5  # Very short timeout
        )
        
        if response.status_code == 200:
            result_text = response.json().get('response', '')
            if not result_text or result_text.strip() == '':
                print("Ollama returned empty response, using fallback")
                return get_fallback_analysis(task_text)
            
            # Clean up the response to extract JSON
            result_text = result_text.strip()
            if result_text.startswith('```json'):
                result_text = result_text[7:]
            if result_text.endswith('```'):
                result_text = result_text[:-3]
            
            # Try to parse JSON
            try:
                result = json.loads(result_text)
                # If AI didn't extract due_date, use our fallback for time extraction
                if not result.get('due_date'):
                    fallback_result = get_fallback_analysis(task_text)
                    result['due_date'] = fallback_result.get('due_date')
                return result
            except json.JSONDecodeError:
                print(f"Failed to parse Ollama JSON response: {result_text}")
                return get_fallback_analysis(task_text)
        else:
            print(f"Ollama API error: {response.status_code}")
            return get_fallback_analysis(task_text)
            
    except requests.exceptions.Timeout:
        print("Ollama request timed out, using fallback")
        return get_fallback_analysis(task_text)
    except Exception as e:
        print(f"AI analysis error: {e}")
        return get_fallback_analysis(task_text)


def get_fallback_analysis(task_text):
    """Fallback analysis when AI is not available"""
    # Simple rule-based analysis
    text_lower = task_text.lower()
    
    # Category detection
    category = 'General'
    if any(word in text_lower for word in ['work', 'job', 'office', 'meeting', 'project']):
        category = 'Work'
    elif any(word in text_lower for word in ['health', 'doctor', 'exercise', 'gym', 'medical']):
        category = 'Health'
    elif any(word in text_lower for word in ['money', 'bill', 'pay', 'finance', 'bank']):
        category = 'Finance'
    elif any(word in text_lower for word in ['study', 'learn', 'school', 'course', 'homework']):
        category = 'Education'
    elif any(word in text_lower for word in ['buy', 'shop', 'purchase', 'grocery']):
        category = 'Shopping'
    elif any(word in text_lower for word in ['travel', 'trip', 'vacation', 'flight']):
        category = 'Travel'
    elif any(word in text_lower for word in ['home', 'house', 'clean', 'repair']):
        category = 'Home'
    elif any(word in text_lower for word in ['family', 'friend', 'personal', 'hobby']):
        category = 'Personal'
    
    # Priority detection
    priority = 'Medium'
    if any(word in text_lower for word in ['urgent', 'asap', 'emergency', 'critical']):
        priority = 'Urgent'
    elif any(word in text_lower for word in ['important', 'high', 'priority']):
        priority = 'High'
    elif any(word in text_lower for word in ['low', 'sometime', 'when possible']):
        priority = 'Low'
    
    # Date and time extraction (improved)
    due_date = None
    due_time = None
    
    # Extract time first - more comprehensive patterns
    time_patterns = [
        r'(\d{1,2}):(\d{2})\s*(am|pm)?',
        r'(\d{1,2})\s*(am|pm)',
        r'at\s+(\d{1,2}):(\d{2})\s*(am|pm)?',
        r'at\s+(\d{1,2})\s*(am|pm)',
        r'(\d{1,2}):(\d{2})\s*(am|pm)',
        r'(\d{1,2})\s*(am|pm)',
        r'(\d{1,2}):(\d{2})',
        r'(\d{1,2})\s*(am|pm)'
    ]
    
    for pattern in time_patterns:
        match = re.search(pattern, text_lower)
        if match:
            groups = match.groups()
            if ':' in match.group(0):
                hour = groups[0]
                minute = groups[1]
                ampm = groups[2] if len(groups) > 2 else None
            else:
                hour = groups[0]
                minute = '00'
                ampm = groups[1] if len(groups) > 1 else None
            
            # Convert to 24-hour format
            hour = int(hour)
            if ampm == 'pm' and hour != 12:
                hour += 12
            elif ampm == 'am' and hour == 12:
                hour = 0
            
            due_time = f"{hour:02d}:{minute}"
            print(f"Extracted time: {due_time} from '{match.group(0)}'")
            break
    
    # Extract date
    if 'tomorrow' in text_lower:
        due_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        print(f"Extracted date: {due_date} (tomorrow)")
    elif 'next week' in text_lower:
        due_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        print(f"Extracted date: {due_date} (next week)")
    elif 'today' in text_lower:
        due_date = datetime.now().strftime('%Y-%m-%d')
        print(f"Extracted date: {due_date} (today)")
    
    # Combine date and time
    if due_date and due_time:
        due_date = f"{due_date} {due_time}"
        print(f"Combined date and time: {due_date}")
    elif due_time:
        # If only time is specified, assume today
        due_date = f"{datetime.now().strftime('%Y-%m-%d')} {due_time}"
        print(f"Time only, assuming today: {due_date}")
    elif due_date:
        print(f"Date only: {due_date}")
    
    return {
        'title': task_text[:50] + ('...' if len(task_text) > 50 else ''),
        'description': task_text,
        'category': category,
        'priority': priority,
        'due_date': due_date,
        'estimated_duration': 1
    }

def get_ai_suggestions():
    """Get AI-powered task suggestions using Ollama"""
    try:
        prompt = """
        Suggest 3-5 productive tasks for today based on common productivity patterns.
        Return as JSON array with objects containing:
        - title: Task title
        - description: Brief description
        - category: Category
        - priority: Priority level
        - reason: Why this task is suggested
        
        Focus on tasks that improve productivity, health, or learning.
        """
        
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": "llama2:7b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 400
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result_text = response.json().get('response', '')
            # Clean up the response to extract JSON
            result_text = result_text.strip()
            if result_text.startswith('```json'):
                result_text = result_text[7:]
            if result_text.endswith('```'):
                result_text = result_text[:-3]
            
            return json.loads(result_text)
        else:
            return get_fallback_suggestions()
            
    except Exception as e:
        print(f"AI suggestions error: {e}")
        return get_fallback_suggestions()

def get_fallback_suggestions():
    """Fallback suggestions when AI is not available"""
    return [
        {
            "title": "Review and organize your workspace",
            "description": "Clean up your desk, organize files, and declutter your digital workspace",
            "category": "Work",
            "priority": "Medium",
            "reason": "A clean workspace improves focus and productivity"
        },
        {
            "title": "Take a 15-minute walk",
            "description": "Step outside for a short walk to refresh your mind and get some exercise",
            "category": "Health",
            "priority": "Medium",
            "reason": "Physical activity boosts energy and mental clarity"
        },
        {
            "title": "Plan tomorrow's priorities",
            "description": "Review your calendar and set 3 main priorities for tomorrow",
            "category": "Work",
            "priority": "High",
            "reason": "Planning ahead reduces stress and improves productivity"
        },
        {
            "title": "Learn something new for 20 minutes",
            "description": "Read an article, watch a tutorial, or practice a new skill",
            "category": "Education",
            "priority": "Low",
            "reason": "Continuous learning keeps your mind sharp and opens new opportunities"
        },
        {
            "title": "Connect with a friend or family member",
            "description": "Send a message, make a call, or plan to meet someone important to you",
            "category": "Personal",
            "priority": "Medium",
            "reason": "Maintaining relationships is important for overall well-being"
        }
    ]

# Reminder System
def check_due_tasks():
    """Check for tasks that are due and show notifications"""
    try:
        with app.app_context():
            now = datetime.now()
            # Check for tasks due in the next 5 minutes
            upcoming_tasks = Task.query.filter(
                Task.due_date.isnot(None),
                Task.due_date <= now + timedelta(minutes=5),
                Task.due_date >= now,
                Task.status == 'Pending'
            ).all()
            
            for task in upcoming_tasks:
                time_until = task.due_date - now
                minutes_until = int(time_until.total_seconds() / 60)
                
                if minutes_until <= 5 and minutes_until >= 0:
                    print(f"🔔 REMINDER: '{task.title}' is due in {minutes_until} minutes!")
                    print(f"   Category: {task.category} | Priority: {task.priority}")
                    print(f"   Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}")
                    print("-" * 50)
                    
    except Exception as e:
        print(f"Reminder check error: {e}")

def reminder_worker():
    """Background worker that checks for reminders every minute"""
    while True:
        check_due_tasks()
        time.sleep(60)  # Check every minute

# Start reminder system
reminder_thread = threading.Thread(target=reminder_worker, daemon=True)
reminder_thread.start()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return jsonify([task.to_dict() for task in tasks])

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task with AI processing"""
    data = request.get_json()
    task_text = data.get('text', '')
    
    if not task_text:
        return jsonify({'error': 'Task text is required'}), 400
    
    # Process with AI
    ai_analysis = analyze_task_with_ai(task_text)
    
    # Parse due date
    due_date = None
    if ai_analysis.get('due_date'):
        try:
            due_date = parser.parse(ai_analysis['due_date'])
        except:
            pass
    
    # Create task
    task = Task(
        title=ai_analysis.get('title', task_text),
        description=ai_analysis.get('description', task_text),
        category=ai_analysis.get('category', 'General'),
        priority=ai_analysis.get('priority', 'Medium'),
        due_date=due_date,
        ai_processed=True
    )
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify(task.to_dict()), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task"""
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'category' in data:
        task.category = data['category']
    if 'priority' in data:
        task.priority = data['priority']
    if 'status' in data:
        task.status = data['status']
        if data['status'] == 'Completed':
            task.completed_at = datetime.utcnow()
    if 'due_date' in data and data['due_date']:
        task.due_date = parser.parse(data['due_date'])
    
    db.session.commit()
    return jsonify(task.to_dict())

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'})

@app.route('/api/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    """Mark task as completed"""
    task = Task.query.get_or_404(task_id)
    task.status = 'Completed'
    task.completed_at = datetime.utcnow()
    db.session.commit()
    return jsonify(task.to_dict())

@app.route('/api/ai/suggestions', methods=['GET'])
def get_suggestions():
    """Get AI-powered task suggestions"""
    suggestions = get_ai_suggestions()
    return jsonify(suggestions)

@app.route('/api/ai/analyze', methods=['POST'])
def analyze_text():
    """Analyze text with AI"""
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'Text is required'}), 400
    
    # Extract entities
    entities = extract_entities(text)
    
    # Analyze with AI
    ai_analysis = analyze_task_with_ai(text)
    
    return jsonify({
        'entities': entities,
        'analysis': ai_analysis
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get task statistics"""
    total_tasks = Task.query.count()
    completed_tasks = Task.query.filter_by(status='Completed').count()
    pending_tasks = Task.query.filter_by(status='Pending').count()
    
    # Category breakdown
    categories = db.session.query(Task.category, db.func.count(Task.id)).group_by(Task.category).all()
    
    # Priority breakdown
    priorities = db.session.query(Task.priority, db.func.count(Task.id)).group_by(Task.priority).all()
    
    return jsonify({
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
        'categories': dict(categories),
        'priorities': dict(priorities)
    })

@app.route('/api/reminders', methods=['GET'])
def get_upcoming_reminders():
    """Get upcoming task reminders"""
    now = datetime.now()
    upcoming_tasks = Task.query.filter(
        Task.due_date.isnot(None),
        Task.due_date <= now + timedelta(hours=24),  # Next 24 hours
        Task.due_date >= now,
        Task.status == 'Pending'
    ).order_by(Task.due_date).all()
    
    reminders = []
    for task in upcoming_tasks:
        time_until = task.due_date - now
        minutes_until = int(time_until.total_seconds() / 60)
        hours_until = int(time_until.total_seconds() / 3600)
        
        if minutes_until < 60:
            time_text = f"{minutes_until} minutes"
        else:
            time_text = f"{hours_until} hours"
        
        reminders.append({
            'id': task.id,
            'title': task.title,
            'due_date': task.due_date.isoformat(),
            'time_until': time_text,
            'minutes_until': minutes_until,
            'category': task.category,
            'priority': task.priority
        })
    
    return jsonify(reminders)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    print("🚀 Starting AI Task Manager...")
    print("🤖 Features:")
    print("   - Natural language task processing")
    print("   - AI-powered task analysis (Local AI with Ollama)")
    print("   - Smart categorization and prioritization")
    print("   - Completely FREE - no API keys needed!")
    print("   - Real-time task management")
    print("   - 🔔 Automatic reminders (checks every minute)")
    print("✅ Ready to manage tasks with local AI!")
    print("=" * 60)
    
    app.run(debug=True, port=5001)