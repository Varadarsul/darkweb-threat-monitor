from db import DatabaseManager, db
from flask import Flask
from datetime import datetime, timedelta
import random

def add_test_data():
    # Initialize Flask app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///threats.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db_manager = DatabaseManager(app)
    
    # Sample threat data
    sample_threats = [
        {
            'source_url': 'http://msydqstlz2kzerdg.onion',
            'threat_type': 'keyword_match',
            'keyword': 'password dump',
            'context': 'Found a large password dump containing 100,000 credentials',
            'severity': 'high'
        },
        {
            'source_url': 'http://phobos4ztgu4f7wf.onion',
            'threat_type': 'keyword_match',
            'keyword': 'exploit kit',
            'context': 'New exploit kit for Windows systems discovered',
            'severity': 'high'
        },
        {
            'source_url': 'http://torlinkbgs6aabns.onion',
            'threat_type': 'pattern_match',
            'keyword': 'credit card',
            'context': 'Credit card numbers and CVV data available',
            'severity': 'high'
        },
        {
            'source_url': 'http://cwnj5t4pld7zv7nt.onion',
            'threat_type': 'keyword_match',
            'keyword': 'hack',
            'context': 'Discussion about hacking techniques',
            'severity': 'medium'
        },
        {
            'source_url': 'http://onionlandsearchengine.onion',
            'threat_type': 'pattern_match',
            'keyword': 'database',
            'context': 'Leaked database containing user information',
            'severity': 'medium'
        }
    ]
    
    # Add threats to database
    with app.app_context():
        for threat in sample_threats:
            # Add some random timestamps within last 24 hours
            timestamp = datetime.utcnow() - timedelta(hours=random.randint(0, 24))
            threat_obj = db_manager.add_threat(
                source_url=threat['source_url'],
                threat_type=threat['threat_type'],
                keyword=threat['keyword'],
                context=threat['context'],
                severity=threat['severity']
            )
            if threat_obj:
                print(f"Added threat: {threat['keyword']}")

if __name__ == "__main__":
    add_test_data() 