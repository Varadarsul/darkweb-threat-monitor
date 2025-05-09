from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging

db = SQLAlchemy()

class Threat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    source_url = db.Column(db.String(500))
    threat_type = db.Column(db.String(50))
    keyword = db.Column(db.String(100))
    context = db.Column(db.Text)
    severity = db.Column(db.String(20))
    
    def __repr__(self):
        return f'<Threat {self.id}: {self.threat_type}>'
        
class DatabaseManager:
    def __init__(self, app):
        db.init_app(app)
        with app.app_context():
            db.create_all()
            
    def add_threat(self, source_url, threat_type, keyword, context, severity):
        """Add a new threat to the database"""
        try:
            threat = Threat(
                source_url=source_url,
                threat_type=threat_type,
                keyword=keyword,
                context=context,
                severity=severity
            )
            db.session.add(threat)
            db.session.commit()
            return threat
        except Exception as e:
            logging.error(f"Error adding threat to database: {str(e)}")
            db.session.rollback()
            return None
            
    def get_all_threats(self):
        """Get all threats from the database"""
        return Threat.query.order_by(Threat.timestamp.desc()).all()
        
    def get_threats_by_type(self, threat_type):
        """Get threats filtered by type"""
        return Threat.query.filter_by(threat_type=threat_type).order_by(Threat.timestamp.desc()).all()
        
    def get_threats_by_date_range(self, start_date, end_date):
        """Get threats within a date range"""
        return Threat.query.filter(
            Threat.timestamp >= start_date,
            Threat.timestamp <= end_date
        ).order_by(Threat.timestamp.desc()).all()
        
    def get_threats_by_severity(self, severity):
        """Get threats filtered by severity"""
        return Threat.query.filter_by(severity=severity).order_by(Threat.timestamp.desc()).all()
        
    def search_threats(self, query):
        """Search threats by keyword or context"""
        return Threat.query.filter(
            (Threat.keyword.ilike(f'%{query}%')) |
            (Threat.context.ilike(f'%{query}%')) |
            (Threat.source_url.ilike(f'%{query}%'))
        ).order_by(Threat.timestamp.desc()).all() 