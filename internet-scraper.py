#!/usr/bin/env python3
"""
Real Internet Internship Scraper
This script actually searches the internet for internships using real web scraping.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import quote
import sys

def search_linkedin_internships(keyword="software engineer", location="United States"):
    """Search LinkedIn for real internships"""
    print(f"🔍 Searching LinkedIn for {keyword} internships in {location}...")
    
    try:
        # LinkedIn search URL
        encoded_keyword = quote(f"{keyword} internship")
        encoded_location = quote(location)
        search_url = f"https://www.linkedin.com/jobs/search/?keywords={encoded_keyword}&location={encoded_location}&f_E=1&f_JT=I&position=1&pageNum=0"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        response = requests.get(search_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find job cards
            job_cards = soup.find_all('div', class_='base-card')
            print(f"Found {len(job_cards)} job cards on LinkedIn")
            
            internships = []
            for card in job_cards[:10]:  # Limit to 10 results
                try:
                    title_elem = card.find('h3', class_='base-search-card__title')
                    company_elem = card.find('h4', class_='base-search-card__subtitle')
                    location_elem = card.find('span', class_='job-search-card__location')
                    link_elem = card.find('a', class_='base-card__full-link')
                    
                    if title_elem and company_elem and link_elem:
                        title = title_elem.get_text(strip=True)
                        company = company_elem.get_text(strip=True)
                        job_location = location_elem.get_text(strip=True) if location_elem else "Remote"
                        apply_url = link_elem['href']
                        
                        # Only add if it's actually an internship
                        if 'intern' in title.lower() or 'internship' in title.lower():
                            internships.append({
                                'title': title,
                                'company': company,
                                'location': job_location,
                                'applyUrl': apply_url,
                                'source': 'LinkedIn'
                            })
                            print(f"✅ Found: {title} at {company}")
                except Exception as e:
                    continue
            
            return internships
        else:
            print(f"LinkedIn returned status code: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"LinkedIn scraping error: {e}")
        return []

def search_indeed_internships(keyword="software engineer", location="United States"):
    """Search Indeed for real internships"""
    print(f"🔍 Searching Indeed for {keyword} internships in {location}...")
    
    try:
        # Indeed search URL
        encoded_keyword = quote(f"{keyword} internship")
        encoded_location = quote(location)
        search_url = f"https://www.indeed.com/jobs?q={encoded_keyword}&l={encoded_location}&jt=internship&sort=date"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        response = requests.get(search_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find job cards
            job_cards = soup.find_all('div', class_='job_seen_beacon')
            print(f"Found {len(job_cards)} job cards on Indeed")
            
            internships = []
            for card in job_cards[:10]:  # Limit to 10 results
                try:
                    title_elem = card.find('h2', class_='jobTitle')
                    company_elem = card.find('span', class_='companyName')
                    location_elem = card.find('div', class_='companyLocation')
                    link_elem = card.find('a', class_='jcs-JobTitle')
                    
                    if title_elem and company_elem and link_elem:
                        title = title_elem.get_text(strip=True)
                        company = company_elem.get_text(strip=True)
                        job_location = location_elem.get_text(strip=True) if location_elem else "Remote"
                        apply_url = "https://www.indeed.com" + link_elem['href']
                        
                        # Only add if it's actually an internship
                        if 'intern' in title.lower() or 'internship' in title.lower():
                            internships.append({
                                'title': title,
                                'company': company,
                                'location': job_location,
                                'applyUrl': apply_url,
                                'source': 'Indeed'
                            })
                            print(f"✅ Found: {title} at {company}")
                except Exception as e:
                    continue
            
            return internships
        else:
            print(f"Indeed returned status code: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Indeed scraping error: {e}")
        return []

def search_real_internships(keyword="software engineer", location="United States"):
    """Search multiple job sites for real internships"""
    print(f"🚀 Starting real internet search for {keyword} internships in {location}")
    print("=" * 60)
    
    all_internships = []
    
    # Search LinkedIn
    linkedin_results = search_linkedin_internships(keyword, location)
    all_internships.extend(linkedin_results)
    print(f"✅ Found {len(linkedin_results)} internships on LinkedIn")
    
    # Search Indeed
    indeed_results = search_indeed_internships(keyword, location)
    all_internships.extend(indeed_results)
    print(f"✅ Found {len(indeed_results)} internships on Indeed")
    
    # Remove duplicates
    unique_internships = []
    seen_titles = set()
    for internship in all_internships:
        if internship['title'] not in seen_titles:
            unique_internships.append(internship)
            seen_titles.add(internship['title'])
    
    print(f"\n🎯 Total unique internships found: {len(unique_internships)}")
    print("=" * 60)
    
    return unique_internships

def main():
    """Main function to run the scraper"""
    if len(sys.argv) < 3:
        print("Usage: python3 internet-scraper.py 'job type' 'location'")
        print("Example: python3 internet-scraper.py 'software engineer' 'San Francisco'")
        print("Example: python3 internet-scraper.py 'data science' 'New York'")
        print("Example: python3 internet-scraper.py 'machine learning' 'Remote'")
        return
    
    keyword = sys.argv[1]
    location = sys.argv[2]
    
    print(f"🔍 Searching for {keyword} internships in {location}")
    print("This will search real job sites on the internet...")
    print()
    
    results = search_real_internships(keyword, location)
    
    if results:
        print(f"\n📋 Found {len(results)} internships:")
        print("-" * 50)
        for i, internship in enumerate(results, 1):
            print(f"\n{i}. {internship['title']}")
            print(f"   Company: {internship['company']}")
            print(f"   Location: {internship['location']}")
            print(f"   Source: {internship['source']}")
            print(f"   Apply: {internship['applyUrl']}")
    else:
        print("\n❌ No internships found. Try different search terms.")
    
    print(f"\n✅ Search completed! Found {len(results)} real internships from the internet.")

if __name__ == "__main__":
    main() 