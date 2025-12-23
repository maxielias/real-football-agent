"""
Demo script showing how to use the Club system for a simple interface.
This demonstrates all the methods available for displaying club information.
"""

from game_data import get_default_clubs, create_initial_players
from club import Club
from agent import Agent
from player import Player


def display_main_menu(clubs):
    """Display main menu with all clubs"""
    print("\n" + "="*70)
    print("FOOTBALL AGENT - LEAGUE OVERVIEW".center(70))
    print("="*70)
    
    # Sort by reputation (like league standings)
    sorted_clubs = sorted(clubs, key=lambda c: c.reputation, reverse=True)
    
    print(f"\n{'Pos':<5}{'Club':<30}{'Reputation':<15}{'Budget':<15}")
    print("-"*70)
    
    for i, club in enumerate(sorted_clubs, 1):
        print(f"{i:<5}{club.name:<30}{club.reputation}/100{'':<10}${club.budget:,}")
    
    print("-"*70)


def display_club_details(club):
    """Display detailed information about a specific club"""
    print("\n" + "="*70)
    print(f"{club.name.upper()}".center(70))
    print("="*70)
    
    print(f"\nGENERAL INFORMATION:")
    print(f"  Manager:              {club.manager}")
    print(f"  Objective:            {club.objective}")
    print(f"  Formation:            {club.formation}")
    print(f"  Tactic:               {club.tactic}")
    print(f"  Reputation:           {club.reputation}/100")
    print(f"  Budget:               ${club.budget:,}")
    print(f"  Training Quality:     {club.training_quality}/20")
    
    print(f"\nSEASON STATISTICS:")
    print(f"  Wins:                 {club.current_season_wins}")
    print(f"  Draws:                {club.current_season_draws}")
    print(f"  Losses:               {club.current_season_losses}")
    print(f"  Goals Scored:         {club.current_season_goals_for}")
    print(f"  Goals Conceded:       {club.current_season_goals_against}")
    print(f"  Points:               {club.current_season_points}")
    
    if club.current_season_wins + club.current_season_draws + club.current_season_losses > 0:
        win_rate = club.get_win_rate()
        print(f"  Win Rate:             {win_rate:.1f}%")
    
    print(f"\nFORMATION ANALYSIS:")
    print(f"  {club.get_formation_info()}")
    
    print(f"\nTACTIC INFORMATION:")
    tactic_info = club.get_tactic_strengths()
    print(f"  Strengths: {', '.join(tactic_info['strengths'])}")
    print(f"  Weaknesses: {', '.join(tactic_info['weaknesses'])}")
    
    print(f"\nMATCH PROBABILITIES (vs Average Opponent):")
    print(f"  Win Probability:      {club.get_win_probability():.1f}%")
    print(f"  Draw Probability:     {club.get_draw_probability():.1f}%")
    print(f"  Loss Probability:     {100 - club.get_win_probability() - club.get_draw_probability():.1f}%")
    
    print(f"\nEXPECTED GOALS:")
    print(f"  Goals Scored:         {club.get_goals_scored_probability():.2f}")
    print(f"  Goals Conceded:       {club.get_goals_conceded_probability():.2f}")
    print(f"  Net Goal Difference:  {club.get_goals_scored_probability() - club.get_goals_conceded_probability():.2f}")
    
    print("="*70)


def simulate_match(home_club, away_club):
    """Simulate a match between two clubs"""
    import random
    
    print(f"\n{'MATCH SIMULATION'.center(70)}")
    print(f"\n{home_club.name} vs {away_club.name}")
    print("-"*70)
    
    # Get probabilities
    home_win_prob = home_club.get_win_probability(away_club)
    away_win_prob = away_club.get_win_probability(home_club)
    draw_prob = 100 - home_win_prob - away_win_prob
    
    # Determine result
    result_rand = random.random() * 100
    if result_rand < home_win_prob:
        result = "home_win"
        home_goals = max(1, int(home_club.get_goals_scored_probability()))
        away_goals = int(away_club.get_goals_conceded_probability())
    elif result_rand < home_win_prob + draw_prob:
        result = "draw"
        home_goals = int(home_club.get_goals_scored_probability() * 0.7)
        away_goals = int(away_club.get_goals_scored_probability() * 0.7)
    else:
        result = "away_win"
        home_goals = int(home_club.get_goals_conceded_probability())
        away_goals = max(1, int(away_club.get_goals_scored_probability()))
    
    # Display result
    print(f"\nRESULT: {home_club.name} {home_goals} - {away_goals} {away_club.name}")
    
    if result == "home_win":
        print(f"Winner: {home_club.name}")
    elif result == "away_win":
        print(f"Winner: {away_club.name}")
    else:
        print(f"Result: DRAW")
    
    print(f"\nMATCH PROBABILITIES:")
    print(f"  {home_club.name} Win: {home_win_prob:.1f}%")
    print(f"  Draw: {draw_prob:.1f}%")
    print(f"  {away_club.name} Win: {away_win_prob:.1f}%")
    
    # Update club records (optional - comment out if not tracking)
    home_club.add_match_result(home_goals, away_goals, result)
    away_club.add_match_result(away_goals, home_goals, 
                               "away_win" if result == "home_win" else "home_win" if result == "away_win" else "draw")
    
    print("-"*70)


def compare_clubs(club1, club2):
    """Display comparison between two clubs"""
    print(club1.compare_with(club2))


def main():
    """Main interface demo"""
    clubs = get_default_clubs()
    
    # Demo 1: Display all clubs
    print("\n" + "="*70)
    print("DEMO 1: League Overview")
    print("="*70)
    display_main_menu(clubs)
    
    # Demo 2: Display detailed club information
    print("\n" + "="*70)
    print("DEMO 2: Club Details (Top Club)")
    print("="*70)
    top_club = sorted(clubs, key=lambda c: c.reputation, reverse=True)[0]
    display_club_details(top_club)
    
    # Demo 3: Simulate a match
    print("\n" + "="*70)
    print("DEMO 3: Match Simulation")
    print("="*70)
    club1 = clubs[0]
    club2 = clubs[1]
    simulate_match(club1, club2)
    
    # Demo 4: Compare two clubs
    print("\n" + "="*70)
    print("DEMO 4: Club Comparison")
    print("="*70)
    compare_clubs(club1, club2)
    
    # Demo 5: Show status summaries
    print("\n" + "="*70)
    print("DEMO 5: Quick Status Summary (all clubs)")
    print("="*70)
    for club in sorted(clubs, key=lambda c: c.reputation, reverse=True):
        print(club.get_status_summary())


if __name__ == "__main__":
    main()
