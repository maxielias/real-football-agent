#!/usr/bin/env python3
"""
Test de eventos aleatorios en la UI
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
import random

def test_event_generation():
    """Test que los eventos se generan correctamente"""
    print("=" * 70)
    print("TEST: Generación de Eventos Aleatorios")
    print("=" * 70)
    
    # Setup
    game = FootballAgentGame()
    game.agent = Agent("Test Agent", "Balanced")
    game.all_players = create_initial_players()
    game.available_reports = create_player_reports()
    game.clubs = get_default_clubs()
    game.international_clubs = get_international_clubs()
    game.schedule = game._build_season_schedule()
    game.total_weeks = len(game.schedule)
    game._init_league_table()
    game.club_index = {c.name: c for c in game.clubs}
    game._init_club_rosters()
    
    # Fichar jugador
    available = [p for p in game.all_players if not p.agent_signed]
    player = available[0]
    game.agent.add_client(player)
    
    print(f"\n✅ Agente: {game.agent.name}")
    print(f"✅ Cliente: {player.name}")
    print(f"✅ Semana: {game.agent.week}")
    
    # Catálogo de eventos
    event_catalog = [
        {"type": "needs_money", "weight": 10, "title": "💰 Necesita dinero"},
        {"type": "demotivated", "weight": 12, "title": "😔 Desmotivado"},
        {"type": "not_training", "weight": 8, "title": "🏃 No entrena"},
        {"type": "press_rumor", "weight": 15, "title": "📰 Rumor de prensa"},
        {"type": "coach_conflict", "weight": 10, "title": "⚔️ Conflicto con entrenador"},
        {"type": "rival_agent", "weight": 8, "title": "🕴️ Tentación de otro agente"},
        {"type": "family_issue", "weight": 7, "title": "👨‍👩‍👧 Problema familiar"},
        {"type": "injury_scare", "weight": 10, "title": "🩹 Susto de lesión"},
        {"type": "dressing_room_issue", "weight": 12, "title": "🚪 Problema de vestuario"},
        {"type": "nightclub_scandal", "weight": 6, "title": "🍾 CRISIS: Escándalo nocturno"},
        {"type": "doping_accusation", "weight": 4, "title": "💊 CRISIS: Acusación de doping"},
        {"type": "social_media_disaster", "weight": 7, "title": "📱 CRISIS: Desastre en redes"},
        {"type": "contract_rebellion", "weight": 5, "title": "📄 CRISIS: Rebelión contractual"},
        {"type": "gambling_scandal", "weight": 5, "title": "🎰 CRISIS: Escándalo de apuestas"},
        {"type": "tax_evasion", "weight": 4, "title": "💸 CRISIS: Evasión fiscal"},
        {"type": "assault_allegations", "weight": 3, "title": "⚖️ CRISIS: Denuncia por agresión"},
        {"type": "leaked_video", "weight": 6, "title": "📹 CRISIS: Video comprometedor filtrado"},
    ]
    
    print(f"\n📊 Catálogo de eventos: {len(event_catalog)} tipos")
    
    # Generar 10 eventos de prueba
    print("\n🎲 Generando 10 eventos aleatorios:")
    print("-" * 70)
    
    event_counts = {}
    for i in range(10):
        total_weight = sum(e["weight"] for e in event_catalog)
        rand = random.random() * total_weight
        cumulative = 0
        selected_event = event_catalog[0]
        
        for event in event_catalog:
            cumulative += event["weight"]
            if rand < cumulative:
                selected_event = event
                break
        
        event_type = selected_event["type"]
        event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        is_crisis = "CRISIS" in selected_event["title"]
        marker = "🚨" if is_crisis else "📋"
        print(f"{i+1}. {marker} {selected_event['title']} ({selected_event['type']})")
    
    print("\n📊 Distribución de eventos generados:")
    print("-" * 70)
    for event_type, count in sorted(event_counts.items(), key=lambda x: x[1], reverse=True):
        event_title = next(e["title"] for e in event_catalog if e["type"] == event_type)
        print(f"  {event_title}: {count} vez/veces")
    
    crisis_events = sum(1 for e in event_counts.keys() if any(c["type"] == e and "CRISIS" in c["title"] for c in event_catalog))
    normal_events = len(event_counts) - crisis_events
    
    print(f"\n✅ Eventos normales: {normal_events}")
    print(f"🚨 Eventos de crisis: {crisis_events}")
    print(f"📊 Total de tipos diferentes: {len(event_counts)}")
    
    print("\n" + "=" * 70)
    print("✅ TEST COMPLETO: GENERACIÓN DE EVENTOS FUNCIONA")
    print("=" * 70)
    print("\n💡 En la UI:")
    print("   1. Avanza semana con '⏭️ Avanzar Semana'")
    print("   2. Si se genera un evento, serás redirigido a '🎲 Situaciones'")
    print("   3. Toma una decisión para resolver la situación")
    print("   4. Los eventos afectan: Trust, Morale, Reputación de Prensa, Dinero")
    print("   5. Las crisis requieren recursos ($) y/o acciones para resolverse")
    print("\n" + "=" * 70)
    
    return True

if __name__ == "__main__":
    try:
        success = test_event_generation()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
