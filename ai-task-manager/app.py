from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta
import openai
import os
from dotenv import load_dotenv
import json
import re
from dateutil import parser

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY', 'your-openai-api-key-here')

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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
def extract_entities_simple(text):
    """Simple entity extraction using regex patterns"""
    entities = {
        'dates': [],
        'times': [],
        'people': [],
        'locations': []
    }
    
    # Simple date patterns
    date_patterns = [
        r'tomorrow',
        r'today',
        r'next week',
        r'next month',
        r'this weekend',
        r'\d{1,2}/\d{1,2}',
        r'\d{1,2}-\d{1,2}',
        r'\d{4}-\d{2}-\d{2}'
    ]
    
    for pattern in date_patterns:
        matches = re.findall(pattern, text.lower())
        entities['dates'].extend(matches)
    
    # Simple time patterns
    time_patterns = [
        r'\d{1,2}:\d{2}\s*(am|pm)?',
        r'\d{1,2}\s*(am|pm)',
        r'morning',
        r'afternoon',
        r'evening',
        r'night'
    ]
    
    for pattern in time_patterns:
        matches = re.findall(pattern, text.lower())
        entities['times'].extend(matches)
    
    return entities

def analyze_task_with_ai(task_text):
    """Hybrid AI task analysis - uses OpenAI when available, smart fallback when not"""
    try:
        # Check if OpenAI API key is properly configured
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'your-openai-api-key-here':
            print("OpenAI API key not configured, using enhanced fallback analysis")
            return analyze_task_enhanced_fallback(task_text)
        
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
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a task analysis assistant. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.3
        )
        
        result = json.loads(response.choices[0].message.content)
        print("✅ AI analysis successful using OpenAI")
        return result
        
    except Exception as e:
        print(f"AI analysis error: {e}")
        print("🔄 Falling back to enhanced rule-based analysis")
        return analyze_task_enhanced_fallback(task_text)

def analyze_task_enhanced_fallback(task_text):
    """Enhanced rule-based task analysis with NLP-like features"""
    text_lower = task_text.lower()
    
    # Enhanced category detection with more keywords
    category_keywords = {
        'Work': ['work', 'job', 'project', 'meeting', 'presentation', 'report', 'deadline', 'client', 'boss', 'office', 'business', 'professional'],
        'Health': ['exercise', 'workout', 'gym', 'run', 'walk', 'health', 'doctor', 'appointment', 'medicine', 'diet', 'fitness', 'yoga'],
        'Shopping': ['buy', 'purchase', 'shop', 'grocery', 'shopping', 'store', 'mall', 'order', 'amazon', 'online'],
        'Education': ['study', 'learn', 'read', 'course', 'education', 'school', 'university', 'homework', 'assignment', 'exam', 'test'],
        'Travel': ['travel', 'trip', 'vacation', 'flight', 'hotel', 'booking', 'reservation', 'destination', 'airport'],
        'Home': ['home', 'house', 'clean', 'repair', 'maintenance', 'garden', 'laundry', 'cooking', 'kitchen'],
        'Finance': ['money', 'finance', 'budget', 'bill', 'payment', 'bank', 'investment', 'savings', 'expense', 'income'],
        'Personal': ['family', 'friend', 'relationship', 'hobby', 'entertainment', 'movie', 'game', 'music', 'party']
    }
    
    # Find the best matching category
    category_scores = {}
    for category, keywords in category_keywords.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        category_scores[category] = score
    
    category = max(category_scores.items(), key=lambda x: x[1])[0]
    if category_scores[category] == 0:
        category = 'Personal'  # Default category
    
    # Enhanced priority detection
    priority_keywords = {
        'Urgent': ['urgent', 'asap', 'emergency', 'immediate', 'now', 'today', 'deadline', 'critical'],
        'High': ['important', 'priority', 'high', 'essential', 'crucial', 'must', 'need'],
        'Low': ['sometime', 'when possible', 'low priority', 'optional', 'maybe', 'if time'],
        'Medium': ['normal', 'regular', 'standard']
    }
    
    priority = 'Medium'  # Default
    for p, keywords in priority_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            priority = p
            break
    
    # Date extraction using regex patterns
    date_patterns = [
        r'tomorrow',
        r'today',
        r'next week',
        r'next month',
        r'this weekend',
        r'\d{1,2}/\d{1,2}',
        r'\d{1,2}-\d{1,2}',
        r'\d{4}-\d{2}-\d{2}'
    ]
    
    due_date = None
    for pattern in date_patterns:
        if re.search(pattern, text_lower):
            due_date = "2024-12-31"  # Placeholder date
            break
    
    # Smart title extraction
    words = task_text.split()
    if len(words) <= 5:
        title = task_text
    else:
        # Take first meaningful phrase
        title = ' '.join(words[:5]) + '...'
    
    # Duration estimation based on category and keywords
    duration_keywords = {
        'quick': 0.5,
        'short': 1,
        'long': 4,
        'meeting': 1,
        'call': 0.5,
        'email': 0.25,
        'study': 2,
        'workout': 1,
        'shopping': 2
    }
    
    estimated_duration = 1  # Default 1 hour
    for keyword, hours in duration_keywords.items():
        if keyword in text_lower:
            estimated_duration = hours
            break
    
    return {
        'title': title,
        'description': task_text,
        'category': category,
        'priority': priority,
        'due_date': due_date,
        'estimated_duration': estimated_duration
    }

def predict_priority_simple(task_text):
    """Simple rule-based priority prediction"""
    urgent_keywords = ['urgent', 'asap', 'emergency', 'deadline', 'due today', 'immediate']
    high_keywords = ['important', 'critical', 'priority', 'deadline', 'meeting', 'presentation']
    low_keywords = ['sometime', 'when possible', 'low priority', 'optional']
    
    text_lower = task_text.lower()
    
    if any(keyword in text_lower for keyword in urgent_keywords):
        return 'Urgent'
    elif any(keyword in text_lower for keyword in high_keywords):
        return 'High'
    elif any(keyword in text_lower for keyword in low_keywords):
        return 'Low'
    else:
        return 'Medium'

def get_ai_suggestions():
    """Get AI-powered task suggestions with hybrid approach"""
    try:
        # Check if OpenAI API key is properly configured
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key == 'your-openai-api-key-here':
            print("OpenAI API key not configured, using enhanced fallback suggestions")
            return get_enhanced_fallback_suggestions()
        
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
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a productivity assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.7
        )
        
        result = json.loads(response.choices[0].message.content)
        print("✅ AI suggestions successful using OpenAI")
        return result
        
    except Exception as e:
        print(f"AI suggestions error: {e}")
        print("🔄 Falling back to enhanced rule-based suggestions")
        return get_enhanced_fallback_suggestions()

def get_enhanced_fallback_suggestions():
    """Enhanced fallback suggestions with variety and context awareness"""
    import random
    
    # Get current time to suggest time-appropriate tasks
    from datetime import datetime
    current_hour = datetime.now().hour
    
    # Morning suggestions (6 AM - 12 PM)
    morning_tasks = [
        {
            "title": "Plan your day ahead",
            "description": "Review your calendar, set priorities, and create a daily schedule",
            "category": "Work",
            "priority": "High",
            "reason": "Morning planning sets the tone for a productive day"
        },
        {
            "title": "Quick morning exercise",
            "description": "Do 15-20 minutes of stretching, yoga, or light cardio",
            "category": "Health",
            "priority": "Medium",
            "reason": "Morning exercise boosts energy and metabolism"
        },
        {
            "title": "Review and respond to important emails",
            "description": "Check your inbox and respond to urgent messages",
            "category": "Work",
            "priority": "High",
            "reason": "Early email management prevents backlog"
        }
    ]
    
    # Afternoon suggestions (12 PM - 6 PM)
    afternoon_tasks = [
        {
            "title": "Take a productive break",
            "description": "Step away from your desk, get fresh air, and recharge",
            "category": "Health",
            "priority": "Medium",
            "reason": "Afternoon breaks improve focus and creativity"
        },
        {
            "title": "Organize your workspace",
            "description": "Clean up your desk, organize files, and declutter",
            "category": "Personal",
            "priority": "Low",
            "reason": "A clean workspace improves productivity"
        },
        {
            "title": "Learn something new",
            "description": "Spend 30 minutes on a skill or topic of interest",
            "category": "Education",
            "priority": "Medium",
            "reason": "Continuous learning keeps your mind sharp"
        }
    ]
    
    # Evening suggestions (6 PM - 12 AM)
    evening_tasks = [
        {
            "title": "Review your day",
            "description": "Reflect on what you accomplished and plan for tomorrow",
            "category": "Personal",
            "priority": "Medium",
            "reason": "Evening reflection helps with continuous improvement"
        },
        {
            "title": "Connect with someone important",
            "description": "Call a friend, family member, or colleague",
            "category": "Personal",
            "priority": "Medium",
            "reason": "Maintaining relationships is important for well-being"
        },
        {
            "title": "Prepare for tomorrow",
            "description": "Set out clothes, prepare lunch, or organize your bag",
            "category": "Personal",
            "priority": "Low",
            "reason": "Evening preparation reduces morning stress"
        }
    ]
    
    # Universal tasks (any time)
    universal_tasks = [
        {
            "title": "Update your budget",
            "description": "Review your spending, update your budget, and track expenses",
            "category": "Finance",
            "priority": "Medium",
            "reason": "Regular financial tracking helps with money management"
        },
        {
            "title": "Read for 20 minutes",
            "description": "Pick up a book, article, or educational content",
            "category": "Education",
            "priority": "Low",
            "reason": "Reading expands knowledge and improves focus"
        },
        {
            "title": "Practice gratitude",
            "description": "Write down 3 things you're grateful for today",
            "category": "Personal",
            "priority": "Low",
            "reason": "Gratitude practice improves mental well-being"
        }
    ]
    
    # Select appropriate tasks based on time
    if 6 <= current_hour < 12:
        time_tasks = morning_tasks
    elif 12 <= current_hour < 18:
        time_tasks = afternoon_tasks
    else:
        time_tasks = evening_tasks
    
    # Combine time-appropriate tasks with universal tasks
    all_tasks = time_tasks + universal_tasks
    
    # Return 5 random tasks
    return random.sample(all_tasks, min(5, len(all_tasks)))

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
    entities = extract_entities_simple(text)
    
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    print("🚀 Starting AI Task Manager...")
    print("🤖 Features:")
    print("   - Natural language task processing")
    print("   - AI-powered task analysis")
    print("   - Smart categorization and prioritization")
    print("   - OpenAI integration")
    print("   - Real-time task management")
    print("✅ Ready to manage tasks with AI!")
    print("=" * 60)
    
    app.run(debug=True, port=5001)
