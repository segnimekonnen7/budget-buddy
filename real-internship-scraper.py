import requests
from bs4 import BeautifulSoup
import json
import time
import random
from urllib.parse import urljoin, urlparse, quote
import re

class RealInternshipScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
    def search_linkedin_internships(self, keyword="software engineer", location="United States"):
        """Search LinkedIn for real internship listings"""
        jobs = []
        try:
            # LinkedIn search URL
            encoded_keyword = quote(f"{keyword} internship")
            encoded_location = quote(location)
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={encoded_keyword}&location={encoded_location}&f_E=1&f_JT=I&position=1&pageNum=0"
            
            print(f"Searching LinkedIn: {search_url}")
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job cards
                job_cards = soup.find_all('div', class_='base-card')
                print(f"Found {len(job_cards)} job cards on LinkedIn")
                
                for card in job_cards[:10]:  # Limit to 10 results
                    try:
                        title_elem = card.find('h3', class_='base-search-card__title')
                        company_elem = card.find('h4', class_='base-search-card__subtitle')
                        location_elem = card.find('span', class_='job-search-card__location')
                        link_elem = card.find('a', class_='base-card__full-link')
                        
                        if title_elem and company_elem:
                            title = title_elem.get_text(strip=True)
                            company = company_elem.get_text(strip=True)
                            job_location = location_elem.get_text(strip=True) if location_elem else "Remote"
                            apply_url = link_elem['href'] if link_elem else "#"
                            
                            # Only add if it's actually an internship
                            if 'intern' in title.lower() or 'internship' in title.lower():
                                jobs.append({
                                    'title': title,
                                    'company': company,
                                    'location': job_location,
                                    'type': 'Internship',
                                    'salary': 'Competitive',
                                    'description': f'Software engineering internship at {company}. Apply through LinkedIn.',
                                    'category': 'software-engineering',
                                    'applyUrl': apply_url,
                                    'source': 'LinkedIn'
                                })
                                print(f"Found LinkedIn internship: {title} at {company}")
                    except Exception as e:
                        continue
            else:
                print(f"LinkedIn returned status code: {response.status_code}")
                
        except Exception as e:
            print(f"LinkedIn scraping error: {e}")
            
        return jobs
    
    def search_indeed_internships(self, keyword="software engineer", location="United States"):
        """Search Indeed for real internship listings"""
        jobs = []
        try:
            # Indeed search URL
            encoded_keyword = quote(f"{keyword} internship")
            encoded_location = quote(location)
            search_url = f"https://www.indeed.com/jobs?q={encoded_keyword}&l={encoded_location}&jt=internship&sort=date"
            
            print(f"Searching Indeed: {search_url}")
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job cards
                job_cards = soup.find_all('div', class_='job_seen_beacon')
                print(f"Found {len(job_cards)} job cards on Indeed")
                
                for card in job_cards[:10]:  # Limit to 10 results
                    try:
                        title_elem = card.find('h2', class_='jobTitle')
                        company_elem = card.find('span', class_='companyName')
                        location_elem = card.find('div', class_='companyLocation')
                        link_elem = card.find('a', class_='jcs-JobTitle')
                        
                        if title_elem and company_elem:
                            title = title_elem.get_text(strip=True)
                            company = company_elem.get_text(strip=True)
                            job_location = location_elem.get_text(strip=True) if location_elem else "Remote"
                            apply_url = "https://www.indeed.com" + link_elem['href'] if link_elem else "#"
                            
                            # Only add if it's actually an internship
                            if 'intern' in title.lower() or 'internship' in title.lower():
                                jobs.append({
                                    'title': title,
                                    'company': company,
                                    'location': job_location,
                                    'type': 'Internship',
                                    'salary': 'Competitive',
                                    'description': f'Software engineering internship at {company}. Apply through Indeed.',
                                    'category': 'software-engineering',
                                    'applyUrl': apply_url,
                                    'source': 'Indeed'
                                })
                                print(f"Found Indeed internship: {title} at {company}")
                    except Exception as e:
                        continue
            else:
                print(f"Indeed returned status code: {response.status_code}")
                
        except Exception as e:
            print(f"Indeed scraping error: {e}")
            
        return jobs
    
    def search_glassdoor_internships(self, keyword="software engineer", location="United States"):
        """Search Glassdoor for real internship listings"""
        jobs = []
        try:
            # Glassdoor search URL
            encoded_keyword = quote(f"{keyword} internship")
            encoded_location = quote(location)
            search_url = f"https://www.glassdoor.com/Job/{encoded_location}-{encoded_keyword}-jobs-SRCH_IL.0,13_IC1147401_KO14,32.htm"
            
            print(f"Searching Glassdoor: {search_url}")
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job cards
                job_cards = soup.find_all('li', class_='react-job-listing')
                print(f"Found {len(job_cards)} job cards on Glassdoor")
                
                for card in job_cards[:10]:  # Limit to 10 results
                    try:
                        title_elem = card.find('a', class_='jobLink')
                        company_elem = card.find('a', class_='job-search-key-l2wjgv')
                        location_elem = card.find('span', class_='location')
                        
                        if title_elem and company_elem:
                            title = title_elem.get_text(strip=True)
                            company = company_elem.get_text(strip=True)
                            job_location = location_elem.get_text(strip=True) if location_elem else "Remote"
                            apply_url = "https://www.glassdoor.com" + title_elem['href'] if title_elem else "#"
                            
                            # Only add if it's actually an internship
                            if 'intern' in title.lower() or 'internship' in title.lower():
                                jobs.append({
                                    'title': title,
                                    'company': company,
                                    'location': job_location,
                                    'type': 'Internship',
                                    'salary': 'Competitive',
                                    'description': f'Software engineering internship at {company}. Apply through Glassdoor.',
                                    'category': 'software-engineering',
                                    'applyUrl': apply_url,
                                    'source': 'Glassdoor'
                                })
                                print(f"Found Glassdoor internship: {title} at {company}")
                    except Exception as e:
                        continue
            else:
                print(f"Glassdoor returned status code: {response.status_code}")
                
        except Exception as e:
            print(f"Glassdoor scraping error: {e}")
            
        return jobs
    
    def search_internships_com(self, keyword="software engineer", location="United States"):
        """Search Internships.com for real internship listings"""
        jobs = []
        try:
            # Internships.com search URL
            encoded_keyword = quote(f"{keyword} internship")
            encoded_location = quote(location)
            search_url = f"https://www.internships.com/search?keywords={encoded_keyword}&location={encoded_location}"
            
            print(f"Searching Internships.com: {search_url}")
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job cards
                job_cards = soup.find_all('div', class_='position')
                print(f"Found {len(job_cards)} job cards on Internships.com")
                
                for card in job_cards[:10]:  # Limit to 10 results
                    try:
                        title_elem = card.find('h3', class_='title')
                        company_elem = card.find('div', class_='company')
                        location_elem = card.find('div', class_='location')
                        link_elem = card.find('a', class_='position-link')
                        
                        if title_elem and company_elem:
                            title = title_elem.get_text(strip=True)
                            company = company_elem.get_text(strip=True)
                            job_location = location_elem.get_text(strip=True) if location_elem else "Remote"
                            apply_url = "https://www.internships.com" + link_elem['href'] if link_elem else "#"
                            
                            jobs.append({
                                'title': title,
                                'company': company,
                                'location': job_location,
                                'type': 'Internship',
                                'salary': 'Competitive',
                                'description': f'Software engineering internship at {company}. Apply through Internships.com.',
                                'category': 'software-engineering',
                                'applyUrl': apply_url,
                                'source': 'Internships.com'
                            })
                            print(f"Found Internships.com internship: {title} at {company}")
                    except Exception as e:
                        continue
            else:
                print(f"Internships.com returned status code: {response.status_code}")
                
        except Exception as e:
            print(f"Internships.com scraping error: {e}")
            
        return jobs
    
    def search_real_internships(self, keyword="software engineer", location="United States"):
        """Main search function that searches multiple real job sites"""
        all_jobs = []
        
        print(f"🔍 Searching for {keyword} internships in {location}...")
        print("=" * 60)
        
        # Search LinkedIn
        print("📱 Searching LinkedIn...")
        linkedin_jobs = self.search_linkedin_internships(keyword, location)
        all_jobs.extend(linkedin_jobs)
        print(f"✅ Found {len(linkedin_jobs)} internships on LinkedIn")
        
        # Search Indeed
        print("\n🔍 Searching Indeed...")
        indeed_jobs = self.search_indeed_internships(keyword, location)
        all_jobs.extend(indeed_jobs)
        print(f"✅ Found {len(indeed_jobs)} internships on Indeed")
        
        # Search Glassdoor
        print("\n🏢 Searching Glassdoor...")
        glassdoor_jobs = self.search_glassdoor_internships(keyword, location)
        all_jobs.extend(glassdoor_jobs)
        print(f"✅ Found {len(glassdoor_jobs)} internships on Glassdoor")
        
        # Search Internships.com
        print("\n🎓 Searching Internships.com...")
        internships_jobs = self.search_internships_com(keyword, location)
        all_jobs.extend(internships_jobs)
        print(f"✅ Found {len(internships_jobs)} internships on Internships.com")
        
        # Remove duplicates
        unique_jobs = []
        seen_titles = set()
        for job in all_jobs:
            if job['title'] not in seen_titles:
                unique_jobs.append(job)
                seen_titles.add(job['title'])
        
        print(f"\n🎯 Total unique internships found: {len(unique_jobs)}")
        print("=" * 60)
        
        return unique_jobs[:20]  # Return top 20 results

# Test the scraper
if __name__ == "__main__":
    scraper = RealInternshipScraper()
    
    # Test with different searches
    searches = [
        ("software engineer", "San Francisco"),
        ("backend developer", "New York"),
        ("machine learning", "United States"),
        ("data science", "Remote")
    ]
    
    for keyword, location in searches:
        print(f"\n🚀 Testing search: {keyword} in {location}")
        print("-" * 50)
        results = scraper.search_real_internships(keyword, location)
        
        print(f"\n📋 Results for '{keyword}' in '{location}':")
        for i, job in enumerate(results, 1):
            print(f"\n{i}. {job['title']}")
            print(f"   Company: {job['company']}")
            print(f"   Location: {job['location']}")
            print(f"   Apply: {job['applyUrl']}")
            print(f"   Source: {job['source']}")
        
        print("\n" + "="*60)
        time.sleep(2)  # Be nice to the servers 