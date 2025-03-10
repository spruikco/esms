# esms/engine/tactics.py
import os

class TacticsManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TacticsManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def init(self, tactics_file):
        """Initialize the tactics manager with tactics from the data file"""
        if self.initialized:
            return
            
        self.tactics = {}  # Map of tactic code to tactic data
        
        # Initialize with default tactics
        self._init_default_tactics()
        
        # Try to load from file if it exists
        if os.path.exists(tactics_file):
            self.load_tactics(tactics_file)
        
        self.initialized = True
    
    def load_tactics(self, tactics_file):
        """Load tactics from file"""
        # This is a placeholder - you'll implement the actual loading logic later
        print(f"Would load tactics from {tactics_file}")
            
    def _init_default_tactics(self):
        """Initialize default tactics if file loading fails"""
        self.tactics = {
            'N': {
                'name': 'Normal',
                'effects': {
                    'attacking_boost': 0,
                    'defensive_boost': 0,
                    'attacking_penalty': 0,
                    'defensive_penalty': 0
                }
            },
            'A': {
                'name': 'Attacking',
                'effects': {
                    'attacking_boost': 2,
                    'defensive_boost': 0,
                    'attacking_penalty': 0,
                    'defensive_penalty': 1
                }
            },
            'D': {
                'name': 'Defensive',
                'effects': {
                    'attacking_boost': 0,
                    'defensive_boost': 2,
                    'attacking_penalty': 1,
                    'defensive_penalty': 0
                }
            }
        }
    
    def tactic_exists(self, tactic_code):
        """Check if a tactic code exists"""
        if not self.initialized:
            return False
        return tactic_code in self.tactics
    
    def get_tactic_name(self, tactic_code):
        """Get the name of a tactic from its code"""
        if not self.initialized or tactic_code not in self.tactics:
            return "Unknown"
        return self.tactics[tactic_code]['name']
    
    def get_tactic_effects(self, tactic_code):
        """Get the effects of a tactic from its code"""
        if not self.initialized or tactic_code not in self.tactics:
            return {}
        return self.tactics[tactic_code]['effects']
    
    def get_all_tactics(self):
        """Get all available tactics"""
        if not self.initialized:
            return {}
        return self.tactics

# Singleton accessor
def tact_manager():
    return TacticsManager()