"""
Test script for player personality system
"""

from player import Player

def test_personalities():
    """Test different personality types"""
    
    print("\n" + "="*80)
    print("TESTING PLAYER PERSONALITY SYSTEM")
    print("="*80)
    
    # Test 1: Model Citizen
    print("\n### Test 1: Model Citizen ###")
    p1 = Player("John Leader", 25, "Midfielder")
    p1.set_mental_attributes(
        determination=16,
        leadership=17,
        ambition=12,
        loyalty=16,
        pressure=16,
        professionalism=18,
        sportsmanship=16,
        temperament=15
    )
    print(p1.get_mental_attributes_description())
    
    # Test 2: Model Professional
    print("\n### Test 2: Model Professional ###")
    p2 = Player("Sarah Pro", 24, "Defender")
    p2.set_mental_attributes(
        determination=12,
        leadership=10,
        ambition=10,
        loyalty=10,
        pressure=10,
        professionalism=19,
        sportsmanship=10,
        temperament=11
    )
    print(p2.get_mental_attributes_description())
    
    # Test 3: Perfectionist
    print("\n### Test 3: Perfectionist ###")
    p3 = Player("Mike Perfect", 22, "Forward")
    p3.set_mental_attributes(
        determination=17,
        leadership=10,
        ambition=16,
        loyalty=10,
        pressure=10,
        professionalism=16,
        sportsmanship=10,
        temperament=8
    )
    print(p3.get_mental_attributes_description())
    
    # Test 4: Iron Willed
    print("\n### Test 4: Iron Willed ###")
    p4 = Player("Emma Strong", 20, "Goalkeeper")
    p4.set_mental_attributes(
        determination=16,
        leadership=10,
        ambition=10,
        loyalty=10,
        pressure=20,
        professionalism=10,
        sportsmanship=10,
        temperament=10
    )
    print(p4.get_mental_attributes_description())
    
    # Test 5: Driven
    print("\n### Test 5: Driven ###")
    p5 = Player("Carlos Determined", 21, "Midfielder")
    p5.set_mental_attributes(
        determination=19,
        leadership=10,
        ambition=12,
        loyalty=10,
        pressure=10,
        professionalism=10,
        sportsmanship=10,
        temperament=10
    )
    print(p5.get_mental_attributes_description())
    
    # Test 6: Charismatic Leader
    print("\n### Test 6: Charismatic Leader ###")
    p6 = Player("Alex Captain", 26, "Defender")
    p6.set_mental_attributes(
        determination=15,
        leadership=19,
        ambition=12,
        loyalty=14,
        pressure=14,
        professionalism=14,
        sportsmanship=18,
        temperament=19
    )
    print(p6.get_mental_attributes_description())
    
    # Test 7: Ambitious
    print("\n### Test 7: Ambitious ###")
    p7 = Player("Luis Ambicioso", 19, "Forward")
    p7.set_mental_attributes(
        determination=14,
        leadership=10,
        ambition=17,
        loyalty=8,
        pressure=10,
        professionalism=10,
        sportsmanship=10,
        temperament=10
    )
    print(p7.get_mental_attributes_description())
    
    # Test 8: Balanced
    print("\n### Test 8: Balanced ###")
    p8 = Player("Tom Average", 20, "Midfielder")
    p8.set_mental_attributes(
        determination=12,
        leadership=11,
        ambition=13,
        loyalty=12,
        pressure=11,
        professionalism=13,
        sportsmanship=12,
        temperament=11
    )
    print(p8.get_mental_attributes_description())
    
    # Test 9: Light-Hearted
    print("\n### Test 9: Light-Hearted ###")
    p9 = Player("Javier Alegre", 22, "Winger")
    p9.set_mental_attributes(
        determination=14,  # Changed to avoid Resilient
        leadership=10,
        ambition=10,
        loyalty=10,
        pressure=16,
        professionalism=14,
        sportsmanship=17,
        temperament=13
    )
    print(p9.get_mental_attributes_description())
    
    # Test 10: Loyal
    print("\n### Test 10: Loyal ###")
    p10 = Player("David Fiel", 23, "Defender")
    p10.set_mental_attributes(
        determination=14,
        leadership=10,
        ambition=5,
        loyalty=19,
        pressure=10,
        professionalism=10,
        sportsmanship=10,
        temperament=10
    )
    print(p10.get_mental_attributes_description())
    
    # Test 11: Regen with bad personality - Mercenary
    print("\n### Test 11: Mercenary (Regen) ###")
    p11 = Player("Robert Mercenario", 17, "Forward")
    p11.set_mental_attributes(
        determination=14,  # Changed from 15 to avoid Fairly Determined
        leadership=10,
        ambition=17,
        loyalty=4,
        pressure=18,  # Changed to avoid Fairly Determined criteria
        professionalism=10,
        sportsmanship=10,
        temperament=10
    )
    p11.update_personality(is_regen=True)
    print(p11.get_mental_attributes_description())
    
    # Test 12: Regen with worst personality - Temperamental
    print("\n### Test 12: Temperamental (Regen) ###")
    p12 = Player("Victor Explosivo", 18, "Midfielder")
    p12.set_mental_attributes(
        determination=10,
        leadership=10,
        ambition=10,
        loyalty=10,
        pressure=10,
        professionalism=8,
        sportsmanship=10,
        temperament=5
    )
    p12.update_personality(is_regen=True)
    print(p12.get_mental_attributes_description())
    
    # Test full player description
    print("\n\n" + "="*80)
    print("FULL PLAYER PROFILE EXAMPLE")
    print("="*80)
    print(p1.describe())

if __name__ == "__main__":
    test_personalities()
