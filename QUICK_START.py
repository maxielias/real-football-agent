#!/usr/bin/env python3
"""
GUÍA RÁPIDA DE INICIO - Real Football Agent
============================================

Use este archivo como punto de entrada para entender rápidamente
cómo usar el sistema de clubes.
"""

def main():
    print("""
╔════════════════════════════════════════════════════════════════════════╗
║               REAL FOOTBALL AGENT - GUÍA DE INICIO RÁPIDO              ║
╚════════════════════════════════════════════════════════════════════════╝

1️⃣  VER DEMO INTERACTIVO
   ✓ Ejecuta: python interface_demo.py
   ✓ Mostrará 5 demos diferentes de funcionalidad
   ✓ Tiempo: ~2 minutos

2️⃣  ENTENDER LA ARQUITECTURA
   ✓ Lee: INTERFACE_GUIDE.py
   ✓ Entenderás cómo funciona todo
   ✓ Tiempo: ~5 minutos

3️⃣  USAR EN TU CÓDIGO
   ✓ from game_data import get_default_clubs
   ✓ clubs = get_default_clubs()
   ✓ print(clubs[0].describe())

4️⃣  OPERACIONES COMUNES
   """)
    
    # Importar y mostrar ejemplos
    from game_data import get_default_clubs
    
    clubs = get_default_clubs()
    
    print("   a) Ver lista de clubes:")
    print("   " + "─" * 60)
    sorted_clubs = sorted(clubs, key=lambda c: c.reputation, reverse=True)
    for i, club in enumerate(sorted_clubs[:3], 1):
        print(f"   {i}. {club.name:<35} Rep: {club.reputation}/100")
    print()
    
    print("   b) Ver detalles de un club:")
    print("   " + "─" * 60)
    club = clubs[0]
    print(f"   {club.describe()}")
    print()
    
    print("   c) Probabilidades de partido:")
    print("   " + "─" * 60)
    home = clubs[0]
    away = clubs[1]
    home_prob = home.get_win_probability(away)
    away_prob = away.get_win_probability(home)
    print(f"   {home.name} ({home_prob:.0f}%) vs {away.name} ({away_prob:.0f}%)")
    print()
    
    print("   d) Simular resultado:")
    print("   " + "─" * 60)
    print(f"   home.add_match_result(2, 1, 'home_win')")
    home.add_match_result(2, 1, "home_win")
    print(f"   Resultado guardado: {home.name} 2-1 {away.name}")
    print()

    print("5️⃣  ARCHIVOS IMPORTANTES")
    print("   " + "─" * 60)
    print("   club.py                  ← Clase Club (core)")
    print("   game_data.py             ← Datos de clubes")
    print("   interface_demo.py        ← Demos funcionales")
    print("   INTERFACE_GUIDE.py       ← Documentación completa")
    print()

    print("6️⃣  ESTRUCTURA DE DATOS")
    print("   " + "─" * 60)
    print("   Club attributes:")
    print(f"     • name: {club.name}")
    print(f"     • manager: {club.manager}")
    print(f"     • objective: {club.objective}")
    print(f"     • formation: {club.formation}")
    print(f"     • tactic: {club.tactic}")
    print(f"     • reputation: {club.reputation}")
    print(f"     • budget: ${club.budget:,}")
    print()

    print("7️⃣  MÉTODOS PRINCIPALES")
    print("   " + "─" * 60)
    print("   club.describe()                    → Descripción completa")
    print("   club.get_win_probability(opponent) → % de victoria")
    print("   club.get_goals_scored_probability()→ xG esperados")
    print("   club.get_goals_conceded_probability()→ xGA")
    print("   club.add_match_result(gf, ga, res) → Registrar partido")
    print("   club.compare_with(other_club)      → Comparación")
    print()

    print("8️⃣  PRÓXIMOS PASOS")
    print("   " + "─" * 60)
    print("   □ Ejecuta: python interface_demo.py")
    print("   □ Lee: INTERFACE_GUIDE.py")
    print("   □ Experimenta con game_data.get_default_clubs()")
    print()

    print("═" * 68)
    print("✅ Sistema listo para usar - ¡Comienza con interface_demo.py!")
    print("═" * 68)


if __name__ == "__main__":
    main()
