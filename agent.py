"""
Agent module - Represents the player's character (the football agent)
"""

class Agent:
    """Represents the football agent controlled by the player"""
    
    def __init__(self, name, agent_type="Balanced"):
        self.name = name
        self.money = 50000  # Starting money
        self.reputation = "Unknown"  # e.g., "Unknown", "Local", "National", "International", "World Class"
        self.clients = []  # List of Player objects
        self.week = 1
        self.actions_per_week = 5  # Number of actions player can take per week
        self.actions_remaining = 5
        
        # Agent Personality/Type
        self.agent_type = agent_type  # "Father", "Shark", "Diplomat", "Balanced"
        self._apply_agent_type_modifiers()
        
        # Triple Confidence System
        self.press_reputation = 50  # 0-100: Press trust (affects rumors, crisis management)
        # Note: club_relationships already exists (dict), player trust is in Player.trust_in_agent
        
        # Relationships with clubs and staff
        self.club_relationships = {}  # club_name: relationship_level (text)
        
        # Reports and opportunities
        self.available_reports = []  # List of player reports to review
        self.pending_offers = []  # Contract offers for clients
        
    def _apply_agent_type_modifiers(self):
        """Apply stat modifiers based on agent type"""
        type_configs = {
            "Father": {
                "money": 45000,  # Less starting money
                "actions": 6,    # More actions (mentoring takes time)
                "commission_rate": 0.03,  # 3% commission (lower)
                "morale_bonus": 0.15,  # +15% to client morale gains
                "potential_bonus": 0.10,  # +10% growth rate for young players
            },
            "Shark": {
                "money": 60000,  # More starting money
                "actions": 4,    # Fewer actions (ruthless efficiency)
                "commission_rate": 0.08,  # 8% commission (higher)
                "morale_bonus": -0.10,  # -10% to client morale (they feel used)
                "negotiation_bonus": 0.20,  # +20% to transfer fees
            },
            "Diplomat": {
                "money": 50000,
                "actions": 5,
                "commission_rate": 0.05,  # Standard 5%
                "club_relationship_bonus": 2,  # Faster club relationship growth
                "loan_access": True,  # Can arrange loans to top clubs
            },
            "Balanced": {
                "money": 50000,
                "actions": 5,
                "commission_rate": 0.05,
            }
        }
        
        config = type_configs.get(self.agent_type, type_configs["Balanced"])
        self.money = config.get("money", 50000)
        self.actions_per_week = config.get("actions", 5)
        self.actions_remaining = self.actions_per_week
        self.commission_rate = config.get("commission_rate", 0.05)
        self.morale_bonus = config.get("morale_bonus", 0.0)
        self.potential_bonus = config.get("potential_bonus", 0.0)
        self.negotiation_bonus = config.get("negotiation_bonus", 0.0)
        self.club_relationship_bonus = config.get("club_relationship_bonus", 1)
        self.loan_access = config.get("loan_access", False)
        
        # Reports and opportunities
        self.available_reports = []  # List of player reports to review
        self.pending_offers = []  # Contract offers for clients
        
    def add_client(self, player):
        """Add a player as a client"""
        if player not in self.clients:
            self.clients.append(player)
            player.sign_with_agent()
            return True
        return False
    
    def remove_client(self, player):
        """Remove a player from client list"""
        if player in self.clients:
            self.clients.remove(player)
            player.agent_signed = False
            return True
        return False
    
    def earn_commission(self, amount):
        """Earn money from commissions"""
        self.money += amount
        return amount
    
    def spend_money(self, amount):
        """Spend money"""
        if self.money >= amount:
            self.money -= amount
            return True
        return False
    
    def advance_week(self):
        """Move to the next week"""
        self.week += 1
        self.actions_remaining = self.actions_per_week
        
        # Advance all clients
        for client in self.clients:
            client.advance_week()
            
            # Earn weekly commission from signed clients (use agent's commission rate)
            if client.signed and client.weekly_wage > 0:
                commission = int(client.weekly_wage * self.commission_rate)
                self.earn_commission(commission)
    
    def use_action(self):
        """Use one action point"""
        if self.actions_remaining > 0:
            self.actions_remaining -= 1
            return True
        return False
    
    def get_status(self):
        """Return current status of the agent"""
        status = f"\n{'='*60}\n"
        status += f"AGENT STATUS - {self.name} ({self.agent_type})\n"
        status += f"{'='*60}\n"
        status += f"Week: {self.week}\n"
        status += f"Money: ${self.money:,}\n"
        status += f"Reputation: {self.reputation}\n"
        status += f"Actions Remaining This Week: {self.actions_remaining}/{self.actions_per_week}\n"
        status += f"Number of Clients: {len(self.clients)}\n"
        status += f"\n{'---'*20}\n"
        status += f"CONFIDENCE BARS:\n"
        status += f"{'---'*20}\n"
        
        # Client Trust Average
        if self.clients:
            trust_map = {"Low": 25, "Neutral": 50, "Good": 75, "Excellent": 100}
            avg_trust = sum(trust_map.get(c.trust_in_agent, 50) for c in self.clients) / len(self.clients)
            status += f"Players:  {self._draw_bar(avg_trust)} {avg_trust:.0f}/100\n"
        else:
            status += f"Players:  {self._draw_bar(50)} No clients\n"
        
        # Club Relationships Average
        if self.club_relationships:
            rel_map = {"Hostile": 0, "Neutral": 50, "Positive": 75, "Excellent": 100}
            avg_club = sum(rel_map.get(rel, 50) for rel in self.club_relationships.values()) / len(self.club_relationships)
            status += f"Clubs:    {self._draw_bar(avg_club)} {avg_club:.0f}/100\n"
        else:
            status += f"Clubs:    {self._draw_bar(50)} No relationships\n"
        
        # Press Reputation
        status += f"Press:    {self._draw_bar(self.press_reputation)} {self.press_reputation}/100\n"
        
        status += f"{'='*60}\n"
        return status
    
    def _draw_bar(self, value):
        """Draw a visual bar for confidence levels (0-100)"""
        filled = int(value / 10)
        empty = 10 - filled
        bar = "█" * filled + "░" * empty
        
        # Color coding
        if value >= 75:
            return f"[{bar}]"  # Good
        elif value >= 50:
            return f"[{bar}]"  # Okay
        elif value >= 25:
            return f"[{bar}]"  # Bad
        else:
            return f"[{bar}]"  # Critical
    
    def change_press_reputation(self, amount):
        """Modify press reputation (clamped 0-100)"""
        self.press_reputation = max(0, min(100, self.press_reputation + amount))
        return self.press_reputation
