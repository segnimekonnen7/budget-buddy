import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin, urlparse, quote_plus
import random

class ImprovedInternshipScraper:
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
        self.results = []
        
        # Pre-defined job categories with better keywords
        self.job_categories = {
            'computer_science': [
                'computer science', 'software engineering', 'programming', 'coding',
                'software development', 'web development', 'full stack', 'backend',
                'frontend', 'mobile development', 'app development', 'internship'
            ],
            'machine_learning': [
                'machine learning', 'ML', 'artificial intelligence', 'AI',
                'deep learning', 'neural networks', 'data science', 'data analytics',
                'predictive modeling', 'algorithm development', 'internship'
            ],
            'data_science': [
                'data science', 'data analytics', 'data engineering', 'big data',
                'statistics', 'business intelligence', 'data visualization',
                'ETL', 'data mining', 'database', 'internship'
            ],
            'cybersecurity': [
                'cybersecurity', 'information security', 'network security',
                'penetration testing', 'security analysis', 'threat detection',
                'vulnerability assessment', 'security engineering', 'internship'
            ],
            'cloud_computing': [
                'cloud computing', 'AWS', 'Azure', 'Google Cloud', 'devops',
                'infrastructure', 'system administration', 'network engineering',
                'cloud architecture', 'containerization', 'internship'
            ]
        }
        
        # Popular locations for tech jobs
        self.popular_locations = [
            'San Francisco, CA', 'New York, NY', 'Seattle, WA', 'Austin, TX',
            'Boston, MA', 'Los Angeles, CA', 'Chicago, IL', 'Denver, CO',
            'Atlanta, GA', 'Washington, DC', 'Portland, OR', 'Minneapolis, MN',
            'Dallas, TX', 'Phoenix, AZ', 'Miami, FL', 'Nashville, TN',
            'Charlotte, NC', 'Pittsburgh, PA', 'Salt Lake City, UT', 'Raleigh, NC',
            'United States', 'Remote', 'Anywhere'
        ]
    
    def search_indeed_improved(self, keywords, location, job_type="", experience=""):
        """Improved Indeed search with better parsing"""
        try:
            # Handle "Search All" for keywords
            if keywords.lower() == "search all":
                keywords = "software engineering internship"
            
            # Handle "Search All" for location
            if location.lower() == "search all":
                location = "United States"
            
            # Build search URL
            search_query = f"{keywords} {location}"
            encoded_query = quote_plus(search_query)
            search_url = f"https://www.indeed.com/jobs?q={encoded_query}&l={quote_plus(location)}&jt=internship"
            
            print(f"🔍 Searching Indeed: {search_url}")
            
            response = self.session.get(search_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Try multiple selectors for job cards
                job_cards = soup.find_all('div', class_='job_seen_beacon') or \
                           soup.find_all('div', class_='cardOutline') or \
                           soup.find_all('div', {'data-jk': True}) or \
                           soup.find_all('div', class_='job_seen_beacon')
                
                print(f"📊 Found {len(job_cards)} job cards on Indeed")
                
                for card in job_cards[:10]:  # Limit to 10 results
                    try:
                        # Try multiple selectors for title
                        title_elem = card.find('h2', class_='jobTitle') or \
                                   card.find('a', class_='jcs-JobTitle') or \
                                   card.find('h2', class_='jobTitle') or \
                                   card.find('a', {'data-jk': True})
                        
                        # Try multiple selectors for company
                        company_elem = card.find('span', class_='companyName') or \
                                     card.find('div', class_='companyName') or \
                                     card.find('span', class_='company')
                        
                        # Try multiple selectors for location
                        location_elem = card.find('div', class_='companyLocation') or \
                                      card.find('span', class_='location') or \
                                      card.find('div', class_='location')
                        
                        # Try multiple selectors for link
                        link_elem = card.find('a', class_='jcs-JobTitle') or \
                                  card.find('a', {'data-jk': True}) or \
                                  card.find('h2', class_='jobTitle').find('a') if card.find('h2', class_='jobTitle') else None
                        
                        if title_elem and company_elem:
                            title = title_elem.get_text(strip=True)
                            company = company_elem.get_text(strip=True)
                            job_location = location_elem.get_text(strip=True) if location_elem else location
                            
                            # Build job URL
                            if link_elem and link_elem.get('href'):
                                job_url = urljoin('https://www.indeed.com', link_elem['href'])
                            else:
                                job_url = f"https://www.indeed.com/jobs?q={quote_plus(title)}&l={quote_plus(job_location)}"
                            
                            job_data = {
                                'title': title,
                                'company': company,
                                'location': job_location,
                                'source': 'Indeed',
                                'url': job_url,
                                'logo': '📊',
                                'category': self.categorize_job(title)
                            }
                            self.results.append(job_data)
                            print(f"✅ Found: {title} at {company}")
                            
                    except Exception as e:
                        print(f"Error parsing Indeed job card: {e}")
                        
        except Exception as e:
            print(f"Error searching Indeed: {e}")
    
    def search_linkedin_improved(self, keywords, location, job_type="", experience=""):
        """Improved LinkedIn search with better parsing"""
        try:
            # Handle "Search All" for keywords
            if keywords.lower() == "search all":
                keywords = "software engineering internship"
            
            # Handle "Search All" for location
            if location.lower() == "search all":
                location = "United States"
            
            # Build search URL
            search_query = f"{keywords} {location}"
            encoded_query = quote_plus(search_query)
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={encoded_query}&location={quote_plus(location)}&f_JT=I"
            
            print(f"🔍 Searching LinkedIn: {search_url}")
            
            response = self.session.get(search_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Try multiple selectors for job cards
                job_cards = soup.find_all('div', class_='base-card') or \
                           soup.find_all('li', class_='result-card') or \
                           soup.find_all('div', class_='job-result-card')
                
                print(f"📊 Found {len(job_cards)} job cards on LinkedIn")
                
                for card in job_cards[:10]:  # Limit to 10 results
                    try:
                        # Try multiple selectors for title
                        title_elem = card.find('h3', class_='base-search-card__title') or \
                                   card.find('h3', class_='result-card__title') or \
                                   card.find('a', class_='result-card__full-card-link')
                        
                        # Try multiple selectors for company
                        company_elem = card.find('h4', class_='base-search-card__subtitle') or \
                                     card.find('h4', class_='result-card__subtitle') or \
                                     card.find('span', class_='result-card__company-name')
                        
                        # Try multiple selectors for location
                        location_elem = card.find('span', class_='job-search-card__location') or \
                                      card.find('span', class_='result-card__location') or \
                                      card.find('span', class_='job-search-card__location')
                        
                        # Try multiple selectors for link
                        link_elem = card.find('a', class_='base-card__full-link') or \
                                  card.find('a', class_='result-card__full-card-link') or \
                                  card.find('a', {'data-control-name': 'job_card_click'})
                        
                        if title_elem and company_elem:
                            title = title_elem.get_text(strip=True)
                            company = company_elem.get_text(strip=True)
                            job_location = location_elem.get_text(strip=True) if location_elem else location
                            
                            # Build job URL
                            if link_elem and link_elem.get('href'):
                                job_url = urljoin('https://www.linkedin.com', link_elem['href'])
                            else:
                                job_url = f"https://www.linkedin.com/jobs/search/?keywords={quote_plus(title)}&location={quote_plus(job_location)}"
                            
                            job_data = {
                                'title': title,
                                'company': company,
                                'location': job_location,
                                'source': 'LinkedIn',
                                'url': job_url,
                                'logo': '💼',
                                'category': self.categorize_job(title)
                            }
                            self.results.append(job_data)
                            print(f"✅ Found: {title} at {company}")
                            
                    except Exception as e:
                        print(f"Error parsing LinkedIn job card: {e}")
                        
        except Exception as e:
            print(f"Error searching LinkedIn: {e}")
    
    def search_glassdoor_improved(self, keywords, location, job_type="", experience=""):
        """Improved Glassdoor search with better parsing"""
        try:
            # Handle "Search All" for keywords
            if keywords.lower() == "search all":
                keywords = "software engineering internship"
            
            # Handle "Search All" for location
            if location.lower() == "search all":
                location = "United States"
            
            # Build search URL
            search_query = f"{keywords} {location}"
            encoded_query = quote_plus(search_query)
            search_url = f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={encoded_query}&locT=C&locId=1147401&jobType=internship"
            
            print(f"🔍 Searching Glassdoor: {search_url}")
            
            response = self.session.get(search_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Try multiple selectors for job cards
                job_cards = soup.find_all('li', class_='react-job-listing') or \
                           soup.find_all('div', class_='job-listing') or \
                           soup.find_all('div', class_='jobListing')
                
                print(f"📊 Found {len(job_cards)} job cards on Glassdoor")
                
                for card in job_cards[:10]:  # Limit to 10 results
                    try:
                        # Try multiple selectors for title
                        title_elem = card.find('a', class_='jobLink') or \
                                   card.find('a', class_='job-title') or \
                                   card.find('h3', class_='job-title')
                        
                        # Try multiple selectors for company
                        company_elem = card.find('a', class_='job-search-key-l2wjgv') or \
                                     card.find('div', class_='employer-name') or \
                                     card.find('span', class_='employer-name')
                        
                        # Try multiple selectors for location
                        location_elem = card.find('span', class_='job-search-key-iii9i8') or \
                                      card.find('span', class_='location') or \
                                      card.find('div', class_='location')
                        
                        if title_elem and company_elem:
                            title = title_elem.get_text(strip=True)
                            company = company_elem.get_text(strip=True)
                            job_location = location_elem.get_text(strip=True) if location_elem else location
                            
                            # Build job URL
                            if title_elem.get('href'):
                                job_url = urljoin('https://www.glassdoor.com', title_elem['href'])
                            else:
                                job_url = f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={quote_plus(title)}&locT=C&locId=1147401"
                            
                            job_data = {
                                'title': title,
                                'company': company,
                                'location': job_location,
                                'source': 'Glassdoor',
                                'url': job_url,
                                'logo': '🏢',
                                'category': self.categorize_job(title)
                            }
                            self.results.append(job_data)
                            print(f"✅ Found: {title} at {company}")
                            
                    except Exception as e:
                        print(f"Error parsing Glassdoor job card: {e}")
                        
        except Exception as e:
            print(f"Error searching Glassdoor: {e}")
    
    def add_sample_internships(self):
        """Add sample internships as fallback when scraping fails"""
        sample_internships = [
            {
                'title': 'Software Engineering Intern',
                'company': 'Google',
                'location': 'Mountain View, CA',
                'source': 'Sample',
                'url': 'https://careers.google.com/jobs/results/',
                'logo': '🔍',
                'category': 'Computer Science'
            },
            {
                'title': 'Machine Learning Intern',
                'company': 'Microsoft',
                'location': 'Redmond, WA',
                'source': 'Sample',
                'url': 'https://careers.microsoft.com/us/en/search-results',
                'logo': '🔍',
                'category': 'Machine Learning'
            },
            {
                'title': 'Data Science Intern',
                'company': 'Amazon',
                'location': 'Seattle, WA',
                'source': 'Sample',
                'url': 'https://www.amazon.jobs/en/teams/internships',
                'logo': '🔍',
                'category': 'Data Science'
            },
            {
                'title': 'AI Research Intern',
                'company': 'OpenAI',
                'location': 'San Francisco, CA',
                'source': 'Sample',
                'url': 'https://openai.com/careers',
                'logo': '🔍',
                'category': 'Machine Learning'
            },
            {
                'title': 'Cybersecurity Intern',
                'company': 'CrowdStrike',
                'location': 'Austin, TX',
                'source': 'Sample',
                'url': 'https://www.crowdstrike.com/careers/',
                'logo': '🔍',
                'category': 'Cybersecurity'
            },
            {
                'title': 'Cloud Engineering Intern',
                'company': 'AWS',
                'location': 'Seattle, WA',
                'source': 'Sample',
                'url': 'https://aws.amazon.com/careers/',
                'logo': '🔍',
                'category': 'Cloud Computing'
            },
            {
                'title': 'Full Stack Developer Intern',
                'company': 'Meta',
                'location': 'Menlo Park, CA',
                'source': 'Sample',
                'url': 'https://www.metacareers.com/students-and-grads/',
                'logo': '🔍',
                'category': 'Computer Science'
            },
            {
                'title': 'DevOps Intern',
                'company': 'Netflix',
                'location': 'Los Gatos, CA',
                'source': 'Sample',
                'url': 'https://jobs.netflix.com/',
                'logo': '🔍',
                'category': 'Cloud Computing'
            }
        ]
        
        for internship in sample_internships:
            self.results.append(internship)
            print(f"✅ Added sample: {internship['title']} at {internship['company']}")
    
    def categorize_job(self, job_title):
        """Categorize job based on title"""
        job_title_lower = job_title.lower()
        
        for category, keywords in self.job_categories.items():
            for keyword in keywords:
                if keyword.lower() in job_title_lower:
                    return category.replace('_', ' ').title()
        
        return 'Technology'
    
    def search_all_sources_improved(self, keywords, location, job_type="", experience="", sources=None):
        """Improved search with better handling and fallback"""
        if sources is None:
            sources = ['indeed', 'linkedin', 'glassdoor']
        
        self.results = []
        
        print(f"🚀 Improved Search Started")
        print(f"📋 Keywords: {keywords}")
        print(f"📍 Location: {location}")
        print(f"🏢 Job Type: {job_type}")
        print(f"👤 Experience: {experience}")
        print(f"🌐 Sources: {', '.join(sources)}")
        
        # Search each source
        for source in sources:
            print(f"\n🔎 Searching {source.title()}...")
            
            if source == 'linkedin':
                self.search_linkedin_improved(keywords, location, job_type, experience)
            elif source == 'indeed':
                self.search_indeed_improved(keywords, location, job_type, experience)
            elif source == 'glassdoor':
                self.search_glassdoor_improved(keywords, location, job_type, experience)
            
            # Add delay to be respectful to websites
            time.sleep(random.uniform(2, 4))
        
        # If no results found, add sample internships
        if len(self.results) == 0:
            print(f"\n⚠️ No results found from web scraping. Adding sample internships...")
            self.add_sample_internships()
        
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
    
    def save_results(self, filename="improved_internship_results.json"):
        """Save results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"💾 Results saved to {filename}")

# Test the improved scraper
if __name__ == "__main__":
    scraper = ImprovedInternshipScraper()
    
    # Test with different scenarios
    test_scenarios = [
        ("Search All", "Search All", "", ""),
        ("machine learning", "San Francisco, CA", "", ""),
        ("software engineering", "New York, NY", "", ""),
        ("data science", "Remote", "", ""),
    ]
    
    for keywords, location, job_type, experience in test_scenarios:
        print(f"\n{'='*60}")
        print(f"Testing: {keywords} in {location}")
        print(f"{'='*60}")
        
        results = scraper.search_all_sources_improved(
            keywords=keywords,
            location=location,
            job_type=job_type,
            experience=experience,
            sources=['indeed', 'linkedin', 'glassdoor']
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
        scraper.save_results(f"test_results_{keywords.replace(' ', '_')}.json")
        
        # Clear results for next test
        scraper.results = []
        time.sleep(5)  # Wait between tests 