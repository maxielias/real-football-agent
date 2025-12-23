"""
SISTEMA DE INTERFAZ - GUÍA DE IMPLEMENTACIÓN
=============================================

Este documento describe cómo usar el sistema de clubes para crear interfaces simples
y qué datos adicionales podrían ser útiles a futuro.

CONTENIDO ACTUAL IMPLEMENTADO
=============================

1. CLASE CLUB (club.py)
   - Nombre, manager, objetivo, formación, táctica
   - Reputación (30-100 basada en objetivo)
   - Presupuesto calculado dinámicamente
   - Estadísticas de temporada (ganadas, empates, derrotas, goles)
   - Calidad de entrenamiento (1-20)
   - Moral del equipo (0-100)
   - Capacidad del estadio

2. CÁLCULOS DE PROBABILIDAD
   - get_win_probability(opponent) → % de ganar
   - get_draw_probability() → % de empate
   - get_goals_scored_probability() → xG (goles esperados a favor)
   - get_goals_conceded_probability() → xGA (goles esperados en contra)

3. MÉTODOS DE INTERFAZ
   - describe() → Resumen del club en texto
   - get_status_summary() → Una línea con estatus
   - get_formation_info() → Análisis de formación
   - get_tactic_strengths() → Fortalezas y debilidades
   - compare_with(otro_club) → Comparación cabeza a cabeza
   - get_probability_report() → Reporte detallado de probabilidades

4. CLUBES POR DEFECTO (10 equipos)
   - Repartidos por objetivo (Campeón/Top3, Libertadores, Sudamericana, Mitad de Tabla, No Descender)
   - Reputación de 30-95
   - Presupuesto de $3M-$10M
   - Diferentes formaciones y tácticas
   - Managers únicos


DATOS ADICIONALES RECOMENDADOS PARA MVP (Mínimo Viable)
=========================================================

NIVEL 1 - IMPRESCINDIBLES (Si se implementa un juego simple)
----------------------------------------------------------
1. Posiciones/Roles disponibles por formación
   - Ej: 4-3-3 = 1 GK, 4 DEF, 3 MID, 3 ATT
   - Usar: POSITION_WEIGHTS ya implementado en Club

2. Clasificación/Puntuación en Liga
   - Usar: get_league_position(all_clubs)
   - Ya tracked: current_season_points

3. Historial de últimos 5 partidos
   - Estructura: [(resultado, goles_a_favor, goles_en_contra, rival), ...]
   - Permite: mostrar forma reciente

4. Lesiones en el equipo
   - Estructura: {nombre_jugador: días_fuera}
   - Afecta: moral del equipo, opciones de alineación

5. Sistema de transferencias
   - Jugadores disponibles, precio mínimo/máximo
   - Usar: presupuesto del club


NIVEL 2 - RECOMENDADO (Para interfaz más completa)
---------------------------------------------------
6. Rivalidades históricas
   - Estructura: {nombre_rival: {'victorias': 5, 'derrotas': 3, 'empates': 2}}
   - Afecta: motivación extra en clásicos

7. Fortaleza de posiciones
   - Ej: defensa 18/20, ataque 14/20
   - Modifica: probabilidades de xG/xGA por zona

8. Jugadores clave/Estrellas
   - Nombre, posición, rating (1-20)
   - Lesión de estrella reduce capacidades del club

9. Contrato de entrenador
   - Años restantes, satisfacción
   - Despido a cambio de dinero

10. Instalaciones del club
    - Academia (ya existe: academy_rating)
    - Centro de entrenamiento (afecta: training_quality)
    - Estadio (ya existe: stadium_name, capacity)


NIVEL 3 - OPCIONAL (Complejidad extra)
---------------------------------------
11. Sistema de Sponsor
    - Nombre, pago mensual, requisitos
    - Ej: sponsor requiere "Top 3" en liga

12. Historial de cambios de manager
    - Quién fue antes, cuándo se fue, razón
    - Afecta: fan_satisfaction

13. Estilo de juego evolucionado
    - No solo "Presión Alta/Posesión", sino más matices
    - Ej: Gegenpressing, Tiki-taka, Catenaccio

14. Efectos de Clima/Ubicación
    - Clima afecta rendimiento (equipos de altura juegan mejor en altura)
    - Ubicación afecta ingresos por entradas

15. Divisiones geográficas/Grupos
    - Estructura de torneo (Grupo A, Grupo B, etc)
    - Clasificación dentro del grupo

16. Sistema de Aficiones
    - Capacidad de estadio × porcentaje de ocupación
    - Ingresos por día de partido
    - Ultras/barrabravas (bans ocasionales)

17. Comparativas con promedio de liga
    - "Club está 5% por encima del promedio"
    - Útil para contexto

18. Predicciones de Analistas
    - Predicción de final de temporada basada en rendimiento
    - Cuota de apuestas (odds)

19. Cumplimiento de Objetivos
    - % de progreso hacia objetivo
    - Fecha de "cálculo" (última jornada posible)

20. Sistema de Confianza con Jugadores
    - Jugadores contentossatisfechos/descontentos
    - Riesgo de salida

21. Dinámicas de Vestuario
    - Liderazgo (capitán), grupos de amigos
    - Conflictos entre jugadores

22. Estadísticas Avanzadas
    - Posesión promedio, pases por minuto, regates, tackles
    - Heatmaps de ataque/defensa

23. Efectos de Fatiga
    - Partidos jugados en semana reduce performance
    - Copa + Liga fatiga extra

24. Budget Carryover
    - Dinero no gastado se acumula
    - Gasto excesivo causa penalización

25. Penalizaciones Disciplinarias
    - Tarjetas rojas/amarillas acumuladas
    - Suspensiones automáticas


RECOMENDACIONES DE ARQUITECTURA
=================================

PARA INTERFAZ SIMPLE (Recomendado para MVP)
--------------------------------------------
1. Mostrar:
   - Lista de clubes ordenados por puntos (Liga)
   - Perfil del club (nombre, manager, objetivo, reputación)
   - Últimas 5 jornadas (resultado, rival, goles)
   - Próximo partido (rival, probabilidades)

2. Funcionalidad:
   - Ver detalles de club → Mostrar formación, táctica, jugadores
   - Simular partido → Usar get_win_probability, get_goals_*_probability
   - Comparar clubs → Usar compare_with()

3. Datos mínimos para esto:
   - Todos ya están implementados ✓

PARA INTERFAZ INTERMEDIA
------------------------
1. Agregar: Historial de últimos 5 partidos
2. Agregar: Lesionados/Disponibles
3. Agregar: Mercado de transferencias simple
4. Agregar: Cambios de manager

PARA INTERFAZ COMPLETA (Simulador tipo FM)
-------------------------------------------
1. Sistema de Ligas/Divisiones
2. Sistema de Tazones/Playoffs
3. Dinámicas de Vestuario
4. Sistema Financiero Completo
5. Predicciones y Análisis


EJEMPLOS DE CÓDIGO
===================

# Obtener todos los clubes
from game_data import get_default_clubs
clubs = get_default_clubs()

# Mostrar tabla de posiciones
sorted_clubs = sorted(clubs, key=lambda c: c.current_season_points, reverse=True)
for i, club in enumerate(sorted_clubs, 1):
    print(f"{i}. {club.name}: {club.current_season_points} pts")

# Ver detalles de un club
club = clubs[0]
print(club.describe())

# Simular un partido
home, away = clubs[0], clubs[1]
home_prob = home.get_win_probability(away)
away_prob = away.get_win_probability(home)
print(f"{home.name} ({home_prob:.1f}%) vs {away.name} ({away_prob:.1f}%)")

# Comparar dos clubs
print(home.compare_with(away))

# Ver probabilidades detalladas
print(home.get_probability_report())

# Obtener resumen rápido
print(home.get_status_summary())

# Agregar resultado de partido
home.add_match_result(2, 1, "home_win")
away.add_match_result(1, 2, "away_win")


FICHERO DE REFERENCIA
=====================

interface_demo.py
- Contiene ejemplos de todas las funciones mencionadas
- Ejecutar: python interface_demo.py

Para ejecutar el demo:
    python /workspaces/real-football-agent/interface_demo.py

Esto mostrará:
    1. League Overview - Tabla de posiciones
    2. Club Details - Información detallada
    3. Match Simulation - Simulación de partido
    4. Club Comparison - Comparación entre dos equipos
    5. Status Summary - Resumen de todos los clubes
"""
