"""
Visualización de la evolución de variables durante la temporada
"""

import random
from game import FootballAgentGame
from agent import Agent
from game_data import create_initial_players, create_player_reports, get_default_clubs, get_international_clubs

random.seed(789)

def visualize_evolution():
    """Visualize variable evolution throughout the season"""
    print("="*70)
    print(" "*20 + "VISUALIZACIÓN DE EVOLUCIÓN")
    print("="*70)
    
    game = FootballAgentGame()
    game.agent = Agent("VisAgent")
    game.all_players = create_initial_players()
    game.available_reports = create_player_reports()
    game.clubs = get_default_clubs()
    game.international_clubs = get_international_clubs()
    game.schedule = game._build_season_schedule()
    game.total_weeks = len(game.schedule)
    game._init_league_table()
    game.club_index = {c.name: c for c in game.clubs}
    game._init_club_rosters()
    
    # Select one club to follow in detail
    club_name = list(game.club_rosters.keys())[0]
    roster = game.club_rosters[club_name]
    
    print(f"\nSiguiendo: {club_name}")
    print(f"Plantilla: {len(roster)} jugadores\n")
    
    # Track metrics over time
    weekly_data = []
    
    for week in range(game.total_weeks):
        current_week_index = game.agent.week - 1
        phase = game.schedule[current_week_index].get('phase', '')
        
        # Calculate team metrics
        avg_rating = sum(p['skill_rating'] for p in roster) / len(roster)
        total_contract_weeks = sum(p['contract_weeks_remaining'] for p in roster)
        
        # Count growth events this week
        before_count = len(game.growth_log)
        
        if phase.startswith('Liga Nacional'):
            game._simulate_week_fixtures(current_week_index)
            game._process_weekly_player_growth(current_week_index)
        else:
            game._simulate_week_fixtures(current_week_index)
        
        after_count = len(game.growth_log)
        growth_this_week = after_count - before_count
        
        weekly_data.append({
            'week': game.agent.week,
            'phase': phase[:20],
            'avg_rating': avg_rating,
            'total_contracts': total_contract_weeks,
            'growth_events': growth_this_week,
        })
        
        game.agent.advance_week()
    
    # Display evolution table
    print("\n" + "="*70)
    print("EVOLUCIÓN SEMANAL DEL EQUIPO")
    print("="*70)
    print(f"{'Sem':<5}{'Fase':<22}{'Rating Prom':<14}{'Contratos':<12}{'Mejoras'}")
    print("-"*70)
    
    for i, data in enumerate(weekly_data):
        if i % 3 == 0:  # Show every 3rd week to keep it readable
            rating_bar = "█" * int(data['avg_rating'] / 10)
            growth_indicator = "✓" * data['growth_events'] if data['growth_events'] > 0 else ""
            print(f"{data['week']:<5}{data['phase']:<22}{data['avg_rating']:<8.1f}{rating_bar:<6}"
                  f"{data['total_contracts']:<12}{growth_indicator}")
    
    # Final comparison
    initial = weekly_data[0]
    final = weekly_data[-1]
    
    print("\n" + "="*70)
    print("COMPARACIÓN INICIO vs FIN DE TEMPORADA")
    print("="*70)
    print(f"Rating promedio: {initial['avg_rating']:.1f} → {final['avg_rating']:.1f} "
          f"({final['avg_rating'] - initial['avg_rating']:+.1f})")
    print(f"Total semanas contrato: {initial['total_contracts']} → {final['total_contracts']} "
          f"({final['total_contracts'] - initial['total_contracts']:+d})")
    print(f"Eventos de crecimiento totales: {sum(d['growth_events'] for d in weekly_data)}")
    
    # Player-by-player breakdown
    print("\n" + "="*70)
    print(f"EVOLUCIÓN INDIVIDUAL - {club_name}")
    print("="*70)
    print(f"{'Jugador':<35}{'Personalidad':<18}{'Rating':<15}{'Cambio'}")
    print("-"*70)
    
    # Get initial ratings from logs or calculate
    for player in roster:
        growth_events = [e for e in game.growth_log if e['player'] == player['name']]
        if growth_events:
            initial_rating = growth_events[0]['old_rating']
            total_growth = sum(e['improvement'] for e in growth_events)
        else:
            # No growth, rating is same
            initial_rating = player['skill_rating']
            total_growth = 0.0
        
        change_indicator = "↑" if total_growth > 0 else "="
        print(f"{player['name'][:34]:<35}{player['personality'][:17]:<18}"
              f"{initial_rating:.1f}→{player['skill_rating']:.1f}{'':<7}"
              f"{change_indicator} {total_growth:+.1f}")
    
    # Renewal projection
    print("\n" + "="*70)
    print("PROYECCIÓN DE RENOVACIONES (jugadores con < 20 semanas)")
    print("="*70)
    
    from personality_impact import renewal_intent_probability
    
    club = game.club_index[club_name]
    club_stats = game.league_table.get(club_name, {})
    club_position = sorted(
        game.league_table.items(),
        key=lambda kv: (kv[1]['points'], kv[1]['gd']),
        reverse=True
    ).index((club_name, club_stats)) + 1 if club_stats else 5
    
    meets_objective = club_position <= 3
    avg_rating = sum(p['skill_rating'] for p in roster) / len(roster)
    
    print(f"Posición en liga: {club_position}")
    print(f"Objetivo cumplido: {'✓' if meets_objective else '✗'}")
    print()
    
    renewal_candidates = [p for p in roster if p['contract_weeks_remaining'] < 20]
    
    if renewal_candidates:
        print(f"{'Jugador':<35}{'Semanas':<10}{'Prob Renueva':<15}{'Estado'}")
        print("-"*70)
        
        for player in sorted(renewal_candidates, key=lambda p: p['contract_weeks_remaining']):
            perf_diff = player['skill_rating'] - avg_rating
            
            prob = renewal_intent_probability(
                player['personality'],
                player['category'],
                cohesion_index=player['cohesion_index'],
                meets_objective=meets_objective,
                performance_diff=perf_diff,
                player_morale=player['morale']
            )
            
            status = "✓ Alta" if prob > 0.15 else "⚠ Media" if prob > 0.08 else "✗ Baja"
            prob_bar = "█" * int(prob * 50)
            
            print(f"{player['name'][:34]:<35}{player['contract_weeks_remaining']:<10}"
                  f"{prob:.3f} {prob_bar:<10}{status}")
    else:
        print("No hay jugadores con contratos próximos a vencer.")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    visualize_evolution()
