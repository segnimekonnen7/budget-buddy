import pandas as pd
import re
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import numpy as np

def clean_text(text):
    """Clean and normalize text"""
    if pd.isna(text):
        return ""
    # Remove PDF metadata artifacts
    text = re.sub(r'[A-Za-z0-9]{8,}', '', text)  # Remove long alphanumeric strings
    text = re.sub(r'[0-9]+ 0 R', '', text)  # Remove PDF object references
    text = re.sub(r'[A-Za-z]+-[A-Za-z]+', '', text)  # Remove font names
    text = re.sub(r'Length\d*', '', text)  # Remove length references
    text = re.sub(r'Contents \d+ 0 R', '', text)  # Remove contents references
    text = re.sub(r'FontFile\d+ \d+ 0 R', '', text)  # Remove font file references
    text = re.sub(r'CreationDate', '', text)  # Remove creation date
    text = re.sub(r'Metadata \d+ 0 R', '', text)  # Remove metadata
    text = re.sub(r'StructParents \d+', '', text)  # Remove struct parents
    text = re.sub(r'MediaBox', '', text)  # Remove media box
    text = re.sub(r'Parent \d+ 0 R', '', text)  # Remove parent references
    text = re.sub(r'ToUnicode \d+ 0 R', '', text)  # Remove unicode references
    text = re.sub(r'Encoding', '', text)  # Remove encoding
    text = re.sub(r'Identity-H', '', text)  # Remove identity
    text = re.sub(r'Description rdf', '', text)  # Remove description
    text = re.sub(r'FontDescriptor \d+ 0 R', '', text)  # Remove font descriptor
    text = re.sub(r'FirstChar \d+', '', text)  # Remove first char
    text = re.sub(r'LastChar \d+', '', text)  # Remove last char
    text = re.sub(r'AvgWidth \d+', '', text)  # Remove avg width
    text = re.sub(r'CapHeight \d+', '', text)  # Remove cap height
    text = re.sub(r'Descent -\d+', '', text)  # Remove descent
    text = re.sub(r'CIDToGIDMap \d+ 0 R', '', text)  # Remove CID map
    text = re.sub(r'Supplement \d+', '', text)  # Remove supplement
    text = re.sub(r'PageMode', '', text)  # Remove page mode
    text = re.sub(r'Roman', '', text)  # Remove roman
    text = re.sub(r'XRefStm \d+', '', text)  # Remove xref
    text = re.sub(r'FlateDecode', '', text)  # Remove flate decode
    text = re.sub(r'JLxJLxJLx', '', text)  # Remove JLx pattern
    text = re.sub(r'KBjCLOhmKF8', '', text)  # Remove specific patterns
    text = re.sub(r'PxpxHxhxXx8', '', text)  # Remove specific patterns
    text = re.sub(r'IDPDdDlDRD', '', text)  # Remove specific patterns
    text = re.sub(r'Root \d+ 0 R', '', text)  # Remove root
    text = re.sub(r'FontStretch', '', text)  # Remove font stretch
    text = re.sub(r'Perceptual', '', text)  # Remove perceptual
    text = re.sub(r'Photoshop \d+', '', text)  # Remove photoshop
    text = re.sub(r'Picture \d+', '', text)  # Remove picture
    text = re.sub(r'Resources \d+ 0 R', '', text)  # Remove resources
    text = re.sub(r'R \d+ 0 R \d+ 0 R \d+ 0 R \d+ 0 R \d+ 0 R', '', text)  # Remove R patterns
    text = re.sub(r'P \d+ 0 R', '', text)  # Remove P patterns
    text = re.sub(r'TT6 \d+ 0 R', '', text)  # Remove TT6 patterns
    text = re.sub(r'MaxWidth \d+', '', text)  # Remove max width
    text = re.sub(r'CMESiSMuE', '', text)  # Remove CMES pattern
    text = re.sub(r'W5M0MpCehiHzreSzNTczkc9d', '', text)  # Remove W5M pattern
    text = re.sub(r'ViewerPreferences \d+ 0 R', '', text)  # Remove viewer preferences
    text = re.sub(r'Microsoft Office User', '', text)  # Remove MS Office
    text = re.sub(r'Word for Office 365 \d{4}-\d{2}-\d{2}T\d{2}', '', text)  # Remove Word timestamps
    text = re.sub(r'[A-F0-9]{32}', '', text)  # Remove 32-char hex strings
    text = re.sub(r'Microsoft', '', text)  # Remove Microsoft
    text = re.sub(r'CD26E82AA3E554EB655531E88C1B714', '', text)  # Remove specific hash
    text = re.sub(r'E471163C160CF4D9920531834330E31', '', text)  # Remove specific hash
    text = re.sub(r'StemV \d+', '', text)  # Remove StemV
    text = re.sub(r'FontAwesome5Brands-Regular', '', text)  # Remove FontAwesome
    text = re.sub(r'IEC 61966-2', '', text)  # Remove IEC
    text = re.sub(r'ColorSpa', '', text)  # Remove ColorSpa
    
    # Clean up extra whitespace and punctuation
    text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single
    text = re.sub(r'[^\w\s]', ' ', text)  # Remove special characters except spaces
    text = text.strip().lower()
    return text

def extract_skills_and_projects(df):
    """Extract skills and projects from the dataframe"""
    all_skills = []
    all_projects = []
    
    for _, row in df.iterrows():
        # Clean skills
        skills_text = clean_text(row['Skills'])
        if skills_text:
            skills = [skill.strip() for skill in skills_text.split(',') if skill.strip()]
            all_skills.extend(skills)
        
        # Clean projects
        projects_text = clean_text(row['Projects'])
        if projects_text:
            projects = [project.strip() for project in projects_text.split(',') if project.strip()]
            all_projects.extend(projects)
    
    return all_skills, all_projects

def analyze_titles(df):
    """Analyze job titles and patterns"""
    titles = df['Title'].dropna().tolist()
    
    # Extract common patterns
    title_patterns = {
        'machine_learning_engineer': 0,
        'ai_engineer': 0,
        'data_scientist': 0,
        'ml_engineer': 0,
        'senior': 0,
        'phd': 0,
        'student': 0,
        'portfolio': 0,
        'resume': 0
    }
    
    for title in titles:
        title_lower = title.lower()
        if 'machine learning engineer' in title_lower:
            title_patterns['machine_learning_engineer'] += 1
        if 'ai engineer' in title_lower or 'artificial intelligence' in title_lower:
            title_patterns['ai_engineer'] += 1
        if 'data scientist' in title_lower:
            title_patterns['data_scientist'] += 1
        if 'ml engineer' in title_lower:
            title_patterns['ml_engineer'] += 1
        if 'senior' in title_lower:
            title_patterns['senior'] += 1
        if 'phd' in title_lower or 'ph.d' in title_lower:
            title_patterns['phd'] += 1
        if 'student' in title_lower:
            title_patterns['student'] += 1
        if 'portfolio' in title_lower:
            title_patterns['portfolio'] += 1
        if 'resume' in title_lower:
            title_patterns['resume'] += 1
    
    return title_patterns

def analyze_urls(df):
    """Analyze URL patterns"""
    urls = df['URL'].dropna().tolist()
    
    url_patterns = {
        'linkedin': 0,
        'github': 0,
        'github.io': 0,
        'pdf': 0,
        'resume': 0,
        'portfolio': 0,
        'personal_website': 0
    }
    
    for url in urls:
        url_lower = url.lower()
        if 'linkedin.com' in url_lower:
            url_patterns['linkedin'] += 1
        if 'github.com' in url_lower:
            url_patterns['github'] += 1
        if 'github.io' in url_lower:
            url_patterns['github.io'] += 1
        if '.pdf' in url_lower:
            url_patterns['pdf'] += 1
        if 'resume' in url_lower:
            url_patterns['resume'] += 1
        if 'portfolio' in url_lower:
            url_patterns['portfolio'] += 1
        if any(domain in url_lower for domain in ['.com', '.org', '.net', '.io']) and not any(platform in url_lower for platform in ['linkedin.com', 'github.com']):
            url_patterns['personal_website'] += 1
    
    return url_patterns

def main():
    # Read the CSV file
    df = pd.read_csv('top_resumes.csv')
    
    print("=== RESUME ANALYSIS REPORT ===\n")
    print(f"Total resumes collected: {len(df)}")
    print(f"Columns: {list(df.columns)}\n")
    
    # Analyze titles
    print("=== JOB TITLE PATTERNS ===")
    title_patterns = analyze_titles(df)
    for pattern, count in title_patterns.items():
        if count > 0:
            print(f"{pattern.replace('_', ' ').title()}: {count}")
    print()
    
    # Analyze URLs
    print("=== URL PATTERNS ===")
    url_patterns = analyze_urls(df)
    for pattern, count in url_patterns.items():
        if count > 0:
            print(f"{pattern.replace('_', ' ').title()}: {count}")
    print()
    
    # Extract and analyze skills
    print("=== SKILLS ANALYSIS ===")
    all_skills, all_projects = extract_skills_and_projects(df)
    
    # Count skills
    skill_counter = Counter(all_skills)
    print("Most common skills:")
    for skill, count in skill_counter.most_common(15):
        if len(skill) > 2:  # Filter out very short strings
            print(f"  {skill}: {count}")
    print()
    
    # Count projects
    project_counter = Counter(all_projects)
    print("Most common project keywords:")
    for project, count in project_counter.most_common(10):
        if len(project) > 3:  # Filter out very short strings
            print(f"  {project}: {count}")
    print()
    
    # Analyze data quality
    print("=== DATA QUALITY ANALYSIS ===")
    skills_filled = df['Skills'].notna().sum()
    projects_filled = df['Projects'].notna().sum()
    print(f"Resumes with skills data: {skills_filled}/{len(df)} ({skills_filled/len(df)*100:.1f}%)")
    print(f"Resumes with projects data: {projects_filled}/{len(df)} ({projects_filled/len(df)*100:.1f}%)")
    print()
    
    # Key findings
    print("=== KEY FINDINGS ===")
    print("1. Most resumes are from LinkedIn profiles and personal websites")
    print("2. Common job titles include 'Machine Learning Engineer' and 'AI Engineer'")
    print("3. Many resumes are in PDF format")
    print("4. Skills data extraction was limited due to PDF parsing challenges")
    print("5. Portfolio websites are common for ML/AI professionals")
    print("6. GitHub presence is strong in this field")
    print()
    
    # Recommendations
    print("=== RECOMMENDATIONS FOR IMPROVEMENT ===")
    print("1. Improve PDF text extraction to get better skills/projects data")
    print("2. Focus on LinkedIn profiles for more structured data")
    print("3. Add more specific search queries for different ML/AI roles")
    print("4. Implement better text cleaning for PDF metadata artifacts")
    print("5. Consider using OCR for better PDF content extraction")

if __name__ == "__main__":
    main() knowi