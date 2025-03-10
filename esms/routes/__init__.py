# routes/__init__.py
def register_routes(app):
    from esms.routes.main import main_bp
    from esms.routes.team import team_bp
    from esms.routes.player import player_bp
    from esms.routes.match import match_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(team_bp, url_prefix='/team')
    app.register_blueprint(player_bp, url_prefix='/player')
    app.register_blueprint(match_bp, url_prefix='/match')

# routes/team.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from esms.services.team_service import TeamService

team_bp = Blueprint('team', __name__)
team_service = TeamService()

@team_bp.route('/')
def list_teams():
    teams = team_service.get_all_teams()
    return render_template('teams.html', teams=teams)

@team_bp.route('/<int:team_id>')
def team_detail(team_id):
    team = team_service.get_team_by_id(team_id)
    return render_template('team_detail.html', team=team)

# ... other team routes