# esms/engine/player.py
import random

class Player:
    """
    Represents a player in the match simulation engine with enhanced attributes
    and performance modeling.
    """
    def __init__(self, name, position, attributes):
        self.name = name
        self.position = position
        self.attributes = attributes
        
        # Base attributes (from roster or database)
        self.speed = attributes.get('speed', 10)
        self.stamina = attributes.get('stamina', 10)
        self.technique = attributes.get('technique', 10)
        self.passing = attributes.get('passing', 10)
        self.shooting = attributes.get('shooting', 10)
        self.tackling = attributes.get('tackling', 10)
        self.heading = attributes.get('heading', 10)
        self.goalkeeper = attributes.get('goalkeeper', 10)
        self.positioning = attributes.get('positioning', 10)
        
        # Additional optional attributes
        self.aggression = attributes.get('aggression', 10)
        self.fitness = attributes.get('fitness', 100)  # 0-100 scale
        
        # Field position attributes (for visualization)
        self.field_x = 0.5  # 0.0 to 1.0 (percentage of field width)
        self.field_y = 0.5  # 0.0 to 1.0 (percentage of field height)
        
        # Match statistics
        self.reset_match_stats()
        
    def reset_match_stats(self):
        """Reset all match-related statistics"""
        self.match_goals = 0
        self.match_assists = 0
        self.match_shots = 0
        self.match_shots_on_target = 0
        self.match_passes = 0
        self.match_passes_completed = 0
        self.match_tackles = 0
        self.match_tackles_won = 0
        self.match_fouls = 0
        self.match_distance = 0
        self.match_minutes = 0
        self.match_saves = 0  # For goalkeepers
        self.match_yellow_card = False
        self.match_red_card = False
        self.current_fatigue = 0
        self.substitution_boost = 1.0  # Fresh players might get a boost
        self.injury_status = None  # None, "minor", "moderate", "severe"
        
    def calculate_fatigue(self, current_minute):
        """
        Calculate player's current fatigue level based on minutes played, 
        stamina, and position
        """
        # No fatigue if not playing
        if self.match_minutes == 0 or current_minute < self.match_minutes:
            return 0
        
        # Base fatigue increases with time, but with diminishing returns
        minutes_played = min(current_minute, 90) - self.match_minutes
        if minutes_played <= 0:
            return 0
            
        # Calculate fatigue curve - increases faster in later minutes
        base_fatigue = (minutes_played / 90.0) ** 1.2 * 10
        
        # Stamina factor - better stamina reduces fatigue impact
        # Scale from 0.5 (best stamina) to 1.5 (worst stamina)
        stamina_factor = 1.5 - (self.stamina / 20.0)
        
        # Position factor - different positions have different workloads
        position_factor = self.get_position_workload()
        
        # Calculate total fatigue
        self.current_fatigue = base_fatigue * stamina_factor * position_factor
        
        # Ensure fatigue is between 0-1
        return max(0, min(1, self.current_fatigue / 10))
        
    def get_position_workload(self):
        """
        Get position-specific workload factor
        Higher values = more fatigue for position
        """
        # Central midfielders and wing-backs typically cover more ground
        if self.position in ['CM', 'LWB', 'RWB']:
            return 1.2
        # Wide midfielders and wingers also run a lot
        elif self.position in ['LM', 'RM', 'LW', 'RW']:
            return 1.15
        # Strikers, attacking midfielders, defensive midfielders with average workload
        elif self.position in ['ST', 'AM', 'DM']:
            return 1.0
        # Defenders have less total running but more high-intensity bursts
        elif self.position in ['CB', 'LB', 'RB']:
            return 0.9
        # Goalkeepers have the least running
        elif self.position == 'GK':
            return 0.5
        # Default for positions not specifically handled
        else:
            return 1.0
        
    def get_effective_attribute(self, attribute_name, current_minute=None):
        """
        Get attribute value adjusted for fatigue, substitution boost and other factors.
        This provides a dynamic performance model throughout the match.
        """
        # Get base attribute value
        base_value = getattr(self, attribute_name, 10)
        
        if current_minute is not None:
            # Apply fatigue penalty
            fatigue = self.calculate_fatigue(current_minute)
            fatigue_penalty = fatigue * 5  # Up to 5 point reduction at max fatigue
            
            # Apply substitution boost for recently substituted players
            boost_value = base_value * (self.substitution_boost - 1.0)
            
            # Reduce substitution boost over time
            if self.substitution_boost > 1.0:
                minutes_since_sub = current_minute - self.match_minutes
                if minutes_since_sub > 15:  # Boost lasts 15 minutes
                    self.substitution_boost = 1.0
                else:
                    # Gradually decrease boost
                    self.substitution_boost = 1.0 + (0.1 * (15 - minutes_since_sub) / 15)
            
            # Random variation factor - players have good and bad moments
            variation = random.uniform(-0.5, 0.5)
            
            # Calculate final value
            final_value = base_value - fatigue_penalty + boost_value + variation
            
            # Ensure value stays in reasonable range
            return max(1, min(20, final_value))
        
        return base_value
        
    def calculate_match_rating(self):
        """
        Calculate player's match rating based on performance metrics,
        position-specific contributions, and overall impact
        """
        # Base rating
        rating = 6.0
        
        # Position-specific rating factors
        if self.position == 'GK':
            # Goalkeepers judged on saves and goals conceded
            save_contribution = self.match_saves * 0.15
            rating += save_contribution
            # Penalty for conceding (approximate as it depends on opponent team)
            # This would need to be handled better in a real implementation
        
        elif self.position in ['CB', 'LB', 'RB', 'LWB', 'RWB']:
            # Defenders judged on tackles, defensive work
            tackle_contribution = self.match_tackles_won * 0.1
            rating += tackle_contribution
            # Bonus for goals/assists as they're rarer for defenders
            rating += self.match_goals * 1.0
            rating += self.match_assists * 0.7
            
        elif self.position in ['CM', 'DM']:
            # Midfielders judged on passing and general play
            pass_contribution = 0
            if self.match_passes > 0:
                pass_completion = self.match_passes_completed / self.match_passes
                pass_contribution = (pass_completion - 0.5) * 2  # Bonus for good passing
            rating += pass_contribution
            rating += self.match_goals * 0.8
            rating += self.match_assists * 0.5
            rating += self.match_tackles_won * 0.08
            
        elif self.position in ['AM', 'LM', 'RM', 'LW', 'RW']:
            # Attacking midfielders/wingers judged on creativity and attack
            rating += self.match_goals * 0.8
            rating += self.match_assists * 0.6
            if self.match_passes > 0:
                pass_completion = self.match_passes_completed / self.match_passes
                pass_contribution = (pass_completion - 0.5) * 1.5
                rating += pass_contribution
            
        elif self.position in ['ST', 'CF']:
            # Strikers judged mainly on goals
            rating += self.match_goals * 1.0
            rating += self.match_assists * 0.4
            # Penalty for strikers who don't get shots on target
            if self.match_shots > 3 and self.match_shots_on_target == 0:
                rating -= 0.5
        
        # Common factors for all positions
        
        # Penalty for cards
        if self.match_yellow_card:
            rating -= 0.3
        if self.match_red_card:
            rating -= 1.5
            
        # Bonus for high involvement (passes, tackles)
        involvement = self.match_passes + self.match_tackles
        if involvement > 30:
            rating += 0.2
            
        # Penalty for high foul count
        if self.match_fouls >= 3:
            rating -= 0.2 * (self.match_fouls - 2)
            
        # Penalty for severe fatigue (if player had to play while very tired)
        if self.current_fatigue > 8:
            rating -= 0.3
            
        # Cap rating between 1-10
        return max(1.0, min(10.0, rating))