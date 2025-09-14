import requests
from bs4 import BeautifulSoup
import json
import time
import random
from urllib.parse import urljoin, quote_plus

class WorkingInternshipScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.results = []
        
    def search_indeed_simple(self, keywords, location):
        """Simple Indeed search that actually works"""
        try:
            # Use Indeed's search API
            search_query = f"{keywords} internship {location}"
            encoded_query = quote_plus(search_query)
            url = f"https://www.indeed.com/jobs?q={encoded_query}&l={quote_plus(location)}&jt=internship"
            
            print(f"🔍 Searching Indeed: {url}")
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job cards
                job_cards = soup.find_all('div', class_='job_seen_beacon')
                if not job_cards:
                    job_cards = soup.find_all('div', {'data-jk': True})
                
                for i, card in enumerate(job_cards[:10]):  # Limit to 10 results
                    try:
                        # Extract job title
                        title_elem = card.find('h2', class_='jobTitle') or card.find('a', class_='jcs-JobTitle')
                        title = title_elem.get_text(strip=True) if title_elem else f"Internship {i+1}"
                        
                        # Extract company
                        company_elem = card.find('span', class_='companyName') or card.find('div', class_='company')
                        company = company_elem.get_text(strip=True) if company_elem else "Company"
                        
                        # Extract location
                        location_elem = card.find('div', class_='companyLocation') or card.find('span', class_='location')
                        job_location = location_elem.get_text(strip=True) if location_elem else location
                        
                        # Extract job URL
                        job_link = card.find('a', class_='jcs-JobTitle')
                        job_url = urljoin('https://www.indeed.com', job_link['href']) if job_link else f"https://www.indeed.com/jobs?q={encoded_query}"
                        
                        job_data = {
                            'title': title,
                            'company': company,
                            'location': job_location,
                            'url': job_url,
                            'source': 'Indeed',
                            'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Indeed_logo.svg/2560px-Indeed_logo.svg.png',
                            'category': self.categorize_job(title)
                        }
                        
                        self.results.append(job_data)
                        print(f"✅ Found: {title} at {company}")
                        
                    except Exception as e:
                        print(f"Error parsing job card: {e}")
                        continue
                        
        except Exception as e:
            print(f"Error searching Indeed: {e}")
    
    def search_linkedin_simple(self, keywords, location):
        """Simple LinkedIn search"""
        try:
            search_query = f"{keywords} internship {location}"
            encoded_query = quote_plus(search_query)
            url = f"https://www.linkedin.com/jobs/search/?keywords={encoded_query}&location={quote_plus(location)}&f_JT=I"
            
            print(f"🔍 Searching LinkedIn: {url}")
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job cards
                job_cards = soup.find_all('div', class_='base-card')
                
                for i, card in enumerate(job_cards[:10]):
                    try:
                        # Extract job title
                        title_elem = card.find('h3', class_='base-search-card__title')
                        title = title_elem.get_text(strip=True) if title_elem else f"LinkedIn Internship {i+1}"
                        
                        # Extract company
                        company_elem = card.find('h4', class_='base-search-card__subtitle')
                        company = company_elem.get_text(strip=True) if company_elem else "Company"
                        
                        # Extract location
                        location_elem = card.find('span', class_='job-search-card__location')
                        job_location = location_elem.get_text(strip=True) if location_elem else location
                        
                        # Extract job URL
                        job_link = card.find('a', class_='base-card__full-link')
                        job_url = job_link['href'] if job_link else url
                        
                        job_data = {
                            'title': title,
                            'company': company,
                            'location': job_location,
                            'url': job_url,
                            'source': 'LinkedIn',
                            'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/LinkedIn_logo_initials.png/800px-LinkedIn_logo_initials.png',
                            'category': self.categorize_job(title)
                        }
                        
                        self.results.append(job_data)
                        print(f"✅ Found: {title} at {company}")
                        
                    except Exception as e:
                        print(f"Error parsing LinkedIn job: {e}")
                        continue
                        
        except Exception as e:
            print(f"Error searching LinkedIn: {e}")
    
    def search_glassdoor_simple(self, keywords, location):
        """Simple Glassdoor search"""
        try:
            search_query = f"{keywords} internship {location}"
            encoded_query = quote_plus(search_query)
            url = f"https://www.glassdoor.com/Job/{location}-{keywords}-internship-jobs-SRCH_IL.0,{len(location)}_{KO0,14}.htm"
            
            print(f"🔍 Searching Glassdoor: {url}")
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find job cards
                job_cards = soup.find_all('li', class_='react-job-listing')
                
                for i, card in enumerate(job_cards[:10]):
                    try:
                        # Extract job title
                        title_elem = card.find('a', class_='jobLink')
                        title = title_elem.get_text(strip=True) if title_elem else f"Glassdoor Internship {i+1}"
                        
                        # Extract company
                        company_elem = card.find('a', class_='job-search-key-l2wjgv')
                        company = company_elem.get_text(strip=True) if company_elem else "Company"
                        
                        # Extract location
                        location_elem = card.find('span', class_='loc')
                        job_location = location_elem.get_text(strip=True) if location_elem else location
                        
                        # Extract job URL
                        job_url = urljoin('https://www.glassdoor.com', title_elem['href']) if title_elem else url
                        
                        job_data = {
                            'title': title,
                            'company': company,
                            'location': job_location,
                            'url': job_url,
                            'source': 'Glassdoor',
                            'logo': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Glassdoor_logo.svg/2560px-Glassdoor_logo.svg.png',
                            'category': self.categorize_job(title)
                        }
                        
                        self.results.append(job_data)
                        print(f"✅ Found: {title} at {company}")
                        
                    except Exception as e:
                        print(f"Error parsing Glassdoor job: {e}")
                        continue
                        
        except Exception as e:
            print(f"Error searching Glassdoor: {e}")
    
    def categorize_job(self, job_title):
        """Categorize job based on title"""
        job_title_lower = job_title.lower()
        
        categories = {
            'computer_science': ['software', 'programming', 'coding', 'developer', 'engineer'],
            'machine_learning': ['machine learning', 'ml', 'ai', 'artificial intelligence', 'deep learning'],
            'data_science': ['data', 'analytics', 'statistics', 'business intelligence'],
            'cybersecurity': ['security', 'cyber', 'penetration', 'threat'],
            'cloud_computing': ['cloud', 'aws', 'azure', 'devops', 'infrastructure']
        }
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in job_title_lower:
                    return category.replace('_', ' ').title()
        
        return 'Technology'
    
    def search_all_sources(self, keywords, location, sources=None):
        """Search all sources for internships"""
        if sources is None:
            sources = ['indeed', 'linkedin', 'glassdoor']
        
        self.results = []
        
        print(f"🔍 Starting search for: {keywords} in {location}")
        print(f"📋 Sources: {', '.join(sources)}")
        
        for source in sources:
            if source == 'indeed':
                self.search_indeed_simple(keywords, location)
            elif source == 'linkedin':
                self.search_linkedin_simple(keywords, location)
            elif source == 'glassdoor':
                self.search_glassdoor_simple(keywords, location)
            
            time.sleep(random.uniform(1, 3))  # Be respectful
        
        # Remove duplicates
        unique_results = []
        seen_titles = set()
        for job in self.results:
            if job['title'] not in seen_titles:
                unique_results.append(job)
                seen_titles.add(job['title'])
        
        self.results = unique_results
        print(f"✅ Found {len(self.results)} unique internships!")
        return self.results
    
    def get_results(self):
        return self.results

if __name__ == "__main__":
    scraper = WorkingInternshipScraper()
    results = scraper.search_all_sources("machine learning", "San Francisco")
    
    for i, job in enumerate(results, 1):
        print(f"\n{i}. {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   Source: {job['source']}")
        print(f"   URL: {job['url']}") 