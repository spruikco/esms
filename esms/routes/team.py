# esms/routes/team.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from esms.models.team import Team
from extensions import db

team_bp = Blueprint('team', __name__)

@team_bp.route('/')
def list_teams():
    """View all teams"""
    teams = Team.query.all()
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