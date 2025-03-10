# esms/models/formation.py
from extensions import db
import json

class Formation(db.Model):
    """Represents a team's formation and player positions"""
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    formation_type = db.Column(db.String(10), default='4-4-2')
    positions_json = db.Column(db.Text, nullable=False)  # Stores player positions as JSON
    
    # Change the backref name from 'formation' to 'team_formation'
    team = db.relationship('Team', backref=db.backref('team_formation', uselist=False))
    
    @property
    def positions(self):
        """Get positions as Python dictionary"""
        if self.positions_json:
            return json.loads(self.positions_json)
        return {}
        
    @positions.setter
    def positions(self, value):
        """Set positions from Python dictionary"""
        self.positions_json = json.dumps(value)
    
    def __repr__(self):
        return f"<Formation {self.formation_type} for Team {self.team_id}>"