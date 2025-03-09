# esms/enhanced_match.py
import random
from esms.tactics import tact_manager
from esms.commentary import commentary_manager

class EnhancedMatchEngine:
    def __init__(self, config):
        self.config = config
        self.home_team = None
        self.away_team = None
        self.current_minute = 0
        self.home_score = 0
        self.away_score = 0
        self.match_events = []
        
        # Match statistics
        self.home_possession = 50
        self.away_possession = 50
        self.home_shots = 0
        self.away_shots = 0
        self.home_shots_on_target = 0
        self.away_shots_on_target = 0
        self.home_fouls = 0
        self.away_fouls = 0
        self.home_corners = 0
        self.away_corners = 0
        
        # Match status
        self.last_team_with_ball = None
        self.current_zone = 3  # Middle zone (1-5 scale: 1=home goal, 5=away goal)
        self.momentum = 0  # -10 to +10 scale (negative=home momentum, positive=away)

    def setup_match(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team
        
        # Reset player stats
        for player in self.home_team.players + self.away_team.players:
            player.reset_match_stats()
            
        # Apply tactical effects
        self.apply_tactical_effects(self.home_team, self.away_team)
        self.apply_tactical_effects(self.away_team, self.home_team)
        
        # Reset match statistics
        self.home_score = 0
        self.away_score = 0
        self.current_minute = 0
        self.match_events = []
        self.last_team_with_ball = self.home_team if random.random() < 0.5 else self.away_team
        self.current_zone = 3
        self.momentum = 0

    def apply_tactical_effects(self, team, opponent):
        """Apply tactical effects to team attributes"""
        tactic = team.tactic
        
        # Default values if tactic not found
        team.temp_attacking_boost = 0
        team.temp_defensive_boost = 0
        team.temp_attacking_penalty = 0
        team.temp_defensive_penalty = 0
        team.temp_counter_bonus = 0
        
        # Get tactic effects from the tactics manager
        tactic_effects = tact_manager().get_tactic_effects(tactic)
        
        if tactic_effects:
            # Apply effects based on tactic
            if tactic == 'A':  # Attacking
                team.temp_attacking_boost = tactic_effects.get('attacking_boost', 2)
                team.temp_defensive_penalty = tactic_effects.get('defensive_penalty', 1)
            elif tactic == 'D':  # Defensive
                team.temp_defensive_boost = tactic_effects.get('defensive_boost', 2)
                team.temp_attacking_penalty = tactic_effects.get('attacking_penalty', 1)
            elif tactic == 'P':  # Possession
                team.temp_passing_boost = tactic_effects.get('passing_boost', 2)
                
            # Consider counter-tactic relationships
            if tactic == 'P' and opponent.tactic == 'A':  # Possession against Attacking
                team.temp_counter_bonus = tactic_effects.get('counter_bonus', 1)
            elif tactic == 'C' and opponent.tactic == 'P':  # Counter against Possession
                team.temp_counter_bonus = tactic_effects.get('counter_bonus', 2)

    def run_full_match(self):
        """Run a complete match simulation"""
        self.add_event(0, "kickoff", "Match begins!")
        
        # Simulate first half
        self.simulate_half(1, 1, 45)
        
        # Half time
        self.add_event(45, "halftime", f"Half time score: {self.home_team.name} {self.home_score} - {self.away_score} {self.away_team.name}")
        
        # Simulate second half
        self.simulate_half(2, 46, 90)
        
        # Generate match stats
        match_stats = self.generate_match_stats()
        
        # Final whistle
        self.add_event(90, "fulltime", f"Full time: {self.home_team.name} {self.home_score} - {self.away_score} {self.away_team.name}")
        
        return {
            'home_team': self.home_team,
            'away_team': self.away_team,
            'home_score': self.home_score,
            'away_score': self.away_score,
            'events': self.match_events,
            'statistics': match_stats
        }

    def simulate_half(self, half_id, start_minute, end_minute):
        """Simulate one half of the match"""
        self.current_minute = start_minute
        
        while self.current_minute < end_minute:
            # Determine event time increment (1-3 minutes)
            time_increment = random.randint(1, 3)
            self.current_minute += time_increment
            
            if self.current_minute > end_minute:
                self.current_minute = end_minute
                
            # Generate match event
            self.generate_match_event()
            
            # Update player fatigue and match distance
            for player in self.home_team.players + self.away_team.players:
                player.match_minutes = self.current_minute
                # Simulate distance covered
                distance_per_minute = random.uniform(0.08, 0.12)  # km per minute
                player.match_distance += distance_per_minute * time_increment

    def generate_match_event(self):
        """Generate a single match event based on current state"""
        # Update possession
        self.update_possession()
        
        # Determine which team has the ball for this event
        if random.random() * 100 < self.home_possession:
            attacking_team = self.home_team
            defending_team = self.away_team
            is_home_attacking = True
        else:
            attacking_team = self.away_team
            defending_team = self.home_team
            is_home_attacking = False
        
        # Update field position based on team with ball
        self.update_field_position(attacking_team, is_home_attacking)
        
        # Determine event type based on field position
        if self.current_zone in [1, 5]:  # Goal zones
            self.process_goal_attempt(attacking_team, defending_team, is_home_attacking)
        elif self.current_zone in [2, 4]:  # Attacking zones
            self.process_attacking_play(attacking_team, defending_team, is_home_attacking)
        else:  # Midfield zone
            self.process_midfield_play(attacking_team, defending_team, is_home_attacking)
            
        # Update momentum
        self.update_momentum(attacking_team, defending_team, is_home_attacking)

    def update_possession(self):
        """Update possession statistics based on team tactics and momentum"""
        # Base possession tendency
        if self.home_team.tactic == 'P':  # Possession tactic
            base_possession = 55
        elif self.away_team.tactic == 'P':
            base_possession = 45
        else:
            base_possession = 50
            
        # Momentum effect (momentum is -10 to +10, negative values favor home team)
        momentum_effect = -self.momentum  # Negated because negative momentum favors home
        
        # Calculate new possession value
        new_possession = base_possession + momentum_effect * 0.5
        
        # Ensure it's within valid range
        self.home_possession = max(30, min(70, new_possession))
        self.away_possession = 100 - self.home_possession

    def update_field_position(self, attacking_team, is_home_attacking):
        """Update the field position based on the attacking team and current state"""
        # Direction of movement (home team moves towards zone 5, away towards zone 1)
        direction = 1 if is_home_attacking else -1
        
        # Base probability of moving forward 
        forward_prob = 0.6
        
        # Adjust based on tactics
        if attacking_team.tactic == 'A':  # Attacking
            forward_prob += 0.1
        elif attacking_team.tactic == 'D':  # Defensive
            forward_prob -= 0.1
            
        # Adjust based on current zone (harder to advance near opponent's goal)
        if (is_home_attacking and self.current_zone >= 4) or (not is_home_attacking and self.current_zone <= 2):
            forward_prob -= 0.15
            
        # Determine movement
        if random.random() < forward_prob:
            # Move forward
            new_zone = self.current_zone + direction
        else:
            # Move backward or stay
            new_zone = self.current_zone - direction
            
        # Ensure zone is within valid range
        self.current_zone = max(1, min(5, new_zone))

    def process_goal_attempt(self, attacking_team, defending_team, is_home_attacking):
        """Process a goal attempt"""
        # Select attacking player (prefer forwards)
        attacker = self.select_player_for_action(attacking_team, preference='forward')
        
        # Select goalkeeper
        goalkeeper = self.select_player_for_action(defending_team, preference='goalkeeper')
        
        # Record shot
        self.increment_shots(is_home_attacking)
        attacker.match_shots += 1
        
        # Determine if it's on target
        shooting_skill = attacker.get_effective_attribute('shooting', self.current_minute)
        on_target_chance = 0.3 + (shooting_skill / 40)  # Base 30% + up to 50% from skill
        
        if random.random() < on_target_chance:
            # Shot is on target
            self.increment_shots_on_target(is_home_attacking)
            attacker.match_shots_on_target += 1
            
            # Determine if it's a goal
            gk_skill = goalkeeper.get_effective_attribute('goalkeeper', self.current_minute)
            save_chance = 0.6 + (gk_skill / 50)  # Base 60% + up to 40% from skill
            
            if random.random() > save_chance:
                # Goal scored!
                if is_home_attacking:
                    self.home_score += 1
                else:
                    self.away_score += 1
                    
                attacker.match_goals += 1
                
                # Determine if there was an assist
                if random.random() < 0.7:  # 70% of goals have assists
                    assister = self.select_player_for_action(attacking_team, exclude=[attacker])
                    assister.match_assists += 1
                    goal_desc = commentary_manager().get_goal_with_assist(
                        attacker.name, assister.name, self.current_minute, self.home_score, self.away_score)
                else:
                    goal_desc = commentary_manager().get_goal(
                        attacker.name, self.current_minute, self.home_score, self.away_score)
                
                self.add_event(self.current_minute, "goal", goal_desc)
                
                # Big momentum swing for scoring team
                self.momentum += -5 if is_home_attacking else 5
            else:
                # Save by goalkeeper
                save_desc = commentary_manager().get_save(goalkeeper.name, attacker.name)
                self.add_event(self.current_minute, "save", save_desc)
                
                # Small momentum boost for good save
                self.momentum += 1 if is_home_attacking else -1
        else:
            # Shot off target
            miss_desc = commentary_manager().get_miss(attacker.name)
            self.add_event(self.current_minute, "miss", miss_desc)

    def process_attacking_play(self, attacking_team, defending_team, is_home_attacking):
        """Process an attacking play in the final third"""
        event_types = ["cross", "through_ball", "shot", "dribble", "pass"]
        weights = [0.25, 0.2, 0.3, 0.15, 0.1]
        
        # Adjust weights based on team tactics
        if attacking_team.tactic == 'A':  # Attacking
            weights[2] += 0.1  # More shots
        elif attacking_team.tactic == 'P':  # Possession
            weights[4] += 0.1  # More passes
            
        # Normalize weights
        total = sum(weights)
        weights = [w/total for w in weights]
        
        # Choose event type
        event_type = random.choices(event_types, weights=weights)[0]
        
        if event_type == "shot":
            self.process_goal_attempt(attacking_team, defending_team, is_home_attacking)
        elif event_type == "cross":
            # Process cross
            crosser = self.select_player_for_action(attacking_team, preference='winger')
            target = self.select_player_for_action(attacking_team, preference='forward', exclude=[crosser])
            defender = self.select_player_for_action(defending_team, preference='defender')
            
            crosser.match_passes += 1
            
            # Determine if cross is successful
            cross_success = random.random() < (crosser.get_effective_attribute('passing', self.current_minute) / 20)
            
            if cross_success:
                crosser.match_passes_completed += 1
                cross_desc = commentary_manager().get_cross(crosser.name, target.name)
            else:
                cross_desc = commentary_manager().get_failed_cross(crosser.name, defender.name)
                
            self.add_event(self.current_minute, "cross", cross_desc)
        elif event_type == "through_ball":
            # Process through ball
            passer = self.select_player_for_action(attacking_team, preference='midfielder')
            receiver = self.select_player_for_action(attacking_team, preference='forward', exclude=[passer])
            
            passer.match_passes += 1
            
            # Determine if through ball is successful
            pass_success = random.random() < (passer.get_effective_attribute('passing', self.current_minute) / 20)
            
            if pass_success:
                passer.match_passes_completed += 1
                through_desc = commentary_manager().get_through_ball(passer.name, receiver.name)
                # Successful through ball likely leads to a shot
                if random.random() < 0.7:
                    self.process_goal_attempt(attacking_team, defending_team, is_home_attacking)
            else:
                defender = self.select_player_for_action(defending_team, preference='defender')
                through_desc = commentary_manager().get_failed_through_ball(passer.name, defender.name)
                
            self.add_event(self.current_minute, "through_ball", through_desc)
        else:
            # Process dribble or pass
            player = self.select_player_for_action(attacking_team)
            target = self.select_player_for_action(attacking_team, exclude=[player])
            
            if event_type == "dribble":
                defender = self.select_player_for_action(defending_team)
                
                # Dribble success calculation
                dribble_skill = player.get_effective_attribute('technique', self.current_minute)
                tackle_skill = defender.get_effective_attribute('tackling', self.current_minute)
                
                dribble_success = random.random() < ((dribble_skill - tackle_skill + 10) / 30)
                
                if dribble_success:
                    dribble_desc = commentary_manager().get_dribble(player.name, defender.name)
                else:
                    dribble_desc = commentary_manager().get_tackle(defender.name, player.name)
                    defender.match_tackles += 1
                    defender.match_tackles_won += 1
                    
                self.add_event(self.current_minute, "dribble", dribble_desc)
            else:  # pass
                player.match_passes += 1
                
                pass_success = random.random() < (player.get_effective_attribute('passing', self.current_minute) / 20)
                
                if pass_success:
                    player.match_passes_completed += 1
                    pass_desc = commentary_manager().get_pass(player.name, target.name)
                    self.add_event(self.current_minute, "pass", pass_desc)

    def process_midfield_play(self, attacking_team, defending_team, is_home_attacking):
        """Process play in the midfield"""
        event_types = ["pass", "dribble", "tackle", "foul"]
        weights = [0.5, 0.2, 0.2, 0.1]
        
        # Choose event type
        event_type = random.choices(event_types, weights=weights)[0]
        
        if event_type == "pass":
            # Process midfield pass
            passer = self.select_player_for_action(attacking_team, preference='midfielder')
            receiver = self.select_player_for_action(attacking_team, exclude=[passer])
            
            passer.match_passes += 1
            
            # Pass success calculation
            pass_skill = passer.get_effective_attribute('passing', self.current_minute)
            pass_success = random.random() < (pass_skill / 20)
            
            if pass_success:
                passer.match_passes_completed += 1
                
                # Important passes get commentary
                if random.random() < 0.3:  # Only 30% of midfield passes get commentary
                    pass_desc = commentary_manager().get_pass(passer.name, receiver.name)
                    self.add_event(self.current_minute, "pass", pass_desc)
            else:
                interceptor = self.select_player_for_action(defending_team)
                interceptor.match_tackles += 1
                interceptor.match_tackles_won += 1
                
                # Turnover of possession
                self.last_team_with_ball = defending_team
                
                interception_desc = commentary_manager().get_interception(interceptor.name, passer.name)
                self.add_event(self.current_minute, "interception", interception_desc)
        
        elif event_type == "dribble":
            # Process midfield dribble
            dribbler = self.select_player_for_action(attacking_team)
            defender = self.select_player_for_action(defending_team)
            
            dribble_skill = dribbler.get_effective_attribute('technique', self.current_minute)
            tackle_skill = defender.get_effective_attribute('tackling', self.current_minute)
            
            dribble_success = random.random() < ((dribble_skill - tackle_skill + 10) / 30)
            
            if dribble_success and random.random() < 0.3:  # Only 30% get commentary
                dribble_desc = commentary_manager().get_dribble(dribbler.name, defender.name)
                self.add_event(self.current_minute, "dribble", dribble_desc)
            elif not dribble_success:
                defender.match_tackles += 1
                defender.match_tackles_won += 1
                
                # Turnover of possession
                self.last_team_with_ball = defending_team
                
                tackle_desc = commentary_manager().get_tackle(defender.name, dribbler.name)
                self.add_event(self.current_minute, "tackle", tackle_desc)
        
        elif event_type == "tackle":
            # Process midfield tackle attempt
            defender = self.select_player_for_action(defending_team)
            attacker = self.select_player_for_action(attacking_team)
            
            defender.match_tackles += 1
            
            tackle_skill = defender.get_effective_attribute('tackling', self.current_minute)
            dribble_skill = attacker.get_effective_attribute('technique', self.current_minute)
            
            tackle_success = random.random() < ((tackle_skill - dribble_skill + 10) / 30)
            
            if tackle_success:
                defender.match_tackles_won += 1
                
                # Turnover of possession
                self.last_team_with_ball = defending_team
                
                tackle_desc = commentary_manager().get_tackle(defender.name, attacker.name)
                self.add_event(self.current_minute, "tackle", tackle_desc)
            else:
                # Failed tackle - possible foul
                foul_chance = 0.3
                if random.random() < foul_chance:
                    self.process_foul(defender, attacker, is_home_attacking)
        
        elif event_type == "foul":
            # Process foul
            defender = self.select_player_for_action(defending_team)
            attacker = self.select_player_for_action(attacking_team)
            
            self.process_foul(defender, attacker, is_home_attacking)

    def process_foul(self, fouler, fouled, is_home_attacking):
        """Process a foul event"""
        # Record foul
        if is_home_attacking:
            self.away_fouls += 1
        else:
            self.home_fouls += 1
            
        fouler.match_fouls += 1
        
        # Determine if it's a card
        card_chance = 0.2 + (fouler.match_fouls * 0.1)  # More fouls = higher card chance
        
        if fouler.match_yellow_card:
            card_chance += 0.1  # Higher chance for second yellow
            
        if random.random() < card_chance:
            if fouler.match_yellow_card:
                # Second yellow = red
                fouler.match_red_card = True
                card_desc = commentary_manager().get_red_card(fouler.name, fouled.name)
                self.add_event(self.current_minute, "red_card", card_desc)
                
                # Major momentum swing
                self.momentum += 3 if is_home_attacking else -3
            else:
                # Yellow card
                fouler.match_yellow_card = True
                card_desc = commentary_manager().get_yellow_card(fouler.name, fouled.name)
                self.add_event(self.current_minute, "yellow_card", card_desc)
                
                # Minor momentum swing
                self.momentum += 1 if is_home_attacking else -1
        else:
            # Just a foul, no card
            foul_desc = commentary_manager().get_foul(fouler.name, fouled.name)
            self.add_event(self.current_minute, "foul", foul_desc)

    def update_momentum(self, attacking_team, defending_team, is_home_attacking):
        """Update match momentum"""
        # Momentum naturally reverts to neutral over time
        if self.momentum > 0:
            self.momentum -= 0.2
        elif self.momentum < 0:
            self.momentum += 0.2
            
        # Cap momentum
        self.momentum = max(-10, min(10, self.momentum))

    def add_event(self, minute, event_type, description):
        """Add an event to the match events list"""
        event = {
            'minute': minute,
            'type': event_type,
            'description': description
        }
        self.match_events.append(event)

    def select_player_for_action(self, team, preference=None, exclude=None):
        """Select a player from the team for an action, with optional position preference"""
        exclude = exclude or []
        available_players = [p for p in team.players if p not in exclude and not p.match_red_card]
        
        if not available_players:
            return team.players[0]  # Fallback
            
        if preference == 'forward':
            forwards = [p for p in available_players if p.position in ['ST', 'CF', 'LF', 'RF']]
            if forwards:
                return random.choice(forwards)
        elif preference == 'midfielder':
            midfielders = [p for p in available_players if p.position in ['CM', 'DM', 'AM', 'LM', 'RM']]
            if midfielders:
                return random.choice(midfielders)
        elif preference == 'winger':
            wingers = [p for p in available_players if p.position in ['LW', 'RW', 'LM', 'RM']]
            if wingers:
                return random.choice(wingers)
        elif preference == 'defender':
            defenders = [p for p in available_players if p.position in ['CB', 'LB', 'RB', 'LWB', 'RWB']]
            if defenders:
                return random.choice(defenders)
        elif preference == 'goalkeeper':
            goalkeepers = [p for p in available_players if p.position == 'GK']
            if goalkeepers:
                return goalkeepers[0]
                
        # Default: return random player
        return random.choice(available_players)

    def increment_shots(self, is_home):
        """Increment shot count for the appropriate team"""
        if is_home:
            self.home_shots += 1
        else:
            self.away_shots += 1
            
    def increment_shots_on_target(self, is_home):
        """Increment shots on target count for the appropriate team"""
        if is_home:
            self.home_shots_on_target += 1
        else:
            self.away_shots_on_target += 1

    def generate_match_stats(self):
        """Generate comprehensive match statistics"""
        home_player_stats = self.generate_player_stats(self.home_team)
        away_player_stats = self.generate_player_stats(self.away_team)
        
        stats = {
            'possession': {
                'home': round(self.home_possession, 1),
                'away': round(self.away_possession, 1)
            },
            'shots': {
                'home': self.home_shots,
                'away': self.away_shots
            },
            'shots_on_target': {
                'home': self.home_shots_on_target,
                'away': self.away_shots_on_target
            },
            'fouls': {
                'home': self.home_fouls,
                'away': self.away_fouls
            },
            'corners': {
                'home': self.home_corners,
                'away': self.away_corners
            },
            'player_stats': {
                'home': home_player_stats,
                'away': away_player_stats
            }
        }
        return stats

    def generate_player_stats(self, team):
        """Generate individual player statistics"""
        player_stats = {}
        for player in team.players:
            player_stats[player.name] = {
                'position': player.position,
                'goals': player.match_goals,
                'assists': player.match_assists,
                'shots': player.match_shots,
                'shots_on_target': player.match_shots_on_target,
                'passes': player.match_passes,
                'pass_completion': round(player.match_passes_completed / max(1, player.match_passes) * 100, 1),
                'tackles': player.match_tackles,
                'tackles_won': player.match_tackles_won,
                'distance': round(player.match_distance, 1),
                'fouls': player.match_fouls,
                'yellow_card': player.match_yellow_card,
                'red_card': player.match_red_card,
                'rating': round(player.calculate_match_rating(), 1)
            }
        return player_stats