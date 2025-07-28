import csv
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
import os

SEARCH_QUERIES = [
    'intitle:"machine learning engineer" resume filetype:pdf',
    'site:linkedin.com/in/ "machine learning engineer" AND (AI OR artificial intelligence)',
    'site:github.com "machine learning" OR "AI" in:readme',
    'site:github.io "machine learning" portfolio',
    'AI student resume OR portfolio',
]

NUM_RESULTS = 20
OUTPUT_CSV = 'top_resumes.csv'

# Email config (prompt user for these)
def get_email_config():
    print("Enter your Gmail address (for sending the results):")
    sender = input().strip()
    print("Enter your Gmail app password (see https://support.google.com/accounts/answer/185833):")
    password = input().strip()
    print("Enter the recipient email address:")
    recipient = input().strip()
    return sender, password, recipient

def send_email_with_attachment(sender, password, recipient, subject, body, filename):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    with open(filename, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(filename)}')
        msg.attach(part)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
        print(f"Email sent to {recipient}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def google_search_selenium(query, num_results=10):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
    driver = webdriver.Chrome(options=chrome_options)
    results = []
    try:
        driver.get('https://www.google.com')
        time.sleep(2)
        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys(query)
        search_box.submit()
        time.sleep(2)
        if "detected unusual traffic" in driver.page_source or "captcha" in driver.page_source.lower():
            print("CAPTCHA detected! Please solve it in the browser window, then press Enter here to continue...")
            input()
        for _ in range(num_results // 10):
            print("--- Google page source (first 500 chars) ---")
            print(driver.page_source[:500])
            soup = BeautifulSoup(driver.page_source, "html.parser")
            found = False
            # Try multiple selectors for Google results
            for g in soup.find_all('div', class_='g'):
                link = g.find('a', href=True)
                title = g.find('h3')
                if link and title:
                    results.append({
                        'title': title.text,
                        'url': link['href']
                    })
                    found = True
            # Try alternative selectors (new Google layouts)
            if not found:
                for g in soup.select('a h3'):
                    link = g.find_parent('a', href=True)
                    if link and g.text:
                        results.append({
                            'title': g.text,
                            'url': link['href']
                        })
                        found = True
            if not found:
                print("[Warning] No results found on this page. Google may have changed its layout or is blocking automation.")
            # Try to go to next page
            try:
                next_btn = driver.find_element(By.ID, 'pnnext')
                next_btn.click()
                time.sleep(2)
            except Exception:
                break
    finally:
        driver.quit()
    return results

def extract_summary(url):
    try:
        resp = requests.get(url, timeout=8)
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text(" ", strip=True)
        # Heuristics for skills/projects
        skills = re.findall(r"Skills?[:\s]+([A-Za-z0-9, .\-_/]+)", text, re.IGNORECASE)
        projects = re.findall(r"Projects?[:\s]+([A-Za-z0-9, .\-_/]+)", text, re.IGNORECASE)
        # Fallback: look for keywords
        if not skills:
            skills = re.findall(r"Python|TensorFlow|PyTorch|scikit-learn|Keras|Flask|Streamlit|SQL|NLP|Machine Learning|Deep Learning", text, re.IGNORECASE)
        if not projects:
            projects = re.findall(r"[A-Z][A-Za-z0-9\- ]{8,40}", text)
        return {
            'skills': ', '.join(set(skills))[:120],
            'projects': ', '.join(set(projects))[:120]
        }
    except Exception as e:
        return {'skills': '', 'projects': ''}

def main():
    all_results = []
    for query in SEARCH_QUERIES:
        print(f"Searching: {query}")
        results = google_search_selenium(query, num_results=NUM_RESULTS)
        for r in results:
            print(f"Extracting: {r['title']} - {r['url']}")
            summary = extract_summary(r['url'])
            all_results.append({
                'Title': r['title'],
                'URL': r['url'],
                'Skills': summary['skills'],
                'Projects': summary['projects']
            })
    # Save to CSV
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Title', 'URL', 'Skills', 'Projects'])
        writer.writeheader()
        for row in all_results:
            writer.writerow(row)
    print(f"Saved {len(all_results)} results to {OUTPUT_CSV}")
    # Email the file
    sender, password, recipient = get_email_config()
    send_email_with_attachment(sender, password, recipient, "Top AI/ML Resumes & Portfolios", "See attached CSV for results.", OUTPUT_CSV)

if __name__ == "__main__":
    main() 