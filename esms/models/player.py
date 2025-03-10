# esms/player.py
class Player:
    def __init__(self, name, position, attributes):
        self.name = name
        self.position = position
        self.attributes = attributes
        
        # Base attributes (read from roster)
        self.speed = attributes.get('speed', 10)
        self.stamina = attributes.get('stamina', 10)
        self.technique = attributes.get('technique', 10)
        self.passing = attributes.get('passing', 10)
        self.shooting = attributes.get('shooting', 10)
        self.tackling = attributes.get('tackling', 10)
        self.heading = attributes.get('heading', 10)
        self.goalkeeper = attributes.get('goalkeeper', 10)
        self.positioning = attributes.get('positioning', 10)
        
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
        self.match_yellow_card = False
        self.match_red_card = False
        self.current_fatigue = 0
        
    def calculate_fatigue(self, current_minute):
        """Calculate player's current fatigue level based on minutes played and stamina"""
        base_fatigue = current_minute / 90.0 * 10  # Base fatigue increases linearly with time
        stamina_factor = (20 - self.stamina) / 10.0  # Lower stamina = higher fatigue
        
        self.current_fatigue = base_fatigue * stamina_factor
        # Ensure fatigue is between 0-1
        return max(0, min(1, self.current_fatigue / 10))
        
    def get_effective_attribute(self, attribute_name, current_minute=None):
        """Get attribute value adjusted for fatigue and other factors"""
        base_value = getattr(self, attribute_name, 10)
        
        if current_minute is not None:
            fatigue_penalty = self.calculate_fatigue(current_minute) * 5
            return max(1, base_value - fatigue_penalty)
        
        return base_value
        
    def calculate_match_rating(self):
        """Calculate player's match rating based on performance"""
        # Base rating
        rating = 6.0
        
        # Contribution to rating from goals and assists
        rating += self.match_goals * 0.8
        rating += self.match_assists * 0.5
        
        # Contribution from general play (passes, tackles)
        if self.match_passes > 0:
            pass_completion = self.match_passes_completed / self.match_passes
            rating += (pass_completion - 0.5) * 2  # Bonus for good passing
        
        tackle_contribution = self.match_tackles_won * 0.1
        rating += tackle_contribution
        
        # Penalty for cards
        if self.match_yellow_card:
            rating -= 0.5
        if self.match_red_card:
            rating -= 2.0
            
        # Cap rating between 1-10
        return max(1.0, min(10.0, rating))