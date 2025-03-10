# services/match_service.py
from esms.models.match import Match, MatchEvent, MatchLineup
from esms.models import db
from esms.utils.converters import team_to_engine_model
from esms.engine.match_engine import EnhancedMatchEngine
from esms.engine.config import Config

class MatchService:
    def run_match_simulation(self, match_id):
        """Run match simulation for a database match"""
        match = self.get_match_by_id(match_id)
        
        # Convert teams to engine models
        home_team = team_to_engine_model(match.home_team)
        away_team = team_to_engine_model(match.away_team)
        
        # Get substitutes
        home_subs = self._get_subs_for_team(match.id, match.home_team_id)
        away_subs = self._get_subs_for_team(match.id, match.away_team_id)
        
        # Run simulation
        config = Config()
        engine = EnhancedMatchEngine(config)
        engine.setup_match(home_team, away_team, home_subs, away_subs)
        result = engine.run_full_match()
        
        # Update match with results
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
        
        return result
        
    def run_file_simulation(self, home_team_data, away_team_data, home_subs=None, away_subs=None):
        """Run match simulation for file-based teams"""
        # Convert data to engine models
        if isinstance(home_team_data, str):
            home_team = roster_to_engine_model(home_team_data)
        else:
            home_team = home_team_data
            
        if isinstance(away_team_data, str):
            away_team = roster_to_engine_model(away_team_data)
        else:
            away_team = away_team_data
        
        # Run simulation
        config = Config()
        engine = EnhancedMatchEngine(config)
        engine.setup_match(home_team, away_team, home_subs, away_subs)
        result = engine.run_full_match()
        
        return result
        
    def _get_subs_for_team(self, match_id, team_id):
        """Get substitute players for a team in a match"""
        lineup = MatchLineup.query.filter_by(
            match_id=match_id, 
            team_id=team_id
        ).first()
        
        if not lineup or not lineup.substitutes:
            return []
            
        subs = []
        for sub_id in lineup.substitutes.split(','):
            player = Player.query.get(int(sub_id))
            if player:
                team_player = TeamPlayer.query.filter_by(
                    team_id=team_id, player_id=player.id
                ).first()
                if team_player:
                    # Convert to engine model
                    attributes = {
                        'speed': player.speed,
                        'stamina': player.stamina,
                        # ... other attributes
                    }
                    engine_player = EnginePlayer(
                        name=player.name,
                        position=team_player.position,
                        attributes=attributes
                    )
                    subs.append(engine_player)
        
        return subs