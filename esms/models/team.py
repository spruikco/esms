# esms/team.py
class Team:
    """
    Represents a match-ready team with players and tactics
    """
    def __init__(self, name, tactic='N'):
        self.name = name
        self.tactic = tactic
        self.players = []
        
        # Tactical modifiers (set by match engine)
        self.temp_attacking_boost = 0
        self.temp_defensive_boost = 0
        self.temp_attacking_penalty = 0
        self.temp_defensive_penalty = 0
        self.temp_counter_bonus = 0
        self.temp_passing_boost = 0
    
    def add_player(self, player):
        """Add a player to the team"""
        self.players.append(player)
    
    def get_goalkeeper(self):
        """Get the team's goalkeeper"""
        for player in self.players:
            if player.position == 'GK':
                return player
        return None
    
    def get_defenders(self):
        """Get the team's defenders"""
        return [p for p in self.players if p.position in ['CB', 'LB', 'RB', 'LWB', 'RWB']]
    
    def get_midfielders(self):
        """Get the team's midfielders"""
        return [p for p in self.players if p.position in ['CM', 'DM', 'AM', 'LM', 'RM']]
    
    def get_forwards(self):
        """Get the team's forwards"""
        return [p for p in self.players if p.position in ['ST', 'CF', 'LF', 'RF', 'LW', 'RW']]
    
    def get_attack_strength(self):
        """Calculate team's overall attacking strength"""
        if not self.players:
            return 10
        
        forwards = self.get_forwards()
        midfielders = self.get_midfielders()
        
        # Calculate base attack from forwards and midfielders
        forward_contribution = sum(p.get_effective_attribute('shooting') for p in forwards) if forwards else 0
        mid_contribution = sum(p.get_effective_attribute('passing') for p in midfielders) if midfielders else 0
        
        if not forwards and not midfielders:
            return 10
        
        # Weight forwards more heavily in attack calculation
        total = (forward_contribution * 0.7 + mid_contribution * 0.3) / (len(forwards) * 0.7 + len(midfielders) * 0.3)
        
        # Apply tactical modifiers
        total += self.temp_attacking_boost
        total -= self.temp_attacking_penalty
        
        return max(1, min(20, total))
    
    def get_defense_strength(self):
        """Calculate team's overall defensive strength"""
        if not self.players:
            return 10
            
        defenders = self.get_defenders()
        midfielders = self.get_midfielders()
        goalkeeper = self.get_goalkeeper()
        
        # Calculate base defense from defenders, midfielders and goalkeeper
        def_contribution = sum(p.get_effective_attribute('tackling') for p in defenders) if defenders else 0
        mid_contribution = sum(p.get_effective_attribute('tackling') for p in midfielders) if midfielders else 0
        gk_contribution = goalkeeper.get_effective_attribute('goalkeeper') if goalkeeper else 10
        
        if not defenders and not midfielders:
            return gk_contribution
        
        # Weight defenders more heavily in defense calculation
        total = (def_contribution * 0.6 + mid_contribution * 0.2 + gk_contribution * 0.2) / (len(defenders) * 0.6 + len(midfielders) * 0.2 + 0.2)
        
        # Apply tactical modifiers
        total += self.temp_defensive_boost
        total -= self.temp_defensive_penalty
        
        return max(1, min(20, total))