# esms/routes/main.py
from flask import Blueprint, render_template
from esms.models.match import Match

# Create the Blueprint object
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Main index page"""
    # Get recent matches for display
    recent_matches = Match.query.filter_by(completed=True).order_by(Match.scheduled_time.desc()).limit(5).all()
    return render_template('index.html', matches=recent_matches)

@main_bp.route('/league')
def league():
    """Placeholder for future league functionality"""
    return render_template('placeholder.html', message="League functionality coming soon!")