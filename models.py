from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    teams = db.relationship('Team', backref='owner', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    formation = db.Column(db.String(20), default='4-4-2')
    tactic = db.Column(db.String(1), default='N')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    players = db.relationship('TeamPlayer', backref='team', lazy=True)
    home_matches = db.relationship('Match', foreign_keys='Match.home_team_id', backref='home_team', lazy=True)
    away_matches = db.relationship('Match', foreign_keys='Match.away_team_id', backref='away_team', lazy=True)
    
    def __repr__(self):
        return f'<Team {self.name}>'
    
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Updated fields for player identity
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)  # Keep for compatibility
    age = db.Column(db.Integer, default=25)
    nationality = db.Column(db.String(50), nullable=True)
    primary_position = db.Column(db.String(10), nullable=False)  # Primary position
    
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
    
    # Meta information
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    team_assignments = db.relationship('TeamPlayer', backref='player', lazy=True)
    
    def __repr__(self):
        return f'<Player {self.name}>'
    
class TeamPlayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    position = db.Column(db.String(3), nullable=False)
    x_position = db.Column(db.Float)  # For formation editor
    y_position = db.Column(db.Float)  # For formation editor
    
    def __repr__(self):
        return f'<TeamPlayer {self.position}>'

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    home_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    home_score = db.Column(db.Integer)
    away_score = db.Column(db.Integer)
    match_events = db.relationship('MatchEvent', backref='match', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Match {self.home_team_id} vs {self.away_team_id}>'
    
class MatchEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    minute = db.Column(db.Integer, nullable=False)
    event_type = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    
    def __repr__(self):
        return f'<MatchEvent {self.event_type} at {self.minute}>'

class Tactic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(50), nullable=False)
    
    # Basic tactical settings
    mentality = db.Column(db.String(20), default='balanced')  # attacking, balanced, defensive
    width = db.Column(db.Integer, default=50)  # 0-100
    tempo = db.Column(db.Integer, default=50)  # 0-100
    passing_style = db.Column(db.String(20), default='mixed')  # direct, mixed, short
    pressing_intensity = db.Column(db.Integer, default=50)  # 0-100
    
    # Advanced settings
    offside_trap = db.Column(db.Boolean, default=False)
    counter_attack = db.Column(db.Boolean, default=False)
    play_out_from_back = db.Column(db.Boolean, default=False)
    
    # Tactical instructions for different game states
    winning_mentality = db.Column(db.String(20))
    losing_mentality = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Tactic {self.name}>'
    
    def get_effects(self):
        """Calculate the tactical effects based on settings"""
        effects = {}
        
        # Mentality effects
        if self.mentality == 'attacking':
            effects['attacking_boost'] = 2
            effects['defensive_penalty'] = 1
        elif self.mentality == 'defensive':
            effects['defensive_boost'] = 2
            effects['attacking_penalty'] = 1
        
        # Passing style effects
        if self.passing_style == 'direct':
            effects['direct_passing_boost'] = 1.5
            effects['possession_penalty'] = 1
        elif self.passing_style == 'short':
            effects['possession_boost'] = 1.5
            effects['direct_passing_penalty'] = 1
        
        # Pressing effects
        if self.pressing_intensity > 75:
            effects['pressing_boost'] = 2
            effects['stamina_drain'] = 1.5
        elif self.pressing_intensity < 25:
            effects['defensive_shape_boost'] = 1.5
            effects['pressing_penalty'] = 1
        
        # Additional tactical effects
        if self.counter_attack:
            effects['counter_attack_boost'] = 2
        if self.offside_trap:
            effects['offside_trap_boost'] = 1.5
            effects['defensive_vulnerability'] = 1
        
        return effects