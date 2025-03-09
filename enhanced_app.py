from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
import os
import shutil
import pycountry
from werkzeug.utils import secure_filename
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # Limit file size to 1MB
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Required for flash messages

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///esms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import and initialize extensions
from extensions import db
db.init_app(app)

# Import models after db is defined 
from models import User, Team, Player, TeamPlayer, Match, MatchEvent, Tactic

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('samples', exist_ok=True)

# Import ESMS modules
from esms.teamsheet import Teamsheet
from esms.roster import Roster
from esms.enhanced_match import EnhancedMatchEngine
from esms.config import Config
from esms.tactics import tact_manager
from esms.commentary import commentary_manager

# Helper function to convert country names to CSS flag codes
def get_country_code(country_name):
    """Convert country name to its 2-letter ISO code"""
    try:
        # Try to find the country by name
        country = pycountry.countries.get(name=country_name)
        if not country:
            # Try to find by common name if not found by official name
            for c in pycountry.countries:
                if hasattr(c, 'common_name') and c.common_name == country_name:
                    country = c
                    break
            
            # Try partial matches if still not found
            if not country:
                matches = [c for c in pycountry.countries if country_name in c.name]
                if matches:
                    country = matches[0]
        
        if country:
            # Return lowercase ISO code for flag-icon-css
            return country.alpha_2.lower()
    except Exception as e:
        print(f"Error finding country code for {country_name}: {str(e)}")
    
    # Return xx as placeholder for unknown
    return 'xx'

# Add context processor for template functions
@app.context_processor
def utility_processor():
    return dict(get_country_code=get_country_code)

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

# Helper function to convert between file-based and database models
def team_from_db(team_db):
    """Convert database team model to ESMS Team object for simulation"""
    from esms.team import Team as ESMSTeam
    from esms.player import Player as ESMSPlayer
    
    esms_team = ESMSTeam(team_db.name, team_db.tactic)
    
    # Add players from database to ESMS team
    for team_player in team_db.players:
        player_db = Player.query.get(team_player.player_id)
        
        # Create attribute dictionary
        attributes = {
            'speed': player_db.speed,
            'stamina': player_db.stamina,
            'technique': player_db.technique,
            'passing': player_db.passing,
            'shooting': player_db.shooting,
            'tackling': player_db.tackling,
            'heading': player_db.heading,
            'goalkeeper': player_db.goalkeeper,
            'positioning': player_db.positioning
        }
        
        # Create ESMS player
        esms_player = ESMSPlayer(
            name=player_db.name,
            position=team_player.position,
            attributes=attributes
        )
        
        esms_team.add_player(esms_player)
    
    return esms_team

# ROUTES
@app.route('/')
def index():
    # Get recent matches for display
    recent_matches = Match.query.filter_by(completed=True).order_by(Match.scheduled_time.desc()).limit(5).all()
    return render_template('index.html', matches=recent_matches)

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

# DATABASE-BACKED ROUTES

@app.route('/league')
def league():
    """Placeholder for future league functionality"""
    return render_template('index.html', message="League functionality coming soon!")

@app.route('/teams')
def teams():
    """View all teams"""
    all_teams = Team.query.all()
    return render_template('teams.html', teams=all_teams)

@app.route('/team/<int:team_id>')
def team_detail(team_id):
    """View a team's details"""
    team = Team.query.get_or_404(team_id)
    return render_template('team_detail.html', team=team)

@app.route('/team/new', methods=['GET', 'POST'])
def team_new():
    """Create a new team"""
    if request.method == 'POST':
        name = request.form.get('name')
        # For now, assign to user_id 1 (later will use current_user.id)
        user_id = 1
        
        team = Team(name=name, user_id=user_id)
        db.session.add(team)
        db.session.commit()
        
        flash(f'Team {name} created successfully!')
        return redirect(url_for('team_detail', team_id=team.id))
    
    return render_template('team_form.html')

@app.route('/team/<int:team_id>/edit', methods=['GET', 'POST'])
def team_edit(team_id):
    """Edit team details"""
    team = Team.query.get_or_404(team_id)
    
    if request.method == 'POST':
        team.name = request.form.get('name')
        team.tactic = request.form.get('tactic')
        team.formation = request.form.get('formation')
        db.session.commit()
        
        flash('Team updated successfully!')
        return redirect(url_for('team_detail', team_id=team.id))
    
    return render_template('team_form.html', team=team)

@app.route('/team/<int:team_id>/formation', methods=['GET', 'POST'])
def team_formation(team_id):
    """Edit team formation"""
    team = Team.query.get_or_404(team_id)
    
    if request.method == 'POST':
        team.formation = request.form.get('formation')
        db.session.commit()
        
        flash('Formation updated successfully!')
        return redirect(url_for('team_detail', team_id=team.id))
    
    return render_template('formation.html', team=team)

@app.route('/api/formation/<int:team_id>', methods=['GET'])
def api_get_formation(team_id):
    """API endpoint to get team formation data"""
    team = Team.query.get_or_404(team_id)
    players = []
    
    for team_player in team.players:
        player = Player.query.get(team_player.player_id)
        players.append({
            'id': player.id,
            'name': player.name,
            'position': team_player.position,
            'x': team_player.x_position if team_player.x_position is not None else None,
            'y': team_player.y_position if team_player.y_position is not None else None
        })
    
    # If team has formation but no player positions are set, set default positions
    if not any(p['x'] is not None and p['y'] is not None for p in players):
        # Apply default formation positions
        formations = {
            '4-4-2': [
                {'position': 'GK', 'x': 0.06, 'y': 0.5},
                {'position': 'LB', 'x': 0.2, 'y': 0.2},
                {'position': 'CB', 'x': 0.2, 'y': 0.4},
                {'position': 'CB', 'x': 0.2, 'y': 0.6},
                {'position': 'RB', 'x': 0.2, 'y': 0.8},
                {'position': 'LM', 'x': 0.4, 'y': 0.2},
                {'position': 'CM', 'x': 0.4, 'y': 0.4},
                {'position': 'CM', 'x': 0.4, 'y': 0.6},
                {'position': 'RM', 'x': 0.4, 'y': 0.8},
                {'position': 'ST', 'x': 0.6, 'y': 0.4},
                {'position': 'ST', 'x': 0.6, 'y': 0.6}
            ],
            '4-3-3': [
                {'position': 'GK', 'x': 0.06, 'y': 0.5},
                {'position': 'LB', 'x': 0.2, 'y': 0.2},
                {'position': 'CB', 'x': 0.2, 'y': 0.4},
                {'position': 'CB', 'x': 0.2, 'y': 0.6},
                {'position': 'RB', 'x': 0.2, 'y': 0.8},
                {'position': 'CM', 'x': 0.4, 'y': 0.3},
                {'position': 'CM', 'x': 0.4, 'y': 0.5},
                {'position': 'CM', 'x': 0.4, 'y': 0.7},
                {'position': 'LW', 'x': 0.6, 'y': 0.2},
                {'position': 'ST', 'x': 0.6, 'y': 0.5},
                {'position': 'RW', 'x': 0.6, 'y': 0.8}
            ],
            '3-5-2': [
                {'position': 'GK', 'x': 0.06, 'y': 0.5},
                {'position': 'CB', 'x': 0.2, 'y': 0.3},
                {'position': 'CB', 'x': 0.2, 'y': 0.5},
                {'position': 'CB', 'x': 0.2, 'y': 0.7},
                {'position': 'LWB', 'x': 0.35, 'y': 0.1},
                {'position': 'CM', 'x': 0.4, 'y': 0.3},
                {'position': 'CM', 'x': 0.4, 'y': 0.5},
                {'position': 'CM', 'x': 0.4, 'y': 0.7},
                {'position': 'RWB', 'x': 0.35, 'y': 0.9},
                {'position': 'ST', 'x': 0.6, 'y': 0.4},
                {'position': 'ST', 'x': 0.6, 'y': 0.6}
            ],
            '5-3-2': [
                {'position': 'GK', 'x': 0.06, 'y': 0.5},
                {'position': 'LWB', 'x': 0.2, 'y': 0.1},
                {'position': 'CB', 'x': 0.2, 'y': 0.3},
                {'position': 'CB', 'x': 0.2, 'y': 0.5},
                {'position': 'CB', 'x': 0.2, 'y': 0.7},
                {'position': 'RWB', 'x': 0.2, 'y': 0.9},
                {'position': 'CM', 'x': 0.4, 'y': 0.3},
                {'position': 'CM', 'x': 0.4, 'y': 0.5},
                {'position': 'CM', 'x': 0.4, 'y': 0.7},
                {'position': 'ST', 'x': 0.6, 'y': 0.4},
                {'position': 'ST', 'x': 0.6, 'y': 0.6}
            ],
            '4-2-3-1': [
                {'position': 'GK', 'x': 0.06, 'y': 0.5},
                {'position': 'LB', 'x': 0.2, 'y': 0.2},
                {'position': 'CB', 'x': 0.2, 'y': 0.4},
                {'position': 'CB', 'x': 0.2, 'y': 0.6},
                {'position': 'RB', 'x': 0.2, 'y': 0.8},
                {'position': 'DM', 'x': 0.35, 'y': 0.35},
                {'position': 'DM', 'x': 0.35, 'y': 0.65},
                {'position': 'LW', 'x': 0.5, 'y': 0.2},
                {'position': 'AM', 'x': 0.5, 'y': 0.5},
                {'position': 'RW', 'x': 0.5, 'y': 0.8},
                {'position': 'ST', 'x': 0.65, 'y': 0.5}
            ]
        }
        
        # Get default positions for current formation
        formation = team.formation if team.formation in formations else '4-4-2'
        default_positions = formations[formation]
        
        # Assign default positions to players based on their assigned position
        for i, player in enumerate(players):
            # Try to find a matching position in the default formation
            matched_position = next((p for p in default_positions if p['position'] == player['position']), None)
            
            if matched_position:
                # Found a matching position, use its coordinates
                player['x'] = matched_position['x'] * 600  # Scale to canvas width
                player['y'] = matched_position['y'] * 400  # Scale to canvas height
            else:
                # No matching position, use a generic position based on index
                player['x'] = 300  # Center X
                player['y'] = 50 + (i * 30)  # Stagger vertically
            
            # Update the database
            team_player = TeamPlayer.query.filter_by(
                team_id=team.id,
                player_id=player['id']
            ).first()
            
            if team_player:
                team_player.x_position = player['x']
                team_player.y_position = player['y']
                
        db.session.commit()
    
    return jsonify({
        'team': team.name,
        'formation': team.formation,
        'players': players
    })

@app.route('/api/formation/<int:team_id>', methods=['POST'])
def api_save_formation(team_id):
    """API endpoint to save team formation data"""
    team = Team.query.get_or_404(team_id)
    data = request.json
    
    if 'formation' in data:
        team.formation = data['formation']
    
    if 'players' in data:
        for player_data in data['players']:
            team_player = TeamPlayer.query.filter_by(
                team_id=team.id, 
                player_id=player_data.get('id')
            ).first()
            
            if team_player:
                team_player.position = player_data.get('position', team_player.position)
                team_player.x_position = player_data.get('x')
                team_player.y_position = player_data.get('y')
    
    db.session.commit()
    return jsonify({'success': True})

@app.route('/players')
def players():
    """View all players"""
    all_players = Player.query.all()
    return render_template('players.html', players=all_players)

@app.route('/player/<int:player_id>')
def player_detail(player_id):
    """View player details"""
    player = Player.query.get_or_404(player_id)
    return render_template('player_detail.html', player=player)

@app.route('/player/new', methods=['GET', 'POST'])
def player_new():
    """Create a new player"""
    if request.method == 'POST':
        # Get basic info
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        full_name = f"{first_name} {last_name}"
        age = int(request.form.get('age', 25))
        nationality = request.form.get('nationality')
        primary_position = request.form.get('primary_position')
        
        # Get attributes from form
        attributes = {
            'speed': int(request.form.get('speed', 10)),
            'stamina': int(request.form.get('stamina', 10)),
            'technique': int(request.form.get('technique', 10)),
            'passing': int(request.form.get('passing', 10)),
            'shooting': int(request.form.get('shooting', 10)),
            'tackling': int(request.form.get('tackling', 10)),
            'heading': int(request.form.get('heading', 10)),
            'goalkeeper': int(request.form.get('goalkeeper', 10)),
            'positioning': int(request.form.get('positioning', 10))
        }
        
        player = Player(
            first_name=first_name,
            last_name=last_name,
            name=full_name,
            age=age,
            nationality=nationality,
            primary_position=primary_position,
            **attributes
        )
        
        db.session.add(player)
        db.session.commit()
        
        flash(f'Player {full_name} created successfully!')
        return redirect(url_for('players'))
    
    return render_template('player_form.html')

@app.route('/player/<int:player_id>/edit', methods=['GET', 'POST'])
def player_edit(player_id):
    """Edit an existing player"""
    player = Player.query.get_or_404(player_id)
    
    if request.method == 'POST':
        # Update basic info
        player.first_name = request.form.get('first_name')
        player.last_name = request.form.get('last_name')
        player.name = f"{player.first_name} {player.last_name}"  # Update full name
        player.age = int(request.form.get('age', 25))
        player.nationality = request.form.get('nationality')
        player.primary_position = request.form.get('primary_position')
        
        # Update attributes
        player.speed = int(request.form.get('speed', 10))
        player.stamina = int(request.form.get('stamina', 10))
        player.technique = int(request.form.get('technique', 10))
        player.passing = int(request.form.get('passing', 10))
        player.shooting = int(request.form.get('shooting', 10))
        player.tackling = int(request.form.get('tackling', 10))
        player.heading = int(request.form.get('heading', 10))
        player.goalkeeper = int(request.form.get('goalkeeper', 10))
        player.positioning = int(request.form.get('positioning', 10))
        
        db.session.commit()
        
        flash(f'Player {player.name} updated successfully!')
        return redirect(url_for('players'))
    
    return render_template('player_form.html', player=player)

@app.route('/team/<int:team_id>/add_player', methods=['GET', 'POST'])
def team_add_player(team_id):
    """Add a player to a team"""
    team = Team.query.get_or_404(team_id)
    
    if request.method == 'POST':
        player_id = request.form.get('player_id')
        position = request.form.get('position')
        
        # Check if player already in team
        existing = TeamPlayer.query.filter_by(
            team_id=team.id, 
            player_id=player_id
        ).first()
        
        if existing:
            flash('Player already in team!')
        else:
            team_player = TeamPlayer(
                team_id=team.id,
                player_id=player_id,
                position=position
            )
            db.session.add(team_player)
            db.session.commit()
            flash('Player added to team!')
        
        return redirect(url_for('team_detail', team_id=team.id))
    
    # Get players not already in the team
    players_in_team = [tp.player_id for tp in team.players]
    available_players = Player.query.filter(~Player.id.in_(players_in_team)).all() if players_in_team else Player.query.all()
    
    return render_template('team_add_player.html', team=team, players=available_players)

@app.route('/schedule')
def schedule():
    """View match schedule"""
    matches = Match.query.filter_by(completed=False).order_by(Match.scheduled_time).all()
    return render_template('schedule.html', matches=matches)

@app.route('/results')
def results():
    """View match results"""
    matches = Match.query.filter_by(completed=True).order_by(Match.scheduled_time.desc()).all()
    return render_template('results.html', matches=matches)

@app.route('/match/new', methods=['GET', 'POST'])
def match_new():
    """Schedule a new match"""
    if request.method == 'POST':
        home_team_id = request.form.get('home_team_id')
        away_team_id = request.form.get('away_team_id')
        
        # Format: YYYY-MM-DDTHH:MM
        scheduled_time_str = request.form.get('scheduled_time')
        scheduled_time = datetime.strptime(scheduled_time_str, '%Y-%m-%dT%H:%M')
        
        match = Match(
            home_team_id=home_team_id,
            away_team_id=away_team_id,
            scheduled_time=scheduled_time
        )
        
        db.session.add(match)
        db.session.commit()
        
        flash('Match scheduled successfully!')
        return redirect(url_for('schedule'))
    
    teams = Team.query.all()
    return render_template('match_form.html', teams=teams)

@app.route('/match/<int:match_id>')
def match_detail(match_id):
    """View match details"""
    match = Match.query.get_or_404(match_id)
    return render_template('match_detail.html', match=match)

# Add this new route to enhanced_app.py
@app.route('/team/<int:team_id>/formation_new', methods=['GET'])
def team_formation_new(team_id):
    """Enhanced interactive formation editor"""
    team = Team.query.get_or_404(team_id)
    return render_template('formation_new.html', team=team)

@app.route('/run_match/<int:match_id>')
def run_match(match_id):
    """Run a match simulation"""
    match = Match.query.get_or_404(match_id)
    
    if match.completed:
        flash('This match has already been played!')
        return redirect(url_for('match_detail', match_id=match.id))
    
    try:
        # Convert database teams to ESMS teams
        home_team = team_from_db(match.home_team)
        away_team = team_from_db(match.away_team)
        
        # Set up and run match simulation
        config = Config()
        engine = EnhancedMatchEngine(config)
        
        # Verify tactics are valid
        if not tact_manager().tactic_exists(home_team.tactic):
            home_team.tactic = "N"  # Default to Normal if invalid
            print(f"Warning: Invalid home team tactic - defaulting to Normal")
        if not tact_manager().tactic_exists(away_team.tactic):
            away_team.tactic = "N"  # Default to Normal if invalid
            print(f"Warning: Invalid away team tactic - defaulting to Normal")
        
        engine.setup_match(home_team, away_team)
        result = engine.run_full_match()
        
        # Update match record with results
        match.home_score = result['home_score']
        match.away_score = result['away_score']
        match.completed = True
        
        # Save match events
        for event in result['events']:
            match_event = MatchEvent(
                match_id=match.id,
                minute=event['minute'],
                event_type=event['type'],
                description=event['description']
            )
            db.session.add(match_event)
        
        db.session.commit()
        
        flash('Match simulated successfully!')
        return render_template('match_result.html', match=match, result=result)
    
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return render_template('error.html', error=error_message)

@app.route('/lineup/<int:match_id>', methods=['GET', 'POST'])
def submit_lineup(match_id):
    """Submit lineup for a match"""
    match = Match.query.get_or_404(match_id)
    
    # For now, we'll use a simple approach without user authentication
    # In a real app, we would check if the current user owns one of the teams
    
    if request.method == 'POST':
        team_id = request.form.get('team_id')
        team = Team.query.get_or_404(team_id)
        
        # Update team's tactic
        team.tactic = request.form.get('tactic', 'N')
        
        # Process player positions
        for key, value in request.form.items():
            if key.startswith('player_pos_'):
                player_id = key.replace('player_pos_', '')
                position = value
                
                # Update or create team player assignment
                team_player = TeamPlayer.query.filter_by(
                    team_id=team.id,
                    player_id=player_id
                ).first()
                
                if team_player:
                    team_player.position = position
        
        db.session.commit()
        flash('Lineup submitted successfully!')
        return redirect(url_for('match_detail', match_id=match.id))
    
    # Choose which team to edit
    # In a real app with authentication, this would be determined by the current user
    home_team = match.home_team
    away_team = match.away_team
    
    return render_template(
        'submit_lineup.html', 
        match=match, 
        home_team=home_team,
        away_team=away_team
    )

# Run the app
if __name__ == '__main__':
    app.run(debug=True)