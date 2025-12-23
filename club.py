"""
Club module - Represents a football club in the league
"""

import random


class Club:
    """Represents a football club with reputation, tactics, and performance metrics"""

    def __init__(self, name, objective, formation, tactic, manager, is_international=False, country=None, reputation=None):
        self.name = name
        self.objective = objective  # Campeón/Top 3, Libertadores, Sudamericana, Mitad de Tabla, No Descender
        self.formation = formation  # e.g., "4-3-3"
        self.tactic = tactic  # Presión alta, Posesión, Ataque, Contraataque, Defensivo
        self.manager = manager
        self.is_international = is_international  # True if international club
        self.country = country  # Country name (for international clubs)

        # Reputation system (1-100)
        # Allow passing reputation directly for international clubs
        if reputation is not None:
            self.reputation = reputation
        else:
            self.reputation = self._calculate_reputation_from_objective()

        # Squad information
        self.players_count = random.randint(20, 25)  # Players in squad
        self.academy_rating = random.randint(1, 20)  # Youth development (1-20)

        # Financial
        self.budget = self._calculate_budget()
        self.wage_budget = self.budget * 0.6  # 60% for wages

        # Performance tracking
        self.current_season_wins = 0
        self.current_season_draws = 0
        self.current_season_losses = 0
        self.current_season_goals_for = 0
        self.current_season_goals_against = 0
        self.current_season_points = 0

        # Stadium
        self.stadium_name = f"{self.name} Stadium"
        self.stadium_capacity = random.randint(15000, 60000)

        # Relations
        self.player_morale = 75  # 0-100
        self.fan_satisfaction = 75  # 0-100
        self.training_quality = self._calculate_training_quality()

    def _calculate_reputation_from_objective(self):
        """Calculate base reputation from objective"""
        reputation_map = {
            "Campeón / Top 3": random.randint(75, 95),
            "Clasificación Libertadores": random.randint(65, 80),
            "Clasificación Sudamericana": random.randint(55, 70),
            "Mitad de Tabla": random.randint(45, 60),
            "No Descender": random.randint(30, 50)
        }
        return reputation_map.get(self.objective, 50)

    def _calculate_budget(self):
        """Calculate budget based on reputation"""
        base_budget = 5000000  # $5M base
        multiplier = self.reputation / 50  # Reputation affects budget
        return int(base_budget * multiplier * random.uniform(0.8, 1.2))

    def _calculate_training_quality(self):
        """Calculate training quality (1-20) based on tactic and reputation"""
        base_quality = (self.reputation / 100) * 20
        return max(1, min(20, int(base_quality + random.randint(-2, 2))))

    # Quick base probabilities for fast simulations (vs average opponent)
    def get_quick_profile(self):
        """Return baseline probabilities and xG/xGA for fast match sims"""
        win = self.get_win_probability()
        draw = self.get_draw_probability()
        loss = max(0.0, 100 - win - draw)
        xg = self.get_goals_scored_probability()
        xga = self.get_goals_conceded_probability()
        return {
            "win_prob": round(win, 2),
            "draw_prob": round(draw, 2),
            "loss_prob": round(loss, 2),
            "xg": round(xg, 2),
            "xga": round(xga, 2),
        }

    # ========== PROBABILITY CALCULATIONS ==========

    def get_win_probability(self, opponent=None):
        """Calculate probability of winning a match (0-100)"""
        base_prob = (self.reputation / 100) * 100
        
        if opponent:
            opponent_factor = (100 - opponent.reputation) / 100
            base_prob += opponent_factor * 20
        
        # Home advantage (simulated average)
        base_prob *= 1.08
        
        # Morale influence
        morale_factor = (self.player_morale - 50) / 100
        base_prob += morale_factor * 10
        
        return max(20, min(80, base_prob))

    def get_goals_scored_probability(self, opponent=None):
        """Calculate expected goals to score (float: 0-3+)"""
        base_xg = 1.2
        
        # Reputation factor
        base_xg += (self.reputation / 100) * 1.5
        
        # Tactic influence
        tactic_xg = {
            "Presion alta": 1.3,
            "Posesion": 1.2,
            "Ataque": 1.8,
            "Contraataque": 1.4,
            "Defensivo": 0.8
        }
        base_xg *= tactic_xg.get(self.tactic, 1.0)
        
        if opponent:
            # Opponent defense affects this
            opponent_defense = (100 - opponent.reputation) / 100
            base_xg *= (0.8 + opponent_defense * 0.4)
        
        return max(0.5, min(4.0, base_xg))

    def get_goals_conceded_probability(self, opponent=None):
        """Calculate expected goals to concede (float: 0-3+)"""
        base_xga = 1.3
        
        # Reputation factor (higher rep = better defense)
        base_xga -= (self.reputation / 100) * 0.8
        
        # Tactic influence
        tactic_xga = {
            "Presion alta": 1.3,  # More goals conceded
            "Posesion": 0.9,
            "Ataque": 1.5,
            "Contraataque": 1.0,
            "Defensivo": 0.7
        }
        base_xga *= tactic_xga.get(self.tactic, 1.0)
        
        if opponent:
            # Opponent attack power
            opponent_attack = (opponent.reputation / 100)
            base_xga *= (0.7 + opponent_attack * 0.6)
        
        return max(0.4, min(3.5, base_xga))

    def get_draw_probability(self):
        """Calculate probability of a draw (0-100)"""
        # Teams with similar reputation are more likely to draw
        base_prob = 25 - abs(self.reputation - 50) / 10
        return max(10, min(35, base_prob))

    # ========== PERFORMANCE TRACKING ==========

    def add_match_result(self, goals_for, goals_against, result):
        """Record a match result"""
        self.current_season_goals_for += goals_for
        self.current_season_goals_against += goals_against

        if result == "win":
            self.current_season_wins += 1
            self.current_season_points += 3
            self.player_morale = min(100, self.player_morale + 5)
        elif result == "draw":
            self.current_season_draws += 1
            self.current_season_points += 1
        elif result == "loss":
            self.current_season_losses += 1
            self.player_morale = max(20, self.player_morale - 5)

    def get_matches_played(self):
        """Get total matches played"""
        return self.current_season_wins + self.current_season_draws + self.current_season_losses

    def get_win_rate(self):
        """Get win rate percentage"""
        matches = self.get_matches_played()
        if matches == 0:
            return 0
        return (self.current_season_wins / matches) * 100

    def get_goal_difference(self):
        """Get goal difference"""
        return self.current_season_goals_for - self.current_season_goals_against

    def get_avg_goals_scored(self):
        """Get average goals per match"""
        matches = self.get_matches_played()
        if matches == 0:
            return 0
        return self.current_season_goals_for / matches

    def get_avg_goals_conceded(self):
        """Get average goals conceded per match"""
        matches = self.get_matches_played()
        if matches == 0:
            return 0
        return self.current_season_goals_against / matches

    # ========== INFO METHODS ==========

    def describe(self):
        """Return detailed club description"""
        description = f"\n{'='*60}\n"
        description += f"CLUB PROFILE: {self.name}\n"
        description += f"{'='*60}\n"
        description += f"Manager: {self.manager}\n"
        description += f"Objective: {self.objective}\n"
        description += f"Formation: {self.formation}\n"
        description += f"Tactic: {self.tactic}\n"
        description += f"\nREPUTATION & STATS:\n"
        description += f"  Reputation: {self.reputation}/100\n"
        description += f"  Training Quality: {self.training_quality}/20\n"
        description += f"  Player Morale: {self.player_morale}/100\n"
        description += f"  Fan Satisfaction: {self.fan_satisfaction}/100\n"
        description += f"  Squad Size: {self.players_count} players\n"
        description += f"\nFINANCIAL:\n"
        description += f"  Budget: ${self.budget:,}\n"
        description += f"  Wage Budget: ${self.wage_budget:,.0f}/season\n"
        description += f"\nSTADIUM:\n"
        description += f"  {self.stadium_name} (Capacity: {self.stadium_capacity:,})\n"
        description += f"{'='*60}\n"
        return description

    def short_info(self):
        """Return brief one-line info"""
        return f"{self.name} - {self.objective} | Rep: {self.reputation}/100 | Manager: {self.manager}"

    def get_probability_report(self):
        """Get a summary of match probabilities"""
        report = f"\n{'='*60}\n"
        report += f"{self.name} - Match Probability Analysis\n"
        report += f"{'='*60}\n"
        report += f"Win Probability:        {self.get_win_probability():.1f}%\n"
        report += f"Draw Probability:       {self.get_draw_probability():.1f}%\n"
        report += f"Loss Probability:       {100 - self.get_win_probability() - self.get_draw_probability():.1f}%\n"
        report += f"\nExpected Goals:\n"
        report += f"  Goals Scored:         {self.get_goals_scored_probability():.2f}\n"
        report += f"  Goals Conceded:       {self.get_goals_conceded_probability():.2f}\n"
        report += f"  Goal Difference:      {self.get_goals_scored_probability() - self.get_goals_conceded_probability():.2f}\n"
        report += f"{'='*60}\n"
        return report

    # ========== ADDITIONAL INTERFACE METHODS ==========

    def get_league_position(self, all_clubs):
        """Calculate league position based on points"""
        sorted_clubs = sorted(all_clubs, key=lambda c: c.current_season_points, reverse=True)
        for i, club in enumerate(sorted_clubs, 1):
            if club.name == self.name:
                return i
        return None

    def get_status_summary(self):
        """Get a one-line status summary for display"""
        status_symbols = {
            "Campeón / Top 3": "🏆",
            "Clasificación Libertadores": "🌟",
            "Clasificación Sudamericana": "⭐",
            "Mitad de Tabla": "⚖️",
            "No Descender": "⚠️"
        }
        symbol = status_symbols.get(self.objective, "")
        return f"{symbol} {self.name} | Rep: {self.reputation}/100 | Points: {self.current_season_points} | W-D-L: {self.current_season_wins}-{self.current_season_draws}-{self.current_season_losses}"

    def get_formation_info(self):
        """Return information about formation"""
        formations = {
            "4-3-3": "Balanced - good for both attack and defense",
            "4-2-3-1": "Defensive - emphasizes midfield control",
            "4-3-1-2": "Flexible - supports both wide play and central attack",
            "4-4-2": "Classic - direct and simple",
            "4-4-1-1": "Compact - good for countering",
            "3-5-2": "Modern - wing-backs provide width",
            "5-3-2": "Very defensive - emphasis on solid defense",
            "5-4-1": "Catenaccio style - ultra-defensive",
        }
        return formations.get(self.formation, f"Formation: {self.formation}")

    def get_tactic_strengths(self):
        """Get strengths and weaknesses of the tactic"""
        tactic_info = {
            "Presion alta": {
                "strengths": ["High ball recovery", "Fast transitions", "Opponent pressure"],
                "weaknesses": ["High player fatigue", "Vulnerable to long balls"],
            },
            "Posesion": {
                "strengths": ["Ball control", "Reduced opponent chances", "Patient play"],
                "weaknesses": ["Requires technical quality", "Can be slow"],
            },
            "Ataque": {
                "strengths": ["Many scoring chances", "Aggressive play", "High morale"],
                "weaknesses": ["Defensive vulnerabilities", "High goals conceded"],
            },
            "Contraataque": {
                "strengths": ["Effective on transitions", "Efficient scoring", "Tires opponents"],
                "weaknesses": ["Less possession", "Fewer chances created"],
            },
            "Defensivo": {
                "strengths": ["Solid defense", "Few goals conceded", "Compact formation"],
                "weaknesses": ["Limited scoring", "Boring play style"],
            },
        }
        return tactic_info.get(self.tactic, {"strengths": ["Unknown"], "weaknesses": ["Unknown"]})

    def compare_with(self, opponent):
        """Compare this club with another club"""
        comparison = f"\n{'='*60}\n"
        comparison += f"COMPARISON: {self.name} vs {opponent.name}\n"
        comparison += f"{'='*60}\n"
        comparison += f"\nREPUTATION:\n"
        comparison += f"  {self.name:<30} {self.reputation}/100\n"
        comparison += f"  {opponent.name:<30} {opponent.reputation}/100\n"
        comparison += f"\nOBJECTIVE:\n"
        comparison += f"  {self.name:<30} {self.objective}\n"
        comparison += f"  {opponent.name:<30} {opponent.objective}\n"
        comparison += f"\nTACTIC:\n"
        comparison += f"  {self.name:<30} {self.tactic}\n"
        comparison += f"  {opponent.name:<30} {opponent.tactic}\n"
        comparison += f"\nFINANCES:\n"
        comparison += f"  {self.name:<30} ${self.budget:,}\n"
        comparison += f"  {opponent.name:<30} ${opponent.budget:,}\n"
        comparison += f"\nPROBABILITIES (Head to Head):\n"
        self_win_prob = self.get_win_probability(opponent)
        opp_win_prob = opponent.get_win_probability(self)
        comparison += f"  {self.name} Win: {self_win_prob:.1f}%\n"
        comparison += f"  {opponent.name} Win: {opp_win_prob:.1f}%\n"
        comparison += f"  Draw: {100 - self_win_prob - opp_win_prob:.1f}%\n"
        comparison += f"{'='*60}\n"
        return comparison
