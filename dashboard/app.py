import sys
import os
# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import threading
import time
from crawler import DarkWebCrawler
from db import DatabaseManager, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///threats.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production

db_manager = DatabaseManager(app)
crawler = DarkWebCrawler()

def background_crawler():
    """Background task to continuously crawl for threats"""
    while True:
        try:
            threats = crawler.start_crawling(max_depth=2)
            with app.app_context():
                for threat in threats:
                    # Determine severity based on keyword and type
                    severity = 'high'
                    if threat['type'] == 'pattern_match':
                        if threat['keyword'] in ['email', 'ip_address']:
                            severity = 'medium'
                    elif 'hack' in threat['keyword'] or 'discussion' in threat['context']:
                        severity = 'medium'
                    
                    db_manager.add_threat(
                        source_url=threat['source_url'],
                        threat_type=threat['type'],
                        keyword=threat['keyword'],
                        context=threat['context'],
                        severity=severity
                    )
            time.sleep(300)  # Wait 5 minutes before next crawl
        except Exception as e:
            print(f"Error in background crawler: {str(e)}")
            time.sleep(60)  # Wait 1 minute on error

# Start background crawler
crawler_thread = threading.Thread(target=background_crawler, daemon=True)
crawler_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/threats')
def get_threats():
    threat_type = request.args.get('type')
    severity = request.args.get('severity')
    search = request.args.get('search')
    time_range = request.args.get('time_range', '24h')
    
    # Calculate time range
    now = datetime.utcnow()
    if time_range == '1h':
        start_time = now - timedelta(hours=1)
    elif time_range == '6h':
        start_time = now - timedelta(hours=6)
    elif time_range == '24h':
        start_time = now - timedelta(hours=24)
    elif time_range == '7d':
        start_time = now - timedelta(days=7)
    else:
        start_time = now - timedelta(hours=24)
    
    if threat_type:
        threats = db_manager.get_threats_by_type(threat_type)
    elif severity:
        threats = db_manager.get_threats_by_severity(severity)
    elif search:
        threats = db_manager.search_threats(search)
    else:
        threats = db_manager.get_all_threats()
    
    # Filter by time range
    threats = [t for t in threats if t.timestamp >= start_time]
        
    return jsonify([{
        'id': t.id,
        'timestamp': t.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'source_url': t.source_url,
        'threat_type': t.threat_type,
        'keyword': t.keyword,
        'context': t.context,
        'severity': t.severity
    } for t in threats])

@app.route('/api/stats')
def get_stats():
    now = datetime.utcnow()
    last_hour = now - timedelta(hours=1)
    last_24h = now - timedelta(hours=24)
    
    # Get all threats
    all_threats = db_manager.get_all_threats()
    
    # Calculate statistics
    total_threats = len(all_threats)
    high_severity = len([t for t in all_threats if t.severity == 'high'])
    medium_severity = len([t for t in all_threats if t.severity == 'medium'])
    low_severity = len([t for t in all_threats if t.severity == 'low'])
    
    # Recent threats
    recent_threats = len([t for t in all_threats if t.timestamp >= last_24h])
    hourly_threats = len([t for t in all_threats if t.timestamp >= last_hour])
    
    # Threat types
    keyword_matches = len([t for t in all_threats if t.threat_type == 'keyword_match'])
    pattern_matches = len([t for t in all_threats if t.threat_type == 'pattern_match'])
    
    return jsonify({
        'total_threats': total_threats,
        'high_severity': high_severity,
        'medium_severity': medium_severity,
        'low_severity': low_severity,
        'recent_threats': recent_threats,
        'hourly_threats': hourly_threats,
        'keyword_matches': keyword_matches,
        'pattern_matches': pattern_matches,
        'last_update': now.strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    app.run(debug=True) 