#!/usr/bin/env python3
"""
Interview Prep - ML Interview Preparation and Practice Tool
"""

import json
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging

class InterviewPrep:
    """Main class for ML interview preparation"""
    
    def __init__(self):
        self.questions_database = {}
        self.user_progress = {}
        self.practice_sessions = []
        
        # ML interview question categories
        self.categories = {
            'technical': {
                'machine_learning': 'Machine Learning Fundamentals',
                'deep_learning': 'Deep Learning & Neural Networks',
                'statistics': 'Statistics & Probability',
                'algorithms': 'Algorithms & Data Structures',
                'python': 'Python Programming',
                'data_structures': 'Data Structures',
                'system_design': 'System Design',
                'sql': 'SQL & Databases'
            },
            'behavioral': {
                'leadership': 'Leadership & Teamwork',
                'problem_solving': 'Problem Solving',
                'communication': 'Communication Skills',
                'projects': 'Project Experience',
                'challenges': 'Challenges & Failures',
                'goals': 'Career Goals'
            },
            'case_studies': {
                'ml_projects': 'ML Project Scenarios',
                'data_analysis': 'Data Analysis Cases',
                'model_optimization': 'Model Optimization',
                'business_impact': 'Business Impact Analysis'
            }
        }
        
        # Initialize question database
        self._load_questions()
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def _load_questions(self):
        """Load interview questions database"""
        self.questions_database = {
            'machine_learning': [
                {
                    'question': 'Explain the difference between supervised and unsupervised learning.',
                    'answer': 'Supervised learning uses labeled data to train models that can make predictions on new data. Unsupervised learning finds patterns in unlabeled data without predefined outputs.',
                    'difficulty': 'easy',
                    'tags': ['fundamentals', 'supervised', 'unsupervised'],
                    'follow_up': 'Can you give examples of each type?'
                },
                {
                    'question': 'What is overfitting and how do you prevent it?',
                    'answer': 'Overfitting occurs when a model learns the training data too well, including noise, leading to poor generalization. Prevention methods include: 1) More training data, 2) Regularization (L1/L2), 3) Cross-validation, 4) Early stopping, 5) Feature selection.',
                    'difficulty': 'medium',
                    'tags': ['overfitting', 'regularization', 'validation'],
                    'follow_up': 'Which regularization technique would you choose and why?'
                },
                {
                    'question': 'Explain cross-validation and its importance.',
                    'answer': 'Cross-validation is a technique to assess model performance by splitting data into multiple folds. It helps prevent overfitting and provides a more reliable estimate of model performance on unseen data.',
                    'difficulty': 'medium',
                    'tags': ['validation', 'model_evaluation'],
                    'follow_up': 'What are the different types of cross-validation?'
                }
            ],
            'deep_learning': [
                {
                    'question': 'What is backpropagation and how does it work?',
                    'answer': 'Backpropagation is an algorithm for training neural networks. It calculates gradients of the loss function with respect to weights by applying the chain rule of calculus, allowing the network to learn from errors.',
                    'difficulty': 'hard',
                    'tags': ['neural_networks', 'optimization', 'gradients'],
                    'follow_up': 'What are the vanishing and exploding gradient problems?'
                },
                {
                    'question': 'Explain the difference between CNN, RNN, and Transformer architectures.',
                    'answer': 'CNNs are designed for spatial data (images), RNNs for sequential data (text/time series), and Transformers use attention mechanisms for parallel processing of sequences.',
                    'difficulty': 'medium',
                    'tags': ['cnn', 'rnn', 'transformer', 'architectures'],
                    'follow_up': 'When would you choose each architecture?'
                }
            ],
            'statistics': [
                {
                    'question': 'What is the difference between correlation and causation?',
                    'answer': 'Correlation measures the relationship between variables, while causation implies one variable directly affects another. Correlation does not imply causation - this is a fundamental principle in statistics.',
                    'difficulty': 'easy',
                    'tags': ['statistics', 'correlation', 'causation'],
                    'follow_up': 'How would you design an experiment to establish causation?'
                },
                {
                    'question': 'Explain p-value and significance testing.',
                    'answer': 'P-value is the probability of observing data as extreme as what we saw, assuming the null hypothesis is true. A low p-value suggests the null hypothesis should be rejected.',
                    'difficulty': 'medium',
                    'tags': ['statistics', 'hypothesis_testing', 'p_value'],
                    'follow_up': 'What are Type I and Type II errors?'
                }
            ],
            'python': [
                {
                    'question': 'How would you optimize a Python function for performance?',
                    'answer': '1) Use list comprehensions, 2) Avoid global variables, 3) Use built-in functions, 4) Profile code to identify bottlenecks, 5) Use NumPy for numerical operations, 6) Consider Cython for critical sections.',
                    'difficulty': 'medium',
                    'tags': ['python', 'optimization', 'performance'],
                    'follow_up': 'Can you show me an example of vectorization?'
                },
                {
                    'question': 'Explain decorators in Python.',
                    'answer': 'Decorators are functions that modify other functions. They use the @ syntax and allow you to add functionality to existing functions without modifying their code.',
                    'difficulty': 'medium',
                    'tags': ['python', 'decorators', 'functions'],
                    'follow_up': 'Can you write a custom decorator?'
                }
            ],
            'algorithms': [
                {
                    'question': 'Explain the time complexity of common sorting algorithms.',
                    'answer': 'Bubble Sort: O(n²), Selection Sort: O(n²), Insertion Sort: O(n²), Merge Sort: O(n log n), Quick Sort: O(n log n) average, O(n²) worst case, Heap Sort: O(n log n).',
                    'difficulty': 'medium',
                    'tags': ['algorithms', 'sorting', 'complexity'],
                    'follow_up': 'When would you choose one over the others?'
                },
                {
                    'question': 'How would you find the k-th largest element in an array?',
                    'answer': '1) Sort and return k-th element: O(n log n), 2) Use QuickSelect algorithm: O(n) average, 3) Use heap: O(n log k). QuickSelect is most efficient for this problem.',
                    'difficulty': 'medium',
                    'tags': ['algorithms', 'selection', 'quickselect'],
                    'follow_up': 'Can you implement QuickSelect?'
                }
            ],
            'behavioral': [
                {
                    'question': 'Tell me about a challenging project you worked on.',
                    'answer': 'Structure: 1) Describe the project and your role, 2) Explain the challenge, 3) Detail your approach and actions, 4) Share the results and what you learned.',
                    'difficulty': 'medium',
                    'tags': ['behavioral', 'projects', 'challenges'],
                    'follow_up': 'What would you do differently next time?'
                },
                {
                    'question': 'How do you handle conflicting priorities?',
                    'answer': '1) Assess urgency and importance, 2) Communicate with stakeholders, 3) Prioritize based on business impact, 4) Delegate when possible, 5) Document decisions and rationale.',
                    'difficulty': 'easy',
                    'tags': ['behavioral', 'priorities', 'communication'],
                    'follow_up': 'Can you give me a specific example?'
                }
            ]
        }
    
    def get_questions_by_category(self, category: str, difficulty: str = None, count: int = 5) -> List[Dict]:
        """Get questions by category and difficulty"""
        if category not in self.questions_database:
            return []
        
        questions = self.questions_database[category]
        
        if difficulty:
            questions = [q for q in questions if q['difficulty'] == difficulty]
        
        # Randomly sample questions
        if len(questions) > count:
            questions = random.sample(questions, count)
        
        return questions
    
    def get_practice_session(self, categories: List[str], difficulty: str = 'mixed', count: int = 10) -> Dict:
        """Generate a practice session with questions"""
        session_questions = []
        
        for category in categories:
            if category in self.questions_database:
                category_questions = self.questions_database[category]
                
                if difficulty != 'mixed':
                    category_questions = [q for q in category_questions if q['difficulty'] == difficulty]
                
                # Sample questions from this category
                category_count = max(1, count // len(categories))
                if len(category_questions) > category_count:
                    category_questions = random.sample(category_questions, category_count)
                
                session_questions.extend(category_questions)
        
        # Shuffle questions
        random.shuffle(session_questions)
        
        session = {
            'id': f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'date': datetime.now().isoformat(),
            'categories': categories,
            'difficulty': difficulty,
            'questions': session_questions,
            'total_questions': len(session_questions),
            'completed': False,
            'score': None
        }
        
        return session
    
    def evaluate_answer(self, question: Dict, user_answer: str) -> Dict:
        """Evaluate user's answer and provide feedback"""
        # Simple keyword matching (in real implementation, would use NLP)
        correct_keywords = self._extract_keywords(question['answer'])
        user_keywords = self._extract_keywords(user_answer)
        
        # Calculate similarity score
        if correct_keywords:
            overlap = len(set(correct_keywords) & set(user_keywords))
            score = min(100, (overlap / len(correct_keywords)) * 100)
        else:
            score = 0
        
        feedback = self._generate_feedback(question, user_answer, score)
        
        return {
            'score': score,
            'feedback': feedback,
            'correct_keywords': correct_keywords,
            'missing_keywords': list(set(correct_keywords) - set(user_keywords)),
            'suggested_improvements': self._suggest_improvements(question, user_answer)
        }
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        # Simple keyword extraction (in real implementation, would use NLP)
        important_words = [
            'supervised', 'unsupervised', 'overfitting', 'regularization',
            'cross-validation', 'backpropagation', 'neural networks',
            'correlation', 'causation', 'p-value', 'decorators',
            'time complexity', 'quickselect', 'heap', 'sorting'
        ]
        
        text_lower = text.lower()
        found_keywords = [word for word in important_words if word in text_lower]
        
        return found_keywords
    
    def _generate_feedback(self, question: Dict, user_answer: str, score: float) -> str:
        """Generate personalized feedback"""
        if score >= 80:
            return "Excellent answer! You demonstrated strong understanding of the concept."
        elif score >= 60:
            return "Good answer! Consider adding more specific details and examples."
        elif score >= 40:
            return "Fair answer. Focus on the key concepts and provide concrete examples."
        else:
            return "This answer needs improvement. Review the fundamental concepts and try again."
    
    def _suggest_improvements(self, question: Dict, user_answer: str) -> List[str]:
        """Suggest specific improvements"""
        suggestions = []
        
        # Check for common issues
        if len(user_answer) < 50:
            suggestions.append("Provide more detailed explanations")
        
        if 'example' not in user_answer.lower():
            suggestions.append("Include specific examples to illustrate your points")
        
        if 'because' not in user_answer.lower() and 'why' not in user_answer.lower():
            suggestions.append("Explain the reasoning behind your answer")
        
        # Add question-specific suggestions
        if 'overfitting' in question['question'].lower():
            suggestions.append("Mention specific prevention techniques like regularization")
        
        if 'complexity' in question['question'].lower():
            suggestions.append("Include time and space complexity analysis")
        
        return suggestions
    
    def track_progress(self, user_id: str, session_id: str, results: List[Dict]):
        """Track user's interview practice progress"""
        session_data = {
            'user_id': user_id,
            'session_id': session_id,
            'date': datetime.now().isoformat(),
            'total_questions': len(results),
            'correct_answers': sum(1 for r in results if r.get('score', 0) >= 70),
            'average_score': np.mean([r.get('score', 0) for r in results]),
            'categories': list(set([r.get('category', '') for r in results])),
            'results': results
        }
        
        # Load existing progress
        try:
            with open('user_progress.json', 'r') as f:
                progress = json.load(f)
        except FileNotFoundError:
            progress = {}
        
        if user_id not in progress:
            progress[user_id] = {'sessions': [], 'stats': {}}
        
        progress[user_id]['sessions'].append(session_data)
        
        # Update statistics
        self._update_user_stats(progress[user_id], session_data)
        
        # Save progress
        with open('user_progress.json', 'w') as f:
            json.dump(progress, f, indent=2)
        
        self.logger.info(f"Progress tracked for user {user_id}, session {session_id}")
    
    def _update_user_stats(self, user_data: Dict, session_data: Dict):
        """Update user statistics"""
        sessions = user_data['sessions']
        
        if not sessions:
            return
        
        # Calculate overall statistics
        total_sessions = len(sessions)
        total_questions = sum(s['total_questions'] for s in sessions)
        total_correct = sum(s['correct_answers'] for s in sessions)
        avg_score = np.mean([s['average_score'] for s in sessions])
        
        # Category performance
        category_scores = {}
        for session in sessions:
            for result in session.get('results', []):
                category = result.get('category', 'unknown')
                score = result.get('score', 0)
                
                if category not in category_scores:
                    category_scores[category] = []
                category_scores[category].append(score)
        
        category_avg = {cat: np.mean(scores) for cat, scores in category_scores.items()}
        
        user_data['stats'] = {
            'total_sessions': total_sessions,
            'total_questions': total_questions,
            'total_correct': total_correct,
            'overall_accuracy': (total_correct / total_questions * 100) if total_questions > 0 else 0,
            'average_score': avg_score,
            'category_performance': category_avg,
            'last_session': sessions[-1]['date']
        }
    
    def get_user_progress(self, user_id: str) -> Dict:
        """Get user's progress and statistics"""
        try:
            with open('user_progress.json', 'r') as f:
                progress = json.load(f)
            
            if user_id in progress:
                return progress[user_id]
        except FileNotFoundError:
            pass
        
        return {'sessions': [], 'stats': {}}
    
    def get_study_recommendations(self, user_id: str) -> List[str]:
        """Get personalized study recommendations based on performance"""
        progress = self.get_user_progress(user_id)
        stats = progress.get('stats', {})
        
        recommendations = []
        
        if not stats:
            recommendations.append("Start with fundamental ML concepts and basic Python programming")
            return recommendations
        
        # Analyze weak areas
        category_performance = stats.get('category_performance', {})
        
        for category, score in category_performance.items():
            if score < 60:
                if category == 'machine_learning':
                    recommendations.append("Focus on ML fundamentals: supervised vs unsupervised learning, overfitting, cross-validation")
                elif category == 'deep_learning':
                    recommendations.append("Study neural network architectures, backpropagation, and activation functions")
                elif category == 'statistics':
                    recommendations.append("Review probability, hypothesis testing, and statistical concepts")
                elif category == 'python':
                    recommendations.append("Practice Python programming, data structures, and optimization techniques")
                elif category == 'algorithms':
                    recommendations.append("Study common algorithms, time complexity, and problem-solving techniques")
        
        # General recommendations
        if stats.get('average_score', 0) < 70:
            recommendations.append("Practice explaining concepts clearly and provide specific examples")
        
        if stats.get('total_sessions', 0) < 5:
            recommendations.append("Complete more practice sessions to build confidence")
        
        return recommendations
    
    def generate_mock_interview(self, user_id: str, duration: int = 60) -> Dict:
        """Generate a comprehensive mock interview"""
        # Get user's weak areas
        progress = self.get_user_progress(user_id)
        stats = progress.get('stats', {})
        category_performance = stats.get('category_performance', {})
        
        # Focus on weak areas
        weak_categories = [cat for cat, score in category_performance.items() if score < 70]
        
        if not weak_categories:
            weak_categories = ['machine_learning', 'python', 'algorithms']
        
        # Generate questions
        questions_per_category = max(2, duration // (len(weak_categories) * 10))
        mock_questions = []
        
        for category in weak_categories:
            category_questions = self.get_questions_by_category(category, count=questions_per_category)
            mock_questions.extend(category_questions)
        
        # Add behavioral questions
        behavioral_questions = self.get_questions_by_category('behavioral', count=2)
        mock_questions.extend(behavioral_questions)
        
        # Shuffle questions
        random.shuffle(mock_questions)
        
        mock_interview = {
            'id': f"mock_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'date': datetime.now().isoformat(),
            'duration': duration,
            'questions': mock_questions,
            'total_questions': len(mock_questions),
            'focus_areas': weak_categories,
            'instructions': [
                "Answer each question thoroughly",
                "Provide specific examples when possible",
                "Explain your reasoning",
                "Take your time to think before answering"
            ]
        }
        
        return mock_interview

# Example usage
if __name__ == "__main__":
    # Initialize interview prep
    prep = InterviewPrep()
    
    # Get practice session
    session = prep.get_practice_session(['machine_learning', 'python'], difficulty='medium', count=5)
    
    print("🧪 Interview Practice Session")
    print("=" * 50)
    
    for i, question in enumerate(session['questions'], 1):
        print(f"\n{i}. {question['question']}")
        print(f"   Difficulty: {question['difficulty']}")
        print(f"   Category: {list(session['categories'])}")
        
        # Simulate user answer
        user_answer = "This is a sample answer for demonstration purposes."
        evaluation = prep.evaluate_answer(question, user_answer)
        
        print(f"   Score: {evaluation['score']:.1f}%")
        print(f"   Feedback: {evaluation['feedback']}") 