# esms/routes/player.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from esms.models.player import Player
from extensions import db

player_bp = Blueprint('player', __name__)

@player_bp.route('/')
def list_players():
    """View all players"""
    players = Player.query.all()
    return render_template('players.html', players=players)

@player_bp.route('/<int:player_id>')
def player_detail(player_id):
    """View player details"""
    player = Player.query.get_or_404(player_id)
    return render_template('player_detail.html', player=player)

@player_bp.route('/new', methods=['GET', 'POST'])
def player_new():
    """Create a new player"""
    if request.method == 'POST':
        # Create a new player from form data
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')
        
        player = Player(
            first_name=first_name,
            last_name=last_name,
            age=int(request.form.get('age', 25)),
            nationality=request.form.get('nationality', ''),
            primary_position=request.form.get('primary_position', ''),
            speed=int(request.form.get('speed', 10)),
            stamina=int(request.form.get('stamina', 10)),
            technique=int(request.form.get('technique', 10)),
            passing=int(request.form.get('passing', 10)),
            shooting=int(request.form.get('shooting', 10)),
            tackling=int(request.form.get('tackling', 10)),
            heading=int(request.form.get('heading', 10)),
            goalkeeper=int(request.form.get('goalkeeper', 10)),
            positioning=int(request.form.get('positioning', 10))
        )
        
        db.session.add(player)
        db.session.commit()
        
        flash(f"Player {player.name} created successfully!")
        return redirect(url_for('player.player_detail', player_id=player.id))
    
    return render_template('player_form.html')

@player_bp.route('/<int:player_id>/edit', methods=['GET', 'POST'])
def player_edit(player_id):
    """Edit an existing player"""
    player = Player.query.get_or_404(player_id)
    
    if request.method == 'POST':
        # Update player from form data
        player.first_name = request.form.get('first_name', '')
        player.last_name = request.form.get('last_name', '')
        player.age = int(request.form.get('age', 25))
        player.nationality = request.form.get('nationality', '')
        player.primary_position = request.form.get('primary_position', '')
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
        flash(f"Player {player.name} updated successfully!")
        return redirect(url_for('player.player_detail', player_id=player.id))
    
    return render_template('player_form.html', player=player)