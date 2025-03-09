"""
Commentary generation module for ESMS Python.
Based on the original ESMS language.dat file.
"""
import random
import re


class CommentaryManager:
    """
    Handles commentary generation for match events.
    Uses templates from the language.dat file.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CommentaryManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        # Initialize commentary templates
        self.commentary_templates = {
            'CHANCE': [],
            'ASSISTEDCHANCE': [],
            'TACKLE': [],
            'SHOT': [],
            'SAVE': [],
            'OFFTARGET': [],
            'GOAL': [],
            'GOALCANCELLED': [],
            'INJURY': [],
            'CHANGEPOSITION': [],
            'SUB': [],
            'NOSUBSLEFT': [],
            'CHANGETACTIC': [],
            'FOUL': [],
            'PENALTY': [],
            'WARNED': [],
            'YELLOWCARD': [],
            'SECONDYELLOWCARD': [],
            'REDCARD': [],
            'COMM_KICKOFF': [],
            'COMM_HALFTIME': [],
            'COMM_FULLTIME': [],
            'COMM_SHOTSOFFTARGET': [],
            'COMM_SHOTSONTARGET': [],
            'PENALTYSHOOTOUT': [],
            'WONPENALTYSHOOTOUT': [],
            'COMM_SCORE': [],
            'COMM_INJURYTIME': [],
            'COMM_STATISTICS': []
        }
        
        self._initialized = True
    
    def init(self, filename):
        """Initialize commentary templates from the language.dat file"""
        try:
            with open(filename, 'r') as langfile:
                lines = langfile.readlines()
        except Exception as e:
            raise Exception(f"Failed to open {filename}: {str(e)}")
            
        # Parse language file
        current_key = None
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('|'):  # Skip empty lines and comments
                continue
                
            # Check if this is a category definition line [CATEGORY]
            match = re.match(r'\[(.*?)\]\s*\{(.*)\}', line)
            if match:
                category, template = match.groups()
                if category in self.commentary_templates:
                    # Remove the leading and trailing braces if present
                    template = template.strip('{}')
                    self.commentary_templates[category].append(template)
    
    def get_text(self, category, *args):
        """
        Get a random commentary text of the given category,
        formatted with the provided arguments.
        """
        if category not in self.commentary_templates:
            return f"[Unknown commentary category: {category}]"
            
        templates = self.commentary_templates[category]
        if not templates:
            return f"[No templates available for: {category}]"
            
        template = random.choice(templates)
        
        try:
            # Format the template with the provided arguments
            return template % args
        except Exception as e:
            return f"[Error formatting commentary: {str(e)}]"
    
    def generate_chance(self, minute, team_abbr, player_name):
        """Generate commentary for a scoring chance"""
        return self.get_text('CHANCE', minute, team_abbr, player_name)
    
    def generate_assisted_chance(self, minute, team_abbr, assisting_player, receiving_player):
        """Generate commentary for an assisted scoring chance"""
        return self.get_text('ASSISTEDCHANCE', minute, team_abbr, assisting_player, receiving_player)
    
    def generate_tackle(self, player_name):
        """Generate commentary for a key tackle"""
        return self.get_text('TACKLE', player_name)
    
    def generate_shot(self, player_name):
        """Generate commentary for a shot"""
        return self.get_text('SHOT', player_name)
    
    def generate_save(self, goalkeeper_name):
        """Generate commentary for a save"""
        return self.get_text('SAVE', goalkeeper_name)
    
    def generate_offtarget(self):
        """Generate commentary for a shot going off target"""
        return self.get_text('OFFTARGET')
    
    def generate_goal(self):
        """Generate commentary for a goal"""
        return self.get_text('GOAL')
    
    def generate_foul(self, minute, team_abbr, player_name):
        """Generate commentary for a foul"""
        return self.get_text('FOUL', minute, team_abbr, player_name)
    
    def generate_yellow_card(self):
        """Generate commentary for a yellow card"""
        return self.get_text('YELLOWCARD')
    
    def generate_red_card(self):
        """Generate commentary for a red card"""
        return self.get_text('REDCARD')
    
    def generate_kickoff(self):
        """Generate commentary for kickoff"""
        return self.get_text('COMM_KICKOFF')
    
    def generate_halftime(self):
        """Generate commentary for halftime"""
        return self.get_text('COMM_HALFTIME')
    
    def generate_fulltime(self):
        """Generate commentary for fulltime"""
        return self.get_text('COMM_FULLTIME')
    
    def generate_substitution(self, minute, team_abbr, player_in, player_out, position):
        """Generate commentary for a substitution"""
        return self.get_text('SUB', minute, team_abbr, player_in, player_out, position)
    
    def generate_tactic_change(self, minute, team_abbr, team_name, new_tactic):
        """Generate commentary for a tactic change"""
        return self.get_text('CHANGETACTIC', minute, team_abbr, team_name, new_tactic)

# Singleton instance
def commentary_manager():
    """Get the singleton instance of CommentaryManager"""
    return CommentaryManager()
