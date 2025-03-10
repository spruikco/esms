# models/match.py
from extensions import db  # Import the SQLAlchemy instance

class MatchLineup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    starters = db.Column(db.String, nullable=False)  # Comma-separated player IDs
    substitutes = db.Column(db.String, nullable=True)  # Comma-separated player IDs
    formation = db.Column(db.String(10), nullable=True)
    tactic = db.Column(db.String(1), default='N')
    
    match = db.relationship('Match', backref='lineups')
    team = db.relationship('Team')

# Add the rest of your match-related models here...

class MatchEvent(db.Model):
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