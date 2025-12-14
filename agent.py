"""
Agent module - Represents the player's character (the football agent)
"""

class Agent:
    """Represents the football agent controlled by the player"""
    
    def __init__(self, name):
        self.name = name
        self.money = 50000  # Starting money
        self.reputation = "Unknown"  # e.g., "Unknown", "Local", "National", "International", "World Class"
        self.clients = []  # List of Player objects
        self.week = 1
        self.actions_per_week = 5  # Number of actions player can take per week
        self.actions_remaining = 5
        
        # Relationships with clubs and staff
        self.club_relationships = {}  # club_name: relationship_level (text)
        
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
            
            # Earn weekly commission from signed clients
            if client.signed and client.weekly_wage > 0:
                commission = int(client.weekly_wage * 0.05)  # 5% commission
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
        status += f"AGENT STATUS - {self.name}\n"
        status += f"{'='*60}\n"
        status += f"Week: {self.week}\n"
        status += f"Money: ${self.money:,}\n"
        status += f"Reputation: {self.reputation}\n"
        status += f"Actions Remaining This Week: {self.actions_remaining}/{self.actions_per_week}\n"
        status += f"Number of Clients: {len(self.clients)}\n"
        status += f"{'='*60}\n"
        return status
