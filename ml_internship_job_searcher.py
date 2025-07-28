import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from collections import Counter
import json

class MLInternshipJobSearcher:
    def __init__(self):
        self.jobs_data = []
        self.requirements_analysis = {
            'skills': Counter(),
            'education': Counter(),
            'experience': Counter(),
            'tools': Counter(),
            'frameworks': Counter(),
            'languages': Counter(),
            'platforms': Counter()
        }
        
    def search_linkedin_jobs(self, query="machine learning engineer internship", location="United States", num_pages=3):
        """Search LinkedIn for ML Engineer internship jobs"""
        print(f"Searching LinkedIn for: {query}")
        
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
        
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            # LinkedIn jobs search URL
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={query.replace(' ', '%20')}&location={location.replace(' ', '%20')}&f_E=1"  # f_E=1 filters for entry level/internships
            driver.get(search_url)
            time.sleep(3)
            
            for page in range(num_pages):
                print(f"Scraping page {page + 1}...")
                
                # Get job listings
                job_cards = driver.find_elements(By.CLASS_NAME, "job-search-card")
                
                for card in job_cards[:10]:  # Limit to 10 jobs per page
                    try:
                        # Extract job info
                        title_elem = card.find_element(By.CLASS_NAME, "job-search-card__title")
                        company_elem = card.find_element(By.CLASS_NAME, "job-search-card__subtitle")
                        location_elem = card.find_element(By.CLASS_NAME, "job-search-card__location")
                        
                        title = title_elem.text.strip()
                        company = company_elem.text.strip()
                        location = location_elem.text.strip()
                        
                        # Click on job to get details
                        card.click()
                        time.sleep(2)
                        
                        # Get job description
                        try:
                            description_elem = driver.find_element(By.CLASS_NAME, "show-more-less-html__markup")
                            description = description_elem.text.strip()
                        except:
                            description = "Description not available"
                        
                        # Extract requirements from description
                        requirements = self.extract_requirements(description)
                        
                        job_data = {
                            'title': title,
                            'company': company,
                            'location': location,
                            'description': description,
                            'requirements': requirements,
                            'source': 'LinkedIn'
                        }
                        
                        self.jobs_data.append(job_data)
                        self.analyze_requirements(requirements)
                        
                        print(f"  - {title} at {company}")
                        
                    except Exception as e:
                        print(f"Error processing job card: {e}")
                        continue
                
                # Go to next page
                try:
                    next_button = driver.find_element(By.CLASS_NAME, "artdeco-pagination__button--next")
                    if next_button.is_enabled():
                        next_button.click()
                        time.sleep(3)
                    else:
                        break
                except:
                    break
                    
        finally:
            driver.quit()
    
    def search_indeed_jobs(self, query="machine learning engineer internship", location="United States", num_pages=3):
        """Search Indeed for ML Engineer internship jobs"""
        print(f"Searching Indeed for: {query}")
        
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
        
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            # Indeed jobs search URL
            search_url = f"https://www.indeed.com/jobs?q={query.replace(' ', '+')}&l={location.replace(' ', '+')}&jt=internship"
            driver.get(search_url)
            time.sleep(3)
            
            for page in range(num_pages):
                print(f"Scraping page {page + 1}...")
                
                # Get job listings
                job_cards = driver.find_elements(By.CLASS_NAME, "job_seen_beacon")
                
                for card in job_cards[:10]:  # Limit to 10 jobs per page
                    try:
                        # Extract job info
                        title_elem = card.find_element(By.CLASS_NAME, "jobTitle")
                        company_elem = card.find_element(By.CLASS_NAME, "companyName")
                        location_elem = card.find_element(By.CLASS_NAME, "companyLocation")
                        
                        title = title_elem.text.strip()
                        company = company_elem.text.strip()
                        location = location_elem.text.strip()
                        
                        # Click on job to get details
                        card.click()
                        time.sleep(2)
                        
                        # Get job description
                        try:
                            description_elem = driver.find_element(By.ID, "jobDescriptionText")
                            description = description_elem.text.strip()
                        except:
                            description = "Description not available"
                        
                        # Extract requirements from description
                        requirements = self.extract_requirements(description)
                        
                        job_data = {
                            'title': title,
                            'company': company,
                            'location': location,
                            'description': description,
                            'requirements': requirements,
                            'source': 'Indeed'
                        }
                        
                        self.jobs_data.append(job_data)
                        self.analyze_requirements(requirements)
                        
                        print(f"  - {title} at {company}")
                        
                    except Exception as e:
                        print(f"Error processing job card: {e}")
                        continue
                
                # Go to next page
                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, "[aria-label='Next Page']")
                    if next_button.is_enabled():
                        next_button.click()
                        time.sleep(3)
                    else:
                        break
                except:
                    break
                    
        finally:
            driver.quit()
    
    def extract_requirements(self, description):
        """Extract requirements from job description"""
        requirements = {
            'skills': [],
            'education': [],
            'experience': [],
            'tools': [],
            'frameworks': [],
            'languages': [],
            'platforms': []
        }
        
        description_lower = description.lower()
        
        # Define skill categories
        ml_skills = [
            'machine learning', 'deep learning', 'artificial intelligence', 'ai', 'ml',
            'natural language processing', 'nlp', 'computer vision', 'cv',
            'neural networks', 'cnn', 'rnn', 'lstm', 'transformer', 'bert', 'gpt',
            'reinforcement learning', 'rl', 'supervised learning', 'unsupervised learning',
            'data science', 'statistics', 'linear algebra', 'calculus', 'probability',
            'optimization', 'feature engineering', 'model training', 'model evaluation'
        ]
        
        programming_languages = [
            'python', 'java', 'c++', 'c#', 'javascript', 'r', 'matlab', 'scala',
            'go', 'rust', 'julia', 'sql', 'bash', 'shell'
        ]
        
        frameworks_libraries = [
            'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'numpy', 'pandas',
            'matplotlib', 'seaborn', 'plotly', 'jupyter', 'opencv', 'pillow',
            'spacy', 'nltk', 'gensim', 'transformers', 'hugging face', 'fastai',
            'xgboost', 'lightgbm', 'catboost', 'spark', 'hadoop', 'kafka'
        ]
        
        tools_platforms = [
            'git', 'github', 'docker', 'kubernetes', 'aws', 'azure', 'gcp',
            'google cloud', 'amazon web services', 'microsoft azure',
            'jira', 'confluence', 'slack', 'teams', 'zoom', 'microsoft office',
            'excel', 'powerpoint', 'word', 'tableau', 'power bi', 'looker'
        ]
        
        education_keywords = [
            'bachelor', 'master', 'phd', 'ph.d', 'degree', 'graduation',
            'computer science', 'cs', 'engineering', 'mathematics', 'math',
            'statistics', 'data science', 'machine learning', 'ai'
        ]
        
        experience_keywords = [
            'experience', 'years', 'internship', 'co-op', 'project',
            'research', 'publication', 'paper', 'conference', 'workshop',
            'hackathon', 'competition', 'kaggle', 'github', 'portfolio'
        ]
        
        # Extract skills
        for skill in ml_skills:
            if skill in description_lower:
                requirements['skills'].append(skill)
        
        # Extract programming languages
        for lang in programming_languages:
            if lang in description_lower:
                requirements['languages'].append(lang)
        
        # Extract frameworks and libraries
        for framework in frameworks_libraries:
            if framework in description_lower:
                requirements['frameworks'].append(framework)
        
        # Extract tools and platforms
        for tool in tools_platforms:
            if tool in description_lower:
                requirements['tools'].append(tool)
        
        # Extract education requirements
        for edu in education_keywords:
            if edu in description_lower:
                requirements['education'].append(edu)
        
        # Extract experience requirements
        for exp in experience_keywords:
            if exp in description_lower:
                requirements['experience'].append(exp)
        
        return requirements
    
    def analyze_requirements(self, requirements):
        """Analyze and count requirements"""
        for category, items in requirements.items():
            for item in items:
                self.requirements_analysis[category][item] += 1
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        print("\n" + "="*80)
        print("MACHINE LEARNING ENGINEER INTERNSHIP ANALYSIS REPORT")
        print("="*80)
        
        print(f"\n📊 Total Jobs Analyzed: {len(self.jobs_data)}")
        
        # Top companies hiring
        companies = [job['company'] for job in self.jobs_data]
        company_counts = Counter(companies)
        print(f"\n🏢 Top Companies Hiring ML Interns:")
        for company, count in company_counts.most_common(10):
            print(f"  {company}: {count} positions")
        
        # Most common requirements
        print(f"\n🎯 MOST COMMON REQUIREMENTS:")
        
        print(f"\n💻 Programming Languages:")
        for lang, count in self.requirements_analysis['languages'].most_common(10):
            print(f"  {lang.title()}: {count} mentions")
        
        print(f"\n🔧 Frameworks & Libraries:")
        for framework, count in self.requirements_analysis['frameworks'].most_common(10):
            print(f"  {framework.title()}: {count} mentions")
        
        print(f"\n🛠️ Tools & Platforms:")
        for tool, count in self.requirements_analysis['tools'].most_common(10):
            print(f"  {tool.title()}: {count} mentions")
        
        print(f"\n🧠 ML/AI Skills:")
        for skill, count in self.requirements_analysis['skills'].most_common(10):
            print(f"  {skill.title()}: {count} mentions")
        
        print(f"\n🎓 Education Requirements:")
        for edu, count in self.requirements_analysis['education'].most_common(10):
            print(f"  {edu.title()}: {count} mentions")
        
        print(f"\n📈 Experience Keywords:")
        for exp, count in self.requirements_analysis['experience'].most_common(10):
            print(f"  {exp.title()}: {count} mentions")
        
        # Save detailed data
        self.save_data()
        
        # Generate recommendations
        self.generate_recommendations()
    
    def save_data(self):
        """Save job data to CSV and JSON"""
        # Save job listings
        df = pd.DataFrame(self.jobs_data)
        df.to_csv('ml_internship_jobs.csv', index=False)
        
        # Save requirements analysis
        with open('ml_internship_requirements.json', 'w') as f:
            json.dump({k: dict(v) for k, v in self.requirements_analysis.items()}, f, indent=2)
        
        print(f"\n💾 Data saved to:")
        print(f"  - ml_internship_jobs.csv ({len(self.jobs_data)} jobs)")
        print(f"  - ml_internship_requirements.json (requirements analysis)")
    
    def generate_recommendations(self):
        """Generate recommendations based on analysis"""
        print(f"\n" + "="*80)
        print("RECOMMENDATIONS FOR ML ENGINEER INTERNSHIPS")
        print("="*80)
        
        # Get top requirements
        top_languages = [lang for lang, _ in self.requirements_analysis['languages'].most_common(5)]
        top_frameworks = [fw for fw, _ in self.requirements_analysis['frameworks'].most_common(5)]
        top_tools = [tool for tool, _ in self.requirements_analysis['tools'].most_common(5)]
        top_skills = [skill for skill, _ in self.requirements_analysis['skills'].most_common(5)]
        
        print(f"\n🎯 PRIORITY SKILLS TO LEARN:")
        print(f"1. Programming Languages: {', '.join(top_languages)}")
        print(f"2. ML Frameworks: {', '.join(top_frameworks)}")
        print(f"3. Tools & Platforms: {', '.join(top_tools)}")
        print(f"4. Core Skills: {', '.join(top_skills)}")
        
        print(f"\n📚 LEARNING RECOMMENDATIONS:")
        print(f"1. Start with Python (most in-demand language)")
        print(f"2. Learn TensorFlow or PyTorch (most popular frameworks)")
        print(f"3. Master Git/GitHub (essential for collaboration)")
        print(f"4. Build projects using scikit-learn and pandas")
        print(f"5. Practice with Jupyter notebooks")
        
        print(f"\n💼 APPLICATION STRATEGY:")
        print(f"1. Focus on companies with multiple openings")
        print(f"2. Highlight relevant projects in your portfolio")
        print(f"3. Emphasize hands-on experience with ML tools")
        print(f"4. Show proficiency in Python and data science libraries")
        print(f"5. Demonstrate understanding of ML fundamentals")

def main():
    searcher = MLInternshipJobSearcher()
    
    # Search multiple platforms
    print("🔍 Starting ML Engineer Internship Job Search...")
    
    # Search LinkedIn
    try:
        searcher.search_linkedin_jobs("machine learning engineer internship", "United States", 2)
    except Exception as e:
        print(f"LinkedIn search failed: {e}")
    
    # Search Indeed
    try:
        searcher.search_indeed_jobs("machine learning engineer internship", "United States", 2)
    except Exception as e:
        print(f"Indeed search failed: {e}")
    
    # Generate report
    if searcher.jobs_data:
        searcher.generate_report()
    else:
        print("No jobs found. Please check your internet connection and try again.")

if __name__ == "__main__":
    main() 