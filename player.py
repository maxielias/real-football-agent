"""
Player module - Represents a football player with numeric attributes
"""

import random


class Player:
    """Represents a football player with numeric attributes (1-20 scale)"""

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

        # Technical attributes (1-20 scale)
        self.defending = 10       # DEF
        self.aerial = 10          # AER
        self.passing = 10         # PAS
        self.technical = 10       # TEC
        self.speed = 10           # SPD
        self.physical = 10        # PHY
        self.shooting = 10        # SHO
        self.mental = 10          # MEN
        self.intelligence = 10    # INT

        # Calculated scores
        self.current_rating = 0
        self.potential_rating = 0
        self.position_rating = {}  # Rating for each position
        self.current_overall_score = 0
        self.potential_overall_score = 0

        self.potential_level = potential_level

        # Mental attributes (1-20 scale) - For personality
        self.determination = 10
        self.leadership = 10
        self.ambition = 10
        self.loyalty = 10
        self.pressure = 10
        self.professionalism = 10
        self.sportsmanship = 10
        self.temperament = 10
        self.concentration = 10  # Nueva: Concentration

        # Personality and media handling (calculated from mental attributes)
        self.personality = "Unknown"
        self.media_handling = "Unknown"

        # Relationship and development
        self.morale = "Content"
        self.trust_in_agent = "Neutral"
        self.development_stage = "Raw"

        # Career stats
        self.appearances = 0
        self.goals = 0
        self.assists = 0

        # History
        self.interaction_history = []
        self.weeks_with_agent = 0

    # ========== POSITION WEIGHTS SYSTEM ==========

    POSITION_WEIGHTS = {
        'FB': {  # Full Back
            'defending': 0.0077, 'aerial': 0.0002, 'passing': 0.0027,
            'technical': 0.0033, 'speed': 0.0099, 'physical': 0.0061,
            'shooting': 0.0000, 'mental': 0.0078, 'intelligence': 0.0123
        },
        'CB': {  # Center Back
            'defending': 0.0110, 'aerial': 0.0083, 'passing': 0.0007,
            'technical': 0.0008, 'speed': 0.0033, 'physical': 0.0053,
            'shooting': 0.0000, 'mental': 0.0048, 'intelligence': 0.0159
        },
        'WB': {  # Wing Back
            'defending': 0.0046, 'aerial': 0.0000, 'passing': 0.0042,
            'technical': 0.0057, 'speed': 0.0126, 'physical': 0.0071,
            'shooting': 0.0001, 'mental': 0.0061, 'intelligence': 0.0098
        },
        'DM': {  # Defensive Midfielder
            'defending': 0.0075, 'aerial': 0.0001, 'passing': 0.0031,
            'technical': 0.0043, 'speed': 0.0030, 'physical': 0.0054,
            'shooting': 0.0009, 'mental': 0.0093, 'intelligence': 0.0166
        },
        'SM': {  # Side Midfielder
            'defending': 0.0013, 'aerial': 0.0000, 'passing': 0.0073,
            'technical': 0.0103, 'speed': 0.0090, 'physical': 0.0041,
            'shooting': 0.0002, 'mental': 0.0071, 'intelligence': 0.0106
        },
        'CM': {  # Center Midfielder
            'defending': 0.0027, 'aerial': 0.0000, 'passing': 0.0061,
            'technical': 0.0095, 'speed': 0.0035, 'physical': 0.0039,
            'shooting': 0.0005, 'mental': 0.0077, 'intelligence': 0.0162
        },
        'WF': {  # Winger/Wing Forward
            'defending': 0.0000, 'aerial': 0.0008, 'passing': 0.0037,
            'technical': 0.0123, 'speed': 0.0144, 'physical': 0.0046,
            'shooting': 0.0011, 'mental': 0.0045, 'intelligence': 0.0085
        },
        'AM': {  # Attacking Midfielder
            'defending': 0.0000, 'aerial': 0.0000, 'passing': 0.0045,
            'technical': 0.0140, 'speed': 0.0068, 'physical': 0.0009,
            'shooting': 0.0020, 'mental': 0.0041, 'intelligence': 0.0178
        },
        'FW': {  # Forward
            'defending': 0.0000, 'aerial': 0.0030, 'passing': 0.0009,
            'technical': 0.0079, 'speed': 0.0094, 'physical': 0.0055,
            'shooting': 0.0045, 'mental': 0.0065, 'intelligence': 0.0123
        },
        'AVG': {  # Average
            'defending': 0.0039, 'aerial': 0.0014, 'passing': 0.0037,
            'technical': 0.0076, 'speed': 0.0080, 'physical': 0.0048,
            'shooting': 0.0010, 'mental': 0.0064, 'intelligence': 0.0133
        }
    }

    POSITION_MAP = {
        'Goalkeeper': 'CB', 'GK': 'CB',
        'Defender': 'CB', 'Centre Back': 'CB', 'Center Back': 'CB', 'CB': 'CB',
        'Full Back': 'FB', 'Fullback': 'FB', 'FB': 'FB',
        'Left Back': 'FB', 'LB': 'FB', 'Right Back': 'FB', 'RB': 'FB',
        'Wing Back': 'WB', 'Wingback': 'WB', 'WB': 'WB', 'LWB': 'WB', 'RWB': 'WB',
        'Defensive Midfielder': 'DM', 'DM': 'DM', 'CDM': 'DM',
        'Midfielder': 'CM', 'Central Midfielder': 'CM', 'Centre Midfielder': 'CM', 'CM': 'CM',
        'Side Midfielder': 'SM', 'SM': 'SM', 'Wide Midfielder': 'SM', 'LM': 'SM', 'RM': 'SM',
        'Winger': 'WF', 'Wing Forward': 'WF', 'WF': 'WF', 'LW': 'WF', 'RW': 'WF',
        'Attacking Midfielder': 'AM', 'AM': 'AM', 'CAM': 'AM',
        'Forward': 'FW', 'Striker': 'FW', 'FW': 'FW', 'ST': 'FW', 'CF': 'FW'
    }

    def describe(self):
        """Return a detailed text description of the player"""
        description = f"\n{'='*60}\n"
        description += f"PLAYER PROFILE: {self.name}\n"
        description += f"{'='*60}\n"
        description += f"Age: {self.age} | Position: {self.position}\n"
        description += f"Club: {self.club if self.club else 'Free Agent'}\n"
        description += f"\nRATINGS:\n"
        description += f"  Current Rating: {self.current_rating:.2f}\n"
        description += f"  Potential Rating: {self.potential_rating:.2f}\n"
        description += f"  Development Stage: {self.development_stage}\n"

        description += f"\nPERSONALITY:\n"
        description += f"  Personality: {self.personality}\n"
        description += f"  Media Handling: {self.media_handling}\n"
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

    # ========== TECHNICAL ATTRIBUTES ==========

    def set_technical_attributes(self, defending=None, aerial=None, passing=None,
                                 technical=None, speed=None, physical=None,
                                 shooting=None, mental=None, intelligence=None):
        """Set technical attributes and recalculate ratings"""
        if defending is not None:
            self.defending = max(1, min(20, defending))
        if aerial is not None:
            self.aerial = max(1, min(20, aerial))
        if passing is not None:
            self.passing = max(1, min(20, passing))
        if technical is not None:
            self.technical = max(1, min(20, technical))
        if speed is not None:
            self.speed = max(1, min(20, speed))
        if physical is not None:
            self.physical = max(1, min(20, physical))
        if shooting is not None:
            self.shooting = max(1, min(20, shooting))
        if mental is not None:
            self.mental = max(1, min(20, mental))
        if intelligence is not None:
            self.intelligence = max(1, min(20, intelligence))

        self.calculate_ratings()

    def calculate_rating_for_position(self, position_key):
        """Calculate rating for a specific position using weights"""
        if position_key not in self.POSITION_WEIGHTS:
            position_key = 'AVG'

        weights = self.POSITION_WEIGHTS[position_key]

        rating = (
            self.defending * weights['defending'] +
            self.aerial * weights['aerial'] +
            self.passing * weights['passing'] +
            self.technical * weights['technical'] +
            self.speed * weights['speed'] +
            self.physical * weights['physical'] +
            self.shooting * weights['shooting'] +
            self.mental * weights['mental'] +
            self.intelligence * weights['intelligence']
        )

        return round(rating, 2)

    def calculate_ratings(self):
        """Calculate current rating, potential rating, and all position ratings"""
        position_key = self.POSITION_MAP.get(self.position, 'AVG')
        self.current_rating = self.calculate_rating_for_position(position_key)

        # Potential rating
        theoretical_max = sum(20 * weight for weight in self.POSITION_WEIGHTS[position_key].values())
        potential_range_min = self.current_rating + 0.01
        potential_range_max = min(theoretical_max, self.current_rating * 1.5 + random.uniform(0.05, 0.15))
        self.potential_rating = round(random.uniform(potential_range_min, potential_range_max), 2)

        # Position ratings
        self.position_rating = {}
        for pos_key in self.POSITION_WEIGHTS.keys():
            if pos_key != 'AVG':
                self.position_rating[pos_key] = self.calculate_rating_for_position(pos_key)

    def get_best_positions(self, top_n=3):
        """Get the top N positions for this player based on ratings"""
        if not self.position_rating:
            self.calculate_ratings()
        sorted_positions = sorted(self.position_rating.items(), key=lambda x: x[1], reverse=True)
        return sorted_positions[:top_n]

    def get_technical_attributes_description(self):
        """Get a formatted description of all technical attributes"""
        attrs = f"\n{'='*60}\n"
        attrs += f"TECHNICAL ATTRIBUTES: {self.name}\n"
        attrs += f"{'='*60}\n"
        attrs += f"Defending (DEF):     {self.defending:2d}\n"
        attrs += f"Aerial (AER):        {self.aerial:2d}\n"
        attrs += f"Passing (PAS):       {self.passing:2d}\n"
        attrs += f"Technical (TEC):     {self.technical:2d}\n"
        attrs += f"Speed (SPD):         {self.speed:2d}\n"
        attrs += f"Physical (PHY):      {self.physical:2d}\n"
        attrs += f"Shooting (SHO):      {self.shooting:2d}\n"
        attrs += f"Mental (MEN):        {self.mental:2d}\n"
        attrs += f"Intelligence (INT):  {self.intelligence:2d}\n"
        attrs += f"\nCurrent Rating: {self.current_rating:.2f}\n"
        attrs += f"Potential Rating: {self.potential_rating:.2f}\n"
        attrs += f"{'='*60}\n"
        return attrs

    # ========== MENTAL ATTRIBUTES & PERSONALITY ==========

    def set_mental_attributes(self, determination=None, leadership=None, ambition=None,
                             loyalty=None, pressure=None, professionalism=None,
                             sportsmanship=None, temperament=None):
        """Set mental attributes and update personality/media handling"""
        if determination is not None:
            self.determination = max(1, min(20, determination))
        if leadership is not None:
            self.leadership = max(1, min(20, leadership))
        if ambition is not None:
            self.ambition = max(1, min(20, ambition))
        if loyalty is not None:
            self.loyalty = max(1, min(20, loyalty))
        if pressure is not None:
            self.pressure = max(1, min(20, pressure))
        if professionalism is not None:
            self.professionalism = max(1, min(20, professionalism))
        if sportsmanship is not None:
            self.sportsmanship = max(1, min(20, sportsmanship))
        if temperament is not None:
            self.temperament = max(1, min(20, temperament))

        self.update_personality()
        self.update_media_handling()

    def set_concentration(self, concentration=None):
        """Set concentration attribute"""
        if concentration is not None:
            self.concentration = max(1, min(20, concentration))

    def update_personality(self, is_regen=False, plays_for_favourite=False):
        """Update the player's personality based on mental attributes"""
        self.personality = self.calculate_personality(is_regen, plays_for_favourite)
        return self.personality

    def calculate_personality(self, is_regen=False, plays_for_favourite=False):
        """
        Calculate player personality based on mental attributes.
        Uses exact ranges from the personality matrix specification.
        """
        det = self.determination
        lead = self.leadership
        amb = self.ambition
        loy = self.loyalty
        pres = self.pressure
        prof = self.professionalism
        sport = self.sportsmanship
        temp = self.temperament
        con = self.concentration

        # ========== BEST PERSONALITIES ==========

        # Model Citizen: Pro 15-20, Pre 14-20, Amb 12-20, Tem 15-20, Loy 15-20, Spo 15-20, Det 14-20
        if (15 <= prof <= 20 and 14 <= pres <= 20 and 12 <= amb <= 20 and
            15 <= temp <= 20 and 15 <= loy <= 20 and 15 <= sport <= 20 and 14 <= det <= 20):
            return "Model Citizen"

        # Model Professional (23+): Pro 20
        if self.age >= 23 and prof == 20:
            return "Model Professional"

        # ========== GOOD PERSONALITIES ==========

        # Charismatic Leader (23+): Tem 18-20, Con 18-20, Leadership 18-20
        if self.age >= 23 and 18 <= temp <= 20 and 18 <= con <= 20 and 18 <= lead <= 20:
            return "Charismatic Leader"

        # Born Leader (23+): Det 20, Con 20, Leadership 20
        if self.age >= 23 and det == 20 and con == 20 and lead == 20:
            return "Born Leader"

        # Leader (23+): Det 19-20, Leadership 19-20
        if self.age >= 23 and 19 <= det <= 20 and 19 <= lead <= 20:
            return "Leader"

        # Perfectionist: Pro 14-20, Tem 1-9
        if 14 <= prof <= 20 and 1 <= temp <= 9:
            return "Perfectionist"

        # Professional: Pro 18-19
        if 18 <= prof <= 19:
            return "Professional"

        # Fairly Professional: Pro 15-20
        if 15 <= prof <= 20:
            return "Fairly Professional"

        # Iron Willed: Pre 20, Det 15-17, Con 5-20
        if pres == 20 and 15 <= det <= 17 and 5 <= con <= 20:
            return "Iron Willed"

        # Resolute: Pro 15-20, Pre 1-16, Det 12-20, Con 15-17
        if 15 <= prof <= 20 and 1 <= pres <= 16 and 12 <= det <= 20 and 15 <= con <= 17:
            return "Resolute"

        # Resilient: Det 15-17, Con 5-20, Leadership 15-17
        if 15 <= det <= 17 and 5 <= con <= 20 and 15 <= lead <= 17:
            return "Resilient"

        # Spirited: Pro 11-17, Pre 15-20, Loy 10-20, Det 1-14, Con 1-17
        if 11 <= prof <= 17 and 15 <= pres <= 20 and 10 <= loy <= 20 and 1 <= det <= 14 and 1 <= con <= 17:
            return "Spirited"

        # Driven: Amb 12-20, Det 17-20
        if 12 <= amb <= 20 and 17 <= det <= 20:
            return "Driven"

        # Determined: Amb 1-11, Det >=17
        if 1 <= amb <= 11 and 17 <= det <= 20:
            return "Determined"

        # Fairly Determined: Pro 1-14, Pre 1-16, Det 12-20, Con 15-17
        if 1 <= prof <= 14 and 1 <= pres <= 16 and 12 <= det <= 20 and 15 <= con <= 17:
            return "Fairly Determined"

        # ========== NEUTRAL PERSONALITIES ==========

        # Very Ambitious: Amb 20, Loy 1-10, Det 1-17, Con 1-17
        if amb == 20 and 1 <= loy <= 10 and 1 <= det <= 17 and 1 <= con <= 17:
            return "Very Ambitious"

        # Ambitious: Amb 16-20, Loy 1-10, Det 1-17, Con 1-17
        if 16 <= amb <= 20 and 1 <= loy <= 10 and 1 <= det <= 17 and 1 <= con <= 17:
            return "Ambitious"

        # Fairly Ambitious: Pro 1-14, Amb 15-20, Con 1-14
        if 1 <= prof <= 14 and 15 <= amb <= 20 and 1 <= con <= 14:
            return "Fairly Ambitious"

        # Very Loyal: Amb 5-8, Con 18-20
        if 5 <= amb <= 8 and 18 <= con <= 20:
            return "Devoted" if plays_for_favourite else "Very Loyal"

        # Loyal: Pro 1-7, Loy 17-19, Det 6-17, Con 1-14
        if 1 <= prof <= 7 and 17 <= loy <= 19 and 6 <= det <= 17 and 1 <= con <= 14:
            return "Loyal"

        # Fairly Loyal: Pro 1-14, Amb 6-14, Loy 15-20, Con 1-14
        if 1 <= prof <= 14 and 6 <= amb <= 14 and 15 <= loy <= 20 and 1 <= con <= 14:
            return "Fairly Loyal"

        # Light-Hearted: Pro 1-17, Pre 15-20, Loy 10-20, Det 15-20, Con 1-17
        if 1 <= prof <= 17 and 15 <= pres <= 20 and 10 <= loy <= 20 and 15 <= det <= 20 and 1 <= con <= 17:
            return "Light-Hearted"

        # Jovial: Pro 1-10, Pre 15-20, Tem 10-20, Det 1-14, Con 1-17
        if 1 <= prof <= 10 and 15 <= pres <= 20 and 10 <= temp <= 20 and 1 <= det <= 14 and 1 <= con <= 17:
            return "Jovial"

        # Honest: Pro 5-20, Sport 20, Det 1-10, Con 1-10
        if 5 <= prof <= 20 and sport == 20 and 1 <= det <= 10 and 1 <= con <= 10:
            return "Honest"

        # Sporting: Pro 8-20, Loy 18-20, Sport 1-10, Det 1-10, Con 1-10
        if 8 <= prof <= 20 and 18 <= loy <= 20 and 1 <= sport <= 10 and 1 <= det <= 10 and 1 <= con <= 10:
            return "Sporting"

        # Fairly Sporting: Pro 1-14, Amb 1-14, Loy 1-14, Sport 15-20, Con 1-14
        if 1 <= prof <= 14 and 1 <= amb <= 14 and 1 <= loy <= 14 and 15 <= sport <= 20 and 1 <= con <= 14:
            return "Fairly Sporting"

        # Balanced: Pro 1-14, Amb 1-14, Loy 1-14, Sport 1-14, Det 1-14, Con 1-14
        if 1 <= prof <= 14 and 1 <= amb <= 14 and 1 <= loy <= 14 and 1 <= sport <= 14 and 1 <= det <= 14 and 1 <= con <= 14:
            return "Balanced"

        # ========== BAD PERSONALITIES (regen only) ==========
        if is_regen:
            # Fickle: Pro 1-14, Pre 15-20, Loy 1-14, Det 1-14, Con 1-14
            if 1 <= prof <= 14 and 15 <= pres <= 20 and 1 <= loy <= 14 and 1 <= det <= 14 and 1 <= con <= 14:
                return "Fickle"

            # Mercenary: Amb 16-20, Loy 1-6
            if 16 <= amb <= 20 and 1 <= loy <= 6:
                return "Mercenary"

        # ========== WORST PERSONALITIES (regen only) ==========
        if is_regen:
            # Slack: Pro 1, Tem 5-20, Det 1-9
            if prof == 1 and 5 <= temp <= 20 and 1 <= det <= 9:
                return "Slack"

            # Casual: Pro 2-4, Tem 5-20, Det 1-9
            if 2 <= prof <= 4 and 5 <= temp <= 20 and 1 <= det <= 9:
                return "Casual"

            # Temperamental: Pro 1-10, Tem 1-4, Con 1-17, Leadership 1
            if 1 <= prof <= 10 and 1 <= temp <= 4 and 1 <= con <= 17 and lead == 1:
                return "Temperamental"

            # Easily Discouraged: Pro 5-20, Tem 1-10, Det 1-5
            if 5 <= prof <= 20 and 1 <= temp <= 10 and 1 <= det <= 5:
                return "Easily Discouraged"

            # Low Determination: Pro 5-20, Tem 1-10, Det 1-5, Con 2-5
            if 5 <= prof <= 20 and 1 <= temp <= 10 and 1 <= det <= 5 and 2 <= con <= 5:
                return "Low Determination"

            # Spineless: Pro 5-20, Pre 1, Det 1-5, Con 1-17, Leadership 1-10
            if 5 <= prof <= 20 and pres == 1 and 1 <= det <= 5 and 1 <= con <= 17 and 1 <= lead <= 10:
                return "Spineless"

            # Low Self-Belief: Pro 5-20, Pre 2-3, Det 1-5, Con 1-17, Leadership 1-10
            if 5 <= prof <= 20 and 2 <= pres <= 3 and 1 <= det <= 5 and 1 <= con <= 17 and 1 <= lead <= 10:
                return "Low Self-Belief"

            # Unambitious: Pro 5-20, Amb 1-5, Loy 11-20, Det 1-5, Con 1-17
            if 5 <= prof <= 20 and 1 <= amb <= 5 and 11 <= loy <= 20 and 1 <= det <= 5 and 1 <= con <= 17:
                return "Unambitious"

            # Unsporting: Tem 1, Sport 1-6, Det 10-17
            if temp == 1 and 1 <= sport <= 6 and 10 <= det <= 17:
                return "Unsporting"

            # Realist: Pro 1-4, Amb 1-4, Tem 1-4
            if 1 <= prof <= 4 and 1 <= amb <= 4 and 1 <= temp <= 4:
                return "Realist"

        # Default fallback
        return "Balanced"

    def update_media_handling(self, is_regen=False):
        """Update the player's media handling style"""
        self.media_handling = self.calculate_media_handling(is_regen)
        return self.media_handling

    def calculate_media_handling(self, is_regen=False):
        """
        Calculate media handling style based on mental attributes.
        Uses the Media Handling Style matrix from the specification.
        """
        det = self.determination
        lead = self.leadership
        amb = self.ambition
        loy = self.loyalty
        pres = self.pressure
        prof = self.professionalism
        sport = self.sportsmanship
        temp = self.temperament
        con = self.concentration

        # ========== BEST MEDIA HANDLING ==========

        # Confrontational: Amb 1-4, Tem 1-4
        if 1 <= amb <= 4 and 1 <= temp <= 4:
            return "Confrontational"

        # ========== GOOD MEDIA HANDLING ==========

        # Evasive: Pre 15-20, Amb 15-20, Con 6-14
        if 15 <= pres <= 20 and 15 <= amb <= 20 and 6 <= con <= 14:
            return "Evasive"

        # Level-Headed: Tem 7-20, Con 11-20, Det 1-14
        if 7 <= temp <= 20 and 11 <= con <= 20 and 1 <= det <= 14:
            return "Level-Headed"

        # Media-Friendly: Con 1-14, Leadership 1-14
        if 1 <= con <= 14 and 1 <= lead <= 14:
            return "Media-Friendly"

        # Outspoken: Det 15-20, Sport 15-20
        if 15 <= det <= 20 and 15 <= sport <= 20:
            return "Outspoken"

        # Reserved: Tem 7-20, Con 1-5
        if 7 <= temp <= 20 and 1 <= con <= 5:
            return "Reserved"

        # Short-Tempered: Amb 1-4, Pre 1-4
        if 1 <= amb <= 4 and 1 <= pres <= 4:
            return "Short-Tempered"

        # ========== NEUTRAL MEDIA HANDLING ==========

        # Unflappable: Pre 15-20, Tem 15-20
        if 15 <= pres <= 20 and 15 <= temp <= 20:
            return "Unflappable"

        # Volatile: Tem 1-6
        if 1 <= temp <= 6:
            return "Volatile"

        # Default
        return "Balanced"

    def get_mental_attributes_description(self):
        """Get a formatted description of all mental attributes"""
        attrs = f"\n{'='*60}\n"
        attrs += f"MENTAL ATTRIBUTES: {self.name}\n"
        attrs += f"{'='*60}\n"
        attrs += f"Determination:    {self.determination:2d}\n"
        attrs += f"Leadership:       {self.leadership:2d}\n"
        attrs += f"Ambition:         {self.ambition:2d}\n"
        attrs += f"Loyalty:          {self.loyalty:2d}\n"
        attrs += f"Pressure:         {self.pressure:2d}\n"
        attrs += f"Professionalism:  {self.professionalism:2d}\n"
        attrs += f"Sportsmanship:    {self.sportsmanship:2d}\n"
        attrs += f"Temperament:      {self.temperament:2d}\n"
        attrs += f"Concentration:    {self.concentration:2d}\n"
        attrs += f"\nPersonality: {self.personality}\n"
        attrs += f"Media Handling: {self.media_handling}\n"
        attrs += f"{'='*60}\n"
        return attrs
