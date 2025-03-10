# esms/engine/config.py
"""Configuration for the match engine"""

class Config:
    """Configuration settings for match engine"""
    def __init__(self, **kwargs):
        # Default configuration values
        self.config = {
            'HOME_BONUS': 150,
            'SUBSTITUTIONS': 3,
            'DP_FOR_YELLOW': 3,
            'DP_FOR_RED': 10,
            'SUSPENSION_MARGIN': 10,
            'MAX_INJURY_LENGTH': 5,
            'UPDTR_FITNESS_GAIN': 10,
            'UPDTR_FITNESS_AFTER_INJURY': 80
        }
        
        # Override defaults with any provided kwargs
        self.config.update(kwargs)
    
    def get(self, key, default=None):
        """Get a configuration value"""
        return self.config.get(key, default)