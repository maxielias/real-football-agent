"""
Test script for player rating system based on position weights
"""

from player import Player

def test_rating_system():
    """Test the rating calculation system"""
    
    print("\n" + "="*80)
    print("TESTING PLAYER RATING SYSTEM")
    print("="*80)
    
    # Test 1: Balanced player
    print("\n### Test 1: Balanced Midfielder ###")
    p1 = Player("Juan Balanced", 23, "Midfielder")
    p1.set_technical_attributes(
        defending=12, aerial=10, passing=14, technical=13,
        speed=12, physical=11, shooting=10, mental=13, intelligence=14
    )
    p1.set_mental_attributes(
        determination=14, leadership=12, ambition=13, loyalty=12,
        pressure=13, professionalism=14, sportsmanship=13, temperament=13
    )
    print(p1.get_technical_attributes_description())
    print(p1.describe())
    
    # Test 2: Defensive specialist
    print("\n### Test 2: Elite Center Back ###")
    p2 = Player("Roberto Wall", 27, "Center Back")
    p2.set_technical_attributes(
        defending=19, aerial=18, passing=10, technical=9,
        speed=11, physical=18, shooting=5, mental=16, intelligence=17
    )
    p2.set_mental_attributes(
        determination=17, leadership=18, ambition=14, loyalty=16,
        pressure=17, professionalism=18, sportsmanship=16, temperament=16
    )
    print(p2.get_technical_attributes_description())
    print(p2.describe())
    
    # Test 3: Attacking talent
    print("\n### Test 3: Young Forward Prospect ###")
    p3 = Player("Marco Striker", 19, "Forward")
    p3.set_technical_attributes(
        defending=6, aerial=11, passing=12, technical=16,
        speed=18, physical=14, shooting=17, mental=13, intelligence=14
    )
    p3.set_mental_attributes(
        determination=16, leadership=10, ambition=18, loyalty=12,
        pressure=14, professionalism=15, sportsmanship=13, temperament=12
    )
    print(p3.get_technical_attributes_description())
    print(p3.describe())
    
    # Test 4: Complete midfielder
    print("\n### Test 4: World Class Playmaker ###")
    p4 = Player("Andrea Maestro", 26, "Attacking Midfielder")
    p4.set_technical_attributes(
        defending=10, aerial=8, passing=19, technical=20,
        speed=15, physical=11, shooting=17, mental=18, intelligence=19
    )
    p4.set_mental_attributes(
        determination=18, leadership=16, ambition=17, loyalty=15,
        pressure=19, professionalism=19, sportsmanship=17, temperament=18
    )
    print(p4.get_technical_attributes_description())
    print(p4.describe())
    
    # Test 5: Versatile player - check multiple positions
    print("\n### Test 5: Versatile Wing Back ###")
    p5 = Player("Luis Versatil", 24, "Wing Back")
    p5.set_technical_attributes(
        defending=14, aerial=11, passing=15, technical=16,
        speed=17, physical=15, shooting=12, mental=15, intelligence=16
    )
    p5.set_mental_attributes(
        determination=16, leadership=14, ambition=15, loyalty=14,
        pressure=16, professionalism=16, sportsmanship=15, temperament=15
    )
    print(p5.get_technical_attributes_description())
    print(p5.describe())
    
    print("\n### Test 6: Position Versatility Analysis ###")
    print("\nShowing how the same player rates in different positions:")
    all_positions = ['FB', 'CB', 'WB', 'DM', 'SM', 'CM', 'WF', 'AM', 'FW']
    print(f"\n{p5.name}'s ratings by position:")
    for pos in all_positions:
        rating = p5.position_rating.get(pos, 0)
        print(f"  {pos}: {rating:.2f}")
    
    # Test 7: Comparison of different player types
    print("\n### Test 7: Player Type Comparison ###")
    
    # Create a specialist and a generalist
    specialist = Player("Diego Specialist", 25, "Striker")
    specialist.set_technical_attributes(
        defending=5, aerial=14, passing=10, technical=14,
        speed=19, physical=16, shooting=20, mental=15, intelligence=13
    )
    
    generalist = Player("Carlos Generalist", 25, "Midfielder")
    generalist.set_technical_attributes(
        defending=13, aerial=12, passing=14, technical=14,
        speed=13, physical=13, shooting=12, mental=14, intelligence=15
    )
    
    print(f"\n{specialist.name} (Striker Specialist):")
    print(f"  Current Rating: {specialist.current_rating:.2f}")
    print(f"  Potential Rating: {specialist.potential_rating:.2f}")
    print(f"  Best as FW: {specialist.position_rating['FW']:.2f}")
    print(f"  Worst as CB: {specialist.position_rating['CB']:.2f}")
    
    print(f"\n{generalist.name} (All-rounder):")
    print(f"  Current Rating: {generalist.current_rating:.2f}")
    print(f"  Potential Rating: {generalist.potential_rating:.2f}")
    top_3 = generalist.get_best_positions(3)
    print(f"  Top 3 positions:")
    for pos, rating in top_3:
        print(f"    {pos}: {rating:.2f}")
    
    # Test 8: Maximum possible rating
    print("\n### Test 8: Theoretical Maximum Player ###")
    perfect = Player("Perfect Player", 25, "Attacking Midfielder")
    perfect.set_technical_attributes(
        defending=20, aerial=20, passing=20, technical=20,
        speed=20, physical=20, shooting=20, mental=20, intelligence=20
    )
    perfect.set_mental_attributes(
        determination=20, leadership=20, ambition=20, loyalty=20,
        pressure=20, professionalism=20, sportsmanship=20, temperament=20
    )
    
    print(f"\n{perfect.name} (All 20s):")
    print(f"  Current Rating: {perfect.current_rating:.2f}")
    print(f"  Potential Rating: {perfect.potential_rating:.2f}")
    print(f"\n  Ratings by position:")
    for pos in all_positions:
        rating = perfect.position_rating.get(pos, 0)
        print(f"    {pos}: {rating:.2f}")

def test_goalkeeper():
    """Test goalkeeper ratings"""
    print("\n\n" + "="*80)
    print("GOALKEEPER TEST")
    print("="*80)
    
    gk = Player("Manuel Keeper", 28, "Goalkeeper")
    gk.set_technical_attributes(
        defending=14, aerial=17, passing=11, technical=12,
        speed=10, physical=16, shooting=8, mental=18, intelligence=19
    )
    gk.set_mental_attributes(
        determination=18, leadership=17, ambition=15, loyalty=17,
        pressure=19, professionalism=19, sportsmanship=18, temperament=18
    )
    
    print(gk.get_technical_attributes_description())
    print(gk.describe())

if __name__ == "__main__":
    test_rating_system()
    test_goalkeeper()
    
    print("\n\n" + "="*80)
    print("ALL TESTS COMPLETED")
    print("="*80)
