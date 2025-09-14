import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin, urlparse
import random

class RealInternshipScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.results = []
        
    def search_linkedin(self, keywords, location, job_type="", experience=""):
        """Search LinkedIn for internships"""
        try:
            # LinkedIn search URL
            search_url = "https://www.linkedin.com/jobs/search/"
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
                
                for card in job_cards[:10]:  # Limit to 10 results
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
                                'logo': '💼'
                            }
                            self.results.append(job_data)
                    except Exception as e:
                        print(f"Error parsing LinkedIn job card: {e}")
                        
        except Exception as e:
            print(f"Error searching LinkedIn: {e}")
    
    def search_indeed(self, keywords, location, job_type="", experience=""):
        """Search Indeed for internships"""
        try:
            # Indeed search URL
            search_url = "https://www.indeed.com/jobs"
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
                
                for card in job_cards[:10]:  # Limit to 10 results
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
                                'logo': '📊'
                            }
                            self.results.append(job_data)
                    except Exception as e:
                        print(f"Error parsing Indeed job card: {e}")
                        
        except Exception as e:
            print(f"Error searching Indeed: {e}")
    
    def search_glassdoor(self, keywords, location, job_type="", experience=""):
        """Search Glassdoor for internships"""
        try:
            # Glassdoor search URL
            search_url = "https://www.glassdoor.com/Job/jobs.htm"
            params = {
                'sc.keyword': f"{keywords} intern internship",
                'locT': 'C',
                'locId': '1147401',  # Default to Minneapolis
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
                
                for card in job_cards[:10]:  # Limit to 10 results
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
                                'logo': '🏢'
                            }
                            self.results.append(job_data)
                    except Exception as e:
                        print(f"Error parsing Glassdoor job card: {e}")
                        
        except Exception as e:
            print(f"Error searching Glassdoor: {e}")
    
    def search_internships_com(self, keywords, location, job_type="", experience=""):
        """Search Internships.com for internships"""
        try:
            # Internships.com search URL
            search_url = "https://www.internships.com/search"
            params = {
                'q': f"{keywords} intern internship",
                'location': location,
                'type': 'internship'
            }
            
            response = self.session.get(search_url, params=params)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                job_cards = soup.find_all('div', class_='position')
                
                for card in job_cards[:10]:  # Limit to 10 results
                    try:
                        title_elem = card.find('h3', class_='title')
                        company_elem = card.find('div', class_='company')
                        location_elem = card.find('div', class_='location')
                        link_elem = card.find('a', class_='position-link')
                        
                        if title_elem and company_elem:
                            job_data = {
                                'title': title_elem.get_text(strip=True),
                                'company': company_elem.get_text(strip=True),
                                'location': location_elem.get_text(strip=True) if location_elem else location,
                                'source': 'Internships.com',
                                'url': urljoin('https://www.internships.com', link_elem['href']) if link_elem else '',
                                'logo': '🎓'
                            }
                            self.results.append(job_data)
                    except Exception as e:
                        print(f"Error parsing Internships.com job card: {e}")
                        
        except Exception as e:
            print(f"Error searching Internships.com: {e}")
    
    def search_angel_list(self, keywords, location, job_type="", experience=""):
        """Search AngelList for internships"""
        try:
            # AngelList search URL
            search_url = "https://angel.co/jobs"
            params = {
                'keywords': f"{keywords} intern internship",
                'locations[]': location,
                'job_types[]': 'internship'
            }
            
            response = self.session.get(search_url, params=params)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                job_cards = soup.find_all('div', class_='listing')
                
                for card in job_cards[:10]:  # Limit to 10 results
                    try:
                        title_elem = card.find('div', class_='title')
                        company_elem = card.find('div', class_='company')
                        location_elem = card.find('div', class_='location')
                        link_elem = card.find('a', class_='listing-link')
                        
                        if title_elem and company_elem:
                            job_data = {
                                'title': title_elem.get_text(strip=True),
                                'company': company_elem.get_text(strip=True),
                                'location': location_elem.get_text(strip=True) if location_elem else location,
                                'source': 'AngelList',
                                'url': urljoin('https://angel.co', link_elem['href']) if link_elem else '',
                                'logo': '👼'
                            }
                            self.results.append(job_data)
                    except Exception as e:
                        print(f"Error parsing AngelList job card: {e}")
                        
        except Exception as e:
            print(f"Error searching AngelList: {e}")
    
    def search_all_sources(self, keywords, location, job_type="", experience="", sources=None):
        """Search all specified sources for internships"""
        if sources is None:
            sources = ['linkedin', 'indeed', 'glassdoor', 'internships', 'angellist']
        
        self.results = []
        
        print(f"🔍 Searching for: {keywords} in {location}")
        print(f"📋 Sources: {', '.join(sources)}")
        print(f"🏢 Job Type: {job_type}")
        print(f"👤 Experience: {experience}")
        
        for source in sources:
            print(f"\n🔎 Searching {source.title()}...")
            
            if source == 'linkedin':
                self.search_linkedin(keywords, location, job_type, experience)
            elif source == 'indeed':
                self.search_indeed(keywords, location, job_type, experience)
            elif source == 'glassdoor':
                self.search_glassdoor(keywords, location, job_type, experience)
            elif source == 'internships':
                self.search_internships_com(keywords, location, job_type, experience)
            elif source == 'angellist':
                self.search_angel_list(keywords, location, job_type, experience)
            
            # Add delay to be respectful to websites
            time.sleep(random.uniform(1, 3))
        
        print(f"\n✅ Found {len(self.results)} internships!")
        return self.results
    
    def get_results(self):
        """Return all found results"""
        return self.results
    
    def save_results(self, filename="internship_results.json"):
        """Save results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"💾 Results saved to {filename}")

# Example usage
if __name__ == "__main__":
    scraper = RealInternshipScraper()
    
    # Search for internships
    results = scraper.search_all_sources(
        keywords="machine learning",
        location="Minneapolis",
        job_type="remote",
        experience="entry",
        sources=['linkedin', 'indeed', 'glassdoor']
    )
    
    # Print results
    for i, job in enumerate(results, 1):
        print(f"\n{i}. {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   Source: {job['source']}")
        print(f"   URL: {job['url']}")
    
    # Save results
    scraper.save_results() 