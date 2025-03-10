from flask import Flask
from config import Config
from extensions import db

def create_app(config_class=Config):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from esms.routes.main import main_bp
    from esms.routes.team import team_bp
    from esms.routes.player import player_bp
    from esms.routes.match import match_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(team_bp, url_prefix='/team')
    app.register_blueprint(player_bp, url_prefix='/player')
    app.register_blueprint(match_bp, url_prefix='/match')
    
    # Ensure directories exist
    import os
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('samples', exist_ok=True)
    
    # Initialize engine components
    with app.app_context():
        from esms.engine import init_engine
        init_engine()
        
        # Create all database tables
        db.create_all()
    
    return app

# Create the application instance
app = create_app()

# Add template context processors
from esms.utils.helpers import get_country_code

@app.context_processor
def utility_processor():
    return dict(get_country_code=get_country_code)

if __name__ == '__main__':
    app.run(debug=True)