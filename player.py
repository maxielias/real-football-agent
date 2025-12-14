"""
Player module - Represents a football player with text-based attributes
"""

class Player:
    """Represents a football player with text-based attributes instead of numbers"""
    
    def __init__(self, name, age, position, potential_level="Unknown"):
        self.name = name
        self.age = age
        self.position = position
        self.club = None
        self.signed = False
        self.agent_signed = False
        self.weekly_wage = 0
        self.transfer_value = 0
        self.contract_length = 0
        
        # Text-based attributes instead of numerical ratings
        self.technical_ability = "Unknown"  # e.g., "Poor", "Average", "Good", "Excellent", "World Class"
        self.physical_condition = "Unknown"
        self.mental_strength = "Unknown"
        self.tactical_awareness = "Unknown"
        self.potential_level = potential_level
        
        # Relationship and development
        self.morale = "Content"  # e.g., "Unhappy", "Content", "Happy", "Delighted"
        self.trust_in_agent = "Neutral"  # e.g., "Low", "Neutral", "Good", "High", "Complete"
        self.development_stage = "Raw"  # e.g., "Raw", "Developing", "Consistent", "Peak", "Declining"
        
        # Career stats (simplified)
        self.appearances = 0
        self.goals = 0
        self.assists = 0
        
        # History and notes
        self.interaction_history = []
        self.weeks_with_agent = 0
        
    def describe(self):
        """Return a detailed text description of the player"""
        description = f"\n{'='*60}\n"
        description += f"PLAYER PROFILE: {self.name}\n"
        description += f"{'='*60}\n"
        description += f"Age: {self.age} | Position: {self.position}\n"
        description += f"Club: {self.club if self.club else 'Free Agent'}\n"
        description += f"\nATTRIBUTES:\n"
        description += f"  Technical Ability: {self.technical_ability}\n"
        description += f"  Physical Condition: {self.physical_condition}\n"
        description += f"  Mental Strength: {self.mental_strength}\n"
        description += f"  Tactical Awareness: {self.tactical_awareness}\n"
        description += f"  Development Stage: {self.development_stage}\n"
        description += f"  Potential: {self.potential_level}\n"
        description += f"\nSTATUS:\n"
        description += f"  Morale: {self.morale}\n"
        description += f"  Trust in Agent: {self.trust_in_agent}\n"
        if self.agent_signed:
            description += f"  Weeks with Agent: {self.weeks_with_agent}\n"
        if self.signed:
            description += f"  Weekly Wage: ${self.weekly_wage:,}\n"
            description += f"  Contract Weeks Remaining: {self.contract_length}\n"
        description += f"\nCAREER STATS:\n"
        description += f"  Appearances: {self.appearances} | Goals: {self.goals} | Assists: {self.assists}\n"
        description += f"{'='*60}\n"
        return description
    
    def short_description(self):
        """Return a brief one-line description"""
        status = "Your Client" if self.agent_signed else "Available"
        return f"{self.name} ({self.age}) - {self.position} - {self.potential_level} potential - {status}"
    
    def interact(self, interaction_type):
        """Record an interaction with the player"""
        self.interaction_history.append(interaction_type)
        return self._get_interaction_response(interaction_type)
    
    def _get_interaction_response(self, interaction_type):
        """Generate response based on interaction type"""
        responses = {
            "counsel": f"{self.name} appreciates your guidance. Trust slightly improved.",
            "training_advice": f"{self.name} is working on their development based on your advice.",
            "contract_negotiation": f"{self.name} is open to discussing contract options.",
            "personal_support": f"{self.name} feels supported and their morale has improved.",
            "career_planning": f"{self.name} values your long-term vision for their career."
        }
        return responses.get(interaction_type, f"{self.name} acknowledges your interaction.")
    
    def advance_week(self):
        """Progress the player by one week"""
        if self.agent_signed:
            self.weeks_with_agent += 1
        if self.signed and self.contract_length > 0:
            self.contract_length -= 1
    
    def sign_with_agent(self):
        """Player signs with the agent"""
        self.agent_signed = True
        self.weeks_with_agent = 0
        return f"{self.name} has signed with you as their agent!"
    
    def sign_with_club(self, club_name, wage, contract_weeks):
        """Player signs with a club"""
        self.club = club_name
        self.signed = True
        self.weekly_wage = wage
        self.contract_length = contract_weeks
        return f"{self.name} has signed with {club_name}!"
