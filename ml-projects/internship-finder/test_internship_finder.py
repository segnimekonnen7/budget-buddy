#!/usr/bin/env python3
"""
Comprehensive test script for internship finder
"""

from internship_finder import InternshipFinder
import json
import os

def test_internship_finder():
    """Test the internship finder functionality"""
    print("Initializing Internship Finder...")
    finder = InternshipFinder()
    
    # Test 1: Set user profile
    print("\n" + "="*60)
    print("TEST 1: USER PROFILE SETTING")
    print("="*60)
    
    test_profiles = [
        {
            'name': 'Segni Mekonnen',
            'skills': ['python', 'machine learning', 'tensorflow', 'pandas', 'scikit-learn', 'git'],
            'preferred_location': 'Remote',
            'remote_preferred': True,
            'min_salary': 20,
            'experience_level': 'Intern'
        },
        {
            'name': 'Test User',
            'skills': ['python', 'deep learning', 'pytorch', 'nlp'],
            'preferred_location': 'San Francisco',
            'remote_preferred': False,
            'min_salary': 30,
            'experience_level': 'Intern'
        }
    ]
    
    for i, profile in enumerate(test_profiles, 1):
        finder.set_user_profile(profile)
        print(f"✓ Profile {i} set: {profile['name']} with {len(profile['skills'])} skills")
    
    # Test 2: Job scraping
    print("\n" + "="*60)
    print("TEST 2: JOB SCRAPING")
    print("="*60)
    
    test_keywords = ["machine learning intern", "ai intern", "data science intern"]
    test_locations = ["remote", "san francisco", "new york"]
    
    for keyword in test_keywords:
        for location in test_locations:
            jobs = finder.scrape_all_sources(keyword, location, 10)
            print(f"✓ Scraped {len(jobs)} jobs for '{keyword}' in '{location}'")
    
    # Test 3: Job filtering
    print("\n" + "="*60)
    print("TEST 3: JOB FILTERING")
    print("="*60)
    
    # Test different filter combinations
    filter_tests = [
        {'remote_only': True, 'min_salary': 20},
        {'remote_only': False, 'min_salary': 15},
        {'required_skills': ['python', 'machine learning']},
        {'required_skills': []}
    ]
    
    for i, filters in enumerate(filter_tests, 1):
        filtered_jobs = finder.filter_jobs(filters)
        print(f"✓ Filter test {i}: {len(filtered_jobs)} jobs with filters {filters}")
    
    # Test 4: Match score calculation
    print("\n" + "="*60)
    print("TEST 4: MATCH SCORE CALCULATION")
    print("="*60)
    
    # Set a specific profile for testing
    finder.set_user_profile(test_profiles[0])
    jobs = finder.scrape_all_sources("machine learning intern", "remote", 5)
    filtered_jobs = finder.filter_jobs()
    
    for i, job in enumerate(filtered_jobs[:3], 1):
        match_score = job.get('match_score', 0)
        print(f"✓ Job {i}: {job['title']} at {job['company']} - Match Score: {match_score:.1f}")
    
    # Test 5: Application tips generation
    print("\n" + "="*60)
    print("TEST 5: APPLICATION TIPS GENERATION")
    print("="*60)
    
    if filtered_jobs:
        job = filtered_jobs[0]
        tips = finder.generate_application_tips(job)
        
        print(f"✓ Generated tips for: {job['title']} at {job['company']}")
        print(f"  - Resume tips: {len(tips['resume_tips'])}")
        print(f"  - Cover letter tips: {len(tips['cover_letter_tips'])}")
        print(f"  - Interview prep: {len(tips['interview_prep'])}")
        print(f"  - Skill gaps: {len(tips['skill_gaps'])}")
    
    # Test 6: Application tracking
    print("\n" + "="*60)
    print("TEST 6: APPLICATION TRACKING")
    print("="*60)
    
    if filtered_jobs:
        # Track a few applications
        for i, job in enumerate(filtered_jobs[:2], 1):
            status = "applied" if i == 1 else "interviewing"
            notes = f"Test application {i}"
            finder.track_application(job, status, notes)
            print(f"✓ Tracked application {i}: {job['title']} - Status: {status}")
        
        # Get application stats
        stats = finder.get_application_stats()
        print(f"✓ Application stats: {stats['total_applications']} total applications")
        print(f"  - Status breakdown: {stats['status_breakdown']}")
        print(f"  - Average match score: {stats['avg_match_score']:.1f}")
    
    # Test 7: Job recommendations
    print("\n" + "="*60)
    print("TEST 7: JOB RECOMMENDATIONS")
    print("="*60)
    
    recommendations = finder.get_job_recommendations(5)
    print(f"✓ Generated {len(recommendations)} job recommendations")
    
    for i, job in enumerate(recommendations[:3], 1):
        print(f"  {i}. {job['title']} at {job['company']} (Score: {job.get('match_score', 0):.1f})")
    
    # Test 8: CSV export
    print("\n" + "="*60)
    print("TEST 8: CSV EXPORT")
    print("="*60)
    
    test_filename = "test_internships.csv"
    finder.export_jobs_to_csv(test_filename)
    
    if os.path.exists(test_filename):
        print(f"✓ Successfully exported jobs to {test_filename}")
        # Clean up test file
        os.remove(test_filename)
        print(f"✓ Cleaned up test file {test_filename}")
    else:
        print(f"✗ Failed to export jobs to {test_filename}")
    
    # Test 9: Edge cases
    print("\n" + "="*60)
    print("TEST 9: EDGE CASES")
    print("="*60)
    
    # Test with empty job data
    finder.jobs_data = []
    empty_filtered = finder.filter_jobs()
    print(f"✓ Empty job data handling: {len(empty_filtered)} jobs")
    
    # Test with no user profile
    finder.user_profile = {}
    no_profile_jobs = finder.scrape_all_sources("test", "remote", 2)
    no_profile_filtered = finder.filter_jobs()
    print(f"✓ No profile handling: {len(no_profile_filtered)} jobs")
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("="*60)

if __name__ == "__main__":
    test_internship_finder() 