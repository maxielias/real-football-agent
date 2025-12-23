"""
Simulación extendida para ver evolución completa de temporada
"""

import sys
import random
from game import FootballAgentGame

random.seed(123)  # Different seed for variety

def extended_simulation():
    """Run full season simulation"""
    print("="*60)
    print("SIMULACIÓN COMPLETA DE TEMPORADA")
    print("="*60)
    
    game = FootballAgentGame()
    
    # Initialize
    from agent import Agent
    from game_data import create_initial_players, create_player_reports, get_default_clubs, get_international_clubs
    
    game.agent = Agent("SimAgent")
    game.all_players = create_initial_players()
    game.available_reports = create_player_reports()
    game.clubs = get_default_clubs()
    game.international_clubs = get_international_clubs()
    game.schedule = game._build_season_schedule()
    game.total_weeks = len(game.schedule)
    game._init_league_table()
    game.club_index = {c.name: c for c in game.clubs}
    game._init_club_rosters()
    
    print(f"\nTemporada: {game.total_weeks} semanas")
    
    # Select 3 players to track in detail
    tracked_players = []
    for i, club_name in enumerate(list(game.club_rosters.keys())[:3]):
        player = game.club_rosters[club_name][0]
        tracked_players.append({
            'club': club_name,
            'player_ref': player,
            'name': player['name'],
            'initial_rating': player['skill_rating'],
        })
    
    print("\n" + "="*60)
    print("JUGADORES EN SEGUIMIENTO DETALLADO:")
    print("="*60)
    for tp in tracked_players:
        print(f"{tp['name']} ({tp['club']})")
        print(f"  Rating inicial: {tp['initial_rating']:.1f}")
        print(f"  Personalidad: {tp['player_ref']['personality']} ({tp['player_ref']['category']})")
    
    # Simulate full season
    print("\n" + "="*60)
    print("SIMULANDO TEMPORADA COMPLETA...")
    print("="*60)
    
    growth_weeks = []
    
    for week in range(game.total_weeks):
        current_week_index = game.agent.week - 1
        phase = game.schedule[current_week_index].get('phase', '')
        
        # Track only league weeks
        if phase.startswith('Liga Nacional'):
            before_counts = {tp['name']: len([e for e in game.growth_log if e['player'] == tp['name']]) 
                           for tp in tracked_players}
            
            game._simulate_week_fixtures(current_week_index)
            game._process_weekly_player_growth(current_week_index)
            
            after_counts = {tp['name']: len([e for e in game.growth_log if e['player'] == tp['name']]) 
                          for tp in tracked_players}
            
            # Check if tracked players grew
            for tp in tracked_players:
                if after_counts[tp['name']] > before_counts[tp['name']]:
                    growth_weeks.append({
                        'week': game.agent.week,
                        'player': tp['name'],
                        'new_rating': tp['player_ref']['skill_rating'],
                    })
        else:
            game._simulate_week_fixtures(current_week_index)
            # No growth processing for non-league weeks
            
        game.agent.advance_week()
        
        # Progress indicator every 5 weeks
        if (week + 1) % 5 == 0:
            print(f"Semana {week+1}/{game.total_weeks} - {phase[:30]}...")
    
    # Final summary
    print("\n" + "="*60)
    print("EVOLUCIÓN DE JUGADORES SEGUIDOS")
    print("="*60)
    for tp in tracked_players:
        final_rating = tp['player_ref']['skill_rating']
        change = final_rating - tp['initial_rating']
        growth_count = len([e for e in game.growth_log if e['player'] == tp['name']])
        
        print(f"\n{tp['name']} ({tp['player_ref']['personality']})")
        print(f"  Rating: {tp['initial_rating']:.1f} → {final_rating:.1f} ({change:+.1f})")
        print(f"  Mejoras: {growth_count}")
        print(f"  Contrato: {tp['player_ref']['contract_weeks_remaining']} semanas restantes")
        
        if growth_weeks:
            player_weeks = [gw for gw in growth_weeks if gw['player'] == tp['name']]
            if player_weeks:
                print(f"  Semanas de crecimiento: {', '.join(str(gw['week']) for gw in player_weeks)}")
    
    # Overall stats
    print("\n" + "="*60)
    print("ESTADÍSTICAS GLOBALES")
    print("="*60)
    print(f"Total eventos de crecimiento: {len(game.growth_log)}")
    
    if game.growth_log:
        total_improvement = sum(e['improvement'] for e in game.growth_log)
        avg_improvement = total_improvement / len(game.growth_log)
        print(f"Mejora total acumulada: +{total_improvement:.1f}")
        print(f"Mejora promedio por evento: +{avg_improvement:.2f}")
        
        # By club
        by_club = {}
        for entry in game.growth_log:
            club = entry['club']
            if club not in by_club:
                by_club[club] = 0
            by_club[club] += 1
        
        print("\nEventos de crecimiento por club:")
        for club, count in sorted(by_club.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {club}: {count} mejoras")
    
    # Renewal simulation (adjust contracts)
    print("\n" + "="*60)
    print("SIMULACIÓN DE RENOVACIONES")
    print("="*60)
    for club_name, roster in game.club_rosters.items():
        for player in roster[:2]:  # 2 per club
            player['contract_weeks_remaining'] = random.randint(1, 9)
    
    game._process_season_end_renewals()

if __name__ == "__main__":
    extended_simulation()
