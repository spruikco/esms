# esms/routes/main.py
from flask import Blueprint, render_template

# Create the Blueprint object
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Main index page"""
    return render_template('index.html')

@main_bp.route('/league')
def league():
    """Placeholder for future league functionality"""
    return render_template('placeholder.html', message="League functionality coming soon!")