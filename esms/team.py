class Team:
    def __init__(self, name, players=None):
        self.name = name
        self.players = players or []
        self.tactic = "N"  # Default normal tactic
        self.lineup = []  # Players on the field
        self.subs = []    # Substitutes
        self.pk_taker = None
        
    def add_player(self, player):
        self.players.append(player)
        
    def set_tactic(self, tactic):
        self.tactic = tactic
        
    def set_lineup(self, positions_dict):
        """Set player positions based on a dictionary mapping positions to player names"""
        self.lineup = []
        for position, player_name in positions_dict.items():
            player = self.get_player_by_name(player_name)
            if player:
                player.position = position
                player.in_game = True
                self.lineup.append(player)
    
    def set_subs(self, subs_list):
        """Set substitutes based on a list of (position, player_name) tuples"""
        self.subs = []
        for position, player_name in subs_list:
            player = self.get_player_by_name(player_name)
            if player:
                player.position = position
                player.in_game = False
                self.subs.append(player)
    
    def get_player_by_name(self, name):
        """Find a player by name"""
        for player in self.players:
            if player.name == name:
                return player
        return None
    
    def get_goalkeeper(self):
        """Get the team's goalkeeper"""
        for player in self.lineup:
            if player.position.startswith("GK"):
                return player
        return None
    
    def get_defenders(self):
        """Get all defenders in the lineup"""
        return [p for p in self.lineup if p.position.startswith("DF")]
    
    def get_midfielders(self):
        """Get all midfielders in the lineup"""
        return [p for p in self.lineup if p.position.startswith("MF") or 
                                           p.position.startswith("DM") or 
                                           p.position.startswith("AM")]
    
    def get_forwards(self):
        """Get all forwards in the lineup"""
        return [p for p in self.lineup if p.position.startswith("FW")]