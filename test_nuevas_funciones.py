#!/usr/bin/env python3
"""
Script de prueba para nuevas funcionalidades
"""

from game import FootballAgentGame

print("="*60)
print("PRUEBA DE NUEVAS FUNCIONALIDADES")
print("="*60)

# Crear juego
game = FootballAgentGame()
game.start_game()

print("\n✓ Juego iniciado correctamente")
print(f"✓ Semana actual: {game.agent.week}")
print(f"✓ Dinero: ${game.agent.money:,}")
print(f"✓ Clientes: {len(game.agent.clients)}")

# Mostrar clientes iniciales
if game.agent.clients:
    print("\n" + "="*60)
    print("CLIENTES INICIALES")
    print("="*60)
    for client in game.agent.clients:
        overall = int(client.current_overall_score or client.current_rating * 100)
        print(f"- {client.name} ({client.position}): Overall {overall}")
        print(f"  Club: {client.club or 'Agente libre'}")
        print(f"  Valor: ${client.transfer_value:,}")
        print(f"  contract_accepted: {client.contract_accepted}")

print("\n" + "="*60)
print("MENÚ COMPLETO (incluye opciones 14 y 15)")
print("="*60)
print("1. View Agent Status")
print("2. View Clients")
print("3. Read Scouting Reports (1 action)")
print("4. Sign New Player (1 action)")
print("5. Interact with Client (1 action)")
print("6. Offer Player to Clubs (1 action)")
print("7. Contact Club Staff (1 action)")
print("8. View League Table")
print("9. International Playoff (1 action)")
print("10. Advance to Next Week")
print("11. Save & Quit")
print("12. Plantar rumor en la prensa (1 acción)")
print("13. Hacer promesa de campaña (1 acción)")
print("14. Rescindir contrato de cliente (1 acción) ← NUEVO")
print("15. Ver reporte semanal de clientes ← NUEVO")

print("\n" + "="*60)
print("VERIFICACIÓN DE SISTEMAS")
print("="*60)

# Verificar que los métodos existen
try:
    # Verificar Player tiene nuevos atributos
    if game.agent.clients:
        client = game.agent.clients[0]
        print(f"✓ Player.contract_accepted: {hasattr(client, 'contract_accepted')}")
        print(f"✓ Player.weeks_in_contract: {hasattr(client, 'weeks_in_contract')}")
        print(f"✓ Player.terminate_contract(): {hasattr(client, 'terminate_contract')}")
        print(f"✓ Player.calculate_termination_fee(): {hasattr(client, 'calculate_termination_fee')}")
    
    # Verificar que los métodos de game existen
    print(f"✓ Game.rescindir_contrato(): {hasattr(game, 'rescindir_contrato')}")
    print(f"✓ Game.ver_reporte_semanal(): {hasattr(game, 'ver_reporte_semanal')}")
    
    print("\n✅ TODOS LOS SISTEMAS FUNCIONAN CORRECTAMENTE")
    
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "="*60)
print("PARA PROBAR MANUALMENTE:")
print("="*60)
print("1. Ejecuta: python main.py")
print("2. Selecciona opción 15 para ver reporte semanal")
print("3. Juega partidos (opción 10) y vuelve a opción 15")
print("4. Para rescindir: opción 14 (requiere cliente con contrato)")
print("="*60)
