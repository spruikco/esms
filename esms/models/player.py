# esms/models/player.py
from extensions import db

class Player(db.Model):
    """Represents a soccer player"""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, default=25)
    nationality = db.Column(db.String(50))
    primary_position = db.Column(db.String(10))
    
    # Player attributes
    speed = db.Column(db.Integer, default=10)
    stamina = db.Column(db.Integer, default=10)
    technique = db.Column(db.Integer, default=10)
    passing = db.Column(db.Integer, default=10)
    shooting = db.Column(db.Integer, default=10)
    tackling = db.Column(db.Integer, default=10)
    heading = db.Column(db.Integer, default=10)
    goalkeeper = db.Column(db.Integer, default=10)
    positioning = db.Column(db.Integer, default=10)
    
    # Player stats
    goals = db.Column(db.Integer, default=0)
    assists = db.Column(db.Integer, default=0)
    
    # Relationships are defined in TeamPlayer model
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
        
    def __repr__(self):
        return f"<Player {self.name}>"