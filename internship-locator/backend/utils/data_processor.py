"""
Data Processor for Internship Locator
Cleans, deduplicates, and structures internship data from multiple sources.
"""

import re
import logging
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self):
        self.seen_titles = set()
        self.seen_companies = set()
    
    def process_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process and clean internship results from multiple sources
        
        Args:
            results (List[Dict]): Raw internship results from scrapers
            
        Returns:
            List[Dict]: Cleaned and deduplicated results
        """
        try:
            logger.info(f"Processing {len(results)} raw internship results")
            
            # Clean each result
            cleaned_results = []
            for result in results:
                cleaned_result = self._clean_result(result)
                if cleaned_result:
                    cleaned_results.append(cleaned_result)
            
            # Remove duplicates
            deduplicated_results = self._remove_duplicates(cleaned_results)
            
            # Sort by relevance
            sorted_results = self._sort_by_relevance(deduplicated_results)
            
            logger.info(f"✅ Processed {len(sorted_results)} unique internships")
            return sorted_results
            
        except Exception as e:
            logger.error(f"Error processing results: {str(e)}")
            return results
    
    def _clean_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean a single internship result
        
        Args:
            result (Dict): Raw internship result
            
        Returns:
            Dict: Cleaned result
        """
        try:
            cleaned = result.copy()
            
            # Clean title
            if 'title' in cleaned:
                cleaned['title'] = self._clean_text(cleaned['title'])
            
            # Clean company name
            if 'company' in cleaned:
                cleaned['company'] = self._clean_text(cleaned['company'])
            
            # Clean location
            if 'location' in cleaned:
                cleaned['location'] = self._clean_text(cleaned['location'])
            
            # Clean salary
            if 'salary' in cleaned:
                cleaned['salary'] = self._clean_salary(cleaned['salary'])
            
            # Clean description
            if 'description' in cleaned:
                cleaned['description'] = self._clean_text(cleaned['description'])
            
            # Ensure required fields
            if not cleaned.get('title') or not cleaned.get('company'):
                return None
            
            # Add metadata
            cleaned['processed_at'] = datetime.now().isoformat()
            cleaned['id'] = self._generate_id(cleaned)
            
            return cleaned
            
        except Exception as e:
            logger.debug(f"Error cleaning result: {str(e)}")
            return result
    
    def _clean_text(self, text: str) -> str:
        """
        Clean text by removing extra whitespace and special characters
        
        Args:
            text (str): Raw text
            
        Returns:
            str: Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters that might cause issues
        text = re.sub(r'[^\w\s\-.,&()]', '', text)
        
        return text
    
    def _clean_salary(self, salary: str) -> str:
        """
        Clean and standardize salary information
        
        Args:
            salary (str): Raw salary text
            
        Returns:
            str: Cleaned salary
        """
        if not salary:
            return "Competitive"
        
        # Remove extra whitespace
        salary = self._clean_text(salary)
        
        # Standardize common salary formats
        salary = re.sub(r'(\d+)[kK]', r'$\1,000', salary)
        salary = re.sub(r'(\d+)[mM]', r'$\1,000,000', salary)
        
        return salary
    
    def _remove_duplicates(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Remove duplicate internships based on title and company
        
        Args:
            results (List[Dict]): List of internship results
            
        Returns:
            List[Dict]: Deduplicated results
        """
        seen = set()
        unique_results = []
        
        for result in results:
            # Create a key based on title and company
            key = f"{result.get('title', '').lower()}_{result.get('company', '').lower()}"
            
            if key not in seen:
                seen.add(key)
                unique_results.append(result)
        
        logger.info(f"Removed {len(results) - len(unique_results)} duplicates")
        return unique_results
    
    def _sort_by_relevance(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Sort results by relevance score
        
        Args:
            results (List[Dict]): List of internship results
            
        Returns:
            List[Dict]: Sorted results
        """
        def calculate_relevance_score(result):
            score = 0
            
            # Prefer non-fallback results
            if not result.get('fallback', False):
                score += 100
            
            # Prefer internships with salary information
            if result.get('salary') and result.get('salary') != 'Competitive':
                score += 50
            
            # Prefer remote opportunities
            if result.get('remote', False):
                score += 25
            
            # Prefer paid internships
            if result.get('paid', True):
                score += 25
            
            # Prefer recent scrapes
            if 'scraped_at' in result:
                try:
                    scraped_time = datetime.fromisoformat(result['scraped_at'].replace('Z', '+00:00'))
                    time_diff = datetime.now() - scraped_time
                    if time_diff.total_seconds() < 3600:  # Less than 1 hour
                        score += 10
                except:
                    pass
            
            return score
        
        # Sort by relevance score (highest first)
        sorted_results = sorted(results, key=calculate_relevance_score, reverse=True)
        
        return sorted_results
    
    def _generate_id(self, result: Dict[str, Any]) -> str:
        """
        Generate a unique ID for an internship result
        
        Args:
            result (Dict): Internship result
            
        Returns:
            str: Unique ID
        """
        title = result.get('title', '').lower()
        company = result.get('company', '').lower()
        platform = result.get('platform', '').lower()
        
        # Create a simple hash
        combined = f"{title}_{company}_{platform}"
        return re.sub(r'[^\w]', '_', combined)
    
    def filter_results(self, results: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Filter results based on criteria
        
        Args:
            results (List[Dict]): List of internship results
            filters (Dict): Filter criteria
            
        Returns:
            List[Dict]: Filtered results
        """
        filtered_results = results
        
        # Filter by remote only
        if filters.get('remote_only', False):
            filtered_results = [r for r in filtered_results if r.get('remote', False)]
        
        # Filter by paid only
        if filters.get('paid_only', False):
            filtered_results = [r for r in filtered_results if r.get('paid', True)]
        
        # Filter by platform
        if filters.get('platforms'):
            platforms = filters['platforms']
            filtered_results = [r for r in filtered_results if r.get('platform', '').lower() in platforms]
        
        # Filter by keyword in title or description
        if filters.get('keyword'):
            keyword = filters['keyword'].lower()
            filtered_results = [
                r for r in filtered_results 
                if keyword in r.get('title', '').lower() or keyword in r.get('description', '').lower()
            ]
        
        # Filter by location
        if filters.get('location'):
            location = filters['location'].lower()
            filtered_results = [
                r for r in filtered_results 
                if location in r.get('location', '').lower()
            ]
        
        return filtered_results 