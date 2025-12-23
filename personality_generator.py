"""
Interactive personality generator - Generate random players with different personalities
"""

import random
from player import Player

def generate_random_mental_attributes():
    """Generate random mental attributes following a normal distribution"""
    # Use normal distribution centered around 12 (slightly above average)
    return {
        'determination': max(1, min(20, int(random.gauss(12, 4)))),
        'leadership': max(1, min(20, int(random.gauss(10, 4)))),
        'ambition': max(1, min(20, int(random.gauss(11, 4)))),
        'loyalty': max(1, min(20, int(random.gauss(12, 4)))),
        'pressure': max(1, min(20, int(random.gauss(11, 4)))),
        'professionalism': max(1, min(20, int(random.gauss(12, 4)))),
        'sportsmanship': max(1, min(20, int(random.gauss(12, 4)))),
        'temperament': max(1, min(20, int(random.gauss(12, 4))))
    }

def generate_player_with_personality(name, age, position, is_regen=False):
    """Generate a player with random mental attributes and personality"""
    player = Player(name, age, position)
    attrs = generate_random_mental_attributes()
    player.set_mental_attributes(**attrs)
    player.update_personality(is_regen=is_regen)
    return player

def generate_squad(num_players=11):
    """Generate a full squad with different personalities"""
    positions = ["Goalkeeper", "Defender", "Defender", "Defender", "Defender",
                 "Midfielder", "Midfielder", "Midfielder", "Midfielder",
                 "Forward", "Forward"]
    
    first_names = ["Carlos", "Miguel", "Juan", "Diego", "Luis", "Pedro", "Andrés",
                   "Roberto", "Fernando", "Javier", "Pablo", "Daniel"]
    last_names = ["García", "Rodríguez", "Martínez", "López", "González", "Pérez",
                  "Sánchez", "Torres", "Ramírez", "Flores", "Rivera", "Silva"]
    
    squad = []
    for i in range(num_players):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        age = random.randint(18, 32)
        position = positions[i] if i < len(positions) else random.choice(positions)
        is_regen = random.random() < 0.3  # 30% chance of being a regen
        
        player = generate_player_with_personality(name, age, position, is_regen)
        squad.append(player)
    
    return squad

def display_squad_personalities(squad):
    """Display personality summary of the squad"""
    print("\n" + "="*80)
    print("SQUAD PERSONALITY ANALYSIS")
    print("="*80)
    
    # Count personalities by category
    categories = {'Best': 0, 'Good': 0, 'Neutral': 0, 'Bad': 0, 'Worst': 0}
    personality_counts = {}
    
    for player in squad:
        personality_desc = player.get_personality_description()
        personality = player.personality
        
        # Count by category
        if '(Best)' in personality_desc:
            categories['Best'] += 1
        elif '(Good)' in personality_desc:
            categories['Good'] += 1
        elif '(Neutral)' in personality_desc:
            categories['Neutral'] += 1
        elif '(Bad)' in personality_desc:
            categories['Bad'] += 1
        elif '(Worst)' in personality_desc:
            categories['Worst'] += 1
        
        # Count specific personalities
        personality_counts[personality] = personality_counts.get(personality, 0) + 1
    
    print("\nCategory Distribution:")
    for category, count in categories.items():
        percentage = (count / len(squad)) * 100
        bar = "█" * int(percentage / 5)
        print(f"  {category:8s}: {count:2d} ({percentage:5.1f}%) {bar}")
    
    print("\nPersonality Distribution:")
    for personality, count in sorted(personality_counts.items(), key=lambda x: -x[1]):
        print(f"  {personality:20s}: {count}")
    
    print("\n" + "="*80)
    print("INDIVIDUAL PLAYER PROFILES")
    print("="*80)
    
    for i, player in enumerate(squad, 1):
        print(f"\n{i}. {player.name} ({player.age}) - {player.position}")
        print(f"   Personality: {player.get_personality_description()}")
        print(f"   Key Attributes: Det:{player.determination} Pro:{player.professionalism} " +
              f"Amb:{player.ambition} Tmp:{player.temperament}")

def interactive_personality_creator():
    """Interactive tool to create a player with custom attributes"""
    print("\n" + "="*80)
    print("INTERACTIVE PERSONALITY CREATOR")
    print("="*80)
    print("\nCreate a player and set their mental attributes to see their personality.")
    print("Enter values from 1-20 for each attribute (or press Enter for random).\n")
    
    name = input("Player Name (or Enter for random): ").strip()
    if not name:
        first_names = ["Juan", "Pedro", "Carlos", "Miguel", "Luis"]
        last_names = ["García", "López", "Martínez", "Rodríguez", "Pérez"]
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
    
    age_input = input("Age (18-35, or Enter for random): ").strip()
    age = int(age_input) if age_input.isdigit() and 18 <= int(age_input) <= 35 else random.randint(18, 32)
    
    positions = ["Goalkeeper", "Defender", "Midfielder", "Forward", "Winger"]
    print(f"Positions: {', '.join(positions)}")
    position = input("Position (or Enter for random): ").strip()
    if position not in positions:
        position = random.choice(positions)
    
    is_regen_input = input("Is regen? (y/n, default n): ").strip().lower()
    is_regen = is_regen_input == 'y'
    
    print("\nMental Attributes (1-20):")
    print("Rating scale: Terrible(1-6), Poor(7-9), Average(10-14), Good(15-17), Excellent(18-20)\n")
    
    attributes = {}
    attr_names = ['determination', 'leadership', 'ambition', 'loyalty', 
                  'pressure', 'professionalism', 'sportsmanship', 'temperament']
    
    for attr in attr_names:
        value_input = input(f"  {attr.capitalize():16s}: ").strip()
        if value_input.isdigit() and 1 <= int(value_input) <= 20:
            attributes[attr] = int(value_input)
        else:
            attributes[attr] = max(1, min(20, int(random.gauss(12, 4))))
    
    player = Player(name, age, position)
    player.set_mental_attributes(**attributes)
    player.update_personality(is_regen=is_regen)
    
    print("\n" + "="*80)
    print("PLAYER CREATED!")
    print("="*80)
    print(player.get_mental_attributes_description())
    
    return player

def main():
    """Main menu for personality system demo"""
    while True:
        print("\n" + "="*80)
        print("PLAYER PERSONALITY SYSTEM - DEMO")
        print("="*80)
        print("\nOptions:")
        print("1. Generate random player")
        print("2. Generate full squad (11 players)")
        print("3. Interactive personality creator")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            player = generate_player_with_personality(
                "Random Player", 
                random.randint(18, 32),
                random.choice(["Goalkeeper", "Defender", "Midfielder", "Forward"]),
                random.random() < 0.3
            )
            print(player.get_mental_attributes_description())
            print(player.describe())
        
        elif choice == '2':
            squad = generate_squad(11)
            display_squad_personalities(squad)
        
        elif choice == '3':
            player = interactive_personality_creator()
        
        elif choice == '4':
            print("\nGracias por usar el sistema de personalidades!")
            break
        
        else:
            print("\nOpción inválida. Por favor seleccione 1-4.")

if __name__ == "__main__":
    main()
