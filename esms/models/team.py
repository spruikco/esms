# esms/models/team.py
from extensions import db
from datetime import datetime

class Team(db.Model):
    """Represents a soccer team"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    tactic = db.Column(db.String(1), default='N')  # N, A, D, P, C
    formation = db.Column(db.String(10), default='4-4-2')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Players will be loaded through relationship from TeamPlayer
    
    def __repr__(self):
        return f"<Team {self.name}>"

class TeamPlayer(db.Model):
    """Represents a player assigned to a team with a position"""
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    position = db.Column(db.String(10), nullable=False)  # GK, CB, LB, etc.
    
    team = db.relationship('Team', backref=db.backref('players', lazy='dynamic'))
    player = db.relationship('Player')