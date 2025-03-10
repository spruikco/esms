# esms/engine/match_engine.py
import random
from datetime import timedelta
from esms.engine.tactics import tact_manager
from esms.engine.commentary import commentary_manager

class EnhancedMatchEngine:
    """
    Enhanced Match Engine with improved simulation features:
    - Substitutions
    - Improved fatigue modeling
    - More realistic player performance 
    - Better tactical influences
    - Contextual commentary
    """
    def __init__(self, config):
        self.config = config
        self.home_team = None
        self.away_team = None
        self.home_subs = []  # Available substitutes
        self.away_subs = []
        self.home_subs_used = 0
        self.away_subs_used = 0
        self.max_subs = config.get('SUBSTITUTIONS', 3)
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
        self.home_offsides = 0
        self.away_offsides = 0
        
        # Match status
        self.last_team_with_ball = None
        self.current_zone = 3  # Middle zone (1-5 scale: 1=home goal, 5=away goal)
        self.momentum = 0  # -10 to +10 scale (negative=home momentum, positive=away)
        self.injury_time = 0  # Injury time in minutes
        self.is_injury_time = False

    def setup_match(self, home_team, away_team, home_subs=None, away_subs=None):
        """Set up the match with teams and substitutes"""
        self.home_team = home_team
        self.away_team = away_team
        self.home_subs = home_subs or []
        self.away_subs = away_subs or []
        self.home_subs_used = 0
        self.away_subs_used = 0
        
        # Reset player stats
        for player in self.home_team.players + self.away_team.players + self.home_subs + self.away_subs:
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
        self.injury_time = 0
        self.is_injury_time = False
        
        # Initialize player positions based on formation
        self._initialize_player_positions(home_team)
        self._initialize_player_positions(away_team)

    def _initialize_player_positions(self, team):
        """Initialize player positions based on team formation"""
        formation = team.formation or "4-4-2"
        
        # Map formation to position distributions
        formation_maps = {
            "4-4-2": {
                "GK": 1, "CB": 2, "LB": 1, "RB": 1, 
                "CM": 2, "LM": 1, "RM": 1, "ST": 2
            },
            "4-3-3": {
                "GK": 1, "CB": 2, "LB": 1, "RB": 1, 
                "CM": 3, "LW": 1, "RW": 1, "ST": 1
            },
            "3-5-2": {
                "GK": 1, "CB": 3, "LWB": 1, "RWB": 1, 
                "CM": 3, "ST": 2
            },
            "5-3-2": {
                "GK": 1, "CB": 3, "LWB": 1, "RWB": 1, 
                "CM": 3, "ST": 2
            },
            "4-2-3-1": {
                "GK": 1, "CB": 2, "LB": 1, "RB": 1, 
                "DM": 2, "AM": 1, "LW": 1, "RW": 1, "ST": 1
            }
        }
        
        # Default to 4-4-2 if formation not recognized
        formation_map = formation_maps.get(formation, formation_maps["4-4-2"])
        
        # Count players already in specified positions
        position_counts = {}
        for player in team.players:
            position_counts[player.position] = position_counts.get(player.position, 0) + 1
            
        # Add position attributes to players if needed
        for player in team.players:
            # Set x, y coordinates for visualization
            if not hasattr(player, 'field_x') or not hasattr(player, 'field_y'):
                player.field_x = 0.5
                player.field_y = 0.5

    def apply_tactical_effects(self, team, opponent):
        """Apply tactical effects to team attributes"""
        tactic = team.tactic
        
        # Default values if tactic not found
        team.temp_attacking_boost = 0
        team.temp_defensive_boost = 0
        team.temp_passing_boost = 0
        team.temp_counter_boost = 0
        team.temp_pressing_boost = 0
        team.temp_attacking_penalty = 0
        team.temp_defensive_penalty = 0
        team.temp_stamina_drain = 1.0  # Multiplier for stamina drain
        
        # Get tactic effects from the tactics manager
        tactic_effects = tact_manager().get_tactic_effects(tactic)
        
        if tactic_effects:
            # Apply effects based on tactic
            if tactic == 'A':  # Attacking
                team.temp_attacking_boost = tactic_effects.get('attacking_boost', 2)
                team.temp_defensive_penalty = tactic_effects.get('defensive_penalty', 1)
                team.temp_stamina_drain = 1.1  # 10% more stamina drain
            elif tactic == 'D':  # Defensive
                team.temp_defensive_boost = tactic_effects.get('defensive_boost', 2)
                team.temp_attacking_penalty = tactic_effects.get('attacking_penalty', 1)
                team.temp_stamina_drain = 0.9  # 10% less stamina drain
            elif tactic == 'P':  # Possession
                team.temp_passing_boost = tactic_effects.get('passing_boost', 2)
                team.temp_stamina_drain = 1.0  # Normal stamina drain
            elif tactic == 'C':  # Counter
                team.temp_counter_boost = tactic_effects.get('counter_boost', 2)
                team.temp_stamina_drain = 0.95  # 5% less stamina drain
            
            # Consider counter-tactic relationships
            counter_bonus = 0
            if (tactic == 'P' and opponent.tactic == 'A'):  # Possession against Attacking
                counter_bonus = tactic_effects.get('counter_bonus', 1)
            elif (tactic == 'C' and opponent.tactic == 'P'):  # Counter against Possession
                counter_bonus = tactic_effects.get('counter_bonus', 2)
            elif (tactic == 'D' and opponent.tactic == 'A'):  # Defensive against Attacking
                counter_bonus = tactic_effects.get('counter_bonus', 1.5)
                
            team.temp_counter_boost += counter_bonus

    def run_full_match(self):
        """Run a complete match simulation"""
        self.add_event(0, "kickoff", "Match begins!")
        
        # Simulate first half
        self.simulate_half(1, 1, 45)
        
        # Half time
        self.add_event(45, "halftime", f"Half time score: {self.home_team.name} {self.home_score} - {self.away_score} {self.away_team.name}")
        
        # Simulate second half
        self.simulate_half(2, 46, 90)
        
        # Injury time
        if self.injury_time > 0:
            self.add_event(90, "injury_time", f"+{self.injury_time} minutes of injury time")
            self.is_injury_time = True
            self.simulate_injury_time(self.injury_time)
        
        # Final whistle
        self.add_event(90 + self.injury_time, "fulltime", f"Full time: {self.home_team.name} {self.home_score} - {self.away_score} {self.away_team.name}")
        
        # Generate match stats
        match_stats = self.generate_match_stats()
        
        return {
            'home_team': self.home_team,
            'away_team': self.away_team,
            'home_score': self.home_score,
            'away_score': self.away_score,
            'events': self.match_events,
            'statistics': match_stats,
            'home_subs_used': self.home_subs_used,
            'away_subs_used': self.away_subs_used
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
            
            # Check for substitutions
            if half_id == 2 and self.current_minute >= 60:
                # More likely to make subs in second half after 60th minute
                self.check_for_substitutions()
            
            # Update player fatigue and match distance
            for player in self.home_team.players + self.away_team.players:
                player.match_minutes = self.current_minute
                # Simulate distance covered
                distance_per_minute = random.uniform(0.08, 0.12)  # km per minute
                player.match_distance += distance_per_minute * time_increment

    def simulate_injury_time(self, injury_time_minutes):
        """Simulate injury time at the end of the match"""
        end_minute = 90 + injury_time_minutes
        
        while self.current_minute < end_minute:
            # Shorter time increments in injury time
            time_increment = random.randint(1, 2)
            self.current_minute += time_increment
            
            if self.current_minute > end_minute:
                self.current_minute = end_minute
                
            # Higher chance of attacking events in injury time
            attacking_chance = 0.6  # 60% chance of an attacking event
            
            if random.random() < attacking_chance:
                # Determine which team attacks (losing team more likely)
                if self.home_score < self.away_score:
                    attacking_team = self.home_team
                    defending_team = self.away_team
                    is_home_attacking = True
                elif self.away_score < self.home_score:
                    attacking_team = self.away_team
                    defending_team = self.home_team
                    is_home_attacking = False
                else:
                    # If tied, random team attacks
                    if random.random() < 0.5:
                        attacking_team = self.home_team
                        defending_team = self.away_team
                        is_home_attacking = True
                    else:
                        attacking_team = self.away_team
                        defending_team = self.home_team
                        is_home_attacking = False
                        
                # Process attacking play in final third
                self.process_attacking_play(attacking_team, defending_team, is_home_attacking)
            else:
                # General midfield play
                if random.random() < 0.5:
                    self.process_midfield_play(self.home_team, self.away_team, True)
                else:
                    self.process_midfield_play(self.away_team, self.home_team, False)

    def check_for_substitutions(self):
        """Check if teams want to make substitutions"""
        # Home team substitution
        if random.random() < self.calculate_substitution_probability(self.home_team, self.away_team):
            self.make_team_substitution(self.home_team, True)
            
        # Away team substitution
        if random.random() < self.calculate_substitution_probability(self.away_team, self.home_team):
            self.make_team_substitution(self.away_team, False)

    def calculate_substitution_probability(self, team, opponent):
        """Calculate probability of making a substitution based on match state"""
        # Base probability increases with match time
        base_prob = min(0.5, self.current_minute / 180)  # Maxes at 0.5 at minute 90
        
        # Adjust based on score difference
        score_diff = self.home_score - self.away_score
        if team == self.away_team:
            score_diff = -score_diff
            
        if score_diff < 0:
            # Losing team more likely to make subs
            base_prob += 0.1 * abs(score_diff)
        
        # Check for tired players
        tired_players = [p for p in team.players if p.calculate_fatigue(self.current_minute) > 0.7]
        if tired_players:
            base_prob += 0.1 * len(tired_players) / len(team.players)
            
        # Already used all subs
        subs_used = self.home_subs_used if team == self.home_team else self.away_subs_used
        if subs_used >= self.max_subs:
            return 0.0
            
        # No available subs
        available_subs = self.home_subs if team == self.home_team else self.away_subs
        if not available_subs:
            return 0.0
            
        return min(0.9, base_prob)  # Cap at 90% chance

    def make_team_substitution(self, team, is_home_team):
        """Make a substitution for the given team"""
        available_subs = self.home_subs if is_home_team else self.away_subs
        subs_used = self.home_subs_used if is_home_team else self.away_subs_used
        
        if subs_used >= self.max_subs or not available_subs:
            return False
            
        # Find player to replace - prioritize tired players, players with poor performance, or tactical changes
        candidates = []
        
        # First priority: tired players (fatigue > 70%)
        tired_players = [(p, 3) for p in team.players if p.calculate_fatigue(self.current_minute) > 0.7]
        candidates.extend(tired_players)
        
        # Second priority: players with yellow cards
        yellow_carded = [(p, 2) for p in team.players if p.match_yellow_card]
        candidates.extend(yellow_carded)
        
        # Third priority: tactical changes based on score
        score_diff = self.home_score - self.away_score
        if is_home_team:
            if score_diff < 0:  # Losing, sub out defensive players
                defensive = [(p, 1) for p in team.players if p.position in ['CB', 'LB', 'RB', 'DM']]
                candidates.extend(defensive)
            elif score_diff > 0:  # Winning, sub out attacking players
                attacking = [(p, 1) for p in team.players if p.position in ['ST', 'LW', 'RW', 'AM']]
                candidates.extend(attacking)
        else:  # Away team
            if score_diff > 0:  # Losing, sub out defensive players
                defensive = [(p, 1) for p in team.players if p.position in ['CB', 'LB', 'RB', 'DM']]
                candidates.extend(defensive)
            elif score_diff < 0:  # Winning, sub out attacking players
                attacking = [(p, 1) for p in team.players if p.position in ['ST', 'LW', 'RW', 'AM']]
                candidates.extend(attacking)
        
        # If no candidates, pick random player
        if not candidates:
            candidates = [(p, 0) for p in team.players]
            
        # Weight selection by priority
        weights = [c[1] for c in candidates]
        total_weight = sum(weights)
        if total_weight == 0:
            normalized_weights = [1/len(candidates)] * len(candidates)
        else:
            normalized_weights = [w/total_weight for w in weights]
            
        player_out = random.choices([c[0] for c in candidates], weights=normalized_weights, k=1)[0]
        
        # Find appropriate replacement with similar position
        position_matches = [s for s in available_subs if s.position == player_out.position]
        position_similar = [s for s in available_subs if self.positions_are_similar(s.position, player_out.position)]
        
        if position_matches:
            player_in = random.choice(position_matches)
        elif position_similar:
            player_in = random.choice(position_similar)
        elif available_subs:
            player_in = random.choice(available_subs)
        else:
            return False
            
        # Make the substitution
        team.players.remove(player_out)
        team.players.append(player_in)
        
        if is_home_team:
            self.home_subs.remove(player_in)
            self.home_subs_used += 1
        else:
            self.away_subs.remove(player_in)
            self.away_subs_used += 1
            
        # Record substitution event
        self.add_event(
            self.current_minute, 
            "substitution", 
            f"{player_in.name} comes on for {player_out.name}"
        )
        
        # Apply tactical impact - fresh player gets a small boost
        player_in.substitution_boost = 1.1  # 10% attribute boost for 10-15 minutes
        
        return True

    def positions_are_similar(self, pos1, pos2):
        """Check if two positions are similar enough for substitution"""
        position_groups = [
            ['GK'],  # Goalkeepers
            ['CB', 'LB', 'RB', 'LWB', 'RWB'],  # Defenders
            ['DM', 'CM', 'LM', 'RM'],  # Midfielders
            ['AM', 'LW', 'RW'],  # Attacking midfielders/wingers
            ['ST', 'CF']  # Strikers
        ]
        
        for group in position_groups:
            if pos1 in group and pos2 in group:
                return True
                
        return False

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
        
        # Small chance of injury
        if random.random() < 0.01:  # 1% chance per event
            self.process_injury(attacking_team if random.random() < 0.5 else defending_team)

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
        
        # Tactical effects
        home_passing_boost = self.home_team.temp_passing_boost
        away_passing_boost = self.away_team.temp_passing_boost
        tactical_effect = (home_passing_boost - away_passing_boost) * 2  # Each point is worth 2% possession
        
        # Player quality effect - average passing skill difference
        home_passing = sum(p.get_effective_attribute('passing', self.current_minute) for p in self.home_team.players) / len(self.home_team.players)
        away_passing = sum(p.get_effective_attribute('passing', self.current_minute) for p in self.away_team.players) / len(self.away_team.players)
        quality_effect = (home_passing - away_passing) / 4  # Each point difference is worth 0.25% possession
        
        # Calculate new possession value
        new_possession = base_possession + momentum_effect * 0.5 + tactical_effect + quality_effect
        
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
        elif attacking_team.tactic == 'C':  # Counter
            if self.current_zone == 3:  # Midfield counter-attacks are more effective
                forward_prob += 0.15
            
        # Adjust based on current zone (harder to advance near opponent's goal)
        if (is_home_attacking and self.current_zone >= 4) or (not is_home_attacking and self.current_zone <= 2):
            forward_prob -= 0.15
            
        # Adjust based on team quality difference in midfield
        midfield_difference = 0
        if is_home_attacking:
            home_mid_quality = self.get_team_midfield_quality(self.home_team)
            away_mid_quality = self.get_team_midfield_quality(self.away_team)
            midfield_difference = home_mid_quality - away_mid_quality
        else:
            home_mid_quality = self.get_team_midfield_quality(self.home_team)
            away_mid_quality = self.get_team_midfield_quality(self.away_team)
            midfield_difference = away_mid_quality - home_mid_quality
            
        forward_prob += midfield_difference * 0.01  # Each point worth 1%
            
        # Determine movement
        if random.random() < forward_prob:
            # Move forward
            new_zone = self.current_zone + direction
        else:
            # Move backward or stay
            new_zone = self.current_zone - direction
            
        # Ensure zone is within valid range
        self.current_zone = max(1, min(5, new_zone))

    def get_team_midfield_quality(self, team):
        """Calculate team's midfield quality"""
        midfielders = [p for p in team.players if p.position in ['CM', 'DM', 'AM', 'LM', 'RM']]
        if not midfielders:
            return 10  # Default if no midfielders
            
        avg_passing = sum(p.get_effective_attribute('passing', self.current_minute) for p in midfielders) / len(midfielders)
        avg_technique = sum(p.get_effective_attribute('technique', self.current_minute) for p in midfielders) / len(midfielders)
        
        return (avg_passing + avg_technique) / 2 + team.temp_passing_boost

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
        
        # Adjust based on position - central positions have better angles
        if attacker.position in ['ST', 'CF', 'AM']:
            on_target_chance += 0.05  # +5% for central positions
        
        if random.random() < on_target_chance:
            # Shot is on target
            self.increment_shots_on_target(is_home_attacking)
            attacker.match_shots_on_target += 1
            
            # Determine if it's a goal
            gk_skill = goalkeeper.get_effective_attribute('goalkeeper', self.current_minute)
            save_chance = 0.6 + (gk_skill / 50)  # Base 60% + up to 40% from skill
            
            # Decrease save chance for very good shots
            if shooting_skill > 15:
                save_chance -= 0.1  # -10% for high quality shooters
                
            # Increase save chance for shots from distance
            if self.current_zone == 2 or self.current_zone == 4:  # Not in the box
                save_chance += 0.1  # +10% for distance shots
            
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
                
                # Add small amount of injury time for goal celebration
                self.injury_time += random.randint(0, 1)
                
                # Big momentum swing for scoring team
                self.momentum += -5 if is_home_attacking else 5
            else:
                # Save by goalkeeper
                goalkeeper.match_saves += 1
                save_desc = commentary_manager().get_save(goalkeeper.name, attacker.name)
                self.add_event(self.current_minute, "save", save_desc)
                
                # Check for corner
                if random.random() < 0.7:  # 70% of saved shots result in corners
                    if is_home_attacking:
                        self.home_corners += 1
                    else:
                        self.away_corners += 1
                    self.add_event(self.current_minute, "corner", f"Corner kick for {attacking_team.name}")
                
                # Small momentum boost for good save
                self.momentum += 1 if is_home_attacking else -1
        else:
            # Shot off target
            miss_desc = commentary_manager().get_miss(attacker.name)
            self.add_event(self.current_minute, "miss", miss_desc)
            
            # Check for goal kick or corner
            if random.random() < 0.3:  # 30% of missed shots result in corners
                if is_home_attacking:
                    self.home_corners += 1
                else:
                    self.away_corners += 1
                self.add_event(self.current_minute, "corner", f"Corner kick for {attacking_team.name}")

    def process_attacking_play(self, attacking_team, defending_team, is_home_attacking):
        """Process an attacking play in the final third"""
        # Weights adjusted based on zone - deeper in attack zone = more shots
        in_box = self.current_zone in [1, 5]  # In the penalty box
        
        if in_box:
            event_types = ["shot", "cross", "through_ball", "dribble", "pass"]
            weights = [0.5, 0.15, 0.15, 0.15, 0.05]  # More shots in the box
        else:
            event_types = ["cross", "through_ball", "shot", "dribble", "pass"]
            weights = [0.3, 0.25, 0.2, 0.15, 0.1]  # More crosses and through balls outside box
        
        # Adjust weights based on team tactics
        if attacking_team.tactic == 'A':  # Attacking
            weights[event_types.index("shot")] += 0.1  # More shots
        elif attacking_team.tactic == 'P':  # Possession
            weights[event_types.index("pass")] += 0.1  # More passes
        elif attacking_team.tactic == 'C':  # Counter
            weights[event_types.index("through_ball")] += 0.1  # More through balls
            
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
            crossing_skill = crosser.get_effective_attribute('passing', self.current_minute)
            defending_skill = defender.get_effective_attribute('tackling', self.current_minute)
            
            cross_success = random.random() < ((crossing_skill - defending_skill + 10) / 30)
            
            if cross_success:
                crosser.match_passes_completed += 1
                cross_desc = commentary_manager().get_cross(crosser.name, target.name)
                self.add_event(self.current_minute, "cross", cross_desc)
                
                # Successful cross often leads to a shot
                if random.random() < 0.6:  # 60% chance of shot from successful cross
                    self.process_goal_attempt(attacking_team, defending_team, is_home_attacking)
            else:
                cross_desc = commentary_manager().get_failed_cross(crosser.name, defender.name)
                self.add_event(self.current_minute, "cross", cross_desc)
                
                # Defender gets tackle credit
                defender.match_tackles += 1
                defender.match_tackles_won += 1
        elif event_type == "through_ball":
            # Process through ball
            passer = self.select_player_for_action(attacking_team, preference='midfielder')
            receiver = self.select_player_for_action(attacking_team, preference='forward', exclude=[passer])
            
            passer.match_passes += 1
            
            # Determine if through ball is successful
            passing_skill = passer.get_effective_attribute('passing', self.current_minute)
            # Through balls are harder than normal passes
            pass_success = random.random() < ((passing_skill - 5) / 20)
            
            if pass_success:
                passer.match_passes_completed += 1
                through_desc = commentary_manager().get_through_ball(passer.name, receiver.name)
                self.add_event(self.current_minute, "through_ball", through_desc)
                
                # Successful through ball likely leads to a shot
                if random.random() < 0.7:  # 70% chance
                    self.process_goal_attempt(attacking_team, defending_team, is_home_attacking)
            else:
                defender = self.select_player_for_action(defending_team, preference='defender')
                through_desc = commentary_manager().get_failed_through_ball(passer.name, defender.name)
                self.add_event(self.current_minute, "through_ball", through_desc)
                
                # Defender gets tackle credit
                defender.match_tackles += 1
                defender.match_tackles_won += 1
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
                    self.add_event(self.current_minute, "dribble", dribble_desc)
                    
                    # Successful dribble can lead to shot opportunity
                    if random.random() < 0.4:  # 40% chance
                        self.process_goal_attempt(attacking_team, defending_team, is_home_attacking)
                else:
                    dribble_desc = commentary_manager().get_tackle(defender.name, player.name)
                    self.add_event(self.current_minute, "tackle", dribble_desc)
                    
                    defender.match_tackles += 1
                    defender.match_tackles_won += 1
            else:  # pass
                player.match_passes += 1
                
                pass_skill = player.get_effective_attribute('passing', self.current_minute)
                pass_success = random.random() < (pass_skill / 20)
                
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
        
        # Higher card chance in dangerous areas
        if self.current_zone in [1, 5]:  # Goal zones
            card_chance += 0.15  # +15% in penalty areas
        elif self.current_zone in [2, 4]:  # Attacking zones
            card_chance += 0.05  # +5% in attacking zones
            
        if fouler.match_yellow_card:
            card_chance += 0.1  # Higher chance for second yellow
            
        if random.random() < card_chance:
            if fouler.match_yellow_card:
                # Second yellow = red
                fouler.match_red_card = True
                card_desc = commentary_manager().get_red_card(fouler.name, fouled.name)
                self.add_event(self.current_minute, "red_card", card_desc)
                
                # Add injury time for red card
                self.injury_time += random.randint(1, 2)
                
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

    def process_injury(self, team):
        """Process a player injury event"""
        # Select random player for injury
        player = random.choice(team.players)
        
        # Generate injury severity
        severity = random.choices(
            ["minor", "moderate", "severe"],
            weights=[0.7, 0.25, 0.05],  # Most injuries are minor
            k=1
        )[0]
        
        # Record injury based on severity
        if severity == "minor":
            description = f"{player.name} is down with a knock but seems able to continue"
            recovery_time = 0  # Can continue
        elif severity == "moderate":
            description = f"{player.name} has picked up an injury and needs treatment"
            recovery_time = random.randint(1, 2)  # 1-2 minutes
            self.injury_time += 1  # Add 1 minute to injury time
        else:  # severe
            description = f"{player.name} has a serious injury and cannot continue"
            recovery_time = 5  # will need substitution
            self.injury_time += random.randint(2, 3)  # Add 2-3 minutes to injury time
            
            # Force substitution if severe and subs available
            if team == self.home_team and self.home_subs and self.home_subs_used < self.max_subs:
                self.make_team_substitution(team, True)
            elif team == self.away_team and self.away_subs and self.away_subs_used < self.max_subs:
                self.make_team_substitution(team, False)
        
        # Add injury event
        self.add_event(self.current_minute, "injury", description)

    def update_momentum(self, attacking_team, defending_team, is_home_attacking):
        """Update match momentum"""
        # Momentum naturally reverts to neutral over time
        if self.momentum > 0:
            self.momentum -= 0.2
        elif self.momentum < 0:
            self.momentum += 0.2
            
        # Home advantage gives slight momentum boost
        if random.random() < 0.1:  # 10% chance per event
            self.momentum -= 0.1  # Negative momentum favors home team
            
        # Score difference affects momentum
        score_diff = self.home_score - self.away_score
        if score_diff != 0:
            # Leading team gets small momentum boost
            momentum_boost = 0.05 * abs(score_diff)
            if score_diff > 0:  # Home team leading
                self.momentum -= momentum_boost
            else:  # Away team leading
                self.momentum += momentum_boost
            
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
            # Fallback to first player if no others available
            return team.players[0] if team.players else None
            
        if preference == 'forward':
            forwards = [p for p in available_players if p.position in ['ST', 'CF', 'LF', 'RF', 'LW', 'RW']]
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
            'offsides': {
                'home': self.home_offsides,
                'away': self.away_offsides
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
                'saves': getattr(player, 'match_saves', 0),  # For goalkeepers
                'yellow_card': player.match_yellow_card,
                'red_card': player.match_red_card,
                'rating': round(player.calculate_match_rating(), 1)
            }
        return player_stats