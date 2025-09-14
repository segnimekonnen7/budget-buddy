import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin, urlparse
import random

class EnhancedInternshipScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.results = []
        
        # Pre-defined job categories
        self.job_categories = {
            'computer_science': [
                'computer science', 'software engineering', 'programming', 'coding',
                'software development', 'web development', 'full stack', 'backend',
                'frontend', 'mobile development', 'app development'
            ],
            'machine_learning': [
                'machine learning', 'ML', 'artificial intelligence', 'AI',
                'deep learning', 'neural networks', 'data science', 'data analytics',
                'predictive modeling', 'algorithm development'
            ],
            'data_science': [
                'data science', 'data analytics', 'data engineering', 'big data',
                'statistics', 'business intelligence', 'data visualization',
                'ETL', 'data mining', 'database'
            ],
            'cybersecurity': [
                'cybersecurity', 'information security', 'network security',
                'penetration testing', 'security analysis', 'threat detection',
                'vulnerability assessment', 'security engineering'
            ],
            'cloud_computing': [
                'cloud computing', 'AWS', 'Azure', 'Google Cloud', 'devops',
                'infrastructure', 'system administration', 'network engineering',
                'cloud architecture', 'containerization'
            ],
            'robotics': [
                'robotics', 'automation', 'control systems', 'mechatronics',
                'embedded systems', 'IoT', 'hardware engineering', 'electronics'
            ],
            'game_development': [
                'game development', 'game design', 'Unity', 'Unreal Engine',
                '3D modeling', 'animation', 'virtual reality', 'VR', 'AR'
            ],
            'fintech': [
                'fintech', 'financial technology', 'blockchain', 'cryptocurrency',
                'quantitative analysis', 'trading systems', 'payment processing'
            ],
            'healthcare_tech': [
                'healthcare technology', 'bioinformatics', 'medical software',
                'health informatics', 'digital health', 'telemedicine'
            ]
        }
        
        # Popular locations for tech jobs
        self.popular_locations = [
            'San Francisco, CA', 'New York, NY', 'Seattle, WA', 'Austin, TX',
            'Boston, MA', 'Los Angeles, CA', 'Chicago, IL', 'Denver, CO',
            'Atlanta, GA', 'Washington, DC', 'Portland, OR', 'Minneapolis, MN',
            'Dallas, TX', 'Phoenix, AZ', 'Miami, FL', 'Nashville, TN',
            'Charlotte, NC', 'Pittsburgh, PA', 'Salt Lake City, UT', 'Raleigh, NC'
        ]
    
    def search_linkedin_enhanced(self, keywords, location, job_type="", experience=""):
        """Enhanced LinkedIn search with better parsing"""
        try:
            search_url = "https://www.linkedin.com/jobs/search/"
            
            # Handle "Search All" for keywords
            if keywords.lower() == "search all":
                all_keywords = []
                for category in self.job_categories.values():
                    all_keywords.extend(category)
                keywords = " ".join(all_keywords[:10])  # Limit to avoid URL too long
            
            # Handle "Search All" for location
            if location.lower() == "search all":
                location = "United States"
            
            params = {
                'keywords': f"{keywords} intern internship",
                'location': location,
                'f_JT': 'I' if 'intern' in keywords.lower() else '',
                'f_E': '1' if experience == 'entry' else '2' if experience == 'mid' else '3' if experience == 'senior' else '',
                'f_WT': '2' if job_type == 'remote' else '1' if job_type == 'onsite' else '3' if job_type == 'hybrid' else '',
                'position': 1,
                'pageNum': 0
            }
            
            response = self.session.get(search_url, params=params)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                job_cards = soup.find_all('div', class_='base-card')
                
                for card in job_cards[:15]:  # Increased limit
                    try:
                        title_elem = card.find('h3', class_='base-search-card__title')
                        company_elem = card.find('h4', class_='base-search-card__subtitle')
                        location_elem = card.find('span', class_='job-search-card__location')
                        link_elem = card.find('a', class_='base-card__full-link')
                        
                        if title_elem and company_elem:
                            job_data = {
                                'title': title_elem.get_text(strip=True),
                                'company': company_elem.get_text(strip=True),
                                'location': location_elem.get_text(strip=True) if location_elem else location,
                                'source': 'LinkedIn',
                                'url': urljoin('https://www.linkedin.com', link_elem['href']) if link_elem else '',
                                'logo': '💼',
                                'category': self.categorize_job(title_elem.get_text(strip=True))
                            }
                            self.results.append(job_data)
                    except Exception as e:
                        print(f"Error parsing LinkedIn job card: {e}")
                        
        except Exception as e:
            print(f"Error searching LinkedIn: {e}")
    
    def search_indeed_enhanced(self, keywords, location, job_type="", experience=""):
        """Enhanced Indeed search with better parsing"""
        try:
            search_url = "https://www.indeed.com/jobs"
            
            # Handle "Search All" for keywords
            if keywords.lower() == "search all":
                keywords = "computer science machine learning software engineering data science"
            
            # Handle "Search All" for location
            if location.lower() == "search all":
                location = "United States"
            
            params = {
                'q': f"{keywords} intern internship",
                'l': location,
                'jt': 'internship',
                'remotejob': '1' if job_type == 'remote' else '0',
                'start': 0
            }
            
            response = self.session.get(search_url, params=params)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                job_cards = soup.find_all('div', class_='job_seen_beacon')
                
                for card in job_cards[:15]:  # Increased limit
                    try:
                        title_elem = card.find('h2', class_='jobTitle')
                        company_elem = card.find('span', class_='companyName')
                        location_elem = card.find('div', class_='companyLocation')
                        link_elem = card.find('a', class_='jcs-JobTitle')
                        
                        if title_elem and company_elem:
                            job_data = {
                                'title': title_elem.get_text(strip=True),
                                'company': company_elem.get_text(strip=True),
                                'location': location_elem.get_text(strip=True) if location_elem else location,
                                'source': 'Indeed',
                                'url': urljoin('https://www.indeed.com', link_elem['href']) if link_elem else '',
                                'logo': '📊',
                                'category': self.categorize_job(title_elem.get_text(strip=True))
                            }
                            self.results.append(job_data)
                    except Exception as e:
                        print(f"Error parsing Indeed job card: {e}")
                        
        except Exception as e:
            print(f"Error searching Indeed: {e}")
    
    def search_glassdoor_enhanced(self, keywords, location, job_type="", experience=""):
        """Enhanced Glassdoor search"""
        try:
            search_url = "https://www.glassdoor.com/Job/jobs.htm"
            
            # Handle "Search All" for keywords
            if keywords.lower() == "search all":
                keywords = "computer science machine learning software engineering"
            
            # Handle "Search All" for location
            if location.lower() == "search all":
                location = "United States"
            
            params = {
                'sc.keyword': f"{keywords} intern internship",
                'locT': 'C',
                'locId': '1147401',  # Default location
                'jobType': 'internship',
                'fromAge': -1,
                'minSalary': 0,
                'includeNoSalaryJobs': 'true',
                'radius': 100,
                'cityId': -1,
                'minRating': 0.0,
                'industryId': -1,
                'sgocId': -1,
                'seniorityType': 'all',
                'companyId': -1,
                'employerSizes': 0,
                'applicationType': 0,
                'remoteWorkType': 0
            }
            
            response = self.session.get(search_url, params=params)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                job_cards = soup.find_all('li', class_='react-job-listing')
                
                for card in job_cards[:15]:  # Increased limit
                    try:
                        title_elem = card.find('a', class_='jobLink')
                        company_elem = card.find('a', class_='job-search-key-l2wjgv')
                        location_elem = card.find('span', class_='job-search-key-iii9i8')
                        
                        if title_elem and company_elem:
                            job_data = {
                                'title': title_elem.get_text(strip=True),
                                'company': company_elem.get_text(strip=True),
                                'location': location_elem.get_text(strip=True) if location_elem else location,
                                'source': 'Glassdoor',
                                'url': urljoin('https://www.glassdoor.com', title_elem['href']) if title_elem else '',
                                'logo': '🏢',
                                'category': self.categorize_job(title_elem.get_text(strip=True))
                            }
                            self.results.append(job_data)
                    except Exception as e:
                        print(f"Error parsing Glassdoor job card: {e}")
                        
        except Exception as e:
            print(f"Error searching Glassdoor: {e}")
    
    def categorize_job(self, job_title):
        """Categorize job based on title"""
        job_title_lower = job_title.lower()
        
        for category, keywords in self.job_categories.items():
            for keyword in keywords:
                if keyword.lower() in job_title_lower:
                    return category.replace('_', ' ').title()
        
        return 'Technology'
    
    def search_all_sources_enhanced(self, keywords, location, job_type="", experience="", sources=None):
        """Enhanced search with better handling of "Search All" options"""
        if sources is None:
            sources = ['linkedin', 'indeed', 'glassdoor']
        
        self.results = []
        
        print(f"🔍 Enhanced Search Started")
        print(f"📋 Keywords: {keywords}")
        print(f"📍 Location: {location}")
        print(f"🏢 Job Type: {job_type}")
        print(f"👤 Experience: {experience}")
        print(f"🌐 Sources: {', '.join(sources)}")
        
        for source in sources:
            print(f"\n🔎 Searching {source.title()}...")
            
            if source == 'linkedin':
                self.search_linkedin_enhanced(keywords, location, job_type, experience)
            elif source == 'indeed':
                self.search_indeed_enhanced(keywords, location, job_type, experience)
            elif source == 'glassdoor':
                self.search_glassdoor_enhanced(keywords, location, job_type, experience)
            
            # Add delay to be respectful to websites
            time.sleep(random.uniform(1, 3))
        
        # Remove duplicates based on title and company
        unique_results = []
        seen = set()
        for job in self.results:
            key = (job['title'].lower(), job['company'].lower())
            if key not in seen:
                seen.add(key)
                unique_results.append(job)
        
        self.results = unique_results
        print(f"\n✅ Found {len(self.results)} unique internships!")
        return self.results
    
    def get_job_categories(self):
        """Get available job categories"""
        return list(self.job_categories.keys())
    
    def get_popular_locations(self):
        """Get popular locations"""
        return self.popular_locations
    
    def get_results(self):
        """Return all found results"""
        return self.results
    
    def save_results(self, filename="enhanced_internship_results.json"):
        """Save results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"💾 Results saved to {filename}")

# Example usage
if __name__ == "__main__":
    scraper = EnhancedInternshipScraper()
    
    # Test enhanced search
    results = scraper.search_all_sources_enhanced(
        keywords="Search All",  # Will search all categories
        location="Search All",  # Will search all locations
        job_type="remote",
        experience="entry",
        sources=['linkedin', 'indeed', 'glassdoor']
    )
    
    # Print results
    for i, job in enumerate(results, 1):
        print(f"\n{i}. {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   Category: {job['category']}")
        print(f"   Source: {job['source']}")
        print(f"   URL: {job['url']}")
    
    # Save results
    scraper.save_results() 