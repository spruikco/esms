# esms/routes/team.py
from flask import Blueprint, render_template

team_bp = Blueprint('team', __name__)

@team_bp.route('/')
def list_teams():
    """View all teams"""
    # This will be implemented later
    return render_template('placeholder.html', message="Team listing will be implemented here")