"""
Documento: Datos Necesarios para una Interfaz Simple del Juego

Este documento proporciona recomendaciones sobre datos adicionales que podrían
mejorarse para una interfaz más completa y funcional.
"""

# ============================================================================
# DATOS ACTUALMENTE IMPLEMENTADOS EN LA CLASE Club
# ============================================================================

DATOS_ACTUALES = {
    # Información Básica
    "name": "Nombre del equipo",
    "objective": "Objetivo de temporada (Campeón/Top3, Libertadores, etc)",
    "formation": "Formación táctica (4-3-3, 4-2-3-1, etc)",
    "tactic": "Estrategia (Presión alta, Posesión, Ataque, Contraataque, Defensivo)",
    "manager": "Nombre del entrenador",
    
    # Reputación y Calidad
    "reputation": "Reputación del equipo (1-100)",
    "training_quality": "Calidad de entrenamientos (1-20)",
    "academy_rating": "Nivel de academia de jóvenes (1-20)",
    
    # Recursos
    "budget": "Presupuesto total para la temporada (en USD)",
    "wage_budget": "Presupuesto para salarios (60% del presupuesto total)",
    "players_count": "Cantidad de jugadores en plantilla",
    
    # Estado Actual
    "player_morale": "Moral de los jugadores (0-100)",
    "fan_satisfaction": "Satisfacción de aficionados (0-100)",
    
    # Estadio
    "stadium_name": "Nombre del estadio",
    "stadium_capacity": "Capacidad del estadio",
    
    # Probabilidades de Partido
    "win_probability": "Probabilidad de ganar (0-100%)",
    "draw_probability": "Probabilidad de empate (0-100%)",
    "goals_scored_probability": "Goles esperados a favor (Expected Goals - xG)",
    "goals_conceded_probability": "Goles esperados en contra (Expected Goals Against - xGA)",
    
    # Estadísticas de Temporada
    "current_season_wins": "Victorias en temporada",
    "current_season_draws": "Empates en temporada",
    "current_season_losses": "Derrotas en temporada",
    "current_season_points": "Puntos acumulados",
    "current_season_goals_for": "Goles a favor en temporada",
    "current_season_goals_against": "Goles en contra en temporada",
}

# ============================================================================
# DATOS ADICIONALES RECOMENDADOS PARA UNA INTERFAZ COMPLETA
# ============================================================================

DATOS_RECOMENDADOS = {
    
    # 1. INFORMACIÓN GEOGRÁFICA
    "city": "Ciudad donde juega el equipo",
    "region": "Región/Provincia",
    "founded_year": "Año de fundación",
    
    # 2. ESTADÍSTICAS DETALLADAS
    "home_record": "Récord en casa (victorias-empates-derrotas)",
    "away_record": "Récord fuera de casa",
    "home_goals_avg": "Goles promedio en casa",
    "away_goals_avg": "Goles promedio fuera de casa",
    "last_5_matches": "Últimos 5 resultados (para tendencia)",
    
    # 3. JUGADORES DESTACADOS
    "top_scorer": {"name": "Nombre", "goals": "Goles"},
    "top_assister": {"name": "Nombre", "assists": "Asistencias"},
    "key_players": ["Lista de 3-5 jugadores clave"],
    "injured_players": ["Jugadores lesionados"],
    "suspended_players": ["Jugadores suspendidos"],
    
    # 4. COMPARATIVAS
    "strength_vs_opponent": "Comparativa de fuerzas (vs oponente específico)",
    "head_to_head": "Historial directo contra otros equipos",
    "league_position": "Posición actual en la liga (1-20)",
    "points_difference": "Diferencia de puntos con líder/perseguidor",
    
    # 5. FINANZAS DETALLADAS
    "total_revenue": "Ingresos totales de la temporada",
    "operating_costs": "Costos operacionales",
    "sponsorship_deals": "Patrocinios activos",
    "transfer_spending": "Dinero gastado en traspasos",
    "player_contracts_expiring": "Contratos que vencen próximamente",
    
    # 6. DINÁMICAS DEL EQUIPO
    "team_cohesion": "Cohesión grupal (1-100)",
    "tactical_flexibility": "Flexibilidad táctica (1-100)",
    "set_pieces_strength": "Fortaleza en jugadas fijas (1-100)",
    "individual_talent": "Talento individual promedio (1-100)",
    
    # 7. FORMA RECIENTE
    "form_rating": "Forma actual del equipo (Buena/Normal/Mala)",
    "confidence_level": "Nivel de confianza (1-100)",
    "recent_injuries": "Lesiones recientes que afecten",
    
    # 8. PREDICCIONES Y ANÁLISIS
    "probability_vs_specific_opponent": "Probabilidad vs equipo X",
    "average_goals_expected": "Promedio de goles esperados por partido",
    "average_goals_conceded": "Promedio de goles recibidos por partido",
    "xg_difference": "Diferencia de xG (goles esperados)",
    
    # 9. RELACIONES
    "relationships_with_agents": "Historial de relaciones con agentes",
    "player_interest_list": "Jugadores que el club quiere fichar",
    "rivalry_teams": "Equipos rivales principales",
    
    # 10. EVENTOS Y NOTICIAS
    "recent_events": "Eventos recientes (cambio de entrenador, etc)",
    "upcoming_important_matches": "Próximos partidos importantes",
    "season_milestone": "Momento en la temporada (Inicio/Mitad/Final)",
}

# ============================================================================
# DATOS MÍNIMOS PARA UNA INTERFAZ SIMPLE (MVP)
# ============================================================================

"""
Para una interfaz simple y funcional, se recomiendan estos datos como mínimo:

1. INFORMACIÓN BÁSICA DEL CLUB:
   - Nombre
   - Entrenador/Manager
   - Objetivo de temporada
   - Formación táctica
   - Reputación (1-100)

2. RECURSOS:
   - Presupuesto
   - Cantidad de jugadores
   - Calidad de entrenamientos

3. ESTADO ACTUAL:
   - Posición en liga
   - Puntos
   - Moral de jugadores
   - Forma reciente

4. PRÓXIMO PARTIDO:
   - Rival
   - Probabilidad de victoria
   - Goles esperados (xG)
   - Goles esperados en contra (xGA)

5. INTERACT ABILITY:
   - Botón para ver detalles completos
   - Botón para contactar entrenador
   - Botón para negociar transferencias

Para una interfaz HTML/Web, esta información se podría mostrar en:
- Una "Tarjeta" o Card con resumen
- Modal/Pop-up para detalles completos
- Tabla comparativa con otros equipos
- Gráficos de probabilidades
"""

# ============================================================================
# SUGERENCIAS DE IMPLEMENTACIÓN
# ============================================================================

MEJORAS_SUGERIDAS = {
    
    "Corto Plazo (Implementar pronto)": [
        "Agregar posición en liga a cada club",
        "Agregar método para generar rivales próximos",
        "Crear comparativas de equipos (Club A vs Club B)",
        "Implementar historial de últimos 5 partidos",
    ],
    
    "Mediano Plazo": [
        "Sistema de mercado de traspasos",
        "Generación dinámica de lesiones/suspensiones",
        "Cambios de entrenador basados en rendimiento",
        "Simulación de partidos",
    ],
    
    "Largo Plazo": [
        "Sistema de ranking ELO para equipos",
        "Predicción de posición final de temporada",
        "Sistema económico completo (ingresos/gastos)",
        "Interfaz gráfica completa",
    ]
}
