from crawler import DarkWebCrawler
from db import DatabaseManager, db
from flask import Flask
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Initialize Flask app for database
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///threats.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db_manager = DatabaseManager(app)
    
    # Create crawler instance
    crawler = DarkWebCrawler()
    
    # Start crawling
    logging.info("Starting dark web crawl...")
    threats = crawler.start_crawling(max_depth=2)
    
    # Store threats in database
    with app.app_context():
        for threat in threats:
            # Determine severity based on keyword
            severity = 'high' if any(kw in threat['keyword'].lower() for kw in ['password', 'credit card', 'cvv']) else 'medium'
            
            # Add threat to database
            db_manager.add_threat(
                source_url=threat.get('source_url', 'Unknown'),
                threat_type=threat['type'],
                keyword=threat['keyword'],
                context=threat['context'],
                severity=severity
            )
    
    logging.info(f"Crawling completed. Found {len(threats)} potential threats.")

if __name__ == "__main__":
    main() 