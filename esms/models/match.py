# esms/models/match.py
from extensions import db
from datetime import datetime

class Match(db.Model):
    """Represents a match between two teams"""
    id = db.Column(db.Integer, primary_key=True)
    home_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    scheduled_time = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    home_score = db.Column(db.Integer, default=0)
    away_score = db.Column(db.Integer, default=0)
    
    # Define relationships using string for class names to avoid circular references
    home_team = db.relationship('Team', foreign_keys=[home_team_id], backref='home_matches')
    away_team = db.relationship('Team', foreign_keys=[away_team_id], backref='away_matches')
    match_events = db.relationship('MatchEvent', backref='match', lazy='dynamic')
    
    def __repr__(self):
        return f"<Match {self.id}>"

class MatchLineup(db.Model):
    """Represents team lineup for a match"""
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    starters = db.Column(db.String, nullable=False)  # Comma-separated player IDs
    substitutes = db.Column(db.String, nullable=True)  # Comma-separated player IDs
    formation = db.Column(db.String(10), nullable=True)
    tactic = db.Column(db.String(1), default='N')
    
    match = db.relationship('Match', backref='lineups')
    team = db.relationship('Team')

class MatchEvent(db.Model):
    """Represents an event that occurred during a match"""
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    minute = db.Column(db.Integer, nullable=False)
    event_type = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    related_player_id = db.Column(db.Integer, db.ForeignKey('player.id'))  # For assists, subs, etc.
    
    player = db.relationship('Player', foreign_keys=[player_id])
    related_player = db.relationship('Player', foreign_keys=[related_player_id])
    team = db.relationship('Team')