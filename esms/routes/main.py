# esms/routes/main.py
from flask import Blueprint, render_template, current_app

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page route"""
    # For now, just render the index template without database calls
    # This avoids dependencies on models that might not be implemented yet
    return render_template('index.html')