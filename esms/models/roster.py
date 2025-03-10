# esms/roster.py
from esms.player import Player
from esms.team import Team

class Roster:
    """
    Represents a team roster with all players and their attributes
    """
    def __init__(self, team_name, players_data):
        self.team_name = team_name
        self.players_data = players_data  # Dictionary mapping player name to attributes
    
    @classmethod
    def parse(cls, roster_text):
        """
        Parse roster from text format.
        
        Expected format:
        # Team name
        [Team Name]
        
        # Players with attributes
        [Player Name], [Position], [Attributes]
        
        Where attributes are comma-separated values:
        speed,stamina,technique,passing,shooting,tackling,heading,goalkeeper,positioning
        """
        lines = roster_text.strip().split('\n')
        team_name = ""
        players_data = {}
        
        # Process lines
        in_player_section = False
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            if line.startswith('[') and line.endswith(']'):
                # This is the team name
                team_name = line[1:-1]
                in_player_section = True
                continue
                
            if in_player_section and ',' in line:
                # Parse player data
                parts = [part.strip() for part in line.split(',')]
                
                if len(parts) < 3:
                    print(f"Warning: Invalid player line: {line}")
                    continue
                    
                player_name = parts[0]
                position = parts[1]
                
                # Parse attributes
                attributes = {}
                attribute_names = ['speed', 'stamina', 'technique', 'passing', 
                                 'shooting', 'tackling', 'heading', 'goalkeeper', 'positioning']
                
                # Check if attributes are provided
                if len(parts) >= 12:  # Name, position, and at least 9 attributes
                    # Parse numeric attributes
                    for i, attr_name in enumerate(attribute_names):
                        try:
                            attr_value = int(parts[i+2])
                            attributes[attr_name] = attr_value
                        except (ValueError, IndexError):
                            # Default to 10 if attribute is missing or invalid
                            attributes[attr_name] = 10
                else:
                    # If no specific attributes, use defaults based on position
                    attributes = cls._get_default_attributes(position)
                
                players_data[player_name] = {
                    'position': position,
                    'attributes': attributes
                }
        
        return cls(team_name, players_data)
    
    @staticmethod
    def _get_default_attributes(position):
        """Generate default attributes based on player position"""
        attributes = {
            'speed': 10,
            'stamina': 10,
            'technique': 10,
            'passing': 10,
            'shooting': 10,
            'tackling': 10,
            'heading': 10,
            'goalkeeper': 10,
            'positioning': 10
        }
        
        # Adjust defaults based on position
        if position == 'GK':  # Goalkeeper
            attributes['goalkeeper'] = 15
            attributes['positioning'] = 12
            attributes['passing'] = 8
            attributes['shooting'] = 5
        elif position in ['CB', 'LB', 'RB', 'LWB', 'RWB']:  # Defenders
            attributes['tackling'] = 14
            attributes['heading'] = 13
            attributes['positioning'] = 13
            attributes['stamina'] = 12
            attributes['shooting'] = 7
        elif position in ['CM', 'DM', 'LM', 'RM']:  # Midfielders
            attributes['passing'] = 13
            attributes['stamina'] = 13
            attributes['technique'] = 12
            attributes['tackling'] = 11
        elif position in ['AM', 'LW', 'RW']:  # Attacking Midfielders/Wingers
            attributes['speed'] = 13
            attributes['technique'] = 13
            attributes['passing'] = 12
            attributes['shooting'] = 11
        elif position in ['ST', 'CF', 'LF', 'RF']:  # Forwards
            attributes['shooting'] = 14
            attributes['speed'] = 12
            attributes['technique'] = 12
            attributes['heading'] = 11
            attributes['tackling'] = 7
            
        return attributes
    
    def to_team(self, teamsheet):
        """
        Convert roster and teamsheet into a Team object
        """
        team = Team(self.team_name, teamsheet.tactic)
        
        # Process players based on teamsheet positions
        for position, player_name in teamsheet.positions.items():
            # Check if player exists in roster
            if player_name in self.players_data:
                player_data = self.players_data[player_name]
                # Create Player object with data from roster
                player = Player(
                    name=player_name,
                    position=position,  # Use position from teamsheet
                    attributes=player_data['attributes']
                )
                team.add_player(player)
            else:
                # Player not found in roster, create with default attributes
                print(f"Warning: Player '{player_name}' not found in roster, using defaults")
                default_attrs = self._get_default_attributes(position)
                player = Player(
                    name=player_name,
                    position=position,
                    attributes=default_attrs
                )
                team.add_player(player)
        
        return team