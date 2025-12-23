"""
Script de prueba automatizado para validar el sistema de crecimiento y renovación
"""

import sys
import random
from game import FootballAgentGame

# Set seed for reproducibility
random.seed(42)

def automated_test():
    """Run automated test of growth system"""
    print("="*60)
    print("PRUEBA AUTOMATIZADA DEL SISTEMA DE CRECIMIENTO")
    print("="*60)
    
    game = FootballAgentGame()
    
    # Initialize manually without user input
    from agent import Agent
    from game_data import create_initial_players, create_player_reports, get_default_clubs, get_international_clubs
    
    game.agent = Agent("TestAgent")
    game.all_players = create_initial_players()
    game.available_reports = create_player_reports()
    game.clubs = get_default_clubs()
    game.international_clubs = get_international_clubs()
    game.schedule = game._build_season_schedule()
    game.total_weeks = len(game.schedule)
    game._init_league_table()
    game.club_index = {c.name: c for c in game.clubs}
    game._init_club_rosters()
    
    print(f"\nTemporada inicializada: {game.total_weeks} semanas")
    print(f"Clubes con rosters: {len(game.club_rosters)}")
    
    # Show initial roster sample
    print("\n" + "="*60)
    print("MUESTRA DE ROSTER INICIAL (Real Madrid)")
    print("="*60)
    if "Real Madrid" in game.club_rosters:
        for player in game.club_rosters["Real Madrid"][:5]:
            print(f"  {player['name']}: {player['personality']} (Rating: {player['skill_rating']:.1f}, Contrato: {player['contract_weeks_remaining']} semanas)")
    
    # Simulate first 15 weeks (includes preseason + some league matches)
    print("\n" + "="*60)
    print("SIMULANDO PRIMERAS 15 SEMANAS...")
    print("="*60)
    
    for week in range(15):
        current_week_index = game.agent.week - 1
        game._simulate_week_fixtures(current_week_index)
        game._process_weekly_player_growth(current_week_index)
        game.agent.advance_week()
        
        # Only show detailed growth for weeks with league matches
        phase = game.schedule[current_week_index].get('phase', '')
        if not phase.startswith('Liga Nacional'):
            print(f"Semana {week+1}: {phase} (sin crecimiento)")
    
    print("\n" + "="*60)
    print(f"ESTADO DESPUÉS DE 15 SEMANAS")
    print("="*60)
    print(f"Total de eventos de crecimiento registrados: {len(game.growth_log)}")
    
    if game.growth_log:
        print("\nÚltimos 10 eventos de crecimiento:")
        for entry in game.growth_log[-10:]:
            print(f"  Semana {entry['week']}: {entry['player']} ({entry['personality']}) "
                  f"{entry['old_rating']:.1f} → {entry['new_rating']:.1f} (+{entry['improvement']:.1f}) "
                  f"[prob: {entry['growth_prob']:.3f}]")
    
    # Show updated roster sample
    print("\n" + "="*60)
    print("ROSTER ACTUALIZADO (Real Madrid - primeros 5)")
    print("="*60)
    if "Real Madrid" in game.club_rosters:
        for player in game.club_rosters["Real Madrid"][:5]:
            print(f"  {player['name']}: Rating {player['skill_rating']:.1f}, Contrato: {player['contract_weeks_remaining']} semanas")
    
    # Test renewal system with manual contract adjustment
    print("\n" + "="*60)
    print("PRUEBA DE SISTEMA DE RENOVACIÓN")
    print("="*60)
    print("Ajustando contratos a punto de vencer para prueba...")
    
    for club_name, roster in game.club_rosters.items():
        for i, player in enumerate(roster[:3]):  # First 3 players per club
            player['contract_weeks_remaining'] = random.randint(1, 9)
    
    game._process_season_end_renewals()
    
    print("\n" + "="*60)
    print("PRUEBA COMPLETADA")
    print("="*60)

if __name__ == "__main__":
    automated_test()
