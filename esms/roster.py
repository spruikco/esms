from .player import Player
from .team import Team

class Roster:
    def __init__(self, team_name):
        self.team_name = team_name
        self.players = []
    
    @classmethod
    def parse(cls, roster_text):
        """Parse a roster from text"""
        lines = roster_text.strip().split('\n')
        
        # First line should be the header
        if not lines or len(lines) < 3:
            raise ValueError("Invalid roster format: missing header or players")
        
        # Extract team name from the filename or first comment line
        team_name = "Unknown"
        for line in lines:
            if line.strip().startswith("//") and "team:" in line.lower():
                team_name = line.split(":", 1)[1].strip()
                break
        
        roster = cls(team_name)
        
        # Skip header (first 2 lines) and parse player lines
        for i in range(2, len(lines)):
            line = lines[i].strip()
            if line and not line.startswith("//") and not all(c == '-' for c in line):
                try:
                    player = Player.from_roster_line(line)
                    roster.players.append(player)
                except Exception as e:
                    print(f"Error parsing player line: {line}\nError: {e}")
        
        return roster
    
    def to_team(self, teamsheet):
        """Convert roster to a Team using the provided teamsheet"""
        team = Team(self.team_name, self.players.copy())
        team.set_tactic(teamsheet.tactic)
        
        # Set lineup based on teamsheet
        positions_dict = {pos: name for pos, name in teamsheet.lineup}
        team.set_lineup(positions_dict)
        
        # Set substitutes
        team.set_subs(teamsheet.subs)
        
        # Set penalty taker
        if teamsheet.pk_taker:
            team.pk_taker = team.get_player_by_name(teamsheet.pk_taker)
        
        return team