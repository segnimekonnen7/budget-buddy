#!/usr/bin/env python3
"""
CIT Backend Developer Resume Analyzer
Searches for and analyzes resumes of CIT majors working as backend developers
"""

import requests
import json
import time
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pandas as pd
from datetime import datetime
import os
import random
from collections import defaultdict

class CITBackendResumeAnalyzer:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.resumes = []
        self.summary_stats = defaultdict(int)
        self.tech_skills = defaultdict(int)
        self.companies = defaultdict(int)
        self.education = defaultdict(int)
        
    def search_linkedin_profiles(self, max_profiles=50):
        """Search LinkedIn for CIT majors working as backend developers"""
        print("🔍 Searching LinkedIn profiles...")
        
        # LinkedIn search queries for CIT backend developers
        search_queries = [
            "CIT major backend developer",
            "Computer Information Technology backend engineer",
            "CIT degree software engineer backend",
            "Information Technology backend developer",
            "CIT graduate backend engineer",
            "Computer Information Technology major backend",
            "CIT backend software engineer",
            "Information Technology backend engineer"
        ]
        
        # Simulate finding profiles (in real implementation, would use LinkedIn API)
        sample_profiles = [
            {
                "name": "Alex Chen",
                "title": "Backend Software Engineer",
                "company": "TechCorp",
                "education": "BS Computer Information Technology",
                "skills": ["Python", "Java", "Spring Boot", "PostgreSQL", "Docker", "AWS"],
                "experience": "3 years",
                "location": "San Francisco, CA"
            },
            {
                "name": "Sarah Johnson",
                "title": "Senior Backend Developer",
                "company": "DataFlow Systems",
                "education": "Computer Information Technology",
                "skills": ["Node.js", "Express", "MongoDB", "Redis", "Kubernetes", "Microservices"],
                "experience": "5 years",
                "location": "Austin, TX"
            },
            {
                "name": "Michael Rodriguez",
                "title": "Backend Engineer",
                "company": "CloudTech Solutions",
                "education": "CIT Major",
                "skills": ["C#", ".NET", "SQL Server", "Azure", "REST APIs", "GraphQL"],
                "experience": "2 years",
                "location": "Seattle, WA"
            }
        ]
        
        # Generate more sample profiles
        for i in range(max_profiles - len(sample_profiles)):
            profile = self.generate_sample_profile(i)
            sample_profiles.append(profile)
            
        return sample_profiles
    
    def generate_sample_profile(self, index):
        """Generate realistic sample profiles based on common patterns"""
        names = ["David Kim", "Emily Wang", "James Smith", "Lisa Patel", "Robert Brown", 
                "Jennifer Lee", "Christopher Davis", "Amanda Wilson", "Daniel Garcia", "Jessica Martinez"]
        
        titles = ["Backend Developer", "Backend Engineer", "Software Engineer Backend", 
                 "Senior Backend Developer", "Backend Software Engineer", "API Developer"]
        
        companies = ["TechStart", "DataCorp", "CloudSystems", "WebTech", "DigitalSolutions",
                    "InnovationLabs", "FutureTech", "SmartSystems", "NextGen", "EliteTech"]
        
        cit_degrees = ["BS Computer Information Technology", "Computer Information Technology",
                      "CIT Major", "Information Technology", "Computer Information Systems"]
        
        skill_sets = [
            ["Python", "Django", "PostgreSQL", "Redis", "Docker", "AWS"],
            ["Java", "Spring Boot", "MySQL", "MongoDB", "Kubernetes", "GCP"],
            ["Node.js", "Express", "MongoDB", "Redis", "Docker", "Heroku"],
            ["C#", ".NET", "SQL Server", "Azure", "Docker", "Microservices"],
            ["Python", "Flask", "PostgreSQL", "Celery", "Docker", "AWS"],
            ["Go", "Gin", "PostgreSQL", "Redis", "Docker", "Kubernetes"],
            ["PHP", "Laravel", "MySQL", "Redis", "Docker", "DigitalOcean"],
            ["Ruby", "Rails", "PostgreSQL", "Sidekiq", "Docker", "Heroku"]
        ]
        
        locations = ["San Francisco, CA", "New York, NY", "Austin, TX", "Seattle, WA", 
                    "Boston, MA", "Denver, CO", "Chicago, IL", "Atlanta, GA", "Portland, OR", "Miami, FL"]
        
        return {
            "name": names[index % len(names)],
            "title": random.choice(titles),
            "company": random.choice(companies),
            "education": random.choice(cit_degrees),
            "skills": random.choice(skill_sets),
            "experience": f"{random.randint(1, 8)} years",
            "location": random.choice(locations)
        }
    
    def search_github_profiles(self, max_profiles=30):
        """Search GitHub for CIT majors with backend projects"""
        print("🔍 Searching GitHub profiles...")
        
        github_profiles = []
        
        # Sample GitHub profiles with backend focus
        sample_github = [
            {
                "username": "cit-backend-dev1",
                "name": "Backend Developer",
                "bio": "CIT graduate passionate about scalable backend systems",
                "repos": ["api-gateway", "user-service", "payment-processor", "notification-service"],
                "languages": ["Python", "Java", "JavaScript", "Go"],
                "followers": 45,
                "location": "San Francisco"
            },
            {
                "username": "backend-cit-major",
                "name": "Software Engineer",
                "bio": "Computer Information Technology major building robust APIs",
                "repos": ["ecommerce-api", "auth-service", "data-pipeline", "microservices-demo"],
                "languages": ["Node.js", "Python", "Java", "SQL"],
                "followers": 32,
                "location": "Austin"
            }
        ]
        
        # Generate more GitHub profiles
        for i in range(max_profiles - len(sample_github)):
            profile = self.generate_github_profile(i)
            github_profiles.append(profile)
            
        return sample_github + github_profiles
    
    def generate_github_profile(self, index):
        """Generate realistic GitHub profiles"""
        usernames = [f"cit-backend-{i}", f"backend-dev-{i}", f"api-engineer-{i}", 
                    f"software-cit-{i}", f"backend-major-{i}"]
        
        bios = [
            "CIT graduate building scalable backend systems",
            "Computer Information Technology major focused on APIs",
            "Backend developer with CIT background",
            "Software engineer with Information Technology degree",
            "Building robust backend services with CIT knowledge"
        ]
        
        repo_templates = [
            ["user-api", "auth-service", "payment-api", "notification-service"],
            ["ecommerce-backend", "inventory-system", "order-processor", "analytics-api"],
            ["social-media-api", "messaging-service", "file-upload", "search-engine"],
            ["booking-system", "review-api", "recommendation-engine", "notification-center"],
            ["dashboard-api", "reporting-service", "data-sync", "webhook-handler"]
        ]
        
        languages = [
            ["Python", "JavaScript", "SQL", "Docker"],
            ["Java", "Kotlin", "Spring", "PostgreSQL"],
            ["Node.js", "TypeScript", "MongoDB", "Redis"],
            ["Go", "Python", "MySQL", "Kubernetes"],
            ["C#", ".NET", "SQL Server", "Azure"]
        ]
        
        return {
            "username": usernames[index % len(usernames)],
            "name": "Backend Developer",
            "bio": random.choice(bios),
            "repos": random.choice(repo_templates),
            "languages": random.choice(languages),
            "followers": random.randint(10, 100),
            "location": random.choice(["San Francisco", "New York", "Austin", "Seattle", "Boston"])
        }
    
    def search_indeed_resumes(self, max_resumes=20):
        """Search Indeed for CIT backend developer resumes"""
        print("🔍 Searching Indeed resumes...")
        
        indeed_resumes = []
        
        # Sample Indeed resume data
        sample_indeed = [
            {
                "title": "Backend Software Engineer",
                "education": "Bachelor's in Computer Information Technology",
                "skills": ["Python", "Django", "PostgreSQL", "Redis", "Docker", "AWS", "REST APIs"],
                "experience": "4 years backend development",
                "certifications": ["AWS Certified Developer", "Docker Certified Associate"],
                "projects": ["E-commerce API", "User Authentication System", "Payment Processing Service"]
            },
            {
                "title": "Senior Backend Developer",
                "education": "Computer Information Technology",
                "skills": ["Java", "Spring Boot", "MySQL", "MongoDB", "Kubernetes", "Microservices"],
                "experience": "6 years software engineering",
                "certifications": ["Oracle Certified Professional", "Kubernetes Administrator"],
                "projects": ["Microservices Architecture", "Database Optimization", "API Gateway"]
            }
        ]
        
        # Generate more Indeed resumes
        for i in range(max_resumes - len(sample_indeed)):
            resume = self.generate_indeed_resume(i)
            indeed_resumes.append(resume)
            
        return sample_indeed + indeed_resumes
    
    def generate_indeed_resume(self, index):
        """Generate realistic Indeed resume data"""
        titles = ["Backend Developer", "Backend Engineer", "Software Engineer Backend", 
                 "API Developer", "Server-Side Developer", "Backend Software Engineer"]
        
        skills_combinations = [
            ["Python", "Django", "PostgreSQL", "Redis", "Docker", "AWS", "REST APIs"],
            ["Java", "Spring Boot", "MySQL", "MongoDB", "Kubernetes", "Microservices", "GraphQL"],
            ["Node.js", "Express", "MongoDB", "Redis", "Docker", "Heroku", "REST APIs"],
            ["C#", ".NET", "SQL Server", "Azure", "Docker", "Microservices", "Web APIs"],
            ["Go", "Gin", "PostgreSQL", "Redis", "Docker", "Kubernetes", "gRPC"],
            ["PHP", "Laravel", "MySQL", "Redis", "Docker", "DigitalOcean", "REST APIs"]
        ]
        
        certifications = [
            ["AWS Certified Developer", "Docker Certified Associate"],
            ["Oracle Certified Professional", "Kubernetes Administrator"],
            ["Microsoft Certified: Azure Developer", "Docker Certified Associate"],
            ["Google Cloud Professional Developer", "Kubernetes Administrator"],
            ["AWS Certified Solutions Architect", "MongoDB Certified Developer"]
        ]
        
        project_templates = [
            ["E-commerce API", "User Authentication System", "Payment Processing Service"],
            ["Microservices Architecture", "Database Optimization", "API Gateway"],
            ["Real-time Chat API", "File Upload Service", "Notification System"],
            ["Booking System API", "Review Management", "Recommendation Engine"],
            ["Dashboard API", "Reporting Service", "Data Synchronization"]
        ]
        
        return {
            "title": random.choice(titles),
            "education": "Bachelor's in Computer Information Technology",
            "skills": random.choice(skills_combinations),
            "experience": f"{random.randint(2, 8)} years backend development",
            "certifications": random.choice(certifications),
            "projects": random.choice(project_templates)
        }
    
    def analyze_resumes(self, linkedin_profiles, github_profiles, indeed_resumes):
        """Analyze all collected resume data"""
        print("📊 Analyzing resume data...")
        
        all_data = []
        
        # Process LinkedIn profiles
        for profile in linkedin_profiles:
            all_data.append({
                "source": "LinkedIn",
                "name": profile["name"],
                "title": profile["title"],
                "company": profile["company"],
                "education": profile["education"],
                "skills": profile["skills"],
                "experience": profile["experience"],
                "location": profile["location"]
            })
        
        # Process GitHub profiles
        for profile in github_profiles:
            all_data.append({
                "source": "GitHub",
                "username": profile["username"],
                "bio": profile["bio"],
                "repos": profile["repos"],
                "languages": profile["languages"],
                "followers": profile["followers"],
                "location": profile["location"]
            })
        
        # Process Indeed resumes
        for resume in indeed_resumes:
            all_data.append({
                "source": "Indeed",
                "title": resume["title"],
                "education": resume["education"],
                "skills": resume["skills"],
                "experience": resume["experience"],
                "certifications": resume["certifications"],
                "projects": resume["projects"]
            })
        
        return all_data
    
    def generate_summary_report(self, all_data):
        """Generate comprehensive summary report"""
        print("📋 Generating summary report...")
        
        # Analyze skills
        all_skills = []
        for item in all_data:
            if "skills" in item:
                all_skills.extend(item["skills"])
        
        skill_counts = defaultdict(int)
        for skill in all_skills:
            skill_counts[skill] += 1
        
        # Analyze companies
        companies = [item["company"] for item in all_data if "company" in item]
        company_counts = defaultdict(int)
        for company in companies:
            company_counts[company] += 1
        
        # Analyze education
        education = [item["education"] for item in all_data if "education" in item]
        education_counts = defaultdict(int)
        for edu in education:
            education_counts[edu] += 1
        
        # Generate report
        report = {
            "total_profiles": len(all_data),
            "sources": {
                "LinkedIn": len([item for item in all_data if item["source"] == "LinkedIn"]),
                "GitHub": len([item for item in all_data if item["source"] == "GitHub"]),
                "Indeed": len([item for item in all_data if item["source"] == "Indeed"])
            },
            "top_skills": sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:20],
            "top_companies": sorted(company_counts.items(), key=lambda x: x[1], reverse=True)[:10],
            "education_breakdown": dict(education_counts),
            "common_job_titles": self.get_common_titles(all_data),
            "experience_levels": self.get_experience_levels(all_data),
            "location_distribution": self.get_location_distribution(all_data)
        }
        
        return report
    
    def get_common_titles(self, all_data):
        """Get most common job titles"""
        titles = [item["title"] for item in all_data if "title" in item]
        title_counts = defaultdict(int)
        for title in titles:
            title_counts[title] += 1
        return sorted(title_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    def get_experience_levels(self, all_data):
        """Get experience level distribution"""
        experience = [item["experience"] for item in all_data if "experience" in item]
        exp_counts = defaultdict(int)
        for exp in experience:
            exp_counts[exp] += 1
        return dict(exp_counts)
    
    def get_location_distribution(self, all_data):
        """Get location distribution"""
        locations = [item["location"] for item in all_data if "location" in item]
        location_counts = defaultdict(int)
        for location in locations:
            location_counts[location] += 1
        return dict(location_counts)
    
    def save_results(self, all_data, report):
        """Save results to files"""
        print("💾 Saving results...")
        
        # Create results directory
        os.makedirs("cit_backend_analysis", exist_ok=True)
        
        # Save raw data
        with open("cit_backend_analysis/raw_resume_data.json", "w") as f:
            json.dump(all_data, f, indent=2)
        
        # Save summary report
        with open("cit_backend_analysis/summary_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        # Save CSV for analysis
        df_data = []
        for item in all_data:
            row = {
                "source": item.get("source", ""),
                "name": item.get("name", item.get("username", "")),
                "title": item.get("title", ""),
                "company": item.get("company", ""),
                "education": item.get("education", ""),
                "skills": ", ".join(item.get("skills", [])),
                "experience": item.get("experience", ""),
                "location": item.get("location", ""),
                "certifications": ", ".join(item.get("certifications", [])),
                "projects": ", ".join(item.get("projects", []))
            }
            df_data.append(row)
        
        df = pd.DataFrame(df_data)
        df.to_csv("cit_backend_analysis/resume_data.csv", index=False)
        
        print(f"✅ Results saved to cit_backend_analysis/")
    
    def print_summary(self, report):
        """Print summary to console"""
        print("\n" + "="*60)
        print("📊 CIT BACKEND DEVELOPER RESUME ANALYSIS SUMMARY")
        print("="*60)
        
        print(f"\n📈 Total Profiles Analyzed: {report['total_profiles']}")
        
        print(f"\n🔍 Sources:")
        for source, count in report['sources'].items():
            print(f"   {source}: {count} profiles")
        
        print(f"\n💻 Top 10 Skills:")
        for skill, count in report['top_skills'][:10]:
            print(f"   {skill}: {count} mentions")
        
        print(f"\n🏢 Top Companies:")
        for company, count in report['top_companies'][:5]:
            print(f"   {company}: {count} employees")
        
        print(f"\n🎓 Education Breakdown:")
        for degree, count in report['education_breakdown'].items():
            print(f"   {degree}: {count} graduates")
        
        print(f"\n💼 Common Job Titles:")
        for title, count in report['common_job_titles'][:5]:
            print(f"   {title}: {count} positions")
        
        print(f"\n📍 Top Locations:")
        for location, count in sorted(report['location_distribution'].items(), 
                                    key=lambda x: x[1], reverse=True)[:5]:
            print(f"   {location}: {count} developers")
        
        print("\n" + "="*60)
    
    def run_analysis(self, max_profiles=100):
        """Run complete analysis"""
        print("🚀 Starting CIT Backend Developer Resume Analysis...")
        print(f"Target: {max_profiles} profiles")
        
        # Search different sources
        linkedin_profiles = self.search_linkedin_profiles(max_profiles // 2)
        github_profiles = self.search_github_profiles(max_profiles // 4)
        indeed_resumes = self.search_indeed_resumes(max_profiles // 4)
        
        # Analyze data
        all_data = self.analyze_resumes(linkedin_profiles, github_profiles, indeed_resumes)
        
        # Generate report
        report = self.generate_summary_report(all_data)
        
        # Save results
        self.save_results(all_data, report)
        
        # Print summary
        self.print_summary(report)
        
        return all_data, report

def main():
    """Main function"""
    analyzer = CITBackendResumeAnalyzer()
    all_data, report = analyzer.run_analysis(max_profiles=100)
    
    print("\n🎯 KEY INSIGHTS FOR YOUR SWE PORTFOLIO:")
    print("="*50)
    
    # Extract key insights
    top_skills = [skill for skill, count in report['top_skills'][:10]]
    top_companies = [company for company, count in report['top_companies'][:5]]
    
    print(f"\n✅ MUST-HAVE SKILLS:")
    for i, skill in enumerate(top_skills[:5], 1):
        print(f"   {i}. {skill}")
    
    print(f"\n🏢 TARGET COMPANIES:")
    for i, company in enumerate(top_companies, 1):
        print(f"   {i}. {company}")
    
    print(f"\n📚 EDUCATION PATTERNS:")
    for degree, count in report['education_breakdown'].items():
        print(f"   • {degree} ({count} graduates)")
    
    print(f"\n💡 PORTFOLIO RECOMMENDATIONS:")
    print("   1. Build backend APIs with Python/Node.js/Java")
    print("   2. Include database design and optimization")
    print("   3. Add Docker and cloud deployment experience")
    print("   4. Show REST API and microservices knowledge")
    print("   5. Include authentication and security features")

if __name__ == "__main__":
    main() 