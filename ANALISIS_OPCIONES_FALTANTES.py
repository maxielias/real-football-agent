#!/usr/bin/env python3
"""
Análisis de Opciones del Menú - Terminal vs Streamlit
"""

MENU_OPTIONS = {
    "1": {
        "nombre": "Ver Estado del Agente",
        "función": "view_agent_status()",
        "acciones": 0,
        "terminal": "✅ Implementado",
        "streamlit": "❌ NO IMPLEMENTADO",
        "descripción": "Muestra barra de confianza (Players, Clubs, Press), dinero, semana, clientes",
        "prioridad": "ALTA"
    },
    "2": {
        "nombre": "Ver Clientes",
        "función": "view_clients()",
        "acciones": 0,
        "terminal": "✅ Implementado",
        "streamlit": "✅ Implementado (Mis Clientes)",
        "descripción": "Lista de clientes con detalles y estadísticas de temporada",
        "prioridad": "BAJA"
    },
    "3": {
        "nombre": "Leer Reportes de Scout",
        "función": "read_reports()",
        "acciones": 1,
        "terminal": "✅ Implementado",
        "streamlit": "❌ NO IMPLEMENTADO",
        "descripción": "Leer reportes de jugadores disponibles para fichar",
        "prioridad": "MEDIA"
    },
    "4": {
        "nombre": "Fichar Nuevo Jugador",
        "función": "sign_player()",
        "acciones": 1,
        "terminal": "✅ Implementado",
        "streamlit": "✅ Implementado (Buscar Jugadores)",
        "descripción": "Buscar y fichar nuevos clientes",
        "prioridad": "BAJA"
    },
    "5": {
        "nombre": "Interactuar con Cliente",
        "función": "interact_with_client()",
        "acciones": 1,
        "terminal": "✅ Implementado",
        "streamlit": "✅ Implementado (Interacciones)",
        "descripción": "Sesiones de coaching, consejos, apoyo emocional",
        "prioridad": "BAJA"
    },
    "6": {
        "nombre": "Ofrecer Jugador a Clubes",
        "función": "offer_player_to_clubs()",
        "acciones": 1,
        "terminal": "✅ Implementado",
        "streamlit": "✅ Implementado (Contratos → Ofrecer)",
        "descripción": "Ofrecer clientes a clubes interesados manualmente",
        "prioridad": "BAJA"
    },
    "7": {
        "nombre": "Contactar Personal de Club",
        "función": "contact_club_staff()",
        "acciones": 1,
        "terminal": "✅ Implementado",
        "streamlit": "❌ NO IMPLEMENTADO",
        "descripción": "Hablar con gerentes de clubes, mejorar relaciones",
        "prioridad": "MEDIA"
    },
    "8": {
        "nombre": "Ver Tabla de Liga",
        "función": "show_league_table()",
        "acciones": 0,
        "terminal": "✅ Implementado",
        "streamlit": "✅ Implementado (Liga)",
        "descripción": "Tabla de posiciones de la liga nacional",
        "prioridad": "BAJA"
    },
    "9": {
        "nombre": "Playoff Internacional",
        "función": "international_playoff()",
        "acciones": 1,
        "terminal": "✅ Implementado",
        "streamlit": "❌ NO IMPLEMENTADO",
        "descripción": "Torneo internacional si tienes clientes en clubes internacionales",
        "prioridad": "MEDIA"
    },
    "10": {
        "nombre": "Avanzar a Siguiente Semana",
        "función": "advance_week()",
        "acciones": 0,
        "terminal": "✅ Implementado",
        "streamlit": "✅ Implementado (Avanzar Semana)",
        "descripción": "Simular partidos, crecimiento, eventos",
        "prioridad": "BAJA"
    },
    "11": {
        "nombre": "Guardar y Salir",
        "función": "quit_game()",
        "acciones": 0,
        "terminal": "✅ Implementado",
        "streamlit": "❌ NO IMPLEMENTADO (parcial)",
        "descripción": "Guardar juego y salir",
        "prioridad": "BAJA"
    },
    "12": {
        "nombre": "Plantar Rumor en Prensa",
        "función": "plantar_rumor_prensa()",
        "acciones": 1,
        "terminal": "✅ Implementado",
        "streamlit": "✅ Implementado (Acciones → Rumores)",
        "descripción": "Plantar rumores positivos/negativos sobre jugadores",
        "prioridad": "BAJA"
    },
    "13": {
        "nombre": "Hacer Promesa de Campaña",
        "función": "hacer_promesa_campania()",
        "acciones": 1,
        "terminal": "✅ Implementado",
        "streamlit": "✅ Implementado (Acciones → Promesas)",
        "descripción": "Hacer promesas a clientes (club grande, salario, etc)",
        "prioridad": "BAJA"
    },
    "14": {
        "nombre": "Rescindir Contrato",
        "función": "rescindir_contrato()",
        "acciones": 1,
        "terminal": "✅ Implementado",
        "streamlit": "✅ Implementado (Contratos → Rescindir)",
        "descripción": "Terminar contrato de cliente con su club",
        "prioridad": "BAJA"
    },
    "15": {
        "nombre": "Ver Reporte Semanal",
        "función": "ver_reporte_semanal()",
        "acciones": 0,
        "terminal": "✅ Implementado",
        "streamlit": "✅ Implementado (Reportes)",
        "descripción": "Actuaciones, promesas, ofertas de la semana",
        "prioridad": "BAJA"
    }
}

print("=" * 100)
print("ANÁLISIS: OPCIONES DEL MENÚ - TERMINAL vs STREAMLIT")
print("=" * 100)

missing = []
for num, data in MENU_OPTIONS.items():
    if "NO IMPLEMENTADO" in data["streamlit"]:
        missing.append((num, data))

print(f"\n❌ OPCIONES FALTANTES EN STREAMLIT: {len(missing)}\n")
print("-" * 100)

for num, data in missing:
    print(f"\n{num}. {data['nombre'].upper()}")
    print(f"   Función: {data['función']}")
    print(f"   Acciones: {data['acciones']}")
    print(f"   Terminal: {data['terminal']}")
    print(f"   Streamlit: {data['streamlit']}")
    print(f"   Descripción: {data['descripción']}")
    print(f"   Prioridad: {data['prioridad']}")

print("\n" + "=" * 100)
print("RESUMEN")
print("=" * 100)

high_priority = [d for d in missing if d[1]["prioridad"] == "ALTA"]
medium_priority = [d for d in missing if d[1]["prioridad"] == "MEDIA"]

print(f"\n🔴 ALTA PRIORIDAD ({len(high_priority)}):")
for num, data in high_priority:
    print(f"   • {num}. {data['nombre']}")

print(f"\n🟡 MEDIA PRIORIDAD ({len(medium_priority)}):")
for num, data in medium_priority:
    print(f"   • {num}. {data['nombre']}")

print("\n" + "=" * 100)
