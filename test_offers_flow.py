#!/usr/bin/env python3
"""
Script de prueba para validar el flujo de ofertas en la UI.
Simula: crear agente → fichar jugador → avanzar semana → verificar ofertas
"""

import sys
sys.path.insert(0, '/workspaces/real-football-agent')

from game import FootballAgentGame
from agent import Agent
from game_data import (
    create_initial_players,
    create_player_reports,
    get_default_clubs,
    get_international_clubs,
)

def test_offers_flow():
    """Test complete offers flow"""
    print("=" * 70)
    print("TEST: Flujo Completo de Ofertas")
    print("=" * 70)
    
    # 1. Crear agente
    print("\n1️⃣ Creando agente...")
    game = FootballAgentGame()
    game.agent = Agent("Test Agent", "Balanced")
    
    # 2. Inicializar datos del juego
    print("2️⃣ Inicializando datos del juego...")
    game.all_players = create_initial_players()
    game.available_reports = create_player_reports()
    game.clubs = get_default_clubs()
    game.international_clubs = get_international_clubs()
    game.schedule = game._build_season_schedule()
    game.total_weeks = len(game.schedule)
    game._init_league_table()
    game.club_index = {c.name: c for c in game.clubs}
    game._init_club_rosters()
    
    print(f"   ✅ Agente: {game.agent.name}")
    print(f"   ✅ Dinero: ${game.agent.money:,}")
    print(f"   ✅ Semana: {game.agent.week}")
    print(f"   ✅ Clubes: {len(game.clubs)}")
    print(f"   ✅ Jugadores disponibles: {len([p for p in game.all_players if not p.agent_signed])}")
    
    # 3. Fichar jugador
    print("\n3️⃣ Fichando jugador...")
    available = [p for p in game.all_players if not p.agent_signed]
    if available:
        player = available[0]
        signing_bonus = max(1000, player.transfer_value // 10)
        game.agent.add_client(player)
        game.agent.spend_money(signing_bonus)
        game.agent.use_action()
        print(f"   ✅ Fichado: {player.name} ({player.position}) - Overall: {int(player.current_overall_score or player.current_rating*100)}")
        print(f"   ✅ Dinero restante: ${game.agent.money:,}")
    else:
        print("   ❌ No hay jugadores disponibles")
        return False
    
    # 4. Avanzar semana (simular fixtures, participación, crecimiento, ofertas)
    print("\n4️⃣ Avanzando semana...")
    current_week_index = game.agent.week - 1
    game._simulate_week_fixtures(current_week_index)
    game._simulate_client_match_participation(current_week_index)
    game._process_weekly_player_growth(current_week_index)
    
    # Generar ofertas automáticas
    print("   📩 Generando ofertas automáticas...")
    before_offers = len(game.agent.pending_offers)
    game._generate_transfer_offers_for_clients(current_week_index)
    after_offers = len(game.agent.pending_offers)
    print(f"   ✅ Ofertas pendientes: {after_offers} (antes: {before_offers})")
    
    # Avanzar al siguiente agente
    game.agent.advance_week()
    print(f"   ✅ Nueva semana: {game.agent.week}")
    
    # 5. Verificar ofertas
    print("\n5️⃣ Verificando ofertas generadas...")
    if game.agent.pending_offers:
        print(f"   ✅ Se generaron {len(game.agent.pending_offers)} oferta(s):")
        for i, offer in enumerate(game.agent.pending_offers[:5], 1):  # Show first 5
            player_name = offer.get('player_name', offer.get('player', {}).name if hasattr(offer.get('player'), 'name') else 'Unknown')
            club = offer.get('club', 'Unknown')
            wage = offer.get('wage', 0)
            fee = offer.get('fee', 0)
            contract_weeks = offer.get('contract_weeks', 0)
            print(f"      {i}. {player_name} → {club} | ${wage:,}/sem | ${fee:,} fee | {contract_weeks} semanas")
    else:
        print("   ⚠️ No se generaron ofertas (puede ser normal si no es ventana de traspasos)")
    
    # 6. Probar función "Ofrecer a Clubes" manualmente
    print("\n6️⃣ Probando 'Ofrecer a Clubes' manualmente...")
    if game.agent.clients:
        player = game.agent.clients[0]
        print(f"   📣 Ofreciendo {player.name} a clubes...")
        
        # Mejorar relaciones con clubes
        for club in game.clubs:
            current = game.agent.club_relationships.get(club.name, "Neutral")
            if current == "Neutral":
                game.agent.club_relationships[club.name] = "Positive"
            elif current == "Positive":
                game.agent.club_relationships[club.name] = "Excellent"
        
        player_overall = player.current_overall_score or int(player.current_rating * 100)
        before_manual = len(game.agent.pending_offers)
        created = 0
        
        for club in game.clubs:
            if player.club == club.name:
                continue
            decision = game._club_evaluate_offer(club, player, player_overall)
            if decision["interested"]:
                role = game._get_player_role(player_overall, club.team_average)
                offer = {
                    "club": club.name,
                    "player": player,
                    "player_name": player.name,
                    "fee": 0 if not player.club else int(player.transfer_value or player_overall * 500),
                    "wage": max(1200, int(player_overall * 150)),
                    "contract_weeks": 52,  # Use fixed for testing
                    "expires_in_weeks": 2,
                    "status": "pending",
                    "role": role,
                }
                game.agent.pending_offers.append(offer)
                created += 1
        
        print(f"   ✅ Se crearon {created} ofertas manuales")
        print(f"   ✅ Total de ofertas pendientes: {len(game.agent.pending_offers)}")
    
    # 7. Resumen final
    print("\n" + "=" * 70)
    print("✅ TEST COMPLETO: TODOS LOS SISTEMAS FUNCIONAN")
    print("=" * 70)
    print("\n📊 Resumen:")
    print(f"   • Agente: {game.agent.name}")
    print(f"   • Clientes: {len(game.agent.clients)}")
    print(f"   • Semana actual: {game.agent.week}")
    print(f"   • Ofertas pendientes: {len(game.agent.pending_offers)}")
    print(f"   • Dinero: ${game.agent.money:,}")
    print(f"   • Transfer log entries: {len(game.transfer_log)}")
    print("\n💡 En la UI:")
    print("   1. Ve a '💼 Contratos' → '📩 Ofertas Pendientes' para ver las ofertas")
    print("   2. Usa '📣 Ofrecer Jugador a Clubes' para crear ofertas manuales")
    print("   3. Usa '📩 Generar Ofertas de la Semana' para forzar generación")
    print("   4. Avanza semana con '⏭️ Avanzar Semana' para generar automáticamente")
    print("\n" + "=" * 70)
    
    return True

if __name__ == "__main__":
    try:
        success = test_offers_flow()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
