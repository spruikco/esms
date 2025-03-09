"""
Statistics management module for ESMS Python.
Handles tracking of player statistics during matches and updating rosters.
"""
import random
import os

class StatisticsManager:
    """
    Manages player statistics during and after matches.
    Handles the updating of rosters with new player statistics.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StatisticsManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        # Initialize statistics tracking
        self.match_stats = {}
        self._initialized = True
    
    def reset_match_stats(self):
        """Reset match statistics for a new match"""
        self.match_stats = {
            'player_stats': {},  # Player-specific stats
            'team_stats': {},    # Team-level stats
            'match_events': []   # List of key events for summary
        }
    
    def record_player_stat(self, player, team, stat_type, value=1):
        """
        Record a statistic for a player during a match
        
        Args:
            player: The Player object
            team: The Team object the player belongs to
            stat_type: Type of statistic (e.g., 'goals', 'assists', 'tackles')
            value: Value to add (default is 1)
        """
        player_id = f"{player.name}_{team.name}"
        
        # Initialize player stats if needed
        if player_id not in self.match_stats['player_stats']:
            self.match_stats['player_stats'][player_id] = {
                'player': player,
                'team': team,
                'goals': 0,
                'assists': 0,
                'shots': 0,
                'saves': 0,
                'key_tackles': 0,
                'key_passes': 0,
                'yellow_cards': 0,
                'red_cards': 0,
                'minutes_played': 0,
                'fitness_loss': 0,
                'ability_changes': {
                    'kab': 0,  # Shot stopping ability change
                    'tab': 0,  # Tackling ability change
                    'pab': 0,  # Passing ability change
                    'sab': 0   # Shooting ability change
                }
            }
        
        # Update the statistic
        if stat_type in self.match_stats['player_stats'][player_id]:
            self.match_stats['player_stats'][player_id][stat_type] += value
        
        # Record ability changes based on events
        self._calculate_ability_changes(player_id, stat_type, value)
    
    def record_team_stat(self, team, stat_type, value=1):
        """
        Record a statistic for a team during a match
        
        Args:
            team: The Team object
            stat_type: Type of statistic (e.g., 'goals', 'shots', 'fouls')
            value: Value to add (default is 1)
        """
        team_id = team.name
        
        # Initialize team stats if needed
        if team_id not in self.match_stats['team_stats']:
            self.match_stats['team_stats'][team_id] = {
                'team': team,
                'goals': 0,
                'shots': 0,
                'shots_on_target': 0,
                'fouls': 0,
                'yellow_cards': 0,
                'red_cards': 0,
                'possession': 50  # Default to 50% possession
            }
        
        # Update the statistic
        if stat_type in self.match_stats['team_stats'][team_id]:
            self.match_stats['team_stats'][team_id][stat_type] += value
    
    def record_match_event(self, minute, event_type, description, player=None, team=None):
        """
        Record a key match event for the summary
        
        Args:
            minute: Match minute when the event occurred
            event_type: Type of event (e.g., 'goal', 'card', 'injury')
            description: Description of the event
            player: Optional Player object involved
            team: Optional Team object involved
        """
        event = {
            'minute': minute,
            'type': event_type,
            'description': description,
            'player_name': player.name if player else None,
            'team_name': team.name if team else None
        }
        
        self.match_stats['match_events'].append(event)
    
    def _calculate_ability_changes(self, player_id, stat_type, value):
        """Calculate ability changes based on match events"""
        ability_changes = self.match_stats['player_stats'][player_id]['ability_changes']
        
        # Different events affect different abilities
        if stat_type == 'goals':
            # Scoring goals improves shooting ability
            ability_changes['sab'] += random.randint(20, 30) * value
        elif stat_type == 'assists':
            # Assists improve passing ability
            ability_changes['pab'] += random.randint(15, 25) * value
        elif stat_type == 'key_tackles':
            # Key tackles improve tackling ability
            ability_changes['tab'] += random.randint(15, 25) * value
        elif stat_type == 'saves':
            # Saves improve goalkeeper ability
            ability_changes['kab'] += random.randint(15, 25) * value
        elif stat_type == 'key_passes':
            # Key passes improve passing ability
            ability_changes['pab'] += random.randint(10, 15) * value
        elif stat_type == 'shots':
            # Shots improve shooting ability (slightly)
            ability_changes['sab'] += random.randint(5, 10) * value
    
    def generate_match_summary(self):
        """Generate a summary of the match statistics"""
        summary = {
            'events': self.match_stats['match_events'],
            'top_players': self._get_top_performers(),
            'team_stats': self.match_stats['team_stats']
        }
        
        return summary
    
    def _get_top_performers(self):
        """Identify top performers from the match"""
        top_players = []
        
        # Find goal scorers
        goal_scorers = [(pid, stats) for pid, stats in self.match_stats['player_stats'].items() 
                       if stats['goals'] > 0]
        goal_scorers.sort(key=lambda x: x[1]['goals'], reverse=True)
        
        # Find players with assists
        assisters = [(pid, stats) for pid, stats in self.match_stats['player_stats'].items() 
                    if stats['assists'] > 0]
        assisters.sort(key=lambda x: x[1]['assists'], reverse=True)
        
        # Find players with key tackles
        tacklers = [(pid, stats) for pid, stats in self.match_stats['player_stats'].items() 
                   if stats['key_tackles'] > 0]
        tacklers.sort(key=lambda x: x[1]['key_tackles'], reverse=True)
        
        # Add top goal scorer
        if goal_scorers:
            player_id, stats = goal_scorers[0]
            top_players.append({
                'player_name': stats['player'].name,
                'team_name': stats['team'].name,
                'category': 'Top Scorer',
                'value': stats['goals']
            })
        
        # Add top assister
        if assisters:
            player_id, stats = assisters[0]
            top_players.append({
                'player_name': stats['player'].name,
                'team_name': stats['team'].name,
                'category': 'Most Assists',
                'value': stats['assists']
            })
        
        # Add top tackler
        if tacklers:
            player_id, stats = tacklers[0]
            top_players.append({
                'player_name': stats['player'].name,
                'team_name': stats['team'].name,
                'category': 'Most Key Tackles',
                'value': stats['key_tackles']
            })
        
        return top_players
    
    def update_rosters(self, home_team, away_team, match_result):
        """
        Update team rosters based on match statistics
        
        Args:
            home_team: Home Team object
            away_team: Away Team object
            match_result: Match result dictionary
        
        Returns:
            Dictionary with summary of updates made
        """
        updates = {
            'skill_increases': [],
            'skill_decreases': [],
            'injuries': [],
            'suspensions': [],
            'fitness_changes': []
        }
        
        # Process all players from both teams
        for player_id, stats in self.match_stats['player_stats'].items():
            player = stats['player']
            team = stats['team']
            
            # Update games played
            player.games += 1
            
            # Update goals
            player.goals += stats['goals']
            
            # Update assists
            player.assists += stats['assists']
            
            # Update shots
            player.shots += stats['shots']
            
            # Update key tackles
            player.ktk += stats['key_tackles']
            
            # Update key passes
            player.kps += stats['key_passes']
            
            # Update saves (for goalkeepers)
            player.saves += stats['saves']
            
            # Process disciplinary points
            dp_for_yellow = 3  # Default value, can be configurable
            dp_for_red = 10    # Default value, can be configurable
            
            player.dp += (stats['yellow_cards'] * dp_for_yellow)
            player.dp += (stats['red_cards'] * dp_for_red)
            
            # Check for suspensions
            suspension_margin = 10  # Default value, can be configurable
            if player.dp >= suspension_margin and player.dp % suspension_margin == 0:
                games_suspended = player.dp // suspension_margin
                player.suspension += games_suspended
                updates['suspensions'].append({
                    'player_name': player.name,
                    'team_name': team.name,
                    'games': games_suspended
                })
            
            # Process random injuries (small chance for players who played)
            if stats['minutes_played'] > 0 and random.random() < 0.05:  # 5% injury chance
                injury_duration = random.randint(1, 3)  # 1-3 weeks of injury
                player.injury += injury_duration
                updates['injuries'].append({
                    'player_name': player.name,
                    'team_name': team.name,
                    'duration': injury_duration
                })
            
            # Update fitness
            fitness_loss = min(30, stats['minutes_played'] // 3)  # Rough estimation
            player.fitness = max(70, player.fitness - fitness_loss)
            updates['fitness_changes'].append({
                'player_name': player.name,
                'team_name': team.name,
                'new_fitness': player.fitness
            })
            
            # Process ability changes and check for skill increases/decreases
            for ability_type, change in stats['ability_changes'].items():
                if ability_type == 'kab':
                    player.kab += change
                    
                    # Check for skill increase
                    if player.kab >= 1000:
                        player.kab -= 1000
                        player.st += 1
                        updates['skill_increases'].append({
                            'player_name': player.name,
                            'team_name': team.name,
                            'skill': 'Shot stopping',
                            'new_value': player.st
                        })
                
                elif ability_type == 'tab':
                    player.tab += change
                    
                    # Check for skill increase
                    if player.tab >= 1000:
                        player.tab -= 1000
                        player.tk += 1
                        updates['skill_increases'].append({
                            'player_name': player.name,
                            'team_name': team.name,
                            'skill': 'Tackling',
                            'new_value': player.tk
                        })
                
                elif ability_type == 'pab':
                    player.pab += change
                    
                    # Check for skill increase
                    if player.pab >= 1000:
                        player.pab -= 1000
                        player.ps += 1
                        updates['skill_increases'].append({
                            'player_name': player.name,
                            'team_name': team.name,
                            'skill': 'Passing',
                            'new_value': player.ps
                        })
                
                elif ability_type == 'sab':
                    player.sab += change
                    
                    # Check for skill increase
                    if player.sab >= 1000:
                        player.sab -= 1000
                        player.sh += 1
                        updates['skill_increases'].append({
                            'player_name': player.name,
                            'team_name': team.name,
                            'skill': 'Shooting',
                            'new_value': player.sh
                        })
        
        # Write updated rosters to files
        self._write_updated_roster(home_team)
        self._write_updated_roster(away_team)
        
        return updates
    
    def _write_updated_roster(self, team):
        """Write the updated roster to file"""
        # Determine the filename based on team name
        filename = f"{team.name.lower()}.txt"
        
        try:
            # Create roster content
            content = f"// team: {team.name}\n"
            content += "Name         Age Nat Prs St Tk Ps Sh Sm Ag KAb TAb PAb SAb Gam Sav Ktk Kps Sht Gls Ass  DP Inj Sus Fit\n"
            content += "------------------------------------------------------------------------------------------------------\n"
            
            # Add each player
            for player in team.players:
                content += f"{player.name.ljust(12)} {str(player.age).rjust(2)} {player.nationality} "
                content += f"{player.preferred_side.ljust(3)} {str(player.st).rjust(2)} {str(player.tk).rjust(2)} "
                content += f"{str(player.ps).rjust(2)} {str(player.sh).rjust(2)} {str(player.sm).rjust(2)} "
                content += f"{str(player.ag).rjust(2)} {str(player.kab).rjust(3)} {str(player.tab).rjust(3)} "
                content += f"{str(player.pab).rjust(3)} {str(player.sab).rjust(3)} {str(player.games).rjust(3)} "
                content += f"{str(player.saves).rjust(3)} {str(player.ktk).rjust(3)} {str(player.kps).rjust(3)} "
                content += f"{str(player.shots).rjust(3)} {str(player.goals).rjust(3)} {str(player.assists).rjust(3)} "
                content += f"{str(player.dp).rjust(3)} {str(player.injury).rjust(3)} {str(player.suspension).rjust(3)} "
                content += f"{str(player.fitness).rjust(3)}\n"
            
            # Create the directory for updated rosters if it doesn't exist
            os.makedirs("updated_rosters", exist_ok=True)
            
            # Write to file
            with open(f"updated_rosters/{filename}", 'w') as f:
                f.write(content)
        
        except Exception as e:
            print(f"Error writing updated roster for {team.name}: {str(e)}")

# Singleton instance
def stats_manager():
    """Get the singleton instance of StatisticsManager"""
    return StatisticsManager()
