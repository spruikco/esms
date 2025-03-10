# esms/services/team_service.py
from extensions import db
from esms.models.team import Team
from esms.utils.converters import team_to_engine_model

class TeamService:
    def get_all_teams(self):
        return Team.query.all()
    
    def get_team_by_id(self, team_id):
        return Team.query.get_or_404(team_id)
    
    # Add more methods as needed
    
    def create_team(self, team_data):
        team = Team(**team_data)
        db.session.add(team)
        db.session.commit()
        return team
    
    def update_team(self, team_id, team_data):
        team = self.get_team_by_id(team_id)
        for key, value in team_data.items():
            setattr(team, key, value)
        db.session.commit()
        return team
    
    def convert_to_engine_model(self, team):
        """Convert DB team model to engine model for simulation"""
        return team_to_engine_model(team)