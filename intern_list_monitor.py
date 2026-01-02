"""
Intern-List.com Internship Monitor
-----------------------------------
Continuously monitors intern-list.com for new internships and sends email
notifications with summaries when new postings are detected.
"""

import json
import os
import smtplib
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# Configuration
INTERN_LIST_URL = "https://www.intern-list.com/"
# Software Engineering category pages - these contain all the internships
SOFTWARE_ENGINEERING_URLS = [
    "https://www.intern-list.com/software-engineer-internship",
    "https://www.intern-list.com/swe-intern-list"
]
SEEN_INTERNSHIPS_FILE = "intern_list_seen_internships.json"
EMAIL_CONFIG_FILE = "intern_list_email_config.json"
CHECK_INTERVAL_MINUTES = 30  # Check every 30 minutes

# Filter settings
FILTER_CATEGORY = "Software Engineering"  # Only Software Engineering
FILTER_TYPE = "intern"  # Only internships

# Headers to mimic a browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}


class InternListMonitor:
    """Monitor intern-list.com for new internships."""

    def __init__(self, email_config_path: Optional[str] = None):
        self.email_config_path = email_config_path or EMAIL_CONFIG_FILE
        self.email_config = self.load_email_config()
        self.seen_internships = self.load_seen_internships()
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def load_json(self, path: str, default=None):
        """Load JSON file, return default if file doesn't exist."""
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading {path}: {e}")
        return default if default is not None else {}

    def save_json(self, path: str, data: dict):
        """Save data to JSON file."""
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving {path}: {e}")

    def load_email_config(self) -> Optional[Dict]:
        """Load email configuration from file or environment variables."""
        # Try environment variables first
        sender = os.getenv('GMAIL_SENDER')
        password = os.getenv('GMAIL_APP_PASSWORD')
        recipient = os.getenv('GMAIL_RECIPIENT')

        if sender and password and recipient:
            return {
                'sender_email': sender,
                'sender_password': password.replace(' ', ''),  # Remove spaces
                'recipient_email': recipient
            }

        # Try config file
        if os.path.exists(self.email_config_path):
            config = self.load_json(self.email_config_path)
            if config.get('sender_password'):
                config['sender_password'] = config['sender_password'].replace(' ', '')
            return config

        # Try the existing instagram_email_config.json as fallback
        fallback_config = 'instagram_email_config.json'
        if os.path.exists(fallback_config):
            config = self.load_json(fallback_config)
            if config.get('sender_password'):
                config['sender_password'] = config['sender_password'].replace(' ', '')
            return config

        return None

    def load_seen_internships(self) -> Dict:
        """Load list of seen internship IDs."""
        return self.load_json(SEEN_INTERNSHIPS_FILE, default={})

    def save_seen_internships(self):
        """Save seen internships to file."""
        self.save_json(SEEN_INTERNSHIPS_FILE, self.seen_internships)

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a webpage."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def extract_internships(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract ALL internship listings from the Software Engineering category page with full details."""
        internships = []

        if not soup:
            return internships

        # The page uses Airtable which loads data dynamically, so we need to extract from visible text
        # Look for text patterns that match internship listings
        
        # Get all text content
        all_text = soup.get_text(separator='\n')
        lines = [line.strip() for line in all_text.split('\n') if line.strip() and len(line.strip()) > 10]
        
        # Look for all links that could be internship listings
        main_content = soup.find('main') or soup.find('body') or soup
        all_links = main_content.find_all('a', href=True)
        
        potential_listings = []
        seen_titles = set()
        
        # Method 1: Extract from links with internship-related text
        for link in all_links:
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            # Skip navigation and non-job links
            if not text or len(text) < 10:
                continue
                
            skip_keywords = ['home', 'about', 'contact', 'privacy', 'terms', 'login', 'signup', 
                           'subscribe', 'share', 'feedback', 'guide', 'master', 'resume', 
                           'salary', 'salaries', 'intern-list.com', 'jobright', 'new grad',
                           'categorized by', 'analyze the hiring', 'looking for internship opportun']
            text_lower = text.lower()
            if any(keyword in text_lower for keyword in skip_keywords):
                continue
            
            # Skip if it's too short or looks like a description/guide text
            if len(text) < 20 or len(text) > 200:
                continue
            
            # Must be an actual internship listing - require "intern" or "internship" in title OR be a job application link
            is_intern = any(keyword in text_lower for keyword in ['intern', 'internship'])
            is_job_link = any(job_word in href.lower() for job_word in ['apply', 'job', 'career', 'position', 'opening'])
            
            if not is_intern and not is_job_link:
                continue
            
            # Skip if it's clearly not a software engineering internship
            # But be lenient since we're on the SWE category page
            if 'salary' in text_lower or 'guide' in text_lower or 'resume' in text_lower:
                continue
                # Get surrounding context for more details
                parent = link.find_parent(['div', 'article', 'li', 'section', 'tr', 'td'])
                context_text = ""
                if parent:
                    context_text = parent.get_text(separator=' | ', strip=True)
                
                # Try to extract structured data from context
                full_url = urljoin(INTERN_LIST_URL, href)
                
                # Extract details from context
                company = ""
                location = ""
                work_model = ""
                date = ""
                
                # Look for patterns in context
                context_lower = context_text.lower()
                
                # Extract work model
                if 'remote' in context_lower:
                    work_model = "Remote"
                elif 'hybrid' in context_lower:
                    work_model = "Hybrid"
                elif 'on site' in context_lower or 'onsite' in context_lower:
                    work_model = "On Site"
                
                # Extract location (look for common patterns)
                location_patterns = ['location', 'united states', 'ca', 'ny', 'tx', 'ma', 'wa', 'ut']
                for pattern in location_patterns:
                    if pattern in context_lower:
                        # Try to extract location text
                        parts = context_text.split('|')
                        for part in parts:
                            part_lower = part.lower()
                            if pattern in part_lower and len(part.strip()) < 100:
                                if not location or len(part.strip()) < len(location):
                                    location = part.strip()
                                break
                
                # Extract company (often appears near the end or in specific format)
                # Look for text that might be company name
                parts = context_text.split('|')
                for part in reversed(parts):  # Company often at end
                    part = part.strip()
                    if part and len(part) < 80 and part != text:
                        # Check if it looks like a company name
                        if not any(skip in part.lower() for skip in ['apply', 'intern', 'internship', 'remote', 'hybrid']):
                            if not company or (len(part) > len(company) and len(part) < 60):
                                company = part
                
                # Extract date (look for date patterns)
                import re
                date_match = re.search(r'\d{4}-\d{2}-\d{2}', context_text)
                if date_match:
                    date = date_match.group()
                
                # If we found a meaningful internship link, add it
                if is_intern or is_job_link:
                    # Skip duplicates
                    if text in seen_titles:
                        continue
                    seen_titles.add(text)
                    
                    internship_id = f"{full_url}_{text[:50]}"
                    
                    internship_data = {
                        'id': internship_id,
                        'title': text,
                        'url': full_url,
                        'company': company if company else "Not specified",
                        'location': location if location else "Not specified",
                        'work_model': work_model if work_model else "Not specified",
                        'date': date if date else datetime.now().strftime('%Y-%m-%d'),
                        'description': context_text[:300] if context_text else "",
                        'found_at': datetime.now().isoformat()
                    }
                    
                    potential_listings.append(internship_data)
        
        # Method 2: Also extract from visible text that looks like internship titles
        # Look for lines that match internship title patterns
        for line in lines:
            line_lower = line.lower()
            # Must contain intern/internship and be software engineering related
            if any(keyword in line_lower for keyword in ['intern', 'internship']) and \
               any(keyword in line_lower for keyword in ['software', 'engineer', 'engineering', 'developer', 'swe', 'sde', 'qa', 'web']):
                # Skip if it's already captured or is a navigation item
                if line in seen_titles or len(line) < 20 or len(line) > 200:
                    continue
                if any(skip in line_lower for skip in ['guide', 'salary', 'resume', 'how to', 'subscribe', 
                                                       'categorized', 'analyze', 'looking for internship opportun']):
                    continue
                
                seen_titles.add(line)
                internship_id = f"text_{line[:50]}"
                
                internship_data = {
                    'id': internship_id,
                    'title': line,
                    'url': INTERN_LIST_URL,  # No specific URL for text-only entries
                    'company': "Not specified",
                    'location': "Not specified",
                    'work_model': "Not specified",
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'description': "",
                    'found_at': datetime.now().isoformat()
                }
                
                potential_listings.append(internship_data)
        
        # Remove duplicates
        seen_ids = set()
        for listing in potential_listings:
            if listing['id'] not in seen_ids:
                seen_ids.add(listing['id'])
                internships.append(listing)
        
        return internships

    def find_new_internships(self) -> List[Dict]:
        """Check for new internships and return list of new ones."""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking for new Software Engineering internships...")
        
        all_internships = []
        
        # Fetch from all Software Engineering category pages
        for url in SOFTWARE_ENGINEERING_URLS:
            print(f"   Fetching from: {url}")
            soup = self.fetch_page(url)
            if soup:
                internships = self.extract_internships(soup)
                print(f"   Found {len(internships)} internship(s) on this page")
                all_internships.extend(internships)
            else:
                print(f"   Failed to fetch {url}")
        
        # Remove duplicates based on title and URL
        seen_ids = set()
        unique_internships = []
        for internship in all_internships:
            # Use both URL and title for uniqueness
            unique_key = f"{internship.get('url', '')}_{internship.get('title', '')}"
            if unique_key not in seen_ids:
                seen_ids.add(unique_key)
                unique_internships.append(internship)
        
        print(f"   Total unique Software Engineering internships: {len(unique_internships)}")
        new_internships = []

        for internship in unique_internships:
            internship_id = internship['id']
            
            # Check if we've seen this before - only add if it's NEW
            if internship_id not in self.seen_internships:
                new_internships.append(internship)
                # Mark as seen so we don't send it again
                self.seen_internships[internship_id] = {
                    'title': internship['title'],
                    'url': internship['url'],
                    'first_seen': internship['found_at']
                }

        if new_internships:
            print(f"✅ Found {len(new_internships)} NEW Software Engineering internship(s)!")
            # Save the seen internships so we remember what we've already sent
            self.save_seen_internships()
        else:
            print("ℹ️  No NEW internships found (all have been seen before).")

        return new_internships

    def send_email_notification(self, new_internships: List[Dict]):
        """Send email notification with summary of NEW internships only."""
        if not self.email_config:
            print("Email not configured. Skipping notification.")
            return

        # Only send if there are actually new internships
        if not new_internships:
            print("No new internships to notify about. Skipping email.")
            return

        try:
            sender_email = self.email_config['sender_email']
            sender_password = self.email_config['sender_password']
            recipient_email = self.email_config['recipient_email']

            # Create email
            msg = MIMEMultipart('alternative')
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = f"💻 {len(new_internships)} New Software Engineering Internship(s) Found!"

            # Create email body
            html_body = f"""
            <html>
              <head></head>
              <body>
                <h2>💻 New Software Engineering Internships Detected!</h2>
                <p>Found <strong>{len(new_internships)}</strong> new Software Engineering internship posting(s) on <a href="{INTERN_LIST_URL}">intern-list.com</a></p>
                <hr>
                <h3>New Postings:</h3>
                <ul>
            """

            for i, internship in enumerate(new_internships, 1):
                company = internship.get('company', 'Not specified')
                location = internship.get('location', 'Not specified')
                work_model = internship.get('work_model', 'Not specified')
                date = internship.get('date', '')
                
                html_body += f"""
                  <li>
                    <strong>{i}. <a href="{internship['url']}">{internship['title']}</a></strong><br>
                    <strong>Company:</strong> {company}<br>
                    <strong>Location:</strong> {location}<br>
                    <strong>Work Model:</strong> {work_model}<br>
                    {f"<strong>Date:</strong> {date}<br>" if date and date != 'Not specified' else ""}
                    {f"<em>{internship['description'][:150]}...</em><br>" if internship.get('description') and len(internship.get('description', '')) > 20 else ""}
                    <a href="{internship['url']}">Apply/View Details →</a>
                  </li>
                  <br>
                """

            html_body += f"""
                </ul>
                <hr>
                <p><a href="{INTERN_LIST_URL}">View All Internships on Intern-List.com</a></p>
                <p><small>Checked at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small></p>
              </body>
            </html>
            """

            text_body = f"""
New Software Engineering Internships Detected!

Found {len(new_internships)} new Software Engineering internship posting(s) on intern-list.com

New Postings:
"""
            for i, internship in enumerate(new_internships, 1):
                company = internship.get('company', 'Not specified')
                location = internship.get('location', 'Not specified')
                work_model = internship.get('work_model', 'Not specified')
                date = internship.get('date', '')
                
                text_body += f"\n{i}. {internship['title']}\n"
                text_body += f"   Company: {company}\n"
                text_body += f"   Location: {location}\n"
                text_body += f"   Work Model: {work_model}\n"
                if date and date != 'Not specified':
                    text_body += f"   Date: {date}\n"
                text_body += f"   URL: {internship['url']}\n"
                if internship.get('description') and len(internship.get('description', '')) > 20:
                    text_body += f"   {internship['description'][:150]}...\n"

            text_body += f"\nView all: {INTERN_LIST_URL}\n"
            text_body += f"Checked at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            # Attach both plain text and HTML
            part1 = MIMEText(text_body, 'plain')
            part2 = MIMEText(html_body, 'html')

            msg.attach(part1)
            msg.attach(part2)

            # Send email
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)

            print(f"✅ Email notification sent to {recipient_email}")

        except Exception as e:
            print(f"❌ Error sending email: {e}")

    def run_once(self):
        """Run a single check for new internships."""
        new_internships = self.find_new_internships()
        # Only send email if there are NEW internships (not ones we've already seen)
        if new_internships:
            print(f"📧 Sending email notification for {len(new_internships)} new internship(s)...")
            self.send_email_notification(new_internships)
        else:
            print("ℹ️  No new internships found. No email sent.")
        return new_internships

    def run_continuous(self, interval_minutes: int = CHECK_INTERVAL_MINUTES):
        """Run continuously, checking at specified intervals."""
        print(f"🚀 Starting Intern-List.com monitor...")
        print(f"📧 Email: {self.email_config['recipient_email'] if self.email_config else 'Not configured'}")
        print(f"🔍 Filter: Software Engineering Internships Only")
        print(f"⏰ Checking every {interval_minutes} minutes")
        print(f"🌐 Monitoring: {INTERN_LIST_URL}")
        print("Press Ctrl+C to stop\n")

        try:
            while True:
                new_internships = self.run_once()
                if new_internships:
                    print(f"✅ Notified about {len(new_internships)} new internship(s)\n")
                
                # Wait for next check
                wait_seconds = interval_minutes * 60
                print(f"⏳ Next check in {interval_minutes} minutes...\n")
                time.sleep(wait_seconds)

        except KeyboardInterrupt:
            print("\n\n👋 Monitor stopped by user")
        except Exception as e:
            print(f"\n❌ Error in monitor loop: {e}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Monitor intern-list.com for new internships'
    )
    parser.add_argument(
        '--once',
        action='store_true',
        help='Run once and exit (for scheduled jobs)'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=CHECK_INTERVAL_MINUTES,
        help=f'Check interval in minutes (default: {CHECK_INTERVAL_MINUTES})'
    )
    parser.add_argument(
        '--email-config',
        type=str,
        help='Path to email config file'
    )

    args = parser.parse_args()

    monitor = InternListMonitor(email_config_path=args.email_config)

    if args.once:
        monitor.run_once()
    else:
        monitor.run_continuous(interval_minutes=args.interval)


if __name__ == '__main__':
    main()

