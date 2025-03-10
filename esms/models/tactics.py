# esms/tactics.py
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
        
        self.load_tactics(tactics_file)
        self.initialized = True
    
    def load_tactics(self, tactics_file):
        """Load tactics from file"""
        if not os.path.exists(tactics_file):
            print(f"Warning: Tactics file {tactics_file} not found.")
            self._init_default_tactics()
            return
            
        try:
            with open(tactics_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                        
                    if line.startswith('[') and ']' in line:
                        parts = line.split(']', 1)
                        tactic_code = parts[0][1:].strip()
                        
                        if len(parts) > 1 and ',' in parts[1]:
                            tactic_parts = parts[1].split(',')
                            if len(tactic_parts) >= 2:
                                tactic_name = tactic_parts[1].strip()
                                
                                # Parse effects
                                effects = {}
                                for i in range(2, len(tactic_parts)):
                                    if ':' in tactic_parts[i]:
                                        effect_parts = tactic_parts[i].split(':')
                                        effect_name = effect_parts[0].strip()
                                        try:
                                            effect_value = float(effect_parts[1].strip())
                                            effects[effect_name] = effect_value
                                        except ValueError:
                                            print(f"Warning: Invalid effect value for {effect_name}")
                                
                                self.tactics[tactic_code] = {
                                    'name': tactic_name,
                                    'effects': effects
                                }
        except Exception as e:
            print(f"Error loading tactics file: {str(e)}")
            self._init_default_tactics()
    
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
            },
            'P': {
                'name': 'Possession',
                'effects': {
                    'passing_boost': 2,
                    'counter_bonus': 0,
                    'attacking_penalty': 0,
                    'defensive_penalty': 0
                }
            },
            'C': {
                'name': 'Counter',
                'effects': {
                    'counter_bonus': 2,
                    'attacking_penalty': 1,
                    'defensive_boost': 1,
                    'passing_boost': 0
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