from bs4 import BeautifulSoup
import logging
from urllib.parse import urljoin
import time
import random
import re
from datetime import datetime
from tor_session import TorSession

class DarkWebCrawler:
    def __init__(self, tor_password=None):
        self.tor_session = TorSession(tor_password)
        self.visited_urls = set()
        self.threat_keywords = [
            # Credentials and Personal Data
            'password', 'dump', 'credentials', 'login', 'account',
            'email', 'username', 'personal data', 'identity',
            
            # Financial Threats
            'credit card', 'cvv', 'dumps', 'bank', 'payment',
            'bitcoin', 'crypto', 'wallet', 'transfer',
            
            # Malware and Exploits
            'exploit', 'hack', 'malware', 'ransomware', 'trojan',
            'virus', 'backdoor', 'rootkit', 'botnet',
            
            # Data Leaks
            'leak', 'breach', 'database', 'stolen', 'compromised',
            'exposed', 'hacked', 'cracked', 'crack',
            
            # Cybercrime Tools
            'ddos', 'botnet', 'spam', 'phishing', 'scam',
            'fraud', 'fake', 'counterfeit', 'forged'
        ]
        
        # Regular expressions for pattern matching
        self.patterns = {
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'credit_card': r'\b(?:\d[ -]*?){13,19}\b',
            'btc_address': r'[13][a-km-zA-HJ-NP-Z1-9]{25,34}',
            'ip_address': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
            'hash': r'\b[a-fA-F0-9]{32,}\b'
        }
        
    def load_onion_sites(self, filename='onion_sites.txt'):
        """Load list of .onion sites to crawl"""
        try:
            with open(filename, 'r') as f:
                return [line.strip().split('#')[0].strip() for line in f 
                       if line.strip() and not line.startswith('#')]
        except FileNotFoundError:
            logging.error(f"Could not find {filename}")
            return []
            
    def extract_links(self, soup, base_url):
        """Extract all links from the page"""
        links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(base_url, href)
            if ('.onion' in full_url or any(domain in full_url for domain in ['.com', '.org'])) and full_url not in self.visited_urls:
                links.append(full_url)
        return links
        
    def detect_threats(self, soup, url):
        """Detect potential threats in the page content"""
        threats = []
        text = soup.get_text().lower()
        
        # Check for threat keywords
        for keyword in self.threat_keywords:
            if keyword in text:
                # Get surrounding context
                context = self._get_context(text, keyword)
                threats.append({
                    'type': 'keyword_match',
                    'keyword': keyword,
                    'context': context,
                    'source_url': url,
                    'timestamp': datetime.utcnow()
                })
        
        # Check for patterns
        for pattern_name, pattern in self.patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                context = self._get_context(text, match.group())
                threats.append({
                    'type': 'pattern_match',
                    'keyword': pattern_name,
                    'context': context,
                    'source_url': url,
                    'timestamp': datetime.utcnow()
                })
                
        return threats
        
    def _get_context(self, text, keyword, context_size=100):
        """Get surrounding context for a keyword match"""
        try:
            index = text.index(keyword)
            start = max(0, index - context_size)
            end = min(len(text), index + len(keyword) + context_size)
            return text[start:end].strip()
        except ValueError:
            return ""
            
    def crawl(self, url, max_depth=2, current_depth=0):
        """Crawl a .onion site recursively"""
        if current_depth >= max_depth or url in self.visited_urls:
            return []
            
        self.visited_urls.add(url)
        logging.info(f"Crawling: {url}")
        
        # Add random delay to avoid detection
        time.sleep(random.uniform(2, 5))
        
        response = self.tor_session.get(url)
        if not response or response.status_code != 200:
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        threats = self.detect_threats(soup, url)
        
        # Recursively crawl linked pages
        if current_depth < max_depth - 1:
            links = self.extract_links(soup, url)
            for link in links:
                threats.extend(self.crawl(link, max_depth, current_depth + 1))
                
        return threats
        
    def start_crawling(self, max_depth=2):
        """Start crawling from the list of onion sites"""
        all_threats = []
        onion_sites = self.load_onion_sites()
        
        for site in onion_sites:
            try:
                threats = self.crawl(site, max_depth)
                all_threats.extend(threats)
                
                # Change Tor identity periodically
                if random.random() < 0.3:  # 30% chance to change identity
                    self.tor_session.get_new_identity()
                    
            except Exception as e:
                logging.error(f"Error crawling {site}: {str(e)}")
                
        return all_threats 