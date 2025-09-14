#!/usr/bin/env python3
"""
Job Scraper - Integrates with existing internship finder functionality
Populates the database with real job data from multiple sources
"""

import requests
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime
from app import app, db, Job
import re

class JobScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def scrape_indeed(self, keyword='software engineer', location='remote', max_jobs=20):
        """Scrape jobs from Indeed"""
        print(f"🔍 Scraping Indeed for: {keyword} in {location}")
        
        jobs = []
        try:
            # Indeed search URL
            url = f"https://www.indeed.com/jobs?q={keyword.replace(' ', '+')}&l={location.replace(' ', '+')}&jt=internship"
            
            response = self.session.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job cards
                job_cards = soup.find_all('div', class_='job_seen_beacon')
                
                for card in job_cards[:max_jobs]:
                    try:
                        # Extract job title
                        title_elem = card.find('h2', class_='jobTitle')
                        title = title_elem.get_text(strip=True) if title_elem else "Software Engineer"
                        
                        # Extract company
                        company_elem = card.find('span', class_='companyName')
                        company = company_elem.get_text(strip=True) if company_elem else "Tech Company"
                        
                        # Extract location
                        location_elem = card.find('div', class_='companyLocation')
                        location_text = location_elem.get_text(strip=True) if location_elem else location
                        
                        # Extract job snippet
                        snippet_elem = card.find('div', class_='job-snippet')
                        description = snippet_elem.get_text(strip=True) if snippet_elem else "Software engineering position"
                        
                        # Extract salary if available
                        salary_elem = card.find('div', class_='salary-snippet')
                        salary = salary_elem.get_text(strip=True) if salary_elem else None
                        
                        # Extract job URL
                        job_link = card.find('a', class_='jcs-JobTitle')
                        source_url = "https://www.indeed.com" + job_link['href'] if job_link else None
                        
                        job_data = {
                            'title': title,
                            'company': company,
                            'location': location_text,
                            'description': description,
                            'salary_range': salary,
                            'job_type': 'internship',
                            'source': 'indeed',
                            'source_url': source_url
                        }
                        
                        jobs.append(job_data)
                        
                    except Exception as e:
                        print(f"Error parsing job card: {e}")
                        continue
                        
        except Exception as e:
            print(f"Error scraping Indeed: {e}")
        
        return jobs
    
    def scrape_linkedin(self, keyword='software engineer', location='remote', max_jobs=20):
        """Scrape jobs from LinkedIn"""
        print(f"🔍 Scraping LinkedIn for: {keyword} in {location}")
        
        jobs = []
        try:
            # LinkedIn search URL
            url = f"https://www.linkedin.com/jobs/search/?keywords={keyword.replace(' ', '%20')}&location={location.replace(' ', '%20')}&f_JT=I"
            
            response = self.session.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job cards
                job_cards = soup.find_all('div', class_='base-card')
                
                for card in job_cards[:max_jobs]:
                    try:
                        # Extract job title
                        title_elem = card.find('h3', class_='base-search-card__title')
                        title = title_elem.get_text(strip=True) if title_elem else "Software Engineer"
                        
                        # Extract company
                        company_elem = card.find('h4', class_='base-search-card__subtitle')
                        company = company_elem.get_text(strip=True) if company_elem else "Tech Company"
                        
                        # Extract location
                        location_elem = card.find('span', class_='job-search-card__location')
                        location_text = location_elem.get_text(strip=True) if location_elem else location
                        
                        # Extract job snippet
                        snippet_elem = card.find('div', class_='base-search-card__snippet')
                        description = snippet_elem.get_text(strip=True) if snippet_elem else "Software engineering position"
                        
                        # Extract job URL
                        job_link = card.find('a', class_='base-card__full-link')
                        source_url = job_link['href'] if job_link else None
                        
                        job_data = {
                            'title': title,
                            'company': company,
                            'location': location_text,
                            'description': description,
                            'job_type': 'internship',
                            'source': 'linkedin',
                            'source_url': source_url
                        }
                        
                        jobs.append(job_data)
                        
                    except Exception as e:
                        print(f"Error parsing job card: {e}")
                        continue
                        
        except Exception as e:
            print(f"Error scraping LinkedIn: {e}")
        
        return jobs
    
    def generate_sample_jobs(self, count=50):
        """Generate sample jobs for testing"""
        print(f"🔍 Generating {count} sample jobs")
        
        sample_companies = [
            "TechCorp", "DataFlow Systems", "CloudTech Solutions", "WebTech", "DigitalSolutions",
            "InnovationLabs", "FutureTech", "SmartSystems", "NextGen", "EliteTech",
            "StartupXYZ", "Enterprise Inc", "TechStart", "DataCorp", "CloudSystems"
        ]
        
        sample_titles = [
            "Software Engineer Intern", "Backend Developer Intern", "Full Stack Intern",
            "Python Developer Intern", "Node.js Developer Intern", "Database Intern",
            "API Developer Intern", "DevOps Intern", "Cloud Engineer Intern"
        ]
        
        sample_locations = [
            "San Francisco, CA", "New York, NY", "Austin, TX", "Seattle, WA", "Boston, MA",
            "Denver, CO", "Chicago, IL", "Atlanta, GA", "Portland, OR", "Miami, FL",
            "Remote", "Hybrid", "On-site"
        ]
        
        sample_descriptions = [
            "Join our team to build scalable backend systems using Python and Django.",
            "Work on real-time applications with Node.js and WebSocket technologies.",
            "Develop REST APIs and microservices for our cloud platform.",
            "Contribute to database design and optimization projects.",
            "Build authentication systems and security features.",
            "Work with Docker and cloud deployment technologies.",
            "Develop full-stack applications with modern frameworks."
        ]
        
        jobs = []
        for i in range(count):
            job_data = {
                'title': random.choice(sample_titles),
                'company': random.choice(sample_companies),
                'location': random.choice(sample_locations),
                'description': random.choice(sample_descriptions),
                'requirements': f"Python, JavaScript, SQL, Docker, AWS\nExperience with web development\nStrong problem-solving skills",
                'salary_range': f"${random.randint(20, 50)}/hour",
                'job_type': 'internship',
                'source': 'sample',
                'source_url': f"https://example.com/job/{i+1}"
            }
            jobs.append(job_data)
        
        return jobs
    
    def save_jobs_to_database(self, jobs):
        """Save scraped jobs to database"""
        print(f"💾 Saving {len(jobs)} jobs to database")
        
        with app.app_context():
            saved_count = 0
            for job_data in jobs:
                try:
                    # Check if job already exists
                    existing_job = Job.query.filter_by(
                        title=job_data['title'],
                        company=job_data['company'],
                        source=job_data['source']
                    ).first()
                    
                    if not existing_job:
                        job = Job(**job_data)
                        db.session.add(job)
                        saved_count += 1
                    
                except Exception as e:
                    print(f"Error saving job: {e}")
                    continue
            
            db.session.commit()
            print(f"✅ Successfully saved {saved_count} new jobs")
            return saved_count
    
    def run_scraping(self, keywords=['software engineer', 'backend developer', 'python developer'], 
                    locations=['remote', 'san francisco', 'new york'], max_jobs_per_source=10):
        """Run complete scraping process"""
        print("🚀 Starting job scraping process...")
        
        all_jobs = []
        
        # Scrape from different sources
        for keyword in keywords:
            for location in locations:
                print(f"\n📋 Scraping: {keyword} in {location}")
                
                # Scrape Indeed
                indeed_jobs = self.scrape_indeed(keyword, location, max_jobs_per_source)
                all_jobs.extend(indeed_jobs)
                
                # Scrape LinkedIn
                linkedin_jobs = self.scrape_linkedin(keyword, location, max_jobs_per_source)
                all_jobs.extend(linkedin_jobs)
                
                # Add delay to be respectful
                time.sleep(random.uniform(2, 5))
        
        # Generate sample jobs if scraping didn't work
        if len(all_jobs) < 20:
            print("⚠️  Scraping didn't get enough jobs, generating samples...")
            sample_jobs = self.generate_sample_jobs(50)
            all_jobs.extend(sample_jobs)
        
        # Remove duplicates
        unique_jobs = []
        seen = set()
        for job in all_jobs:
            job_key = (job['title'], job['company'], job['source'])
            if job_key not in seen:
                seen.add(job_key)
                unique_jobs.append(job)
        
        print(f"📊 Total unique jobs found: {len(unique_jobs)}")
        
        # Save to database
        saved_count = self.save_jobs_to_database(unique_jobs)
        
        return saved_count

def main():
    """Main function to run the scraper"""
    scraper = JobScraper()
    
    # Run scraping
    saved_count = scraper.run_scraping(
        keywords=['software engineer', 'backend developer', 'python developer'],
        locations=['remote', 'san francisco', 'new york'],
        max_jobs_per_source=5
    )
    
    print(f"\n🎉 Scraping complete! Saved {saved_count} jobs to database")
    print("You can now start the API server with: python app.py")

if __name__ == "__main__":
    main() 