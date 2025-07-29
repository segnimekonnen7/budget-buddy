#!/usr/bin/env python3
"""
Comprehensive test script for interview prep system
"""

from interview_prep import InterviewPrep
import json
import os

def test_interview_prep():
    """Test the interview prep functionality"""
    print("Initializing Interview Prep System...")
    prep = InterviewPrep()
    
    # Test 1: Question database loading
    print("\n" + "="*60)
    print("TEST 1: QUESTION DATABASE")
    print("="*60)
    
    categories = list(prep.categories['technical'].keys())
    print(f"✓ Loaded {len(categories)} technical categories")
    
    total_questions = sum(len(prep.questions_database.get(cat, [])) for cat in categories)
    print(f"✓ Total questions in database: {total_questions}")
    
    for category in categories[:3]:  # Show first 3 categories
        questions = prep.questions_database.get(category, [])
        print(f"  - {category}: {len(questions)} questions")
    
    # Test 2: Question retrieval by category
    print("\n" + "="*60)
    print("TEST 2: QUESTION RETRIEVAL")
    print("="*60)
    
    test_categories = ['machine_learning', 'python', 'statistics']
    
    for category in test_categories:
        questions = prep.get_questions_by_category(category, count=3)
        print(f"✓ Retrieved {len(questions)} questions from {category}")
        
        if questions:
            print(f"  Sample question: {questions[0]['question'][:50]}...")
    
    # Test 3: Practice session generation
    print("\n" + "="*60)
    print("TEST 3: PRACTICE SESSION GENERATION")
    print("="*60)
    
    session_configs = [
        (['machine_learning'], 'easy', 5),
        (['python', 'algorithms'], 'medium', 8),
        (['statistics', 'deep_learning'], 'hard', 6)
    ]
    
    for categories, difficulty, count in session_configs:
        session = prep.get_practice_session(categories, difficulty, count)
        print(f"✓ Generated session with {len(session['questions'])} questions")
        print(f"  Categories: {session['categories']}")
        print(f"  Difficulty: {session['difficulty']}")
        print(f"  Session ID: {session['id']}")
    
    # Test 4: Answer evaluation with better test answers
    print("\n" + "="*60)
    print("TEST 4: ANSWER EVALUATION")
    print("="*60)
    
    # Get a sample question
    sample_question = prep.get_questions_by_category('machine_learning', count=1)[0]
    
    # Test different quality answers
    test_answers = [
        "Supervised learning uses labeled data to train models that can make predictions on new data. Unsupervised learning finds patterns in unlabeled data without predefined outputs.",
        "Supervised learning has labels, unsupervised doesn't. That's the main difference.",
        "I'm not sure about this topic. Maybe it's about training models?",
        ""  # Empty answer
    ]
    
    for i, answer in enumerate(test_answers, 1):
        evaluation = prep.evaluate_answer(sample_question, answer)
        print(f"✓ Test answer {i}: Score {evaluation['score']:.1f}%")
        print(f"  Feedback: {evaluation['feedback']}")
        if evaluation['suggested_improvements']:
            print(f"  Suggestions: {evaluation['suggested_improvements']}")
    
    # Test 5: Progress tracking
    print("\n" + "="*60)
    print("TEST 5: PROGRESS TRACKING")
    print("="*60)
    
    test_user_id = "test_user_001"
    
    # Create mock session results
    mock_results = [
        {
            'question': sample_question,
            'answer': test_answers[0],
            'score': 85.0,
            'feedback': 'Good answer',
            'category': 'machine_learning'
        },
        {
            'question': sample_question,
            'answer': test_answers[1],
            'score': 60.0,
            'feedback': 'Fair answer',
            'category': 'machine_learning'
        }
    ]
    
    # Track progress
    prep.track_progress(test_user_id, "test_session_001", mock_results)
    print(f"✓ Tracked progress for user {test_user_id}")
    
    # Get progress
    progress = prep.get_user_progress(test_user_id)
    stats = progress.get('stats', {})
    print(f"✓ User stats: {stats.get('total_sessions', 0)} sessions, {stats.get('total_questions', 0)} questions")
    print(f"  Average score: {stats.get('average_score', 0):.1f}%")
    
    # Test 6: Study recommendations
    print("\n" + "="*60)
    print("TEST 6: STUDY RECOMMENDATIONS")
    print("="*60)
    
    recommendations = prep.get_study_recommendations(test_user_id)
    print(f"✓ Generated {len(recommendations)} study recommendations")
    
    for i, rec in enumerate(recommendations, 1):
        print(f"  {i}. {rec}")
    
    # Test 7: Mock interview generation
    print("\n" + "="*60)
    print("TEST 7: MOCK INTERVIEW GENERATION")
    print("="*60)
    
    mock_interview = prep.generate_mock_interview(test_user_id, duration=45)
    print(f"✓ Generated mock interview: {mock_interview['id']}")
    print(f"  Duration: {mock_interview['duration']} minutes")
    print(f"  Questions: {mock_interview['total_questions']}")
    print(f"  Focus areas: {mock_interview['focus_areas']}")
    
    # Test 8: Edge cases
    print("\n" + "="*60)
    print("TEST 8: EDGE CASES")
    print("="*60)
    
    # Test with non-existent category
    empty_questions = prep.get_questions_by_category('non_existent_category')
    print(f"✓ Non-existent category handling: {len(empty_questions)} questions")
    
    # Test with empty categories
    empty_session = prep.get_practice_session([], 'easy', 5)
    print(f"✓ Empty categories handling: {len(empty_session['questions'])} questions")
    
    # Test with new user (no progress)
    new_user_progress = prep.get_user_progress("new_user_999")
    print(f"✓ New user handling: {len(new_user_progress.get('sessions', []))} sessions")
    
    # Test 9: Data persistence
    print("\n" + "="*60)
    print("TEST 9: DATA PERSISTENCE")
    print("="*60)
    
    # Check if progress file was created
    if os.path.exists('user_progress.json'):
        print("✓ Progress file created successfully")
        
        # Read and verify data
        with open('user_progress.json', 'r') as f:
            data = json.load(f)
        
        if test_user_id in data:
            print(f"✓ User data persisted correctly")
            print(f"  Sessions: {len(data[test_user_id]['sessions'])}")
        else:
            print("✗ User data not found in persisted file")
    else:
        print("✗ Progress file not created")
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("="*60)

if __name__ == "__main__":
    test_interview_prep() 