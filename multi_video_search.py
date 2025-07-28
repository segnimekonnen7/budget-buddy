import time
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

EMAIL_FROM = 'grimes2020rick@gmail.com'
EMAIL_TO = 'grimes2020rick@gmail.com'
EMAIL_PASS = 'lbgl rpkm okbp soan'  # Use an app password

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument(f'user-data-dir=/Users/segnimekonnen/multi_video_search_profile')
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
chrome_options.add_argument(f'user-agent={user_agent}')

PLATFORMS = [
    'youtube',
    'vimeo',
    'dailymotion',
    'tiktok',
    'facebook',
    'bilibili',
    'google_videos',
]

SEARCH_URLS = {
    'youtube': 'https://www.youtube.com/results?search_query={}',
    'vimeo': 'https://vimeo.com/search?q={}',
    'dailymotion': 'https://www.dailymotion.com/search/{}',
    'tiktok': 'https://www.tiktok.com/search?q={}',
    'facebook': 'https://www.facebook.com/search/videos/?q={}',
    'bilibili': 'https://search.bilibili.com/all?keyword={}',
    'google_videos': 'https://www.google.com/search?q={}&tbm=vid',
}

XPATHS = {
    'youtube': "//a[@id='video-title']",
    'vimeo': "//a[contains(@href, '/video/') and @data-clip-id]",
    'dailymotion': "//a[contains(@href, '/video/') and @class='video_link']",
    'tiktok': "//a[contains(@href, '/video/') or contains(@href, '/@')]",
    'facebook': "//a[contains(@href, '/videos/') or contains(@href, '/watch/?v=')]",
    'bilibili': "//a[contains(@href, '/video/') and @target='_blank']",
    'google_videos': "//a[@href and (contains(@href, 'youtube.com') or contains(@href, 'vimeo.com') or contains(@href, 'dailymotion.com') or contains(@href, 'tiktok.com') or contains(@href, 'facebook.com') or contains(@href, 'bilibili.com'))]",
}

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASS)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    print(f"Email sent to {EMAIL_TO}")

def search_platform(driver, platform, query, max_results=20):
    url = SEARCH_URLS[platform].format(query.replace(' ', '+'))
    driver.get(url)
    time.sleep(5)
    results = []
    seen = set()
    try:
        elements = driver.find_elements(By.XPATH, XPATHS[platform])
        for el in elements:
            href = el.get_attribute('href')
            title = el.text.strip()
            if href and title and href not in seen:
                results.append({'title': title, 'url': href, 'platform': platform})
                seen.add(href)
            if len(results) >= max_results:
                break
    except Exception as e:
        pass
    return results

def main():
    query = input('Enter your video search query: ')
    all_results = []
    with webdriver.Chrome(options=chrome_options) as driver:
        for platform in PLATFORMS:
            print(f"Searching {platform}...")
            results = search_platform(driver, platform, query, max_results=20)
            all_results.extend(results)
    # Deduplicate by URL
    unique_results = {r['url']: r for r in all_results}.values()
    if not unique_results:
        body = f"No videos found for query: {query}"
    else:
        body = f"Video search results for: {query}\n\n"
        for i, r in enumerate(unique_results, 1):
            body += f"{i}. [{r['platform'].capitalize()}] {r['title']}\n{r['url']}\n\n"
    send_email(f"Video search results for: {query}", body)

if __name__ == '__main__':
    main() 