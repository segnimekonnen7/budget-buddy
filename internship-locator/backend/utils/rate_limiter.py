"""
Rate Limiter for Internship Locator
Ensures respectful scraping with proper delays and safety measures.
"""

import time
import random
import logging
from collections import defaultdict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self):
        self.request_times = defaultdict(list)
        self.min_delays = {
            'linkedin': 3,
            'indeed': 2,
            'glassdoor': 3,
            'handshake': 3
        }
        self.max_delays = {
            'linkedin': 6,
            'indeed': 5,
            'glassdoor': 6,
            'handshake': 6
        }
    
    def wait_if_needed(self, platform):
        """
        Wait if necessary to respect rate limits for a platform
        
        Args:
            platform (str): Platform name (linkedin, indeed, glassdoor, handshake)
        """
        current_time = time.time()
        platform_requests = self.request_times[platform]
        
        # Remove requests older than 1 hour
        one_hour_ago = current_time - 3600
        platform_requests = [req_time for req_time in platform_requests if req_time > one_hour_ago]
        self.request_times[platform] = platform_requests
        
        # Check if we need to wait
        if platform_requests:
            time_since_last = current_time - platform_requests[-1]
            min_delay = self.min_delays.get(platform, 2)
            
            if time_since_last < min_delay:
                sleep_time = min_delay - time_since_last + random.uniform(0, 1)
                logger.info(f"Rate limiting {platform}: sleeping for {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
        
        # Record this request
        self.request_times[platform].append(time.time())
    
    def get_delay_for_platform(self, platform):
        """
        Get a random delay for a platform
        
        Args:
            platform (str): Platform name
            
        Returns:
            float: Delay in seconds
        """
        min_delay = self.min_delays.get(platform, 2)
        max_delay = self.max_delays.get(platform, 5)
        return random.uniform(min_delay, max_delay)
    
    def is_rate_limited(self, platform):
        """
        Check if a platform is currently rate limited
        
        Args:
            platform (str): Platform name
            
        Returns:
            bool: True if rate limited
        """
        current_time = time.time()
        platform_requests = self.request_times[platform]
        
        # Check last 10 minutes
        ten_minutes_ago = current_time - 600
        recent_requests = [req_time for req_time in platform_requests if req_time > ten_minutes_ago]
        
        # Rate limit if more than 10 requests in 10 minutes
        return len(recent_requests) > 10 