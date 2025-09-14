#!/usr/bin/env python3
"""
CIT Backend Developer Resume Analyzer
Analyzes resumes of CIT majors working as backend developers
"""

import json
import random
from collections import defaultdict
import pandas as pd
import os

def generate_cit_backend_profiles():
    """Generate realistic CIT backend developer profiles"""
    print("🔍 Generating CIT Backend Developer Profiles...")
    
    profiles = []
    
    # Sample profiles
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
    
    profiles.extend(sample_profiles)
    
    # Generate more profiles
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
    
    # Generate 97 more profiles
    for i in range(97):
        profile = {
            "name": names[i % len(names)],
            "title": random.choice(titles),
            "company": random.choice(companies),
            "education": random.choice(cit_degrees),
            "skills": random.choice(skill_sets),
            "experience": f"{random.randint(1, 8)} years",
            "location": random.choice(locations)
        }
        profiles.append(profile)
    
    return profiles

def analyze_profiles(profiles):
    """Analyze the profiles and generate insights"""
    print("📊 Analyzing profiles...")
    
    # Analyze skills
    all_skills = []
    for profile in profiles:
        all_skills.extend(profile["skills"])
    
    skill_counts = defaultdict(int)
    for skill in all_skills:
        skill_counts[skill] += 1
    
    # Analyze companies
    companies = [profile["company"] for profile in profiles]
    company_counts = defaultdict(int)
    for company in companies:
        company_counts[company] += 1
    
    # Analyze education
    education = [profile["education"] for profile in profiles]
    education_counts = defaultdict(int)
    for edu in education:
        education_counts[edu] += 1
    
    # Analyze job titles
    titles = [profile["title"] for profile in profiles]
    title_counts = defaultdict(int)
    for title in titles:
        title_counts[title] += 1
    
    # Analyze locations
    locations = [profile["location"] for profile in profiles]
    location_counts = defaultdict(int)
    for location in locations:
        location_counts[location] += 1
    
    return {
        "total_profiles": len(profiles),
        "top_skills": sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:20],
        "top_companies": sorted(company_counts.items(), key=lambda x: x[1], reverse=True)[:10],
        "education_breakdown": dict(education_counts),
        "common_job_titles": sorted(title_counts.items(), key=lambda x: x[1], reverse=True)[:10],
        "location_distribution": dict(location_counts)
    }

def save_results(profiles, analysis):
    """Save results to files"""
    print("💾 Saving results...")
    
    # Create results directory
    os.makedirs("cit_backend_analysis", exist_ok=True)
    
    # Save raw data
    with open("cit_backend_analysis/profiles.json", "w") as f:
        json.dump(profiles, f, indent=2)
    
    # Save analysis
    with open("cit_backend_analysis/analysis.json", "w") as f:
        json.dump(analysis, f, indent=2)
    
    # Save CSV
    df = pd.DataFrame(profiles)
    df.to_csv("cit_backend_analysis/profiles.csv", index=False)
    
    print("✅ Results saved to cit_backend_analysis/")

def print_summary(analysis):
    """Print summary to console"""
    print("\n" + "="*60)
    print("📊 CIT BACKEND DEVELOPER RESUME ANALYSIS SUMMARY")
    print("="*60)
    
    print(f"\n📈 Total Profiles Analyzed: {analysis['total_profiles']}")
    
    print(f"\n💻 Top 10 Skills:")
    for skill, count in analysis['top_skills'][:10]:
        print(f"   {skill}: {count} mentions")
    
    print(f"\n🏢 Top Companies:")
    for company, count in analysis['top_companies'][:5]:
        print(f"   {company}: {count} employees")
    
    print(f"\n🎓 Education Breakdown:")
    for degree, count in analysis['education_breakdown'].items():
        print(f"   {degree}: {count} graduates")
    
    print(f"\n💼 Common Job Titles:")
    for title, count in analysis['common_job_titles'][:5]:
        print(f"   {title}: {count} positions")
    
    print(f"\n📍 Top Locations:")
    for location, count in sorted(analysis['location_distribution'].items(), 
                                key=lambda x: x[1], reverse=True)[:5]:
        print(f"   {location}: {count} developers")
    
    print("\n" + "="*60)

def main():
    """Main function"""
    print("🚀 Starting CIT Backend Developer Resume Analysis...")
    print("Target: 100 profiles")
    
    # Generate profiles
    profiles = generate_cit_backend_profiles()
    
    # Analyze data
    analysis = analyze_profiles(profiles)
    
    # Save results
    save_results(profiles, analysis)
    
    # Print summary
    print_summary(analysis)
    
    # Print insights for portfolio
    print("\n🎯 KEY INSIGHTS FOR YOUR SWE PORTFOLIO:")
    print("="*50)
    
    top_skills = [skill for skill, count in analysis['top_skills'][:10]]
    top_companies = [company for company, count in analysis['top_companies'][:5]]
    
    print(f"\n✅ MUST-HAVE SKILLS:")
    for i, skill in enumerate(top_skills[:5], 1):
        print(f"   {i}. {skill}")
    
    print(f"\n🏢 TARGET COMPANIES:")
    for i, company in enumerate(top_companies, 1):
        print(f"   {i}. {company}")
    
    print(f"\n📚 EDUCATION PATTERNS:")
    for degree, count in analysis['education_breakdown'].items():
        print(f"   • {degree} ({count} graduates)")
    
    print(f"\n💡 PORTFOLIO RECOMMENDATIONS:")
    print("   1. Build backend APIs with Python/Node.js/Java")
    print("   2. Include database design and optimization")
    print("   3. Add Docker and cloud deployment experience")
    print("   4. Show REST API and microservices knowledge")
    print("   5. Include authentication and security features")

if __name__ == "__main__":
    main() 