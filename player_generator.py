"""
Player generator with rating system - Create players with realistic attributes
"""

import random
from player import Player

def generate_random_attributes(base_rating=12, variation=4):
    """
    Generate random attributes based on a base rating with variation.
    
    Args:
        base_rating: Center point for attribute distribution (default 12)
        variation: Standard deviation for the distribution (default 4)
    
    Returns:
        dict: Dictionary with all technical attributes
    """
    return {
        'defending': max(1, min(20, int(random.gauss(base_rating, variation)))),
        'aerial': max(1, min(20, int(random.gauss(base_rating, variation)))),
        'passing': max(1, min(20, int(random.gauss(base_rating, variation)))),
        'technical': max(1, min(20, int(random.gauss(base_rating, variation)))),
        'speed': max(1, min(20, int(random.gauss(base_rating, variation)))),
        'physical': max(1, min(20, int(random.gauss(base_rating, variation)))),
        'shooting': max(1, min(20, int(random.gauss(base_rating, variation)))),
        'mental': max(1, min(20, int(random.gauss(base_rating, variation)))),
        'intelligence': max(1, min(20, int(random.gauss(base_rating, variation))))
    }

def generate_position_specialist(position, quality='good'):
    """
    Generate attributes for a position specialist.
    
    Args:
        position: Position key (FB, CB, WB, DM, SM, CM, WF, AM, FW)
        quality: 'poor', 'average', 'good', 'excellent', 'world_class'
    
    Returns:
        dict: Specialized attributes for the position
    """
    # Base ratings by quality
    quality_bases = {
        'poor': (8, 3),        # base, variation
        'average': (12, 3),
        'good': (15, 2),
        'excellent': (17, 2),
        'world_class': (19, 1)
    }
    
    base, variation = quality_bases.get(quality, (12, 3))
    
    # Position-specific attribute priorities
    position_profiles = {
        'FB': {
            'high': ['defending', 'speed', 'intelligence'],
            'medium': ['passing', 'physical', 'mental'],
            'low': ['aerial', 'technical', 'shooting']
        },
        'CB': {
            'high': ['defending', 'aerial', 'intelligence'],
            'medium': ['physical', 'mental'],
            'low': ['passing', 'technical', 'speed', 'shooting']
        },
        'WB': {
            'high': ['speed', 'intelligence'],
            'medium': ['defending', 'passing', 'technical', 'physical', 'mental'],
            'low': ['aerial', 'shooting']
        },
        'DM': {
            'high': ['defending', 'mental', 'intelligence'],
            'medium': ['passing', 'physical', 'technical'],
            'low': ['aerial', 'speed', 'shooting']
        },
        'SM': {
            'high': ['technical', 'speed', 'intelligence'],
            'medium': ['passing', 'mental'],
            'low': ['defending', 'aerial', 'physical', 'shooting']
        },
        'CM': {
            'high': ['passing', 'technical', 'intelligence'],
            'medium': ['mental', 'defending'],
            'low': ['aerial', 'speed', 'physical', 'shooting']
        },
        'WF': {
            'high': ['technical', 'speed'],
            'medium': ['passing', 'shooting', 'mental', 'intelligence'],
            'low': ['defending', 'aerial', 'physical']
        },
        'AM': {
            'high': ['technical', 'intelligence'],
            'medium': ['passing', 'shooting', 'mental', 'speed'],
            'low': ['defending', 'aerial', 'physical']
        },
        'FW': {
            'high': ['shooting', 'speed', 'intelligence'],
            'medium': ['technical', 'aerial', 'mental', 'physical'],
            'low': ['defending', 'passing']
        }
    }
    
    profile = position_profiles.get(position, position_profiles['CM'])
    
    attrs = {}
    for attr in ['defending', 'aerial', 'passing', 'technical', 'speed', 
                 'physical', 'shooting', 'mental', 'intelligence']:
        if attr in profile['high']:
            attr_base = base + 2
        elif attr in profile['medium']:
            attr_base = base
        else:
            attr_base = max(1, base - 3)
        
        attrs[attr] = max(1, min(20, int(random.gauss(attr_base, variation))))
    
    return attrs

def generate_player(name, age, position, quality='average', specialist=True):
    """
    Generate a complete player with all attributes.
    
    Args:
        name: Player name
        age: Player age
        position: Position name (will be mapped to position key)
        quality: Quality level for attributes
        specialist: If True, generate position-specific attributes
    
    Returns:
        Player: Fully configured player object
    """
    player = Player(name, age, position)
    
    # Map position to key
    position_key = Player.POSITION_MAP.get(position, 'CM')
    
    # Generate technical attributes
    if specialist:
        tech_attrs = generate_position_specialist(position_key, quality)
    else:
        quality_bases = {
            'poor': (8, 3),
            'average': (12, 3),
            'good': (15, 2),
            'excellent': (17, 2),
            'world_class': (19, 1)
        }
        base, variation = quality_bases.get(quality, (12, 3))
        tech_attrs = generate_random_attributes(base, variation)
    
    player.set_technical_attributes(**tech_attrs)
    
    # Generate mental attributes
    quality_bases = {
        'poor': (8, 3),
        'average': (12, 3),
        'good': (15, 2),
        'excellent': (17, 2),
        'world_class': (19, 1)
    }
    base, variation = quality_bases.get(quality, (12, 3))
    
    mental_attrs = {
        'determination': max(1, min(20, int(random.gauss(base, variation)))),
        'leadership': max(1, min(20, int(random.gauss(base, variation)))),
        'ambition': max(1, min(20, int(random.gauss(base, variation)))),
        'loyalty': max(1, min(20, int(random.gauss(base, variation)))),
        'pressure': max(1, min(20, int(random.gauss(base, variation)))),
        'professionalism': max(1, min(20, int(random.gauss(base, variation)))),
        'sportsmanship': max(1, min(20, int(random.gauss(base, variation)))),
        'temperament': max(1, min(20, int(random.gauss(base, variation))))
    }
    
    player.set_mental_attributes(**mental_attrs)
    
    return player

def create_squad_by_quality(quality='average'):
    """Create a full 11-player squad of a specific quality level"""
    positions = [
        ("Goalkeeper", "GK"),
        ("Center Back", "CB"),
        ("Center Back", "CB"),
        ("Full Back", "LB"),
        ("Full Back", "RB"),
        ("Defensive Midfielder", "DM"),
        ("Central Midfielder", "CM"),
        ("Central Midfielder", "CM"),
        ("Winger", "LW"),
        ("Winger", "RW"),
        ("Forward", "ST")
    ]
    
    first_names = ["Carlos", "Miguel", "Juan", "Diego", "Luis", "Pedro", "Andrés",
                   "Roberto", "Fernando", "Javier", "Pablo", "Daniel", "Marco", "Alex"]
    last_names = ["García", "Rodríguez", "Martínez", "López", "González", "Pérez",
                  "Sánchez", "Torres", "Ramírez", "Flores", "Rivera", "Silva"]
    
    squad = []
    for i, (pos_name, pos_code) in enumerate(positions):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        age = random.randint(20, 30)
        player = generate_player(name, age, pos_name, quality, specialist=True)
        squad.append(player)
    
    return squad

def display_squad_summary(squad):
    """Display a summary of squad ratings"""
    print("\n" + "="*80)
    print("SQUAD SUMMARY")
    print("="*80)
    
    total_rating = 0
    for i, player in enumerate(squad, 1):
        print(f"\n{i:2d}. {player.name:20s} ({player.age}) - {player.position:20s}")
        print(f"    Rating: {player.current_rating:.2f} | Potential: {player.potential_rating:.2f}")
        print(f"    Personality: {player.personality}")
        total_rating += player.current_rating
    
    avg_rating = total_rating / len(squad)
    print("\n" + "="*80)
    print(f"TEAM AVERAGE RATING: {avg_rating:.2f}")
    print("="*80)

def interactive_player_creator():
    """Interactive tool to create a player"""
    print("\n" + "="*80)
    print("INTERACTIVE PLAYER CREATOR WITH RATING SYSTEM")
    print("="*80)
    
    name = input("\nPlayer Name: ").strip()
    if not name:
        name = "Test Player"
    
    age = input("Age (18-40): ").strip()
    age = int(age) if age.isdigit() and 18 <= int(age) <= 40 else 25
    
    positions = ["Goalkeeper", "Defender", "Center Back", "Full Back", "Wing Back",
                 "Defensive Midfielder", "Midfielder", "Attacking Midfielder",
                 "Winger", "Forward"]
    print(f"\nPositions: {', '.join(positions)}")
    position = input("Position: ").strip()
    if position not in positions:
        position = "Midfielder"
    
    print("\nQuality levels: poor, average, good, excellent, world_class")
    quality = input("Quality (default: average): ").strip()
    if quality not in ['poor', 'average', 'good', 'excellent', 'world_class']:
        quality = 'average'
    
    specialist = input("Generate as position specialist? (y/n, default: y): ").strip().lower()
    specialist = specialist != 'n'
    
    print("\nGenerating player...")
    player = generate_player(name, age, position, quality, specialist)
    
    print("\n" + "="*80)
    print("PLAYER CREATED!")
    print("="*80)
    print(player.get_technical_attributes_description())
    print(player.get_mental_attributes_description())
    print(player.describe())
    
    return player

def main():
    """Main menu"""
    while True:
        print("\n" + "="*80)
        print("PLAYER GENERATOR WITH RATING SYSTEM")
        print("="*80)
        print("\nOptions:")
        print("1. Generate random player")
        print("2. Generate quality squad (poor)")
        print("3. Generate quality squad (average)")
        print("4. Generate quality squad (good)")
        print("5. Generate quality squad (excellent)")
        print("6. Generate quality squad (world class)")
        print("7. Interactive player creator")
        print("8. Exit")
        
        choice = input("\nSelect option (1-8): ").strip()
        
        if choice == '1':
            qualities = ['poor', 'average', 'good', 'excellent', 'world_class']
            positions = ["Center Back", "Midfielder", "Forward", "Winger"]
            player = generate_player(
                "Random Player",
                random.randint(18, 32),
                random.choice(positions),
                random.choice(qualities),
                specialist=True
            )
            print(player.get_technical_attributes_description())
            print(player.describe())
        
        elif choice in ['2', '3', '4', '5', '6']:
            quality_map = {
                '2': 'poor',
                '3': 'average',
                '4': 'good',
                '5': 'excellent',
                '6': 'world_class'
            }
            quality = quality_map[choice]
            print(f"\nGenerating {quality} quality squad...")
            squad = create_squad_by_quality(quality)
            display_squad_summary(squad)
        
        elif choice == '7':
            player = interactive_player_creator()
        
        elif choice == '8':
            print("\nGracias por usar el generador de jugadores!")
            break
        
        else:
            print("\nOpción inválida. Por favor seleccione 1-8.")

if __name__ == "__main__":
    main()
