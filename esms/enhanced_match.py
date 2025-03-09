"""
Enhanced match simulation engine for ESMS Python.
Integrates proper tactics and commentary systems.
"""
import random
from .tactics import tact_manager
from .commentary import commentary_manager

class MatchEvent:
    def __init__(self, minute, event_type, team=None, player=None, text=None, 
                 assisting_player=None, additional_data=None):
        self.minute = minute
        self.event_type = event_type
        self.team = team
        self.player = player
        self.assisting_player = assisting_player
        self.additional_data = additional_data or {}
        self.text = text or self.generate_text()
    
    def generate_text(self):
        """Generate text for this event using the commentary system"""
        cm = commentary_manager()
        
        if self.event_type == "kickoff":
            return f"Match begins! {self.team.name} kicks off!"
        elif self.event_type == "halftime":
            return f"Half time! The score is {self.additional_data.get('score', '')}"
        elif self.event_type == "fulltime":
            return f"Full time! Final score: {self.additional_data.get('score', '')}"
        elif self.event_type == "chance":
            return f"Min. {self.minute} :({self.team.name}) {self.player.name} finds some space"
        elif self.event_type == "assisted_chance":
            if self.assisting_player:
                return f"Min. {self.minute} :({self.team.name}) {self.assisting_player.name} passes to {self.player.name}"
            return f"Min. {self.minute} :({self.team.name}) {self.player.name} receives a good pass"
        elif self.event_type == "tackle":
            return f"          ... Cleared by {self.player.name}"
        elif self.event_type == "shot":
            return f"          ... {self.player.name} takes a shot!"
        elif self.event_type == "save":
            return f"          ... Saved by {self.player.name}"
        elif self.event_type == "offtarget":
            return f"          ... But it goes wide"
        elif self.event_type == "goal":
            return f"          ... GOAL!! {self.player.name} scores for {self.team.name}!"
        elif self.event_type == "foul":
            return f"Min. {self.minute} :({self.team.name}) {self.player.name} commits a foul"
        elif self.event_type == "yellow":
            return f"          ... Yellow card for {self.player.name}"
        elif self.event_type == "red":
            return f"          ... RED CARD! {self.player.name} is sent off!"
        elif self.event_type == "pass":
            if self.assisting_player:
                return f"Min. {self.minute} :({self.team.name}) {self.player.name} passes to {self.assisting_player.name}"
            return f"Min. {self.minute} :({self.team.name}) {self.player.name} makes a pass"
        elif self.event_type == "commentary":
            return self.additional_data.get('commentary', f"Min. {self.minute} : Match continues...")
        
        # Generic fallback text
        return f"[{self.event_type.upper()} at minute {self.minute}]"

class EnhancedMatchEngine:
    """
    Enhanced match simulation engine with proper tactics and commentary.
    """
    def __init__(self, config=None):
        self.config = config
        self.events = []
        self.home_team = None
        self.away_team = None
        self.home_score = 0
        self.away_score = 0
        self.current_minute = 0
        
        # Initialize tactics and commentary managers if needed
        try:
            tact_manager().init('tactics.dat')
        except Exception as e:
            print(f"Warning: Could not initialize tactics: {str(e)}")
            
        try:
            commentary_manager().init('language.dat')
        except Exception as e:
            print(f"Warning: Could not initialize commentary: {str(e)}")
    
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
    
    def calculate_player_contribution(self, player, role_positions, skill, tactic, opp_tactic):
        """
        Calculate a player's contribution for a particular skill,
        using the tactics system for proper multipliers.
        """
        # Get the player's position without side (e.g., DF, MF, FW)
        # Assume position is like "DFL", "MFC", etc.
        if player.position and len(player.position) >= 2:
            pos = player.position[0:2]
            
            # Check if the position is a valid one for the role
            if pos in role_positions:
                # Get the player's skill value for this skill
                if skill == "TK":
                    skill_value = player.tk
                elif skill == "PS":
                    skill_value = player.ps
                elif skill == "SH":
                    skill_value = player.sh
                else:
                    return 0
                
                try:
                    # Get the proper multiplier from the tactics system
                    mult = tact_manager().get_mult(tactic, opp_tactic, pos, skill)
                    
                    # Calculate contribution (skill value * multiplier)
                    contribution = skill_value * mult
                    
                    # Apply fitness adjustment (players with low fitness contribute less)
                    fitness_factor = player.fitness / 100.0
                    contribution *= fitness_factor
                    
                    # Apply side adjustment (players on their preferred side perform better)
                    if len(player.position) >= 3 and player.preferred_side:
                        side = player.position[2]
                        if side in player.preferred_side:
                            # Playing on preferred side
                            contribution *= 1.1
                        else:
                            # Playing on non-preferred side
                            contribution *= 0.9
                    
                    return contribution
                    
                except Exception:
                    # If tactics system fails, use a simple fallback
                    return skill_value * 0.5
        
        return 0
    
    def calculate_team_strength(self, team, area, opp_team):
        """
        Calculate team strength in a particular area (attack, midfield, defense)
        using proper tactics multipliers.
        """
        opp_tactic = opp_team.tactic
        
        if area == "attack":
            # Calculate attack strength using shooting and passing
            attack_strength = 0
            
            # Calculate contributions from players
            for player in team.lineup:
                # Forwards contribute most to attack with shooting
                if player.position and player.position.startswith("FW"):
                    attack_strength += self.calculate_player_contribution(
                        player, ["FW"], "SH", team.tactic, opp_tactic)
                    attack_strength += self.calculate_player_contribution(
                        player, ["FW"], "PS", team.tactic, opp_tactic) * 0.5
                
                # Attacking midfielders also contribute significantly
                elif player.position and player.position.startswith("AM"):
                    attack_strength += self.calculate_player_contribution(
                        player, ["AM"], "SH", team.tactic, opp_tactic) * 0.8
                    attack_strength += self.calculate_player_contribution(
                        player, ["AM"], "PS", team.tactic, opp_tactic) * 0.6
                
                # Midfielders contribute with passing primarily
                elif player.position and player.position.startswith("MF"):
                    attack_strength += self.calculate_player_contribution(
                        player, ["MF"], "PS", team.tactic, opp_tactic) * 0.7
                    attack_strength += self.calculate_player_contribution(
                        player, ["MF"], "SH", team.tactic, opp_tactic) * 0.3
                
                # Defensive midfielders contribute a bit
                elif player.position and player.position.startswith("DM"):
                    attack_strength += self.calculate_player_contribution(
                        player, ["DM"], "PS", team.tactic, opp_tactic) * 0.4
                
                # Defenders contribute minimally to attack
                elif player.position and player.position.startswith("DF"):
                    attack_strength += self.calculate_player_contribution(
                        player, ["DF"], "PS", team.tactic, opp_tactic) * 0.2
            
            return attack_strength
            
        elif area == "defense":
            # Calculate defense strength using tackling primarily
            defense_strength = 0
            
            # Add goalkeeper's contribution (shot stopping)
            goalkeeper = team.get_goalkeeper()
            if goalkeeper:
                defense_strength += goalkeeper.st * 3
            
            # Calculate contributions from players
            for player in team.lineup:
                # Defenders contribute most to defense
                if player.position and player.position.startswith("DF"):
                    defense_strength += self.calculate_player_contribution(
                        player, ["DF"], "TK", team.tactic, opp_tactic) * 1.0
                
                # Defensive midfielders also contribute significantly
                elif player.position and player.position.startswith("DM"):
                    defense_strength += self.calculate_player_contribution(
                        player, ["DM"], "TK", team.tactic, opp_tactic) * 0.8
                
                # Midfielders contribute somewhat
                elif player.position and player.position.startswith("MF"):
                    defense_strength += self.calculate_player_contribution(
                        player, ["MF"], "TK", team.tactic, opp_tactic) * 0.5
                
                # Attacking players contribute minimally to defense
                elif player.position and player.position.startswith("AM"):
                    defense_strength += self.calculate_player_contribution(
                        player, ["AM"], "TK", team.tactic, opp_tactic) * 0.3
                elif player.position and player.position.startswith("FW"):
                    defense_strength += self.calculate_player_contribution(
                        player, ["FW"], "TK", team.tactic, opp_tactic) * 0.2
            
            return defense_strength
            
        elif area == "midfield":
            # Calculate midfield strength using primarily passing and some tackling
            midfield_strength = 0
            
            # Calculate contributions from players
            for player in team.lineup:
                # Midfielders contribute most to midfield control
                if player.position and player.position.startswith("MF"):
                    midfield_strength += self.calculate_player_contribution(
                        player, ["MF"], "PS", team.tactic, opp_tactic) * 1.0
                    midfield_strength += self.calculate_player_contribution(
                        player, ["MF"], "TK", team.tactic, opp_tactic) * 0.5
                
                # Defensive and attacking midfielders also contribute significantly
                elif player.position and player.position.startswith("DM"):
                    midfield_strength += self.calculate_player_contribution(
                        player, ["DM"], "PS", team.tactic, opp_tactic) * 0.8
                    midfield_strength += self.calculate_player_contribution(
                        player, ["DM"], "TK", team.tactic, opp_tactic) * 0.7
                elif player.position and player.position.startswith("AM"):
                    midfield_strength += self.calculate_player_contribution(
                        player, ["AM"], "PS", team.tactic, opp_tactic) * 0.8
                    midfield_strength += self.calculate_player_contribution(
                        player, ["AM"], "TK", team.tactic, opp_tactic) * 0.3
                
                # Other positions contribute less to midfield
                elif player.position and player.position.startswith("DF"):
                    midfield_strength += self.calculate_player_contribution(
                        player, ["DF"], "PS", team.tactic, opp_tactic) * 0.3
                elif player.position and player.position.startswith("FW"):
                    midfield_strength += self.calculate_player_contribution(
                        player, ["FW"], "PS", team.tactic, opp_tactic) * 0.3
            
            return midfield_strength
        
        return 0
    
    def simulate_attack(self, attacking_team, defending_team):
        """Simulate an attack using proper tactics"""
        # Get attack and defense strengths
        attack_strength = self.calculate_team_strength(attacking_team, "attack", defending_team)
        defense_strength = self.calculate_team_strength(defending_team, "defense", attacking_team)
        
        # Apply home advantage if applicable
        if attacking_team == self.home_team:
            home_bonus = self.config.get('HOME_BONUS', 150) if self.config else 150
            attack_strength *= (1 + home_bonus / 1000.0)
        
        # Random factor to add variability (0.7 to 1.3)
        random_factor = 0.7 + random.random() * 0.6
        
        # Determine if attack creates a chance
        chance_probability = attack_strength / (attack_strength + defense_strength) * random_factor
        
        if random.random() < chance_probability:
            # Choose attacking player - prefer forwards and attacking midfielders
            forwards = [p for p in attacking_team.lineup if p.position and p.position.startswith("FW")]
            attacking_mids = [p for p in attacking_team.lineup if p.position and p.position.startswith("AM")]
            midfielders = [p for p in attacking_team.lineup if p.position and p.position.startswith("MF")]
            
            # Choose player based on roles and probabilities
            if forwards and random.random() < 0.6:
                # 60% chance a forward creates/receives the chance
                primary_player = random.choice(forwards)
            elif attacking_mids and random.random() < 0.5:
                # 30% chance an attacking midfielder creates/receives the chance
                primary_player = random.choice(attacking_mids)
            elif midfielders and random.random() < 0.8:
                # 8% chance a midfielder creates/receives the chance
                primary_player = random.choice(midfielders)
            else:
                # 2% chance another player creates/receives the chance
                primary_player = random.choice(attacking_team.lineup)
            
            # Determine if this is a solo chance or assisted
            if random.random() < 0.4:  # 40% chance of assisted chance
                # Find a player to assist
                potential_assisters = [p for p in attacking_team.lineup if p != primary_player]
                
                # Prefer midfielders and forwards for assist
                midfield_attackers = [p for p in potential_assisters if p.position and 
                                    (p.position.startswith("MF") or p.position.startswith("AM"))]
                
                if midfield_attackers and random.random() < 0.7:  # 70% chance midfielder assists
                    assister = random.choice(midfield_attackers)
                else:  # 30% chance another player assists
                    assister = random.choice(potential_assisters) if potential_assisters else primary_player
                
                # Create assisted chance event
                chance_event = MatchEvent(
                    self.current_minute, 
                    "assisted_chance", 
                    team=attacking_team, 
                    player=primary_player,
                    assisting_player=assister
                )
            else:
                # Create solo chance event
                chance_event = MatchEvent(
                    self.current_minute, 
                    "chance", 
                    team=attacking_team, 
                    player=primary_player
                )
            
            self.events.append(chance_event)
            
            # Now determine if the chance results in a goal
            # First, check if the defense makes a key tackle
            if random.random() < defense_strength / (attack_strength * 2):
                # Chance stopped by a key tackle
                # Choose a defending player - prefer defenders and defensive midfielders
                defenders = [p for p in defending_team.lineup if p.position and p.position.startswith("DF")]
                def_mids = [p for p in defending_team.lineup if p.position and p.position.startswith("DM")]
                
                if defenders and random.random() < 0.7:  # 70% chance a defender makes the tackle
                    tackler = random.choice(defenders)
                elif def_mids and random.random() < 0.6:  # 18% chance a defensive midfielder makes the tackle
                    tackler = random.choice(def_mids)
                else:  # 12% chance another player makes the tackle
                    tackler = random.choice([p for p in defending_team.lineup if p != defending_team.get_goalkeeper()])
                
                # Create tackle event
                tackle_event = MatchEvent(
                    self.current_minute, 
                    "tackle", 
                    team=defending_team, 
                    player=tackler
                )
                self.events.append(tackle_event)
                
                # Update player stats
                tackler.ktk = getattr(tackler, 'ktk', 0) + 1
            else:
                # Chance results in a shot
                shot_event = MatchEvent(
                    self.current_minute, 
                    "shot", 
                    team=attacking_team, 
                    player=primary_player
                )
                self.events.append(shot_event)
                
                # Update player stats
                primary_player.shots = getattr(primary_player, 'shots', 0) + 1
                
                # Determine if the shot results in a goal
                goalkeeper = defending_team.get_goalkeeper()
                
                if goalkeeper:
                    # Calculate shot power vs goalkeeper ability
                    shot_power = primary_player.sh * (0.8 + random.random() * 0.4)  # Random factor
                    save_power = goalkeeper.st * (0.8 + random.random() * 0.4)  # Random factor
                    
                    # Apply fitness adjustments
                    shot_power *= primary_player.fitness / 100.0
                    save_power *= goalkeeper.fitness / 100.0
                    
                    # Determine goal probability
                    goal_chance = shot_power / (shot_power + save_power)
                    
                    # Random chance of shot going off target
                    if random.random() < 0.2:  # 20% chance of shot off target
                        off_target_event = MatchEvent(
                            self.current_minute, 
                            "offtarget", 
                            team=attacking_team,
                            player=primary_player
                        )
                        self.events.append(off_target_event)
                    elif random.random() < goal_chance:
                        # Goal!
                        self.add_goal(attacking_team, primary_player)
                        
                        # If there was an assister, update their stats
                        if hasattr(chance_event, 'assisting_player') and chance_event.assisting_player:
                            chance_event.assisting_player.assists = getattr(chance_event.assisting_player, 'assists', 0) + 1
                    else:
                        # Save by goalkeeper
                        save_event = MatchEvent(
                            self.current_minute, 
                            "save", 
                            team=defending_team, 
                            player=goalkeeper
                        )
                        self.events.append(save_event)
                        
                        # Update goalkeeper stats
                        goalkeeper.saves = getattr(goalkeeper, 'saves', 0) + 1
                else:
                    # No goalkeeper (highly unlikely) - 90% chance of goal
                    if random.random() < 0.9:
                        self.add_goal(attacking_team, primary_player)
                        
                        # If there was an assister, update their stats
                        if hasattr(chance_event, 'assisting_player') and chance_event.assisting_player:
                            chance_event.assisting_player.assists = getattr(chance_event.assisting_player, 'assists', 0) + 1
    
    def simulate_passing_sequence(self, team):
        """Simulate a passing sequence that doesn't result in a shot"""
        # Choose a midfielder or defender to start the sequence
        midfielders = [p for p in team.lineup if p.position and 
                      (p.position.startswith("MF") or p.position.startswith("DM"))]
        defenders = [p for p in team.lineup if p.position and p.position.startswith("DF")]
        
        if midfielders and random.random() < 0.7:  # 70% chance to start with a midfielder
            starter = random.choice(midfielders)
        elif defenders:  # Otherwise start with a defender
            starter = random.choice(defenders)
        else:
            starter = random.choice(team.lineup)  # Fallback to any player
        
        # Choose another player to receive the pass
        receivers = [p for p in team.lineup if p != starter]
        if not receivers:
            return
        
        receiver = random.choice(receivers)
        
        # Create a passing event
        pass_event = MatchEvent(
            self.current_minute,
            "pass",
            team=team,
            player=starter,
            assisting_player=receiver,
            text=f"Min. {self.current_minute} :({team.name}) {starter.name} passes to {receiver.name}"
        )
        self.events.append(pass_event)
        
        # Update player statistics
        starter.kps = getattr(starter, 'kps', 0) + 1  # Count as a key pass for statistics
        
        # Occasionally add a second pass in the sequence
        if random.random() < 0.4:  # 40% chance for a second pass
            second_receivers = [p for p in team.lineup if p != receiver and p != starter]
            if not second_receivers:
                return
                
            second_receiver = random.choice(second_receivers)
            
            second_pass_event = MatchEvent(
                self.current_minute,
                "pass",
                team=team,
                player=receiver,
                assisting_player=second_receiver,
                text=f"          ... {receiver.name} finds {second_receiver.name}"
            )
            self.events.append(second_pass_event)
            receiver.kps = getattr(receiver, 'kps', 0) + 1

    def add_game_state_commentary(self):
        """Add commentary about the current state of the game"""
        score_diff = abs(self.home_score - self.away_score)
        leading_team = self.home_team if self.home_score > self.away_score else self.away_team
        trailing_team = self.away_team if self.home_score > self.away_score else self.home_team
        
        commentary = ""
        
        # Different commentary based on game state
        if self.home_score == self.away_score:
            options = [
                f"Both teams look evenly matched so far.",
                f"It's still all square with neither team able to break the deadlock.",
                f"The managers will be thinking about changes as we remain tied."
            ]
            commentary = random.choice(options)
        elif score_diff == 1:
            options = [
                f"{leading_team.name} with a slender lead, but it's still anyone's game.",
                f"{trailing_team.name} pushing for an equalizer.",
                f"Just one goal in it as {leading_team.name} tries to hold on."
            ]
            commentary = random.choice(options)
        elif score_diff > 1:
            options = [
                f"{leading_team.name} in control with a {score_diff} goal lead.",
                f"{trailing_team.name} has a mountain to climb, down by {score_diff}.",
                f"It's looking comfortable for {leading_team.name} with their {score_diff} goal cushion."
            ]
            commentary = random.choice(options)
        
        # Add time-specific commentary
        if 30 <= self.current_minute <= 44:
            options = [
                f"Approaching half-time now.",
                f"The first half is winding down."
            ]
            if random.random() < 0.5:  # 50% chance to add this
                commentary += " " + random.choice(options)
        elif 75 <= self.current_minute <= 85:
            options = [
                f"Into the closing stages of the match.",
                f"Not much time left for any more goals."
            ]
            if random.random() < 0.5:  # 50% chance to add this
                commentary += " " + random.choice(options)
        elif self.current_minute > 85:
            options = [
                f"We're deep into the final minutes now.",
                f"The final whistle is approaching."
            ]
            if random.random() < 0.5:  # 50% chance to add this
                commentary += " " + random.choice(options)
        
        if commentary:
            commentary_event = MatchEvent(
                self.current_minute,
                "commentary",
                additional_data={'commentary': f"Min. {self.current_minute} : {commentary}"},
                text=f"Min. {self.current_minute} : {commentary}"
            )
            self.events.append(commentary_event)
    
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
        scorer.goals = getattr(scorer, 'goals', 0) + 1
    
    def check_for_cards(self, team):
        """Check if any players should receive cards"""
        for player in team.lineup:
            # Higher aggression increases card chance
            card_chance = player.ag / 1000.0  # 0-100 aggression gives 0-10% chance
            
            if random.random() < card_chance:
                # Create foul event
                foul_event = MatchEvent(
                    self.current_minute, 
                    "foul", 
                    team=team, 
                    player=player
                )
                self.events.append(foul_event)
                
                # Determine card (yellow most common, red rare)
                card_severity = random.random()
                
                if card_severity < 0.7:  # 70% chance of no card
                    pass  # No card, just a foul
                elif card_severity < 0.95:  # 25% chance of yellow
                    # Yellow card
                    card_event = MatchEvent(
                        self.current_minute, 
                        "yellow", 
                        team=team, 
                        player=player
                    )
                    self.events.append(card_event)
                    if not hasattr(player, 'cards'):
                        player.cards = []
                    player.cards.append("yellow")
                    
                    # Check for second yellow
                    if player.cards.count("yellow") >= 2:
                        red_event = MatchEvent(
                            self.current_minute, 
                            "red", 
                            team=team, 
                            player=player
                        )
                        self.events.append(red_event)
                        player.cards.append("red")
                else:  # 5% chance of straight red
                    # Direct red card
                    red_event = MatchEvent(
                        self.current_minute, 
                        "red", 
                        team=team, 
                        player=player
                    )
                    self.events.append(red_event)
                    if not hasattr(player, 'cards'):
                        player.cards = []
                    player.cards.append("red")
    
    def process_team_orders(self, team, other_team):
        """Process team orders for substitutions and tactic changes"""
        # Score difference (positive if team is winning, negative if losing)
        score_diff = self.home_score - self.away_score
        if team == self.away_team:
            score_diff = -score_diff
            
        # Check for tactic changes based on score and time
        if hasattr(team, 'orders') and team.orders:
            for order in team.orders:
                if order.get('type') == 'TACTIC' and order.get('new_tactic'):
                    # Check conditions
                    min_condition = order.get('min')
                    score_condition = order.get('score')
                    
                    min_met = (min_condition is None or 
                              (min_condition.get('operator') == '>=' and self.current_minute >= min_condition.get('value')) or
                              (min_condition.get('operator') == '<=' and self.current_minute <= min_condition.get('value')) or
                              (min_condition.get('operator') == '=' and self.current_minute == min_condition.get('value')))
                    
                    score_met = (score_condition is None or 
                                (score_condition.get('operator') == '>=' and score_diff >= score_condition.get('value')) or
                                (score_condition.get('operator') == '<=' and score_diff <= score_condition.get('value')) or
                                (score_condition.get('operator') == '=' and score_diff == score_condition.get('value')))
                    
                    if min_met and score_met:
                        # Change tactic
                        old_tactic = team.tactic
                        team.tactic = order.get('new_tactic')
                        
                        # Create tactic change event
                        tactic_event = MatchEvent(
                            self.current_minute,
                            "tactic_change",
                            team=team,
                            additional_data={'new_tactic': team.tactic},
                            text=f"Min. {self.current_minute} :({team.name}) {team.name} will now play {team.tactic}"
                        )
                        self.events.append(tactic_event)
    
    def simulate_minute(self):
        """Simulate one minute of play with increased events"""
        # Process team orders first
        self.process_team_orders(self.home_team, self.away_team)
        self.process_team_orders(self.away_team, self.home_team)
        
        # Determine which team has initiative in this minute
        home_midfield = self.calculate_team_strength(self.home_team, "midfield", self.away_team)
        away_midfield = self.calculate_team_strength(self.away_team, "midfield", self.home_team)
        
        # Apply home advantage to midfield
        home_bonus = self.config.get('HOME_BONUS', 150) if self.config else 150
        home_midfield *= (1 + home_bonus / 1000.0)
        
        # Probability of home team having initiative
        if home_midfield + away_midfield > 0:
            home_initiative_prob = home_midfield / (home_midfield + away_midfield)
        else:
            home_initiative_prob = 0.5
        
        # Determine if an action occurs - INCREASED from 15% to 35% chance per minute
        if random.random() < 0.35:  # Increased event probability
            # Determine attacking team
            if random.random() < home_initiative_prob:
                self.simulate_attack(self.home_team, self.away_team)
            else:
                self.simulate_attack(self.away_team, self.home_team)
        
        # Add occasional passing sequences without shots (for more varied commentary)
        elif random.random() < 0.2:  # 20% chance for a passing sequence
            if random.random() < home_initiative_prob:
                self.simulate_passing_sequence(self.home_team)
            else:
                self.simulate_passing_sequence(self.away_team)
        
        # Check for cards (increased probability)
        if random.random() < 0.05:  # Increased from 3% to 5% chance per minute
            if random.random() < 0.5:
                self.check_for_cards(self.home_team)
            else:
                self.check_for_cards(self.away_team)
        
        # Update player fitness (they get more tired as the game progresses)
        for team in [self.home_team, self.away_team]:
            for player in team.lineup:
                # Reduce fitness based on stamina (higher stamina = less fitness loss)
                fitness_loss = 0.1 * (100 - player.sm) / 100.0
                player.fitness = max(50, player.fitness - fitness_loss)
        
        # Special events at certain minutes
        if self.current_minute == 45:
            halftime_event = MatchEvent(
                45, 
                "halftime", 
                additional_data={'score': f"{self.home_team.name} {self.home_score} - {self.away_score} {self.away_team.name}"}
            )
            self.events.append(halftime_event)
        
        # Add occasional commentator observations about the game state
        if random.random() < 0.05 and self.current_minute > 15:  # 5% chance after minute 15
            self.add_game_state_commentary()
    
    def run_full_match(self):
        """Simulate all minutes of the match"""
        # Simulate each minute
        for minute in range(1, 91):
            self.current_minute = minute
            self.simulate_minute()
        
        # Add full time event
        fulltime_event = MatchEvent(
            90, 
            "fulltime", 
            additional_data={'score': f"{self.home_team.name} {self.home_score} - {self.away_score} {self.away_team.name}"}
        )
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