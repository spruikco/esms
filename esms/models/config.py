class Config:
    def __init__(self, config_file=None):
        # Default configuration
        self.config = {
            'HOME_BONUS': 150,
            'CUP': 0,
            'TEAM_STATS_TOTAL': 0,
            'NUM_SUBS': 7,
            'SUBSTITUTIONS': 3,
            'DP_FOR_YELLOW': 3,
            'DP_FOR_RED': 10,
            'SUSPENSION_MARGIN': 10,
            'MAX_INJURY_LENGTH': 5,
            'UPDTR_FITNESS_GAIN': 10,
            'UPDTR_FITNESS_AFTER_INJURY': 80
        }
        
        # Load from file if provided
        if config_file:
            self.load_from_file(config_file)
    
    def load_from_file(self, file_path):
        """Load configuration from league.dat file"""
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                
            for line in lines:
                line = line.strip()
                if line and '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    key = key.strip().upper()
                    value = value.strip()
                    
                    # Try to convert to int if possible
                    try:
                        value = int(value)
                    except ValueError:
                        pass
                    
                    self.config[key] = value
        except Exception as e:
            print(f"Error loading configuration file: {e}")
    
    def get(self, key, default=None):
        """Get a configuration value"""
        return self.config.get(key, default)