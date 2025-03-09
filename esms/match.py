import random

class MatchEvent:
    def __init__(self, minute, event_type, team=None, player=None, text=None):
        self.minute = minute
        self.event_type = event_type
        self.team = team
        self.player = player
        self.text = text or self.generate_text()
    
    def generate_text(self):
        """Generate default text for this event"""
        if self.event_type == "goal":
            return f"GOAL! {self.player.name} scores for {self.team.name}!"
        elif self.event_type == "shot":
            return f"{self.player.name} takes a shot for {self.team.name}."
        elif self.event_type == "save":
            return f"Great save by {self.player.name} of {self.team.name}!"
        elif self.event_type == "foul":
            return f"Foul by {self.player.name} of {self.team.name}."
        elif self.event_type == "yellow":
            return f"Yellow card for {self.player.name} of {self.team.name}."
        elif self.event_type == "red":
            return f"RED CARD! {self.player.name} of {self.team.name} is sent off!"
        elif self.event_type == "kickoff":
            return f"Kickoff! {self.team.name} start the game."
        elif self.event_type == "halftime":
            return f"Half time!"
        elif self.event_type == "fulltime":
            return f"Full time!"
        return f"Event: {self.event_type}"

class MatchEngine:
    def __init__(self, config=None):
        self.config = config
        self.events = []
        self.home_team = None
        self.away_team = None
        self.home_score = 0
        self.away_score = 0
        self.current_minute = 0
        
    def setup_match(self, home_team, away_team):
        """Configure teams for the match"""
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = 0
        self.away_score = 0
        self.events = []
        self.current_minute = 0
        
        # Add kickoff event
        kickoff_event = MatchEvent(1, "kickoff", team=self.home_team)
        self.events.append(kickoff_event)
        
    def calculate_team_strength(self, team, area="attack"):
        """Calculate team strength in a particular area (attack, midfield, defense)"""
        if area == "attack":
            # Forwards contribute most to attack
            forwards = team.get_forwards()
            midfielders = team.get_midfielders()
            
            fw_strength = sum(p.sh for p in forwards) * 2 + sum(p.ps for p in forwards)
            mf_strength = sum(p.ps for p in midfielders) + sum(p.sh for p in midfielders) * 0.5
            
            # Apply tactic modifiers (simplified)
            tactic_modifier = 1.0
            if team.tactic == "A":  # Attacking
                tactic_modifier = 1.3
            elif team.tactic == "D":  # Defensive
                tactic_modifier = 0.7
            
            return (fw_strength + mf_strength) * tactic_modifier
            
        elif area == "defense":
            # Defenders and goalkeeper contribute most to defense
            defenders = team.get_defenders()
            goalkeeper = team.get_goalkeeper()
            midfielders = team.get_midfielders()
            
            gk_strength = goalkeeper.st * 3 if goalkeeper else 0
            df_strength = sum(p.tk for p in defenders) * 2
            mf_strength = sum(p.tk for p in midfielders) * 0.5
            
            # Apply tactic modifiers
            tactic_modifier = 1.0
            if team.tactic == "D":  # Defensive
                tactic_modifier = 1.3
            elif team.tactic == "A":  # Attacking
                tactic_modifier = 0.7
            
            return (gk_strength + df_strength + mf_strength) * tactic_modifier
            
        elif area == "midfield":
            # Midfielders contribute most to midfield control
            midfielders = team.get_midfielders()
            defenders = team.get_defenders()
            forwards = team.get_forwards()
            
            mf_strength = sum(p.ps for p in midfielders) * 2 + sum(p.tk for p in midfielders)
            df_strength = sum(p.ps for p in defenders) * 0.5
            fw_strength = sum(p.ps for p in forwards) * 0.5
            
            # Apply tactic modifiers
            tactic_modifier = 1.0
            if team.tactic == "P":  # Passing
                tactic_modifier = 1.2
            
            return (mf_strength + df_strength + fw_strength) * tactic_modifier
        
        return 0
        
    def simulate_attack(self, attacking_team, defending_team):
        """Simulate an attack by one team against another"""
        attack_strength = self.calculate_team_strength(attacking_team, "attack")
        defense_strength = self.calculate_team_strength(defending_team, "defense")
        
        # Home advantage (10% boost for home team)
        if attacking_team == self.home_team:
            attack_strength *= 1.1
        
        # Random factor (0.7 to 1.3)
        random_factor = 0.7 + random.random() * 0.6
        
        # Attack success chance
        success_chance = attack_strength / (attack_strength + defense_strength) * random_factor
        
        # Determine if attack leads to a shot
        if random.random() < success_chance:
            # Choose a player to make the shot (prefer forwards, then midfielders)
            forwards = attacking_team.get_forwards()
            midfielders = attacking_team.get_midfielders()
            
            if forwards and random.random() < 0.7:  # 70% chance a forward takes the shot
                shooter = random.choice(forwards)
            elif midfielders:
                shooter = random.choice(midfielders)
            else:
                shooter = random.choice(attacking_team.lineup)
            
            # Create shot event
            shot_event = MatchEvent(self.current_minute, "shot", team=attacking_team, player=shooter)
            self.events.append(shot_event)
            
            # Determine if shot becomes a goal (based on shooter skill vs GK skill)
            goalkeeper = defending_team.get_goalkeeper()
            
            if goalkeeper:
                shot_power = shooter.sh * (0.8 + random.random() * 0.4)  # Shooting skill with random factor
                save_power = goalkeeper.st * (0.8 + random.random() * 0.4)  # Shot stopping with random factor
                
                goal_chance = shot_power / (shot_power + save_power)
                
                if random.random() < goal_chance:
                    # Goal!
                    self.add_goal(attacking_team, shooter)
                else:
                    # Save
                    save_event = MatchEvent(self.current_minute, "save", team=defending_team, player=goalkeeper)
                    self.events.append(save_event)
            else:
                # No goalkeeper (unlikely), goal is very likely
                if random.random() < 0.9:
                    self.add_goal(attacking_team, shooter)
    
    def add_goal(self, team, scorer):
        """Add a goal to the match"""
        if team == self.home_team:
            self.home_score += 1
        else:
            self.away_score += 1
        
        # Create goal event
        goal_event = MatchEvent(self.current_minute, "goal", team=team, player=scorer)
        self.events.append(goal_event)
        
        # Update player statistics
        scorer.goals += 1
    
    def check_for_cards(self, team):
        """Check if any players should receive cards"""
        for player in team.lineup:
            # Higher aggression increases card chance
            card_chance = player.ag / 500.0  # 0-100 aggression gives 0-20% chance
            
            if random.random() < card_chance:
                # Determine card type (yellow most common, red rare)
                if random.random() < 0.9:  # 90% chance of yellow
                    # Yellow card
                    card_event = MatchEvent(self.current_minute, "yellow", team=team, player=player)
                    self.events.append(card_event)
                    player.cards.append("yellow")
                    
                    # Check for second yellow
                    if player.cards.count("yellow") >= 2:
                        red_event = MatchEvent(self.current_minute, "red", team=team, player=player)
                        self.events.append(red_event)
                        player.cards.append("red")
                else:
                    # Direct red card
                    red_event = MatchEvent(self.current_minute, "red", team=team, player=player)
                    self.events.append(red_event)
                    player.cards.append("red")
    
    def simulate_minute(self):
        """Simulate one minute of play"""
        # Determine which team has initiative in this minute
        home_midfield = self.calculate_team_strength(self.home_team, "midfield")
        away_midfield = self.calculate_team_strength(self.away_team, "midfield")
        
        # Home advantage in midfield
        home_midfield *= 1.1
        
        # Probability of home team having initiative
        home_initiative_prob = home_midfield / (home_midfield + away_midfield)
        
        # 50% chance of an action occurring in this minute
        if random.random() < 0.15:  # Only 15% of minutes have significant actions for simplicity
            # Determine attacking team
            if random.random() < home_initiative_prob:
                self.simulate_attack(self.home_team, self.away_team)
            else:
                self.simulate_attack(self.away_team, self.home_team)
        
        # Check for cards (very low probability)
        if random.random() < 0.02:  # 2% chance per minute
            if random.random() < 0.5:
                self.check_for_cards(self.home_team)
            else:
                self.check_for_cards(self.away_team)
        
        # Special events at certain minutes
        if self.current_minute == 45:
            halftime_event = MatchEvent(45, "halftime")
            self.events.append(halftime_event)
        
    def run_full_match(self):
        """Simulate the full match"""
        for minute in range(1, 91):
            self.current_minute = minute
            self.simulate_minute()
        
        # Add full time event
        fulltime_event = MatchEvent(90, "fulltime")
        self.events.append(fulltime_event)
        
        # Return match result
        return {
            'events': self.events,
            'home_score': self.home_score,
            'away_score': self.away_score,
            'home_team': self.home_team.name,
            'away_team': self.away_team.name,
            'home_team_obj': self.home_team,
            'away_team_obj': self.away_team
        }