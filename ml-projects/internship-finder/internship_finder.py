#!/usr/bin/env python3
"""
Internship Finder - Automated ML Internship Discovery and Application Tool
"""

import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging

class InternshipFinder:
    """Main class for finding and managing ML internships"""
    
    def __init__(self):
        self.jobs_data = []
        self.filtered_jobs = []
        self.user_profile = {}
        self.sources = {
            'linkedin': 'https://www.linkedin.com/jobs/search/',
            'indeed': 'https://www.indeed.com/jobs',
            'glassdoor': 'https://www.glassdoor.com/Job/',
            'angel_list': 'https://angel.co/jobs',
            'built_in': 'https://builtin.com/jobs'
        }
        
        # ML-specific keywords and filters
        self.ml_keywords = [
            'machine learning', 'ml', 'artificial intelligence', 'ai',
            'deep learning', 'neural networks', 'computer vision',
            'natural language processing', 'nlp', 'data science',
            'predictive modeling', 'algorithm', 'modeling',
            'tensorflow', 'pytorch', 'scikit-learn', 'pandas',
            'python', 'r', 'matlab', 'julia'
        ]
        
        self.required_skills = [
            'python', 'machine learning', 'data analysis',
            'statistics', 'sql', 'git'
        ]
        
        self.preferred_skills = [
            'tensorflow', 'pytorch', 'deep learning', 'nlp',
            'computer vision', 'aws', 'docker', 'kubernetes',
            'spark', 'hadoop', 'tableau', 'power bi'
        ]
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def set_user_profile(self, profile: Dict[str, Any]):
        """Set user profile for job matching"""
        self.user_profile = profile
        self.logger.info(f"User profile set: {profile.get('name', 'Unknown')}")
    
    def scrape_linkedin_jobs(self, keywords: str = "machine learning intern", location: str = "remote", limit: int = 50) -> List[Dict]:
        """Scrape LinkedIn jobs (simulated - in real implementation would use API)"""
        self.logger.info(f"Scraping LinkedIn jobs for: {keywords}")
        
        # Simulate job data (in real implementation, this would scrape actual LinkedIn)
        simulated_jobs = [
            {
                'title': 'Machine Learning Intern',
                'company': 'TechCorp AI',
                'location': 'Remote',
                'description': 'Join our ML team working on computer vision and NLP projects. Requirements: Python, TensorFlow, strong math background.',
                'salary': '$25-35/hour',
                'posted_date': '2024-01-15',
                'application_url': 'https://linkedin.com/jobs/view/123',
                'source': 'LinkedIn',
                'skills_required': ['python', 'tensorflow', 'machine learning'],
                'experience_level': 'Intern',
                'remote_friendly': True
            },
            {
                'title': 'AI Research Intern',
                'company': 'Innovation Labs',
                'location': 'San Francisco, CA',
                'description': 'Research position in deep learning and neural networks. Work on cutting-edge AI projects.',
                'salary': '$30-40/hour',
                'posted_date': '2024-01-14',
                'application_url': 'https://linkedin.com/jobs/view/124',
                'source': 'LinkedIn',
                'skills_required': ['python', 'pytorch', 'deep learning', 'research'],
                'experience_level': 'Intern',
                'remote_friendly': False
            },
            {
                'title': 'Data Science Intern',
                'company': 'Analytics Pro',
                'location': 'Remote',
                'description': 'Build predictive models and analyze large datasets. Experience with pandas, scikit-learn required.',
                'salary': '$20-30/hour',
                'posted_date': '2024-01-13',
                'application_url': 'https://linkedin.com/jobs/view/125',
                'source': 'LinkedIn',
                'skills_required': ['python', 'pandas', 'scikit-learn', 'sql'],
                'experience_level': 'Intern',
                'remote_friendly': True
            }
        ]
        
        return simulated_jobs
    
    def scrape_indeed_jobs(self, keywords: str = "machine learning intern", location: str = "remote", limit: int = 50) -> List[Dict]:
        """Scrape Indeed jobs (simulated)"""
        self.logger.info(f"Scraping Indeed jobs for: {keywords}")
        
        simulated_jobs = [
            {
                'title': 'ML Engineering Intern',
                'company': 'StartupAI',
                'location': 'New York, NY',
                'description': 'Build and deploy machine learning models. Work with real-world data and production systems.',
                'salary': '$28-38/hour',
                'posted_date': '2024-01-15',
                'application_url': 'https://indeed.com/jobs/view/456',
                'source': 'Indeed',
                'skills_required': ['python', 'machine learning', 'aws', 'docker'],
                'experience_level': 'Intern',
                'remote_friendly': True
            },
            {
                'title': 'Computer Vision Intern',
                'company': 'VisionTech',
                'location': 'Austin, TX',
                'description': 'Develop computer vision algorithms for autonomous systems. Experience with OpenCV and deep learning frameworks.',
                'salary': '$32-42/hour',
                'posted_date': '2024-01-14',
                'application_url': 'https://indeed.com/jobs/view/457',
                'source': 'Indeed',
                'skills_required': ['python', 'opencv', 'tensorflow', 'computer vision'],
                'experience_level': 'Intern',
                'remote_friendly': False
            }
        ]
        
        return simulated_jobs
    
    def scrape_glassdoor_jobs(self, keywords: str = "machine learning intern", location: str = "remote", limit: int = 50) -> List[Dict]:
        """Scrape Glassdoor jobs (simulated)"""
        self.logger.info(f"Scraping Glassdoor jobs for: {keywords}")
        
        simulated_jobs = [
            {
                'title': 'AI/ML Intern',
                'company': 'Fortune 500 Tech',
                'location': 'Seattle, WA',
                'description': 'Join our AI team working on large-scale machine learning projects. Competitive salary and benefits.',
                'salary': '$35-45/hour',
                'posted_date': '2024-01-15',
                'application_url': 'https://glassdoor.com/jobs/view/789',
                'source': 'Glassdoor',
                'skills_required': ['python', 'machine learning', 'big data', 'cloud computing'],
                'experience_level': 'Intern',
                'remote_friendly': True
            }
        ]
        
        return simulated_jobs
    
    def scrape_all_sources(self, keywords: str = "machine learning intern", location: str = "remote", limit: int = 50) -> List[Dict]:
        """Scrape jobs from all sources"""
        all_jobs = []
        
        # Scrape from different sources
        sources = [
            self.scrape_linkedin_jobs,
            self.scrape_indeed_jobs,
            self.scrape_glassdoor_jobs
        ]
        
        for source_func in sources:
            try:
                jobs = source_func(keywords, location, limit)
                all_jobs.extend(jobs)
                time.sleep(1)  # Be respectful to servers
            except Exception as e:
                self.logger.error(f"Error scraping {source_func.__name__}: {e}")
        
        self.jobs_data = all_jobs
        self.logger.info(f"Total jobs scraped: {len(all_jobs)}")
        return all_jobs
    
    def filter_jobs(self, filters: Dict[str, Any] = None) -> List[Dict]:
        """Filter jobs based on criteria"""
        if not filters:
            filters = {
                'remote_only': False,  # Changed to False to be less restrictive
                'min_salary': 15,      # Lowered minimum salary
                'max_salary': 50,
                'required_skills': [],  # Made skills optional for filtering
                'preferred_skills': self.preferred_skills,
                'experience_level': 'Intern'
            }
        
        filtered_jobs = []
        
        for job in self.jobs_data:
            # Check if job matches filters
            if self._job_matches_filters(job, filters):
                # Calculate match score
                match_score = self._calculate_match_score(job)
                job['match_score'] = match_score
                filtered_jobs.append(job)
        
        # Sort by match score
        filtered_jobs.sort(key=lambda x: x['match_score'], reverse=True)
        self.filtered_jobs = filtered_jobs
        
        self.logger.info(f"Filtered jobs: {len(filtered_jobs)} out of {len(self.jobs_data)}")
        return filtered_jobs
    
    def _job_matches_filters(self, job: Dict, filters: Dict) -> bool:
        """Check if job matches given filters"""
        # Remote filter - only apply if remote_only is True
        if filters.get('remote_only') and not job.get('remote_friendly'):
            return False
        
        # Salary filter - only apply if salary is specified
        salary_range = job.get('salary', '')
        if 'min_salary' in filters or 'max_salary' in filters:
            # Extract numeric salary (simplified)
            salary_match = re.search(r'\$(\d+)', salary_range)
            if salary_match:
                salary = int(salary_match.group(1))
                if 'min_salary' in filters and salary < filters['min_salary']:
                    return False
                if 'max_salary' in filters and salary > filters['max_salary']:
                    return False
        
        # Skills filter - only apply if required_skills is not empty
        if filters.get('required_skills') and len(filters['required_skills']) > 0:
            job_skills = set(job.get('skills_required', []))
            required_skills = set(filters['required_skills'])
            if not required_skills.issubset(job_skills):
                return False
        
        return True
    
    def _calculate_match_score(self, job: Dict) -> float:
        """Calculate how well a job matches user profile"""
        score = 0.0
        
        # Skills match
        user_skills = set(self.user_profile.get('skills', []))
        job_skills = set(job.get('skills_required', []))
        
        # Required skills match
        required_match = len(user_skills.intersection(job_skills))
        score += required_match * 10
        
        # Preferred skills bonus
        preferred_skills = set(self.preferred_skills)
        preferred_match = len(user_skills.intersection(preferred_skills))
        score += preferred_match * 5
        
        # Location preference
        if self.user_profile.get('preferred_location') == job.get('location'):
            score += 20
        
        # Remote preference
        if self.user_profile.get('remote_preferred') and job.get('remote_friendly'):
            score += 15
        
        # Salary preference
        salary_range = job.get('salary', '')
        salary_match = re.search(r'\$(\d+)', salary_range)
        if salary_match:
            salary = int(salary_match.group(1))
            user_min_salary = self.user_profile.get('min_salary', 0)
            if salary >= user_min_salary:
                score += 10
        
        return score
    
    def generate_application_tips(self, job: Dict) -> Dict[str, Any]:
        """Generate personalized application tips for a job"""
        tips = {
            'resume_tips': [],
            'cover_letter_tips': [],
            'interview_prep': [],
            'skill_gaps': []
        }
        
        # Analyze skill gaps
        user_skills = set(self.user_profile.get('skills', []))
        job_skills = set(job.get('skills_required', []))
        missing_skills = job_skills - user_skills
        
        if missing_skills:
            tips['skill_gaps'] = list(missing_skills)
            tips['resume_tips'].append(f"Highlight any related experience with: {', '.join(missing_skills)}")
            tips['cover_letter_tips'].append(f"Address how you plan to learn: {', '.join(missing_skills)}")
        
        # Resume tips
        tips['resume_tips'].extend([
            "Quantify your ML project results (accuracy, performance improvements)",
            "Include links to your GitHub portfolio with the 4 ML projects",
            "Highlight any relevant coursework or certifications",
            "Use action verbs: 'Developed', 'Implemented', 'Optimized'"
        ])
        
        # Cover letter tips
        tips['cover_letter_tips'].extend([
            f"Show enthusiasm for {job['company']}'s specific work",
            "Mention your relevant projects and their business impact",
            "Explain why you're interested in this specific role",
            "Demonstrate your learning ability and growth mindset"
        ])
        
        # Interview prep
        tips['interview_prep'].extend([
            "Prepare to discuss your ML projects in detail",
            "Practice explaining technical concepts clearly",
            "Research the company's recent ML/AI initiatives",
            "Prepare questions about the team and projects"
        ])
        
        return tips
    
    def track_application(self, job: Dict, status: str = "applied", notes: str = ""):
        """Track application status"""
        application = {
            'job_id': job.get('title', '') + '_' + job.get('company', ''),
            'job_title': job.get('title', ''),
            'company': job.get('company', ''),
            'application_date': datetime.now().strftime('%Y-%m-%d'),
            'status': status,
            'notes': notes,
            'application_url': job.get('application_url', ''),
            'match_score': job.get('match_score', 0)
        }
        
        # Save to file (in real implementation, would use database)
        try:
            with open('applications.json', 'r') as f:
                applications = json.load(f)
        except FileNotFoundError:
            applications = []
        
        applications.append(application)
        
        with open('applications.json', 'w') as f:
            json.dump(applications, f, indent=2)
        
        self.logger.info(f"Application tracked: {job.get('title')} at {job.get('company')}")
    
    def get_application_stats(self) -> Dict[str, Any]:
        """Get application statistics"""
        try:
            with open('applications.json', 'r') as f:
                applications = json.load(f)
        except FileNotFoundError:
            return {
                'total_applications': 0,
                'status_breakdown': {},
                'avg_match_score': 0,
                'top_companies': []
            }
        
        stats = {
            'total_applications': len(applications),
            'status_breakdown': {},
            'avg_match_score': 0,
            'top_companies': []
        }
        
        if applications:
            # Status breakdown
            for app in applications:
                status = app.get('status', 'unknown')
                stats['status_breakdown'][status] = stats['status_breakdown'].get(status, 0) + 1
            
            # Average match score
            scores = [app.get('match_score', 0) for app in applications]
            stats['avg_match_score'] = sum(scores) / len(scores)
            
            # Top companies
            companies = [app.get('company', '') for app in applications]
            company_counts = {}
            for company in companies:
                company_counts[company] = company_counts.get(company, 0) + 1
            
            stats['top_companies'] = sorted(company_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return stats
    
    def export_jobs_to_csv(self, filename: str = "ml_internships.csv"):
        """Export filtered jobs to CSV"""
        if not self.filtered_jobs:
            self.logger.warning("No filtered jobs to export")
            return
        
        df = pd.DataFrame(self.filtered_jobs)
        df.to_csv(filename, index=False)
        self.logger.info(f"Jobs exported to {filename}")
    
    def get_job_recommendations(self, limit: int = 10) -> List[Dict]:
        """Get personalized job recommendations"""
        if not self.filtered_jobs:
            return []
        
        # Sort by match score and return top recommendations
        recommendations = sorted(self.filtered_jobs, key=lambda x: x.get('match_score', 0), reverse=True)
        return recommendations[:limit]

# Example usage
if __name__ == "__main__":
    # Initialize finder
    finder = InternshipFinder()
    
    # Set user profile
    user_profile = {
        'name': 'Segni Mekonnen',
        'skills': ['python', 'machine learning', 'tensorflow', 'pandas', 'scikit-learn', 'git'],
        'preferred_location': 'Remote',
        'remote_preferred': True,
        'min_salary': 20,
        'experience_level': 'Intern'
    }
    finder.set_user_profile(user_profile)
    
    # Scrape jobs
    print("🔍 Scraping ML internships...")
    jobs = finder.scrape_all_sources("machine learning intern", "remote", 50)
    
    # Filter jobs
    print("🎯 Filtering jobs...")
    filtered_jobs = finder.filter_jobs()
    
    # Show top recommendations
    print("\n🏆 Top Job Recommendations:")
    for i, job in enumerate(filtered_jobs[:5], 1):
        print(f"\n{i}. {job['title']} at {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   Salary: {job['salary']}")
        print(f"   Match Score: {job.get('match_score', 0):.1f}")
        print(f"   Skills: {', '.join(job.get('skills_required', []))}")
    
    # Export to CSV
    finder.export_jobs_to_csv()
    
    print(f"\n✅ Found {len(filtered_jobs)} matching internships!")
    print("📊 Check 'ml_internships.csv' for full list") 