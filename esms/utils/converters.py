# utils/converters.py
def team_to_engine_model(team_db):
    """Convert database team model to engine Team object for simulation"""
    from esms.engine.team import Team as EngineTeam
    from esms.engine.player import Player as EnginePlayer
    
    engine_team = EngineTeam(team_db.name, team_db.tactic)
    
    # Add players from database to engine team
    for team_player in team_db.players:
        player_db = team_player.player
        
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
        
        # Create engine player
        engine_player = EnginePlayer(
            name=player_db.name,
            position=team_player.position,
            attributes=attributes
        )
        
        engine_team.add_player(engine_player)
    
    return engine_team

def roster_to_engine_model(roster_text):
    """Convert roster text file to engine Team object for simulation"""
    from esms.engine.team import Team as EngineTeam
    from esms.engine.player import Player as EnginePlayer
    from esms.engine.roster import Roster
    
    roster = Roster.parse(roster_text)
    
    # Create Team from roster
    engine_team = EngineTeam(roster.team_name, 'N')  # Default tactic
    
    # Add players
    for player_name, player_data in roster.players_data.items():
        engine_player = EnginePlayer(
            name=player_name,
            position=player_data['position'],
            attributes=player_data['attributes']
        )
        engine_team.add_player(engine_player)
    
    return engine_team