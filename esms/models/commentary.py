# esms/commentary.py
import random
import os

class commentary_manager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(commentary_manager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def init(self, language_file):
        """Initialize the commentary manager with templates from the language file"""
        if self.initialized:
            return
            
        self.templates = {
            'goal': [],
            'goal_with_assist': [],
            'save': [],
            'miss': [],
            'cross': [],
            'failed_cross': [],
            'through_ball': [],
            'failed_through_ball': [],
            'dribble': [],
            'tackle': [],
            'interception': [],
            'pass': [],
            'foul': [],
            'yellow_card': [],
            'red_card': [],
            'early_game': [],
            'late_game': [],
            'equalizer': [],
            'go_ahead': [],
            'extend_lead': []
        }
        
        self.load_templates(language_file)
        self.initialized = True
    
    def load_templates(self, language_file):
        """Load commentary templates from file"""
        if not os.path.exists(language_file):
            print(f"Warning: Language file {language_file} not found.")
            return
            
        try:
            current_section = None
            with open(language_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                        
                    if line.startswith('[') and line.endswith(']'):
                        current_section = line[1:-1]
                        continue
                        
                    if current_section and current_section in self.templates:
                        self.templates[current_section].append(line)
        except Exception as e:
            print(f"Error loading language file: {str(e)}")
    
    def get_template(self, category, context=None):
        """Get a random template from the specified category, with optional context"""
        if not self.initialized:
            return f"Commentary not initialized."
            
        if category not in self.templates or not self.templates[category]:
            return f"[{category}]"  # Default if no templates available
            
        # Select from appropriate templates based on context
        if context and context in self.templates and self.templates[context]:
            # 50% chance to use context-specific template if available
            if random.random() < 0.5:
                return random.choice(self.templates[context])
                
        return random.choice(self.templates[category])
    
    def get_goal(self, scorer, minute, home_score, away_score):
        """Get goal commentary"""
        # Determine context based on match situation
        context = None
        if minute < 15:
            context = 'early_game'
        elif minute > 75:
            context = 'late_game'
            
        if home_score == away_score:
            context = 'equalizer'
        elif abs(home_score - away_score) == 1:
            context = 'go_ahead'
        elif abs(home_score - away_score) > 1:
            context = 'extend_lead'
            
        template = self.get_template('goal', context)
        return template.replace('{player}', scorer).replace('{minute}', str(minute))
    
    def get_goal_with_assist(self, scorer, assister, minute, home_score, away_score):
        """Get goal with assist commentary"""
        context = None
        if minute < 15:
            context = 'early_game'
        elif minute > 75:
            context = 'late_game'
            
        if home_score == away_score:
            context = 'equalizer'
        elif abs(home_score - away_score) == 1:
            context = 'go_ahead'
        elif abs(home_score - away_score) > 1:
            context = 'extend_lead'
            
        template = self.get_template('goal_with_assist', context)
        return template.replace('{player}', scorer).replace('{assist}', assister).replace('{minute}', str(minute))
    
    def get_save(self, goalkeeper, shooter):
        """Get save commentary"""
        template = self.get_template('save')
        return template.replace('{goalkeeper}', goalkeeper).replace('{player}', shooter)
    
    def get_miss(self, shooter):
        """Get miss commentary"""
        template = self.get_template('miss')
        return template.replace('{player}', shooter)
    
    def get_cross(self, crosser, target):
        """Get cross commentary"""
        template = self.get_template('cross')
        return template.replace('{player}', crosser).replace('{target}', target)
    
    def get_failed_cross(self, crosser, defender):
        """Get failed cross commentary"""
        template = self.get_template('failed_cross')
        return template.replace('{player}', crosser).replace('{defender}', defender)
    
    def get_through_ball(self, passer, receiver):
        """Get through ball commentary"""
        template = self.get_template('through_ball')
        return template.replace('{player}', passer).replace('{target}', receiver)
    
    def get_failed_through_ball(self, passer, defender):
        """Get failed through ball commentary"""
        template = self.get_template('failed_through_ball')
        return template.replace('{player}', passer).replace('{defender}', defender)
    
    def get_dribble(self, dribbler, defender):
        """Get dribble commentary"""
        template = self.get_template('dribble')
        return template.replace('{player}', dribbler).replace('{defender}', defender)
    
    def get_tackle(self, defender, attacker):
        """Get tackle commentary"""
        template = self.get_template('tackle')
        return template.replace('{defender}', defender).replace('{player}', attacker)
    
    def get_interception(self, defender, passer):
        """Get interception commentary"""
        template = self.get_template('interception')
        return template.replace('{defender}', defender).replace('{player}', passer)
    
    def get_pass(self, passer, receiver):
        """Get pass commentary"""
        template = self.get_template('pass')
        return template.replace('{player}', passer).replace('{target}', receiver)
    
    def get_foul(self, fouler, fouled):
        """Get foul commentary"""
        template = self.get_template('foul')
        return template.replace('{player}', fouler).replace('{victim}', fouled)
    
    def get_yellow_card(self, carded, fouled):
        """Get yellow card commentary"""
        template = self.get_template('yellow_card')
        return template.replace('{player}', carded).replace('{victim}', fouled)
    
    def get_red_card(self, carded, fouled):
        """Get red card commentary"""
        template = self.get_template('red_card')
        return template.replace('{player}', carded).replace('{victim}', fouled)