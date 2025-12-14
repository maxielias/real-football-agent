"""
Game data module - Contains initial game data like players, clubs, etc.
"""

from player import Player

def create_initial_players():
    """Create a pool of initial players for the game"""
    players = []
    
    # Young prospects with high potential
    p1 = Player("Marcus Rodriguez", 18, "Forward", "Exceptional")
    p1.technical_ability = "Good"
    p1.physical_condition = "Excellent"
    p1.mental_strength = "Average"
    p1.tactical_awareness = "Developing"
    p1.development_stage = "Raw"
    p1.transfer_value = 50000
    players.append(p1)
    
    p2 = Player("Luca Santini", 19, "Midfielder", "High")
    p2.technical_ability = "Excellent"
    p2.physical_condition = "Good"
    p2.mental_strength = "Good"
    p2.tactical_awareness = "Good"
    p2.development_stage = "Developing"
    p2.transfer_value = 80000
    players.append(p2)
    
    p3 = Player("James O'Connor", 17, "Defender", "Very High")
    p3.technical_ability = "Average"
    p3.physical_condition = "Excellent"
    p3.mental_strength = "Excellent"
    p3.tactical_awareness = "Average"
    p3.development_stage = "Raw"
    p3.transfer_value = 30000
    players.append(p3)
    
    # Mid-career players
    p4 = Player("Andre Silva", 24, "Forward", "Moderate")
    p4.technical_ability = "Excellent"
    p4.physical_condition = "Excellent"
    p4.mental_strength = "Good"
    p4.tactical_awareness = "Excellent"
    p4.development_stage = "Peak"
    p4.club = "FC Valencia"
    p4.signed = True
    p4.weekly_wage = 15000
    p4.contract_length = 52
    p4.appearances = 120
    p4.goals = 45
    p4.assists = 20
    p4.transfer_value = 500000
    players.append(p4)
    
    p5 = Player("Kofi Mensah", 22, "Midfielder", "High")
    p5.technical_ability = "Good"
    p5.physical_condition = "Excellent"
    p5.mental_strength = "Excellent"
    p5.tactical_awareness = "Good"
    p5.development_stage = "Consistent"
    p5.club = "Athletic Bilbao"
    p5.signed = True
    p5.weekly_wage = 8000
    p5.contract_length = 78
    p5.appearances = 65
    p5.goals = 8
    p5.assists = 15
    p5.transfer_value = 200000
    players.append(p5)
    
    # Experienced player
    p6 = Player("Paolo Bianchi", 29, "Defender", "Limited")
    p6.technical_ability = "Excellent"
    p6.physical_condition = "Good"
    p6.mental_strength = "Excellent"
    p6.tactical_awareness = "World Class"
    p6.development_stage = "Peak"
    p6.club = "AS Roma"
    p6.signed = True
    p6.weekly_wage = 25000
    p6.contract_length = 26
    p6.appearances = 350
    p6.goals = 15
    p6.assists = 30
    p6.transfer_value = 300000
    players.append(p6)
    
    # Young goalkeeper
    p7 = Player("Erik Johansson", 20, "Goalkeeper", "Very High")
    p7.technical_ability = "Good"
    p7.physical_condition = "Excellent"
    p7.mental_strength = "Good"
    p7.tactical_awareness = "Average"
    p7.development_stage = "Developing"
    p7.transfer_value = 100000
    players.append(p7)
    
    # Unpolished talent
    p8 = Player("Diego Ramirez", 16, "Forward", "Unknown but Promising")
    p8.technical_ability = "Average"
    p8.physical_condition = "Average"
    p8.mental_strength = "Poor"
    p8.tactical_awareness = "Poor"
    p8.development_stage = "Raw"
    p8.transfer_value = 10000
    players.append(p8)
    
    return players

def create_player_reports():
    """Create initial scouting reports for available players"""
    reports = [
        {
            "player_name": "Marcus Rodriguez",
            "preview": "18-year-old forward from Spain. Scouts rave about his pace and finishing.",
            "full_report": """
SCOUTING REPORT: Marcus Rodriguez
Age: 18 | Position: Forward | Current Club: Youth Academy
            
Our scouts have been tracking this young Spanish forward for months. 
His pace is exceptional for his age, and he shows natural finishing 
instinct in front of goal. Physical development is ahead of his peers.

However, he's still very raw tactically and needs guidance on positioning.
Mental maturity is a concern - he can be easily frustrated.

RECOMMENDATION: High potential prospect. Could become world class with 
proper development and mentorship. Act quickly as bigger agents are 
circling.

Estimated Signing Bonus: $5,000
Expected Development Time: 2-3 years to reach consistency
            """
        },
        {
            "player_name": "Luca Santini",
            "preview": "19-year-old Italian midfielder with exceptional technical skills.",
            "full_report": """
SCOUTING REPORT: Luca Santini
Age: 19 | Position: Midfielder | Current Club: Free Agent

This Italian midfielder is a technical gem. His passing range and vision
are already at a professional level. Good physical condition and shows
maturity beyond his years.

Tactically aware and can adapt to different systems. Good mentality and
work ethic reported by former coaches.

RECOMMENDATION: Ready to sign with a professional club soon. Lower risk
investment with high potential return. Several clubs are interested.

Estimated Signing Bonus: $8,000
Expected Development Time: 1-2 years to peak performance
            """
        },
        {
            "player_name": "James O'Connor",
            "preview": "17-year-old Irish defender. Raw but physically impressive.",
            "full_report": """
SCOUTING REPORT: James O'Connor
Age: 17 | Position: Defender | Current Club: Youth Setup

Young Irish defender with exceptional physical attributes and mental
strength. Shows real leadership qualities despite his age.

Technical ability is just average for now, and tactical awareness needs
work. However, his mentality and physicality are rare at this age.

RECOMMENDATION: Long-term investment. Could develop into a commanding
central defender. Needs patient development and right coaching environment.

Estimated Signing Bonus: $3,000
Expected Development Time: 3-4 years to reach full potential
            """
        },
        {
            "player_name": "Erik Johansson",
            "preview": "20-year-old Swedish goalkeeper with high ceiling.",
            "full_report": """
SCOUTING REPORT: Erik Johansson
Age: 20 | Position: Goalkeeper | Current Club: Free Agent

Talented young Swedish goalkeeper with impressive reflexes and good
technical foundation. Physical presence in goal and commands his area well.

Mental strength is good but needs more experience at higher levels.
Tactical positioning is still developing.

RECOMMENDATION: Solid investment for goalkeeper position. Less competition
from other agents for goalkeepers. Could secure good club contract soon.

Estimated Signing Bonus: $6,000
Expected Development Time: 2 years to reach consistency
            """
        },
        {
            "player_name": "Diego Ramirez",
            "preview": "16-year-old raw talent from Argentina. High risk, high reward.",
            "full_report": """
SCOUTING REPORT: Diego Ramirez
Age: 16 | Position: Forward | Current Club: Street Football

An unusual case. This kid was spotted playing street football in Buenos
Aires. Incredible raw talent but completely unpolished.

Technically average, physically average, mentally immature, tactically
clueless. BUT - he has something special. Natural instinct and creativity
that can't be taught.

RECOMMENDATION: Extreme high-risk gamble. Could become nothing or could
become world class. Needs complete development program and lots of support.
Cheap signing bonus.

Estimated Signing Bonus: $1,000
Expected Development Time: 4-5 years, outcome uncertain
            """
        }
    ]
    return reports

def get_clubs():
    """Return list of clubs in the game"""
    return [
        "FC Valencia",
        "Athletic Bilbao", 
        "AS Roma",
        "Manchester United",
        "Bayern Munich",
        "Paris Saint-Germain",
        "Ajax Amsterdam",
        "Porto FC",
        "Celtic FC",
        "Sporting Lisbon"
    ]

def get_club_contacts():
    """Return club staff members for interactions"""
    contacts = {
        "FC Valencia": {
            "director": "Carlos Mendez",
            "coach": "Miguel Torres"
        },
        "Athletic Bilbao": {
            "director": "Inaki Azpilicueta",
            "coach": "Javier Clemente"
        },
        "AS Roma": {
            "director": "Giancarlo Rossi",
            "coach": "Roberto Mancini"
        },
        "Manchester United": {
            "director": "David Gill",
            "coach": "Thomas Edwards"
        },
        "Porto FC": {
            "director": "António Silva",
            "coach": "João Santos"
        }
    }
    return contacts
