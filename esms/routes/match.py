# esms/routes/match.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from esms.models.match import Match, MatchEvent, MatchLineup
from esms.models.team import Team
from esms.services.match_service import MatchService
from extensions import db
from datetime import datetime

match_bp = Blueprint('match', __name__)
match_service = MatchService()

@match_bp.route('/results')
def list_results():
    """List match results"""
    matches = Match.query.filter_by(completed=True).order_by(Match.scheduled_time.desc()).all()
    return render_template('results.html', matches=matches)

@match_bp.route('/schedule')
def schedule():
    """List upcoming matches"""
    matches = Match.query.filter_by(completed=False).order_by(Match.scheduled_time).all()
    return render_template('schedule.html', matches=matches)

@match_bp.route('/matches')
def list_matches():
    """List all matches (alias for schedule)"""
    return redirect(url_for('match.schedule'))

@match_bp.route('/<int:match_id>')
def match_detail(match_id):
    """View match details"""
    match = Match.query.get_or_404(match_id)
    return render_template('match_detail.html', match=match)

@match_bp.route('/new', methods=['GET', 'POST'])
def match_new():
    """Create new match"""
    if request.method == 'POST':
        home_team_id = request.form.get('home_team_id')
        away_team_id = request.form.get('away_team_id')
        scheduled_time = datetime.strptime(request.form.get('scheduled_time'), '%Y-%m-%dT%H:%M')
        
        match = Match(
            home_team_id=home_team_id,
            away_team_id=away_team_id,
            scheduled_time=scheduled_time,
            completed=False,
            home_score=0,
            away_score=0
        )
        
        db.session.add(match)
        db.session.commit()
        
        flash(f"Match scheduled successfully for {scheduled_time.strftime('%Y-%m-%d %H:%M')}")
        return redirect(url_for('match.match_detail', match_id=match.id))
    
    teams = Team.query.all()
    return render_template('match_form.html', teams=teams)

@match_bp.route('/sample')
def sample():
    """Run a sample match"""
    # Load sample data
    with open('samples/home_roster.txt', 'r') as f:
        home_roster = f.read()
    
    with open('samples/away_roster.txt', 'r') as f:
        away_roster = f.read()
        
    with open('samples/home_teamsheet.txt', 'r') as f:
        home_teamsheet = f.read()
        
    with open('samples/away_teamsheet.txt', 'r') as f:
        away_teamsheet = f.read()
    
    # Run sample match
    result = match_service.run_file_simulation(
        home_roster,
        away_roster,
        home_teamsheet,
        away_teamsheet
    )
    
    return render_template('match_result.html', result=result)

@match_bp.route('/simulate', methods=['POST'])
def simulate():
    """Simulate a match from uploaded files"""
    # Get uploaded files
    home_roster_file = request.files.get('home_roster')
    away_roster_file = request.files.get('away_roster')
    home_teamsheet_file = request.files.get('home_teamsheet')
    away_teamsheet_file = request.files.get('away_teamsheet')
    
    if not all([home_roster_file, away_roster_file, home_teamsheet_file, away_teamsheet_file]):
        flash("Please upload all required files")
        return redirect(url_for('main.index'))
    
    # Read file contents
    home_roster = home_roster_file.read().decode('utf-8')
    away_roster = away_roster_file.read().decode('utf-8')
    home_teamsheet = home_teamsheet_file.read().decode('utf-8')
    away_teamsheet = away_teamsheet_file.read().decode('utf-8')
    
    # Run the simulation
    result = match_service.run_file_simulation(
        home_roster,
        away_roster,
        home_teamsheet,
        away_teamsheet
    )
    
    return render_template('match_result.html', result=result)

@match_bp.route('/run/<int:match_id>')
def run_match(match_id):
    """Run simulation for a specific match"""
    match = Match.query.get_or_404(match_id)
    
    if match.completed:
        flash("This match has already been played.")
        return redirect(url_for('match.match_detail', match_id=match.id))
    
    # Run the simulation
    result = match_service.run_match_simulation(match.id)
    
    flash("Match simulation completed!")
    return render_template('match_result.html', result=result, match=match)

@match_bp.route('/lineup/<int:match_id>', methods=['GET', 'POST'])
def submit_lineup(match_id):
    """Submit lineup for a match"""
    match = Match.query.get_or_404(match_id)
    team_id = request.args.get('team_id')
    
    if not team_id:
        flash("Please specify a team.")
        return redirect(url_for('match.match_detail', match_id=match_id))
    
    team = Team.query.get_or_404(team_id)
    
    if request.method == 'POST':
        # Process lineup form
        # Logic to save the lineup to MatchLineup model
        flash("Lineup submitted successfully")
        return redirect(url_for('match.match_detail', match_id=match_id))
    
    # Get all available players for this team
    positions = ['GK', 'LB', 'CB', 'RB', 'LWB', 'RWB', 'DM', 'CM', 'LM', 'RM', 'AM', 'LW', 'RW', 'ST']
    
    # Check for existing lineup
    lineup = MatchLineup.query.filter_by(match_id=match_id, team_id=team_id).first()
    current_starters = []
    current_subs = []
    current_positions = {}
    
    if lineup:
        # Parse existing lineup data
        if lineup.starters:
            current_starters = [int(pid) for pid in lineup.starters.split(',')]
        if lineup.substitutes:
            current_subs = [int(pid) for pid in lineup.substitutes.split(',')]
    
    return render_template('submit_lineup.html', 
                          match=match, 
                          team=team, 
                          positions=positions, 
                          players=team.players,
                          current_starters=current_starters,
                          current_subs=current_subs,
                          current_positions=current_positions)