# esms/engine/commentary.py
class CommentaryManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CommentaryManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def init(self, language_file):
        """Initialize the commentary manager with templates from the language file"""
        if self.initialized:
            return
            
        self.templates = {
            'goal': ["GOAL! {player} scores!"],
            'save': ["Save by {goalkeeper}!"],
            'miss': ["{player} shoots wide!"],
            'foul': ["Foul by {player}!"],
            'yellow_card': ["Yellow card for {player}!"],
            'red_card': ["Red card! {player} is sent off!"]
        }
        
        # Load from file if it exists
        if os.path.exists(language_file):
            self.load_templates(language_file)
        
        self.initialized = True
    
    def load_templates(self, language_file):
        """Load commentary templates from file"""
        # This is a placeholder - you'll implement the actual loading logic later
        print(f"Would load commentary from {language_file}")
    
    def get_template(self, category, context=None):
        """Get a random template from the specified category, with optional context"""
        if not self.initialized:
            return f"Commentary not initialized."
            
        if category not in self.templates or not self.templates[category]:
            return f"[{category}]"  # Default if no templates available
            
        import random
        return random.choice(self.templates[category])
    
    def get_goal(self, scorer, minute, home_score, away_score):
        """Get goal commentary"""
        template = self.get_template('goal')
        return template.replace('{player}', scorer).replace('{minute}', str(minute))
    
    def get_goal_with_assist(self, scorer, assister, minute, home_score, away_score):
        """Get goal with assist commentary"""
        return f"GOAL! {scorer} scores after a brilliant assist from {assister}!"
    
    def get_save(self, goalkeeper, shooter):
        """Get save commentary"""
        template = self.get_template('save')
        return template.replace('{goalkeeper}', goalkeeper).replace('{player}', shooter)
    
    def get_miss(self, shooter):
        """Get miss commentary"""
        template = self.get_template('miss')
        return template.replace('{player}', shooter)
    
    # Add more commentary methods as needed

# Add missing import
import os

# Singleton accessor
def commentary_manager():
    return CommentaryManager()