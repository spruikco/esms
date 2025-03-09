class Teamsheet:
    def __init__(self, team_name):
        self.team_name = team_name
        self.tactic = "N"  # Default to Normal
        self.lineup = []  # List of (position, player_name) tuples
        self.subs = []    # List of (position, player_name) tuples
        self.pk_taker = None
        self.orders = []  # List of Order objects
    
    @classmethod
    def parse(cls, teamsheet_text):
        """Parse a teamsheet from text"""
        lines = teamsheet_text.strip().split('\n')
        
        # Remove empty lines and comments
        lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith('//')]
        
        if not lines:
            raise ValueError("Empty teamsheet")
        
        # First line is team name
        team_name = lines[0].strip()
        teamsheet = cls(team_name)
        
        # Second line is tactic
        if len(lines) > 1:
            teamsheet.tactic = lines[1].strip()
        
        # Next 11 lines are starting lineup
        lineup_end = min(13, len(lines))
        for i in range(2, lineup_end):
            parts = lines[i].strip().split()
            if len(parts) >= 2:
                position = parts[0]
                player_name = parts[1]
                teamsheet.lineup.append((position, player_name))
        
        # Next lines are substitutes
        subs_end = min(20, len(lines))  # Assuming up to 7 subs
        for i in range(lineup_end, subs_end):
            if i < len(lines):
                parts = lines[i].strip().split()
                if len(parts) >= 2:
                    position = parts[0]
                    player_name = parts[1]
                    teamsheet.subs.append((position, player_name))
        
        # Find penalty kick taker if specified
        for i in range(subs_end, len(lines)):
            line = lines[i].strip()
            if line.startswith("PK:"):
                pk_parts = line.split(":")
                if len(pk_parts) > 1:
                    teamsheet.pk_taker = pk_parts[1].strip()
                break
        
        # Parse orders (basic implementation for now)
        # Will be expanded in future versions
        
        return teamsheet