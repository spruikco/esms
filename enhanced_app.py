from flask import Flask, request, render_template, redirect, url_for
import os
import shutil
from werkzeug.utils import secure_filename

# Import our ESMS modules
from esms.teamsheet import Teamsheet
from esms.roster import Roster
from esms.enhanced_match import EnhancedMatchEngine
from esms.config import Config
from esms.tactics import tact_manager
from esms.commentary import commentary_manager

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # Limit file size to 1MB

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('samples', exist_ok=True)

# Copy sample files to the right location if needed
def ensure_sample_files():
    # Check if we need to copy sample files
    if not os.path.exists('samples/home_roster.txt'):
        print("Setting up sample files...")
        try:
            # Copy tactics.dat and language.dat if they don't exist
            if not os.path.exists('tactics.dat') and os.path.exists('samples/tactics.dat'):
                shutil.copy('samples/tactics.dat', 'tactics.dat')
            if not os.path.exists('language.dat') and os.path.exists('samples/language.dat'):
                shutil.copy('samples/language.dat', 'language.dat')
        except Exception as e:
            print(f"Warning: Could not copy sample files: {str(e)}")

# Initialize tactics and commentary managers
def initialize_managers():
    try:
        tact_manager().init('tactics.dat')
        print("Tactics manager initialized")
    except Exception as e:
        print(f"Warning: Could not initialize tactics manager: {str(e)}")
    
    try:
        commentary_manager().init('language.dat')
        print("Commentary manager initialized")
    except Exception as e:
        print(f"Warning: Could not initialize commentary manager: {str(e)}")

# Ensure sample files and initialize managers on startup
ensure_sample_files()
initialize_managers()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        # Get teamsheet and roster files from form
        home_teamsheet_file = request.files['home_teamsheet']
        away_teamsheet_file = request.files['away_teamsheet']
        home_roster_file = request.files['home_roster']
        away_roster_file = request.files['away_roster']
        
        # Save files temporarily
        home_ts_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(home_teamsheet_file.filename))
        away_ts_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(away_teamsheet_file.filename))
        home_roster_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(home_roster_file.filename))
        away_roster_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(away_roster_file.filename))
        
        home_teamsheet_file.save(home_ts_path)
        away_teamsheet_file.save(away_ts_path)
        home_roster_file.save(home_roster_path)
        away_roster_file.save(away_roster_path)
        
        # Read file contents
        with open(home_ts_path, 'r') as f:
            home_teamsheet_text = f.read()
        with open(away_ts_path, 'r') as f:
            away_teamsheet_text = f.read()
        with open(home_roster_path, 'r') as f:
            home_roster_text = f.read()
        with open(away_roster_path, 'r') as f:
            away_roster_text = f.read()
        
        # Parse teamsheets and rosters
        home_teamsheet = Teamsheet.parse(home_teamsheet_text)
        away_teamsheet = Teamsheet.parse(away_teamsheet_text)
        home_roster = Roster.parse(home_roster_text)
        away_roster = Roster.parse(away_roster_text)
        
        # Set up and run match simulation with the enhanced engine
        config = Config()  # Using default configuration for now
        engine = EnhancedMatchEngine(config)
        
        home_team = home_roster.to_team(home_teamsheet)
        away_team = away_roster.to_team(away_teamsheet)
        
        # Verify tactics are valid
        if not tact_manager().tactic_exists(home_team.tactic):
            home_team.tactic = "N"  # Default to Normal if invalid
            print(f"Warning: Invalid home team tactic - defaulting to Normal")
        if not tact_manager().tactic_exists(away_team.tactic):
            away_team.tactic = "N"  # Default to Normal if invalid
            print(f"Warning: Invalid away team tactic - defaulting to Normal")
        
        engine.setup_match(home_team, away_team)
        result = engine.run_full_match()
        
        return render_template('match.html', result=result)
    
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return render_template('error.html', error=error_message)

@app.route('/sample')
def sample():
    """Provide sample match for testing without file uploads"""
    
    # Load sample data
    try:
        with open('samples/home_teamsheet.txt', 'r') as f:
            home_teamsheet_text = f.read()
        with open('samples/away_teamsheet.txt', 'r') as f:
            away_teamsheet_text = f.read()
        with open('samples/home_roster.txt', 'r') as f:
            home_roster_text = f.read()
        with open('samples/away_roster.txt', 'r') as f:
            away_roster_text = f.read()
    except Exception as e:
        error_message = f"Could not load sample files: {str(e)}"
        return render_template('error.html', error=error_message)
    
    # Parse teamsheets and rosters
    home_teamsheet = Teamsheet.parse(home_teamsheet_text)
    away_teamsheet = Teamsheet.parse(away_teamsheet_text)
    home_roster = Roster.parse(home_roster_text)
    away_roster = Roster.parse(away_roster_text)
    
    # Set up and run match simulation with the enhanced engine
    config = Config()  # Using default configuration for now
    engine = EnhancedMatchEngine(config)
    
    home_team = home_roster.to_team(home_teamsheet)
    away_team = away_roster.to_team(away_teamsheet)
    
    engine.setup_match(home_team, away_team)
    result = engine.run_full_match()
    
    return render_template('match.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
