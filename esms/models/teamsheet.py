# esms/teamsheet.py
class Teamsheet:
    """
    Represents a team selection for a match, including positions and tactics
    """
    def __init__(self, team_name, tactic='N'):
        self.team_name = team_name
        self.tactic = tactic
        self.positions = {}  # Map of position -> player name
    
    @classmethod
    def parse(cls, teamsheet_text):
        """
        Parse teamsheet from text format.
        
        Expected format:
        [Team Name]
        [Tactic Code]
        Position: Player Name
        ...
        """
        lines = teamsheet_text.strip().split('\n')
        team_name = ""
        tactic = "N"  # Default tactic
        positions = {}
        
        line_index = 0
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            if line.startswith('[') and line.endswith(']') and line_index == 0:
                # This is the team name
                team_name = line[1:-1]
                line_index += 1
                continue
                
            if line.startswith('[') and line.endswith(']') and line_index == 1:
                # This is the tactic code
                tactic = line[1:-1]
                line_index += 1
                continue
                
            if ':' in line:
                # Parse position and player
                parts = line.split(':', 1)
                position = parts[0].strip()
                player_name = parts[1].strip()
                positions[position] = player_name
                line_index += 1
        
        # Create and configure the teamsheet
        teamsheet = cls(team_name, tactic)
        teamsheet.positions = positions
        return teamsheet
    
    def __str__(self):
        """String representation of the teamsheet"""
        result = f"Team: {self.team_name}\nTactic: {self.tactic}\n\nPlayers:\n"
        for position, player in self.positions.items():
            result += f"{position}: {player}\n"
        return result