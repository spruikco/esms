# esms/routes/team.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from esms.models.team import Team, TeamPlayer
from esms.models.player import Player
from esms.models.formation import Formation
from extensions import db
import json

team_bp = Blueprint('team', __name__)

@team_bp.route('/')
def list_teams():
    """View all teams"""
    teams = Team.query.all()
    # Add player count for each team using count() method
    for team in teams:
        team.player_count = team.players.count()  # Use count() instead of len()
    return render_template('teams.html', teams=teams)

@team_bp.route('/<int:team_id>')
def team_detail(team_id):
    """View team details"""
    team = Team.query.get_or_404(team_id)
    return render_template('team_detail.html', team=team)

@team_bp.route('/new', methods=['GET', 'POST'])
def team_new():
    """Create a new team"""
    if request.method == 'POST':
        name = request.form.get('name')
        tactic = request.form.get('tactic', 'N')
        formation = request.form.get('formation', '4-4-2')
        
        team = Team(name=name, tactic=tactic, formation=formation)
        db.session.add(team)
        db.session.commit()
        
        flash(f"Team '{name}' created successfully!")
        return redirect(url_for('team.team_detail', team_id=team.id))
    
    return render_template('team_form.html')

@team_bp.route('/<int:team_id>/edit', methods=['GET', 'POST'])
def team_edit(team_id):
    """Edit an existing team"""
    team = Team.query.get_or_404(team_id)
    
    if request.method == 'POST':
        team.name = request.form.get('name')
        team.tactic = request.form.get('tactic', 'N')
        team.formation = request.form.get('formation', '4-4-2')
        
        db.session.commit()
        flash(f"Team '{team.name}' updated successfully!")
        return redirect(url_for('team.team_detail', team_id=team.id))
    
    return render_template('team_form.html', team=team)

@team_bp.route('/<int:team_id>/add_player', methods=['GET', 'POST'])
def team_add_player(team_id):
    """Add a player to a team"""
    from esms.models.player import Player
    from esms.models.team import TeamPlayer
    
    team = Team.query.get_or_404(team_id)
    
    if request.method == 'POST':
        player_id = request.form.get('player_id')
        position = request.form.get('position')
        
        player = Player.query.get_or_404(player_id)
        
        # Create team-player association
        team_player = TeamPlayer(team_id=team.id, player_id=player.id, position=position)
        db.session.add(team_player)
        db.session.commit()
        
        flash(f"Added {player.name} to {team.name} as {position}!")
        return redirect(url_for('team.team_detail', team_id=team.id))
    
    # Get players not already in this team
    team_player_ids = [tp.player_id for tp in team.players]
    available_players = Player.query.filter(~Player.id.in_(team_player_ids)).all() if team_player_ids else Player.query.all()
    
    return render_template('team_add_player.html', team=team, players=available_players)

# Formation related routes
@team_bp.route('/<int:team_id>/formation')
def formation(team_id):
    """View and edit team formation"""
    team = Team.query.get_or_404(team_id)
    
    # Get all players for this team with their positions
    players = db.session.query(TeamPlayer, Player).join(
        Player, TeamPlayer.player_id == Player.id
    ).filter(TeamPlayer.team_id == team_id).all()
    
    # Format player data for the frontend
    player_data = []
    for team_player, player in players:
        player_data.append({
            'id': player.id,
            'name': player.name,
            'position': team_player.position,
            'number': getattr(player, 'number', None)  # In case you add jersey numbers later
        })
    
    # Get or create formation
    formation = Formation.query.filter_by(team_id=team_id).first()
    if not formation:
        formation = Formation(
            team_id=team_id,
            formation_type='4-4-2',
            positions={}  # Empty positions to start
        )
        db.session.add(formation)
        db.session.commit()
    
    return render_template(
        'formation.html',
        team=team,
        players=player_data,
        formation=formation
    )

# API endpoints for formation data
@team_bp.route('/<int:team_id>/formation/data')
def formation_data(team_id):
    """API endpoint to get formation data"""
    formation = Formation.query.filter_by(team_id=team_id).first()
    if not formation:
        return jsonify({
            'team_id': team_id,
            'formation_type': '4-4-2',
            'positions': {}
        })
    
    return jsonify({
        'team_id': formation.team_id,
        'formation_type': formation.formation_type,
        'positions': formation.positions
    })

@team_bp.route('/<int:team_id>/formation/save', methods=['POST'])
def formation_save(team_id):
    """API endpoint to save formation data"""
    team = Team.query.get_or_404(team_id)
    
    # Get formation data from request
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    # Get or create formation
    formation = Formation.query.filter_by(team_id=team_id).first()
    if not formation:
        formation = Formation(team_id=team_id)
        db.session.add(formation)
    
    # Update formation data
    formation.formation_type = data.get('formation_type', '4-4-2')
    formation.positions = data.get('positions', {})
    
    try:
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@team_bp.route('/<int:team_id>/players', methods=['GET'])
def team_players_api(team_id):
    """API endpoint to get team players for formation editor"""
    team = Team.query.get_or_404(team_id)
    
    # Get all players for this team with their positions
    team_players = db.session.query(TeamPlayer, Player).join(
        Player, TeamPlayer.player_id == Player.id
    ).filter(TeamPlayer.team_id == team_id).all()
    
    # Format player data for the frontend
    player_data = []
    for team_player, player in team_players:
        player_data.append({
            'id': player.id,
            'name': player.name,
            'position': team_player.position,
            'number': getattr(player, 'number', None)  # In case you add jersey numbers later
        })
    
    return jsonify(player_data)