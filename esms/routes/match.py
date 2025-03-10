# esms/routes/match.py
from flask import Blueprint, render_template

match_bp = Blueprint('match', __name__)

@match_bp.route('/')
def list_matches():
    """View all matches"""
    # This will be implemented later
    return render_template('placeholder.html', message="Match listing will be implemented here")