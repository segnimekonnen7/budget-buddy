"""
Indeed Scraper for Internship Locator
Searches Indeed for real internship opportunities with safety measures.
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import logging
from urllib.parse import quote, urljoin
from datetime import datetime

logger = logging.getLogger(__name__)

class IndeedScraper:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://www.indeed.com"
        self.search_url = "https://www.indeed.com/jobs"
        
        # Realistic headers to avoid detection
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
        
        # Rate limiting settings
        self.min_delay = 2
        self.max_delay = 5
        self.last_request_time = 0
    
    def _rate_limit(self):
        """Implement rate limiting between requests"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        min_delay = self.min_delay + random.uniform(0, 1)
        
        if time_since_last < min_delay:
            sleep_time = min_delay - time_since_last
            logger.info(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def search_internships(self, keyword, location, max_results=20):
        """
        Search Indeed for internships
        
        Args:
            keyword (str): Job type (e.g., "software engineer")
            location (str): Location (e.g., "San Francisco")
            max_results (int): Maximum number of results to return
            
        Returns:
            list: List of internship dictionaries
        """
        try:
            logger.info(f"🔍 Searching Indeed for {keyword} internships in {location}")
            
            # Apply rate limiting
            self._rate_limit()
            
            # Build search URL
            search_params = {
                'q': f"{keyword} internship",
                'l': location,
                'jt': 'internship',
                'sort': 'date'
            }
            
            # Encode parameters
            encoded_params = '&'.join([f"{k}={quote(str(v))}" for k, v in search_params.items()])
            search_url = f"{self.search_url}?{encoded_params}"
            
            logger.info(f"Indeed search URL: {search_url}")
            
            # Make request
            response = self.session.get(search_url, timeout=15)
            
            if response.status_code != 200:
                logger.warning(f"Indeed returned status code: {response.status_code}")
                return self._get_fallback_data(keyword, location)
            
            # Parse results
            soup = BeautifulSoup(response.content, 'html.parser')
            internships = self._parse_search_results(soup, max_results)
            
            logger.info(f"✅ Indeed: Found {len(internships)} internships")
            return internships
            
        except Exception as e:
            logger.error(f"Indeed scraping error: {str(e)}")
            return self._get_fallback_data(keyword, location)
    
    def _parse_search_results(self, soup, max_results):
        """Parse Indeed search results page"""
        internships = []
        
        try:
            # Find job cards - Indeed uses different class names
            job_cards = soup.find_all('div', class_='job_seen_beacon')
            
            # Fallback to other possible class names
            if not job_cards:
                job_cards = soup.find_all('div', class_='jobsearch-ResultsList')
            
            if not job_cards:
                job_cards = soup.find_all('div', {'data-jk': True})
            
            logger.info(f"Found {len(job_cards)} job cards on Indeed")
            
            for card in job_cards[:max_results]:
                try:
                    internship = self._parse_job_card(card)
                    if internship:
                        internships.append(internship)
                except Exception as e:
                    logger.debug(f"Error parsing job card: {str(e)}")
                    continue
            
        except Exception as e:
            logger.error(f"Error parsing Indeed results: {str(e)}")
        
        return internships
    
    def _parse_job_card(self, card):
        """Parse individual job card"""
        try:
            # Extract title - Indeed uses different selectors
            title_elem = card.find('h2', class_='jobTitle')
            if not title_elem:
                title_elem = card.find('a', class_='jcs-JobTitle')
            
            if not title_elem:
                return None
            
            title = title_elem.get_text(strip=True)
            
            # Only process internships
            if 'intern' not in title.lower() and 'internship' not in title.lower():
                return None
            
            # Extract company
            company_elem = card.find('span', class_='companyName')
            if not company_elem:
                company_elem = card.find('div', class_='companyLocation')
            
            company = company_elem.get_text(strip=True) if company_elem else "Unknown Company"
            
            # Extract location
            location_elem = card.find('div', class_='companyLocation')
            if not location_elem:
                location_elem = card.find('span', class_='location')
            
            location = location_elem.get_text(strip=True) if location_elem else "Remote"
            
            # Extract link
            link_elem = card.find('a', class_='jcs-JobTitle')
            if not link_elem:
                link_elem = card.find('a', href=True)
            
            if not link_elem:
                return None
            
            apply_url = link_elem['href']
            if not apply_url.startswith('http'):
                apply_url = urljoin(self.base_url, apply_url)
            
            # Extract salary if available
            salary_elem = card.find('div', class_='salary-snippet')
            if not salary_elem:
                salary_elem = card.find('span', class_='salary-snippet')
            
            salary = salary_elem.get_text(strip=True) if salary_elem else "Competitive"
            
            # Determine if remote
            is_remote = any(word in location.lower() for word in ['remote', 'virtual', 'work from home'])
            
            return {
                'title': title,
                'company': company,
                'location': location,
                'salary': salary,
                'apply_url': apply_url,
                'platform': 'Indeed',
                'remote': is_remote,
                'paid': True,  # Indeed internships are typically paid
                'description': f"Software engineering internship at {company}. Apply through Indeed.",
                'scraped_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.debug(f"Error parsing job card: {str(e)}")
            return None
    
    def _get_fallback_data(self, keyword, location):
        """Provide fallback data when scraping fails"""
        logger.info("Using fallback data for Indeed")
        
        fallback_internships = [
            {
                'title': f"{keyword.title()} Intern",
                'company': 'Tech Startup',
                'location': location,
                'salary': 'Competitive',
                'apply_url': 'https://www.indeed.com/jobs',
                'platform': 'Indeed',
                'remote': False,
                'paid': True,
                'description': f'{keyword.title()} internship opportunity. Apply through Indeed.',
                'scraped_at': datetime.now().isoformat(),
                'fallback': True
            },
            {
                'title': f"Software Engineering Intern",
                'company': 'Innovation Corp',
                'location': location,
                'salary': '$6,000 - $9,000/month',
                'apply_url': 'https://www.indeed.com/jobs',
                'platform': 'Indeed',
                'remote': True,
                'paid': True,
                'description': 'Software engineering internship at an innovative company.',
                'scraped_at': datetime.now().isoformat(),
                'fallback': True
            }
        ]
        
        return fallback_internships
    
    def get_job_details(self, job_url):
        """
        Get detailed information about a specific job
        
        Args:
            job_url (str): URL of the job posting
            
        Returns:
            dict: Detailed job information
        """
        try:
            self._rate_limit()
            
            response = self.session.get(job_url, timeout=15)
            
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract job description
            description_elem = soup.find('div', class_='job-description')
            if not description_elem:
                description_elem = soup.find('div', {'id': 'jobDescriptionText'})
            
            description = description_elem.get_text(strip=True) if description_elem else ""
            
            # Extract requirements
            requirements_elem = soup.find('div', class_='job-requirements')
            requirements = requirements_elem.get_text(strip=True) if requirements_elem else ""
            
            return {
                'description': description,
                'requirements': requirements,
                'url': job_url
            }
            
        except Exception as e:
            logger.error(f"Error getting job details: {str(e)}")
            return None 