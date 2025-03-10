# esms/routes/player.py
from flask import Blueprint, render_template

# Create the Blueprint object 
player_bp = Blueprint('player', __name__)

@player_bp.route('/')
def list_players():
    """View all players"""
    # This will be implemented later
    return render_template('placeholder.html', message="Player listing will be implemented here")