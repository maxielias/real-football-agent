"""
Football Agent Simulator - Streamlit Web Interface
Deploy to Streamlit Cloud for free sharing
"""

import streamlit as st
from game import FootballAgentGame
from agent import Agent
from game_data import (
    create_initial_players,
    create_player_reports,
    get_default_clubs,
    get_international_clubs,
)
import time
import random

# Page config
st.set_page_config(
    page_title="Football Agent Simulator",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    .success-box {
        padding: 10px;
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning-box {
        padding: 10px;
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        border-radius: 5px;
        margin: 10px 0;
    }
    .player-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'game' not in st.session_state:
    st.session_state.game = None
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = "🏠 Inicio"
if 'pending_event' not in st.session_state:
    st.session_state.pending_event = None
if 'event_player' not in st.session_state:
    st.session_state.event_player = None

def init_game(agent_name, agent_type_display):
    """Initialize new game (headless, without input prompts)"""
    # Map display type to internal type
    type_map = {
        "THE FATHER": "Father",
        "THE SHARK": "Shark",
        "THE DIPLOMAT": "Diplomat",
        "BALANCED": "Balanced",
    }
    agent_type = type_map.get(agent_type_display, "Balanced")

    # Create game and agent
    game = FootballAgentGame()
    game.agent = Agent(agent_name, agent_type)

    # Initialize core game data (mirrors start_game, but headless)
    game.all_players = create_initial_players()
    game.available_reports = create_player_reports()
    game.clubs = get_default_clubs()
    game.international_clubs = get_international_clubs()
    game.schedule = game._build_season_schedule()
    game.total_weeks = len(game.schedule)
    game._init_league_table()
    game.club_index = {c.name: c for c in game.clubs}
    game._init_club_rosters()

    # Persist game in session
    st.session_state.game = game
    st.session_state.game_started = True

def render_sidebar():
    """Render sidebar with navigation and game info"""
    with st.sidebar:
        st.title("⚽ Football Agent")
        
        if st.session_state.game_started:
            game = st.session_state.game
            
            st.markdown("---")
            st.subheader(f"Agente: {game.agent.name}")
            
            # Key metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric("💰 Dinero", f"${game.agent.money:,}")
                st.metric("📅 Semana", game.agent.week)
            with col2:
                st.metric("👥 Clientes", len(game.agent.clients))
                st.metric("⚡ Acciones", f"{game.agent.actions_remaining}/{game.agent.actions_per_week}")
            
            st.markdown("---")
            
            # Navigation
            st.subheader("📋 Menú")
            pages = [
                "🏠 Inicio",
                "👤 Mis Clientes",
                "📊 Estadísticas",
                "📝 Reportes",
                "💼 Contratos",
                "📰 Ofertas",
                "🔍 Buscar Jugadores",
                "🤝 Interacciones",
                "🎲 Situaciones",
                "📈 Liga",
                "⚙️ Acciones"
            ]
            
            for page in pages:
                if st.button(page, use_container_width=True):
                    st.session_state.selected_page = page
                    st.rerun()
            
            st.markdown("---")
            
            # Quick actions
            if st.button("⏭️ Avanzar Semana", type="primary", use_container_width=True):
                st.session_state.selected_page = "⏭️ Avanzar"
                st.rerun()
            
            if st.button("💾 Guardar", use_container_width=True):
                # TODO: Implement save
                st.success("Juego guardado!")
        else:
            st.info("👈 Inicia un nuevo juego para comenzar")

def render_home():
    """Render home page"""
    st.title("🏠 Panel Principal")
    
    if not st.session_state.game_started:
        render_new_game()
    else:
        game = st.session_state.game
        
        # Header stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💰 Presupuesto", f"${game.agent.money:,}")
        with col2:
            st.metric("👥 Clientes", len(game.agent.clients))
        with col3:
            st.metric("📅 Semana", game.agent.week)
        with col4:
            st.metric("⚡ Acciones", f"{game.agent.actions_remaining}/{game.agent.actions_per_week}")
        
        st.markdown("---")
        
        # Recent activity
        st.subheader("📰 Actividad Reciente")
        
        # Show recent transfers
        if game.transfer_log:
            recent = game.transfer_log[-5:]
            for log in reversed(recent):
                status_emoji = "✅" if log.get("status") == "accepted" else "📩"
                st.markdown(f"""
                <div class="player-card">
                    {status_emoji} <strong>{log.get('player_name', 'Jugador')}</strong> → {log.get('club', 'Club')}<br>
                    💵 ${log.get('wage', 0):,}/sem | 📅 Semana {log.get('week', 0)}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No hay actividad reciente")
        
        # Quick links
        st.markdown("---")
        st.subheader("⚡ Acciones Rápidas")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("👤 Ver Clientes", use_container_width=True):
                st.session_state.selected_page = "👤 Mis Clientes"
                st.rerun()
        with col2:
            if st.button("📰 Ver Ofertas", use_container_width=True):
                st.session_state.selected_page = "📰 Ofertas"
                st.rerun()
        with col3:
            if st.button("🔍 Buscar Jugadores", use_container_width=True):
                st.session_state.selected_page = "🔍 Buscar Jugadores"
                st.rerun()

def render_new_game():
    """Render new game setup"""
    st.title("⚽ Football Agent Simulator")
    
    st.markdown("""
    ### Bienvenido al Simulador de Agente de Fútbol
    
    Eres un agente de fútbol que empieza su carrera en el competitivo mundo de la representación 
    de jugadores. Tu objetivo es descubrir talento, firmar clientes, desarrollar sus carreras, 
    y ganar dinero a través de comisiones.
    """)
    
    st.markdown("---")
    
    with st.form("new_game_form"):
        st.subheader("🎮 Configuración Inicial")
        
        agent_name = st.text_input("Tu nombre:", value="John Doe")
        
        agent_type = st.selectbox(
            "Tipo de Agente:",
            ["BALANCED", "THE FATHER", "THE SHARK", "THE DIPLOMAT"],
            help="""
            - BALANCED: Equilibrado (5 acciones/semana, 5% comisión)
            - THE FATHER: Mentor (6 acciones/semana, 3% comisión, +moral clientes)
            - THE SHARK: Negociador (4 acciones/semana, 8% comisión, +fees)
            - THE DIPLOMAT: Conector (5 acciones/semana, 5% comisión, +relaciones)
            """
        )
        
        submitted = st.form_submit_button("🚀 Iniciar Juego", use_container_width=True)
        
        if submitted:
            init_game(agent_name, agent_type)
            st.success(f"¡Bienvenido, {agent_name}!")
            time.sleep(1)
            st.rerun()

def render_clients():
    """Render clients page"""
    st.title("👤 Mis Clientes")
    
    game = st.session_state.game
    
    if not game.agent.clients:
        st.warning("No tienes clientes todavía. ¡Ve a buscar jugadores!")
        if st.button("🔍 Buscar Jugadores"):
            st.session_state.selected_page = "🔍 Buscar Jugadores"
            st.rerun()
        return
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_position = st.selectbox("Posición:", ["Todos"] + list(set(c.position for c in game.agent.clients)))
    with col2:
        filter_status = st.selectbox("Estado:", ["Todos", "Con club", "Agente libre"])
    with col3:
        sort_by = st.selectbox("Ordenar por:", ["Nombre", "Overall", "Valor", "Edad"])
    
    # Filter clients
    filtered = game.agent.clients
    if filter_position != "Todos":
        filtered = [c for c in filtered if c.position == filter_position]
    if filter_status == "Con club":
        filtered = [c for c in filtered if c.club]
    elif filter_status == "Agente libre":
        filtered = [c for c in filtered if not c.club]
    
    # Sort
    if sort_by == "Overall":
        filtered = sorted(filtered, key=lambda x: x.current_overall_score or x.current_rating*100, reverse=True)
    elif sort_by == "Valor":
        filtered = sorted(filtered, key=lambda x: x.transfer_value, reverse=True)
    elif sort_by == "Edad":
        filtered = sorted(filtered, key=lambda x: x.age)
    
    st.markdown(f"**Total: {len(filtered)} cliente(s)**")
    st.markdown("---")
    
    # Display clients
    for client in filtered:
        overall = int(client.current_overall_score or client.current_rating * 100)
        
        with st.expander(f"⚽ {client.name} ({client.position}) - Overall {overall}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **Información Básica:**
                - 🎂 Edad: {client.age}
                - 📍 Posición: {client.position}
                - 💎 Overall: {overall}
                - 💰 Valor: ${client.transfer_value:,}
                - 🏆 Club: {client.club or 'Agente libre'}
                """)
                
                if client.signed:
                    st.markdown(f"""
                    **Contrato:**
                    - 💵 Salario: ${client.weekly_wage:,}/sem
                    - 📅 Semanas restantes: {client.contract_length}
                    - ✅ Contrato aceptado: {'Sí' if client.contract_accepted else 'No'}
                    """)
            
            with col2:
                st.markdown(f"""
                **Estadísticas Temporada:**
                - ⚽ Goles: {client.season_goals}
                - 🅰️ Asistencias: {client.season_assists}
                - 📊 Partidos: {client.season_appearances}
                - 📈 Promedio: {client.season_goals/max(1, client.season_appearances):.2f} G/partido
                """)
                
                if client.weekly_stats:
                    st.markdown("**Últimos 5 partidos:**")
                    for stat in client.weekly_stats[-5:]:
                        cards = ""
                        if stat.get('yellow_card'): cards += "🟨"
                        if stat.get('red_card'): cards += "🟥"
                        st.caption(f"S{stat['week']}: vs {stat['opponent']} | {stat['goals']}G {stat['assists']}A | ⭐{stat['rating']}/10 {cards}")

def render_stats():
    """Render statistics page"""
    st.title("📊 Estadísticas Detalladas")
    
    game = st.session_state.game
    
    if not game.agent.clients:
        st.warning("No tienes clientes para mostrar estadísticas")
        return
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["🎯 Top Scorers", "🅰️ Top Assists", "⭐ Best Ratings"])
    
    with tab1:
        st.subheader("🎯 Máximos Goleadores")
        scorers = sorted(game.agent.clients, key=lambda x: x.season_goals, reverse=True)
        for i, player in enumerate(scorers[:10], 1):
            if player.season_appearances > 0:
                avg = player.season_goals / player.season_appearances
                st.markdown(f"{i}. **{player.name}** - {player.season_goals} goles en {player.season_appearances} partidos ({avg:.2f} G/partido)")
    
    with tab2:
        st.subheader("🅰️ Máximos Asistidores")
        assisters = sorted(game.agent.clients, key=lambda x: x.season_assists, reverse=True)
        for i, player in enumerate(assisters[:10], 1):
            if player.season_appearances > 0:
                st.markdown(f"{i}. **{player.name}** - {player.season_assists} asistencias en {player.season_appearances} partidos")
    
    with tab3:
        st.subheader("⭐ Mejores Ratings")
        # Calculate average ratings
        players_with_ratings = []
        for player in game.agent.clients:
            if player.weekly_stats:
                avg_rating = sum(s['rating'] for s in player.weekly_stats) / len(player.weekly_stats)
                players_with_ratings.append((player, avg_rating))
        
        players_with_ratings.sort(key=lambda x: x[1], reverse=True)
        for i, (player, rating) in enumerate(players_with_ratings[:10], 1):
            st.markdown(f"{i}. **{player.name}** - {rating:.2f}/10 promedio")

def render_reports():
    """Render weekly reports"""
    st.title("📝 Reporte Semanal")
    
    game = st.session_state.game
    
    st.subheader(f"Semana {game.agent.week}")
    
    # Performance this week
    st.markdown("### ⚽ Actuaciones Esta Semana")
    
    performances = []
    for client in game.agent.clients:
        if client.weekly_stats and len(client.weekly_stats) > 0:
            last = client.weekly_stats[-1]
            if last['week'] == game.agent.week - 1:
                performances.append((client, last))
    
    if performances:
        for client, stats in performances:
            overall = int(client.current_overall_score or client.current_rating * 100)
            
            if client.club and client.club in game.club_index:
                role = game._get_player_role(overall, game.club_index[client.club].team_average)
            else:
                role = "Desconocido"
            
            st.markdown(f"""
            <div class="player-card">
                <strong>{client.name}</strong> ({client.position})<br>
                Club: {client.club} | Rol: {role}<br>
                vs {stats['opponent']}: {stats['goals']}G {stats['assists']}A | Rating: {stats['rating']}/10
                {'🟨' if stats.get('yellow_card') else ''} {'🟥' if stats.get('red_card') else ''}<br>
                Temporada: {client.season_goals}G {client.season_assists}A en {client.season_appearances} partidos
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Ningún cliente jugó esta semana")
    
    # Active promises
    st.markdown("### 📝 Promesas Activas")
    pending = [p for p in game.active_promises if not p["cumplida"] and not p["fallida"]]
    
    if pending:
        for promise in pending:
            remaining = promise["plazo"] - (game.agent.week - promise["semana_hecha"])
            promise_type = {
                "club_grande": "Club grande",
                "mejorar_salario": "Mejorar salario",
                "titularidad": "Titularidad",
                "seleccion_nacional": "Selección nacional"
            }.get(promise["tipo"], promise["tipo"])
            
            st.info(f"**{promise['nombre']}**: {promise_type} ({remaining} semanas restantes)")
    else:
        st.success("No hay promesas pendientes")
    
    # Offers received
    st.markdown("### 📩 Ofertas Recibidas Esta Semana")
    recent_offers = [o for o in game.transfer_log if o.get("week") == game.agent.week and o.get("status") in ["created", "created_free_agent"]]
    
    if recent_offers:
        for offer in recent_offers:
            st.markdown(f"- **{offer['player_name']}** → {offer['club']}: ${offer['wage']:,}/sem | {offer['contract_weeks']} semanas")
    else:
        st.info("No se recibieron ofertas esta semana")

def render_contracts():
    """Render contracts management"""
    st.title("💼 Gestión de Contratos")
    
    game = st.session_state.game
    
    # Pending offers
    st.subheader("📩 Ofertas Pendientes")
    
    if game.agent.pending_offers:
        for offer in game.agent.pending_offers:
            player = offer["player"]
            
            with st.expander(f"⚽ {player.name} ← {offer['club']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    **Oferta:**
                    - 🏆 Club: {offer['club']}
                    - 💵 Salario: ${offer['wage']:,}/sem
                    - 📅 Contrato: {offer['contract_weeks']} semanas
                    - 💰 Fee transfer: ${offer['fee']:,}
                    - ⏰ Expira en: {offer.get('expires_in_weeks', 2)} semanas
                    """)
                
                with col2:
                    st.markdown(f"""
                    **Comisión estimada:**
                    - 💎 ${int(offer['fee'] * 0.05 + offer['wage'] * 2 * 0.05):,}
                    """)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✅ Aceptar", key=f"accept_{player.name}_{offer['club']}"):
                        game._accept_transfer_offer(offer)
                        st.success(f"¡{player.name} firmó con {offer['club']}!")
                        time.sleep(1)
                        st.rerun()
                
                with col2:
                    if st.button(f"❌ Rechazar", key=f"reject_{player.name}_{offer['club']}"):
                        game.agent.pending_offers.remove(offer)
                        st.warning("Oferta rechazada")
                        time.sleep(1)
                        st.rerun()
    else:
        st.info("No hay ofertas pendientes")
    
    # Generate offers manually
    if st.button("📩 Generar Ofertas de la Semana"):
        game._generate_transfer_offers_for_clients(game.agent.week - 1)
        st.success("Ofertas generadas")
        time.sleep(1)
        st.rerun()
    
    st.markdown("---")
    
    # Proactively offer player to clubs
    st.subheader("📣 Ofrecer Jugador a Clubes")
    if game.agent.clients:
        player_choice = st.selectbox("Seleccionar cliente:", [""] + [c.name for c in game.agent.clients], key="offer_client")
        if player_choice:
            player = next(c for c in game.agent.clients if c.name == player_choice)
            if st.button("📣 Ofrecer a Clubes", type="primary"):
                # Improve relationships with all clubs (as in CLI)
                for club in game.clubs:
                    current = game.agent.club_relationships.get(club.name, "Neutral")
                    if current == "Neutral":
                        game.agent.club_relationships[club.name] = "Positive"
                    elif current == "Positive":
                        game.agent.club_relationships[club.name] = "Excellent"
                
                player_overall = player.current_overall_score or int(player.current_rating * 100)
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
                            "contract_weeks": random.randint(52, 156),
                            "expires_in_weeks": 2,
                            "status": "pending",
                            "role": role,
                        }
                        game.agent.pending_offers.append(offer)
                        game.transfer_log.append({**offer, "status": "created_player_offer", "week": game.agent.week})
                        created += 1
                if created:
                    st.success(f"Se crearon {created} ofertas para {player.name}")
                else:
                    st.warning("Ningún club mostró interés")
                time.sleep(1)
                st.rerun()
    
    st.markdown("---")
    
    # Contract termination
    st.subheader("✂️ Rescindir Contrato")
    
    signed_clients = [c for c in game.agent.clients if c.signed and c.club]
    
    if signed_clients:
        client_choice = st.selectbox(
            "Seleccionar cliente:",
            [""] + [f"{c.name} ({c.club})" for c in signed_clients]
        )
        
        if client_choice:
            idx = [f"{c.name} ({c.club})" for c in signed_clients].index(client_choice)
            client = signed_clients[idx]
            fee = client.calculate_termination_fee()
            
            st.warning(f"""
            **Fee de rescisión:** ${fee:,}
            
            - Semanas restantes: {client.contract_length}
            - Salario actual: ${client.weekly_wage:,}/sem
            - Fondos disponibles: ${game.agent.money:,}
            """)
            
            if game.agent.money >= fee:
                if st.button("✂️ Rescindir Contrato", type="primary"):
                    if game.agent.spend_money(fee):
                        client.terminate_contract()
                        st.success(f"Contrato de {client.name} rescindido!")
                        time.sleep(1)
                        st.rerun()
            else:
                st.error(f"Fondos insuficientes. Necesitas ${fee - game.agent.money:,} más")
    else:
        st.info("No tienes clientes con contrato para rescindir")

def render_offers():
    """Render offers page"""
    st.title("📰 Ofertas y Transferencias")
    
    render_contracts()

def render_search_players():
    """Render player search/signing"""
    st.title("🔍 Buscar y Fichar Jugadores")
    
    game = st.session_state.game
    
    if game.agent.actions_remaining <= 0:
        st.error("No te quedan acciones esta semana!")
        return
    
    available = [p for p in game.all_players if not p.agent_signed]
    
    if not available:
        st.warning("No hay jugadores disponibles en este momento")
        return
    
    st.markdown(f"**Jugadores disponibles: {len(available)}**")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_pos = st.selectbox("Posición:", ["Todos"] + list(set(p.position for p in available)))
    with col2:
        filter_potential = st.selectbox("Potencial:", ["Todos", "Elite", "World Class", "High", "Medium"])
    with col3:
        sort_by = st.selectbox("Ordenar por:", ["Overall", "Potencial", "Edad", "Valor"])
    
    # Filter
    filtered = available
    if filter_pos != "Todos":
        filtered = [p for p in filtered if p.position == filter_pos]
    if filter_potential != "Todos":
        filtered = [p for p in filtered if p.potential_level == filter_potential]
    
    # Sort
    if sort_by == "Overall":
        filtered = sorted(filtered, key=lambda x: x.current_overall_score or x.current_rating*100, reverse=True)
    elif sort_by == "Potencial":
        filtered = sorted(filtered, key=lambda x: x.potential_overall_score or x.potential_rating*100, reverse=True)
    elif sort_by == "Edad":
        filtered = sorted(filtered, key=lambda x: x.age)
    elif sort_by == "Valor":
        filtered = sorted(filtered, key=lambda x: x.transfer_value, reverse=True)
    
    st.markdown("---")
    
    # Display players
    for player in filtered[:20]:  # Show first 20
        overall = int(player.current_overall_score or player.current_rating * 100)
        potential = int(player.potential_overall_score or player.potential_rating * 100)
        signing_bonus = max(1000, player.transfer_value // 10)
        
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            st.markdown(f"""
            **⚽ {player.name}** ({player.age} años)
            
            📍 {player.position} | 💎 Overall: {overall} | 🌟 Potencial: {potential} ({player.potential_level})
            """)
        
        with col2:
            st.markdown(f"""
            💰 Valor: ${player.transfer_value:,}
            
            💵 Bonus firma: ${signing_bonus:,}
            """)
        
        with col3:
            if st.button("✍️ Fichar", key=f"sign_{player.name}"):
                if game.agent.spend_money(signing_bonus):
                    game.agent.add_client(player)
                    game.agent.use_action()
                    st.success(f"¡{player.name} es ahora tu cliente!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Fondos insuficientes!")
        
        st.markdown("---")

def render_interactions():
    """Render client interactions"""
    st.title("🤝 Interacciones con Clientes")
    
    game = st.session_state.game
    
    if not game.agent.clients:
        st.warning("No tienes clientes para interactuar")
        return
    
    if game.agent.actions_remaining <= 0:
        st.error("No te quedan acciones esta semana!")
        return
    
    # Select client
    client_choice = st.selectbox(
        "Seleccionar cliente:",
        [""] + [c.name for c in game.agent.clients]
    )
    
    if client_choice:
        client = next(c for c in game.agent.clients if c.name == client_choice)
        
        st.markdown(f"### Interactuando con {client.name}")
        
        overall = int(client.current_overall_score or client.current_rating * 100)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Overall", overall)
            st.metric("Moral", client.morale)
        with col2:
            st.metric("Confianza", client.trust_in_agent)
            st.metric("Club", client.club or "Agente libre")
        
        st.markdown("---")
        
        # Interaction types
        st.subheader("Tipo de interacción:")
        
        interaction = st.radio(
            "Selecciona:",
            [
                "Asesoramiento de carrera",
                "Consejo de entrenamiento",
                "Discusión contractual",
                "Apoyo personal",
                "Planificación de carrera"
            ]
        )
        
        if st.button("💬 Interactuar", type="primary"):
            interaction_types = {
                "Asesoramiento de carrera": "counsel",
                "Consejo de entrenamiento": "training_advice",
                "Discusión contractual": "contract_negotiation",
                "Apoyo personal": "personal_support",
                "Planificación de carrera": "career_planning"
            }
            
            response = client.interact(interaction_types[interaction])
            game.agent.use_action()
            
            # Improve relationship
            if client.trust_in_agent == "Neutral":
                client.trust_in_agent = "Good"
            elif client.trust_in_agent == "Low":
                client.trust_in_agent = "Neutral"
            
            if client.morale in ["Unhappy", "Content"]:
                client.morale = "Happy"
            
            st.success(response)
            time.sleep(2)
            st.rerun()

def render_league():
    """Render league table"""
    st.title("📈 Tabla de Posiciones")
    
    game = st.session_state.game
    
    if not game.league_table:
        st.info("La liga aún no ha comenzado")
        return
    
    # Sort by points, then goal difference
    sorted_table = sorted(
        game.league_table.items(),
        key=lambda x: (x[1].get('points', 0), x[1].get('gf', 0) - x[1].get('ga', 0)),
        reverse=True
    )
    
    # Display table
    for i, (team, stats) in enumerate(sorted_table, 1):
        col1, col2, col3, col4, col5, col6 = st.columns([1, 4, 2, 2, 2, 2])
        
        with col1:
            st.markdown(f"**{i}**")
        with col2:
            st.markdown(f"**{team}**")
        with col3:
            st.markdown(f"PJ: {stats.get('played', 0)}")
        with col4:
            st.markdown(f"Pts: {stats.get('points', 0)}")
        with col5:
            st.markdown(f"GF: {stats.get('gf', 0)}")
        with col6:
            st.markdown(f"GA: {stats.get('ga', 0)}")
        
        st.markdown("---")

def render_actions():
    """Render special actions page"""
    st.title("⚙️ Acciones Especiales")
    
    game = st.session_state.game
    
    tab1, tab2 = st.tabs(["📰 Rumores", "🤝 Promesas"])
    
    with tab1:
        st.subheader("📰 Plantar Rumor en la Prensa")
        
        if game.agent.actions_remaining <= 0:
            st.error("No te quedan acciones!")
        elif not game.agent.clients:
            st.warning("Necesitas clientes para plantar rumores")
        else:
            client_choice = st.selectbox("Cliente objetivo:", [c.name for c in game.agent.clients])
            
            if client_choice:
                client = next(c for c in game.agent.clients if c.name == client_choice)
                
                rumor_type = st.radio(
                    "Tipo de rumor:",
                    ["Positivo (aumenta valor)", "Negativo (afecta rival)"]
                )
                
                cost = 5000
                st.warning(f"Costo: ${cost:,} | Riesgo de descubrimiento: 20%")
                
                if st.button("📰 Plantar Rumor"):
                    if game.agent.money >= cost:
                        game.agent.spend_money(cost)
                        game.agent.use_action()
                        
                        # Implementation would go here
                        st.success(f"Rumor plantado sobre {client.name}!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Fondos insuficientes!")
    
    with tab2:
        st.subheader("🤝 Hacer Promesa de Campaña")
        
        if game.agent.actions_remaining <= 0:
            st.error("No te quedan acciones!")
        elif not game.agent.clients:
            st.warning("Necesitas clientes para hacer promesas")
        else:
            client_choice = st.selectbox("Cliente objetivo:", [c.name for c in game.agent.clients], key="promise_client")
            
            if client_choice:
                client = next(c for c in game.agent.clients if c.name == client_choice)
                
                promise_type = st.selectbox(
                    "Tipo de promesa:",
                    [
                        "Conseguirle un club grande",
                        "Mejorar su salario en 10 semanas",
                        "Conseguirle titularidad",
                        "Prometerle selección nacional"
                    ]
                )
                
                if st.button("🤝 Hacer Promesa"):
                    game.agent.use_action()
                    
                    tipo_map = {
                        "Conseguirle un club grande": "club_grande",
                        "Mejorar su salario en 10 semanas": "mejorar_salario",
                        "Conseguirle titularidad": "titularidad",
                        "Prometerle selección nacional": "seleccion_nacional"
                    }
                    
                    plazo = 10 if "salario" in promise_type else 20
                    
                    game.active_promises.append({
                        "jugador": client,
                        "nombre": client.name,
                        "tipo": tipo_map[promise_type],
                        "semana_hecha": game.agent.week,
                        "plazo": plazo,
                        "cumplida": False,
                        "fallida": False
                    })
                    
                    st.success(f"Promesa registrada: {promise_type} a {client.name}")
                    time.sleep(1)
                    st.rerun()

def render_situations():
    """Render random situations/events page"""
    st.title("🎲 Situación Semanal")
    
    game = st.session_state.game
    
    if not st.session_state.pending_event or not st.session_state.event_player:
        st.info("No hay situaciones pendientes esta semana")
        if st.button("🔙 Volver"):
            st.session_state.selected_page = "🏠 Inicio"
            st.rerun()
        return
    
    event = st.session_state.pending_event
    player = st.session_state.event_player
    
    # Display event header
    st.markdown(f"""
    <div class="player-card">
        <h3>{event['title']}</h3>
        <p><strong>Jugador:</strong> {player.name} ({player.position})</p>
        <p><strong>Club:</strong> {player.club or 'Libre'}</p>
        <p><strong>Morale:</strong> {player.morale} | <strong>Trust:</strong> {player.trust_in_agent}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    event_type = event["type"]
    
    # Handle each event type
    if event_type == "needs_money":
        amount = random.randint(2000, 8000)
        st.markdown(f"💰 **{player.name} necesita un adelanto urgente de ${amount:,}.**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💵 Darle adelanto personal", use_container_width=True):
                if game.agent.spend_money(amount):
                    player.trust_in_agent = "Good" if player.trust_in_agent == "Neutral" else "Excellent"
                    st.success(f"✓ {player.name} está muy agradecido. Trust mejorado.")
                else:
                    st.error("✗ No tienes suficiente dinero.")
                    player.trust_in_agent = "Low"
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col2:
            if st.button("🤝 Negociar con club", use_container_width=True):
                if player.club:
                    st.success(f"✓ Negociaste un bonus con {player.club}. {player.name} está satisfecho.")
                else:
                    st.warning(f"✗ {player.name} está libre, no hay club.")
                    player.morale = "Unhappy"
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col3:
            if st.button("❌ Negarle adelanto", use_container_width=True):
                player.trust_in_agent = "Low"
                player.morale = "Unhappy"
                st.warning(f"✗ {player.name} está decepcionado.")
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
    
    elif event_type == "demotivated":
        st.markdown(f"😔 **{player.name} se siente desmotivado y sin objetivos claros.**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💬 Sesión motivacional intensa", use_container_width=True):
                player.morale = "Happy"
                player.trust_in_agent = "Good" if player.trust_in_agent != "Low" else "Neutral"
                st.success(f"✓ {player.name} recuperó su motivación.")
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col2:
            if st.button("🏖️ Darle tiempo libre", use_container_width=True):
                player.morale = "Content"
                st.info(f"↷ {player.name} tomó un descanso.")
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col3:
            if st.button("💪 Presionarlo a entrenar", use_container_width=True):
                player.morale = "Unhappy"
                player.trust_in_agent = "Low"
                st.warning(f"✗ {player.name} se siente presionado.")
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
    
    elif event_type == "press_rumor":
        rumor_positive = random.random() > 0.5
        if rumor_positive:
            st.markdown(f"📰 **La prensa habla positivamente de {player.name}.**")
            player.morale = "Happy"
            st.success("✓ Morale mejorado.")
            if st.button("Continuar"):
                st.session_state.pending_event = None
                st.rerun()
        else:
            st.markdown(f"📰 **La prensa publicó rumores negativos sobre {player.name}.**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📄 Comunicado oficial", use_container_width=True):
                    player.morale = "Content"
                    st.success("✓ El comunicado calmó la situación.")
                    st.session_state.pending_event = None
                    time.sleep(2)
                    st.rerun()
            
            with col2:
                if st.button("🤐 Ignorar rumor", use_container_width=True):
                    player.morale = "Unhappy"
                    st.warning("↷ El rumor persiste.")
                    st.session_state.pending_event = None
                    time.sleep(2)
                    st.rerun()
            
            with col3:
                if st.button("⚔️ Confrontar periodista", use_container_width=True):
                    player.morale = "Content"
                    player.trust_in_agent = "Good"
                    st.success(f"✓ {player.name} apreció tu defensa.")
                    st.session_state.pending_event = None
                    time.sleep(2)
                    st.rerun()
    
    elif event_type == "nightclub_scandal":
        st.markdown(f"""
        🚨 **CRISIS: {player.name} fue visto en un boliche a las 4 AM antes de un partido importante.**
        
        La prensa ya tiene fotos. El club está furioso.
        
        💡 Tu energía: {game.agent.actions_remaining}/{game.agent.actions_per_week}
        """)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🤫 Encubrir ($8,000)", use_container_width=True):
                cost = 8000
                if game.agent.spend_money(cost):
                    game.agent.change_press_reputation(-15)
                    st.success(f"✓ Pagaste ${cost:,} para encubrir. No salió en medios.")
                    st.warning(f"⚠️ Prensa: {game.agent.press_reputation}/100")
                else:
                    st.error("✗ No tienes dinero. Escándalo explotó.")
                    player.morale = "Unhappy"
                    game.agent.change_press_reputation(-25)
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col2:
            if st.button("😠 Regañarlo públicamente", use_container_width=True):
                player.morale = "Unhappy"
                player.trust_in_agent = "Low"
                st.success("✓ El club apreció tu postura firme.")
                st.warning(f"✗ {player.name} está molesto contigo.")
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col3:
            if st.button("🛡️ Decir que tú lo manejas", use_container_width=True):
                player.trust_in_agent = "Good"
                game.agent.change_press_reputation(-10)
                st.success(f"✓ {player.name} valoró tu apoyo.")
                st.warning(f"⚠️ Prensa: {game.agent.press_reputation}/100")
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
    
    elif event_type == "social_media_disaster":
        st.markdown(f"""
        🚨 **CRISIS: {player.name} publicó un tweet polémico insultando al entrenador.**
        
        Está viralizándose. El club exige acción inmediata.
        
        💡 Tu energía: {game.agent.actions_remaining}/{game.agent.actions_per_week}
        """)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🗑️ Borrar y disculparse", use_container_width=True):
                player.morale = "Content"
                game.agent.change_press_reputation(+10)
                st.success("✓ Tweet borrado. Crisis controlada.")
                st.info(f"Prensa: {game.agent.press_reputation}/100")
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col2:
            if st.button("🛡️ Defenderlo", use_container_width=True):
                player.trust_in_agent = "Excellent"
                game.agent.change_press_reputation(-15)
                st.success(f"✓ {player.name} agradece tu lealtad.")
                st.warning(f"⚠️ Prensa: {game.agent.press_reputation}/100")
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col3:
            if st.button("🤖 Fingir hackeo ($5,000)", use_container_width=True):
                cost = 5000
                if game.agent.spend_money(cost):
                    st.success(f"✓ Historia creíble. Crisis neutralizada (${cost:,}).")
                else:
                    st.error("✗ No tienes dinero. Desastre total.")
                    player.morale = "Unhappy"
                    game.agent.change_press_reputation(-20)
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
    
    elif event_type == "gambling_scandal":
        st.markdown(f"""
        🚨 **CRISIS: {player.name} fue fotografiado en un casino apostando grandes sumas.**
        
        El club está preocupado por adicción al juego. La prensa pide explicaciones.
        
        💡 Tu energía: {game.agent.actions_remaining}/{game.agent.actions_per_week}
        """)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🏥 Clínica ($15,000 + 2 acc)", use_container_width=True):
                cost = 15000
                if game.agent.spend_money(cost) and game.agent.actions_remaining >= 2:
                    game.agent.actions_remaining -= 2
                    player.trust_in_agent = "Excellent"
                    game.agent.change_press_reputation(+15)
                    st.success(f"✓ Tratamiento iniciado (${cost:,}, -2 acc). Prensa elogia.")
                else:
                    st.error("✗ Recursos insuficientes. Escándalo explota.")
                    player.morale = "Unhappy"
                    game.agent.change_press_reputation(-25)
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col2:
            if st.button("⚖️ Negar ($8,000 + 1 acc)", use_container_width=True):
                cost = 8000
                if game.agent.spend_money(cost) and game.agent.actions_remaining >= 1:
                    game.agent.actions_remaining -= 1
                    game.agent.change_press_reputation(-20)
                    st.warning(f"✓ Demandas presentadas (${cost:,}, -1 acc).")
                else:
                    st.error("✗ Recursos insuficientes.")
                    game.agent.change_press_reputation(-30)
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col3:
            if st.button("🤝 Admitir y supervisar", use_container_width=True):
                player.trust_in_agent = "Good"
                player.morale = "Content"
                st.info("↷ Crisis parcialmente controlada.")
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
    
    elif event_type == "coach_conflict":
        if not player.club:
            st.warning(f"✗ {player.name} está libre, no hay entrenador.")
            if st.button("Continuar"):
                st.session_state.pending_event = None
                st.rerun()
        else:
            st.markdown(f"⚔️ **{player.name} tuvo un conflicto con el entrenador de {player.club}.**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🤝 Mediar entre ambos", use_container_width=True):
                    player.morale = "Content"
                    player.trust_in_agent = "Good"
                    st.success("✓ Mediaste exitosamente. Relación restaurada.")
                    st.session_state.pending_event = None
                    time.sleep(2)
                    st.rerun()
            
            with col2:
                if st.button("😔 Exigir disculpa", use_container_width=True):
                    player.trust_in_agent = "Low"
                    st.warning(f"↷ {player.name} se disculpó pero está resentido.")
                    st.session_state.pending_event = None
                    time.sleep(2)
                    st.rerun()
            
            with col3:
                if st.button("🚪 Buscar transferencia", use_container_width=True):
                    player.morale = "Unhappy"
                    st.warning(f"⚠️ {player.name} quiere irse. Busca ofertas.")
                    st.session_state.pending_event = None
                    time.sleep(2)
                    st.rerun()
    
    elif event_type == "rival_agent":
        st.markdown(f"🕴️ **Otro agente está intentando seducir a {player.name}.**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            cost = random.randint(1000, 3000)
            if st.button(f"💼 Renovar compromiso (${cost:,})", use_container_width=True):
                if game.agent.spend_money(cost):
                    player.trust_in_agent = "Excellent"
                    st.success(f"✓ {player.name} rechazó al otro agente.")
                else:
                    st.error(f"✗ No tienes dinero. {player.name} está dudando.")
                    player.trust_in_agent = "Low"
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col2:
            if st.button("🤞 Confiar en lealtad", use_container_width=True):
                if random.random() > 0.3:
                    player.trust_in_agent = "Good"
                    st.success(f"✓ {player.name} se mantuvo leal.")
                else:
                    game.agent.remove_client(player)
                    st.error(f"✗ {player.name} cambió de agente.")
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col3:
            if st.button("⚖️ Amenazar legalmente", use_container_width=True):
                player.trust_in_agent = "Very Low"
                st.error(f"✗ {player.name} se sintió amenazado.")
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
    
    elif event_type == "family_issue":
        st.markdown(f"👨‍👩‍👧 **{player.name} tiene un problema familiar grave.**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("❤️ Apoyo emocional", use_container_width=True):
                player.trust_in_agent = "Excellent"
                player.morale = "Happy"
                st.success(f"✓ {player.name} agradece tu comprensión.")
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col2:
            if st.button("⚽ Enfocarse en fútbol", use_container_width=True):
                player.trust_in_agent = "Low"
                player.morale = "Unhappy"
                st.error(f"✗ {player.name} se sintió ignorado.")
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col3:
            cost = random.randint(3000, 7000)
            if st.button(f"💰 Ayuda financiera (${cost:,})", use_container_width=True):
                if game.agent.spend_money(cost):
                    player.trust_in_agent = "Excellent"
                    st.success(f"✓ Tu ayuda fue invaluable.")
                else:
                    st.warning("✗ No tienes dinero suficiente.")
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
    
    elif event_type == "injury_scare":
        st.markdown(f"🩹 **{player.name} sufrió una molestia física que lo tiene preocupado.**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            cost = random.randint(1500, 3500)
            if st.button(f"🏥 Médicos (${cost:,})", use_container_width=True):
                if game.agent.spend_money(cost):
                    player.morale = "Happy"
                    player.trust_in_agent = "Good"
                    st.success(f"✓ Consulta exitosa (${cost:,}). {player.name} está tranquilo.")
                else:
                    st.error(f"✗ No tienes dinero. {player.name} está nervioso.")
                    player.morale = "Unhappy"
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col2:
            if st.button("😴 Descanso preventivo", use_container_width=True):
                player.morale = "Content"
                st.info("↷ Situación estable.")
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col3:
            if st.button("💪 Ignorar y continuar", use_container_width=True):
                if random.random() < 0.3:
                    player.morale = "Unhappy"
                    st.error("✗ La molestia empeoró.")
                else:
                    st.success("✓ La molestia pasó.")
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
    
    elif event_type == "dressing_room_issue":
        if not player.club:
            st.warning(f"✗ {player.name} está libre, no hay vestuario.")
            if st.button("Continuar"):
                st.session_state.pending_event = None
                st.rerun()
        else:
            st.markdown(f"🚪 **{player.name} tiene un conflicto con compañeros en {player.club}.**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("👥 Reunión de equipo", use_container_width=True):
                    player.morale = "Content"
                    player.trust_in_agent = "Good"
                    st.success("✓ Reunión ayudó a resolver tensiones.")
                    st.session_state.pending_event = None
                    time.sleep(2)
                    st.rerun()
            
            with col2:
                if st.button("📢 Apoyar públicamente", use_container_width=True):
                    player.trust_in_agent = "Excellent"
                    player.morale = "Happy"
                    st.success(f"✓ {player.name} apreció tu apoyo incondicional.")
                    st.session_state.pending_event = None
                    time.sleep(2)
                    st.rerun()
            
            with col3:
                if st.button("😔 Pedir disculpa al equipo", use_container_width=True):
                    player.morale = "Unhappy"
                    player.trust_in_agent = "Low"
                    st.warning(f"✗ {player.name} se sintió traicionado.")
                    st.session_state.pending_event = None
                    time.sleep(2)
                    st.rerun()
    
    elif event_type == "not_training":
        st.markdown(f"🏃 **{player.name} no está asistiendo a entrenamientos.**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🤝 Hablar en privado", use_container_width=True):
                player.trust_in_agent = "Good"
                st.success(f"✓ {player.name} apreció tu apoyo. Volverá a entrenar.")
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col2:
            if st.button("📞 Alertar al club", use_container_width=True):
                if player.club:
                    player.morale = "Content"
                    st.info(f"↷ {player.club} está al tanto.")
                else:
                    st.warning(f"✗ {player.name} está libre, no hay club.")
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col3:
            if st.button("⚠️ Darle ultimátum", use_container_width=True):
                player.trust_in_agent = "Low"
                player.morale = "Unhappy"
                st.error(f"✗ {player.name} se molestó con el ultimátum.")
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
    
    elif event_type == "doping_accusation":
        st.markdown(f"""
        🚨 **CRISIS: {player.name} fue acusado de doping por un medio amarillista.**
        
        No hay pruebas, pero el rumor se expande rápido.
        
        💡 Tu energía: {game.agent.actions_remaining}/{game.agent.actions_per_week}
        """)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⚖️ Abogados ($12,000)", use_container_width=True):
                cost = 12000
                if game.agent.spend_money(cost):
                    game.agent.change_press_reputation(+20)
                    player.trust_in_agent = "Excellent"
                    st.success(f"✓ Demanda exitosa. Medio retractado.")
                    st.info(f"Prensa: {game.agent.press_reputation}/100")
                else:
                    st.error("✗ No tienes dinero. Rumor sigue vivo.")
                    game.agent.change_press_reputation(-15)
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col2:
            if st.button("📄 Desmentida rápida", use_container_width=True):
                game.agent.change_press_reputation(+5)
                player.trust_in_agent = "Good"
                st.info("↷ Daño parcialmente controlado.")
                st.info(f"Prensa: {game.agent.press_reputation}/100")
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col3:
            if st.button("🤐 No hacer nada", use_container_width=True):
                game.agent.change_press_reputation(-20)
                player.trust_in_agent = "Low"
                player.morale = "Unhappy"
                st.error(f"✗ {player.name} está furioso. La prensa te odia.")
                st.info(f"⚠️ Prensa: {game.agent.press_reputation}/100")
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
    
    elif event_type == "contract_rebellion":
        st.markdown(f"""
        🚨 **CRISIS: {player.name} está exigiendo renovación YA o amenaza con irse libre.**
        
        Club: {player.club or 'Libre'}
        
        💡 Tu energía: {game.agent.actions_remaining}/{game.agent.actions_per_week}
        """)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💼 Negociar mejora ahora", use_container_width=True):
                player.trust_in_agent = "Excellent"
                player.morale = "Happy"
                st.success(f"✓ {player.name} está feliz. Presionarás al club.")
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col2:
            if st.button("⏳ Esperar fin de temporada", use_container_width=True):
                player.trust_in_agent = "Neutral"
                player.morale = "Content"
                st.warning(f"↷ {player.name} aceptó esperar, pero no está contento.")
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col3:
            if st.button("📰 Filtrar a prensa", use_container_width=True):
                game.agent.change_press_reputation(-15)
                player.transfer_value = int(player.transfer_value * 1.2) if player.transfer_value else 0
                st.success("✓ Rumor plantado. Valor +20%.")
                st.warning(f"⚠️ Prensa: {game.agent.press_reputation}/100")
                st.info(f"💰 Nuevo valor: ${player.transfer_value:,}")
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
    
    elif event_type == "tax_evasion":
        amount = random.randint(50000, 200000)
        st.markdown(f"""
        🚨 **CRISIS: Hacienda acusa a {player.name} de evadir impuestos por ${amount:,}.**
        
        Juicio inminente. El jugador te culpa por malos consejos fiscales.
        
        💡 Tu energía: {game.agent.actions_remaining}/{game.agent.actions_per_week}
        """)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⚖️ Élite legal ($25k + 2 acc)", use_container_width=True):
                cost = 25000
                if game.agent.spend_money(cost) and game.agent.actions_remaining >= 2:
                    game.agent.actions_remaining -= 2
                    if random.random() < 0.70:
                        player.trust_in_agent = "Excellent"
                        game.agent.change_press_reputation(+20)
                        st.success(f"✓ ¡Absuelto! (${cost:,}, -2 acc)")
                    else:
                        player.trust_in_agent = "Neutral"
                        game.agent.change_press_reputation(-10)
                        st.error(f"✗ Condenado (${cost:,}, -2 acc)")
                else:
                    st.error("✗ Recursos insuficientes. Condenado.")
                    player.trust_in_agent = "Low"
                    game.agent.change_press_reputation(-30)
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col2:
            if st.button("🤝 Acuerdo ($18k + 1 acc)", use_container_width=True):
                cost = 18000
                if game.agent.spend_money(cost) and game.agent.actions_remaining >= 1:
                    game.agent.actions_remaining -= 1
                    player.trust_in_agent = "Good"
                    game.agent.change_press_reputation(-5)
                    st.success(f"✓ Acuerdo firmado (${cost:,}, -1 acc)")
                else:
                    st.error("✗ Recursos insuficientes.")
                    player.trust_in_agent = "Low"
                    game.agent.change_press_reputation(-20)
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col3:
            if st.button("🚫 Dejar solo", use_container_width=True):
                player.trust_in_agent = "Very Low"
                player.morale = "Unhappy"
                game.agent.change_press_reputation(-35)
                st.error(f"✗ {player.name} fue condenado. Te odia.")
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
    
    elif event_type == "assault_allegations":
        st.markdown(f"""
        🚨 **CRISIS: Una persona acusa a {player.name} de agresión en un bar.**
        
        Hay testigos, pero versiones contradictorias. Policía investiga.
        
        💡 Tu energía: {game.agent.actions_remaining}/{game.agent.actions_per_week}
        """)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔍 Investigador ($20k + 2 acc)", use_container_width=True):
                cost = 20000
                if game.agent.spend_money(cost) and game.agent.actions_remaining >= 2:
                    game.agent.actions_remaining -= 2
                    if random.random() < 0.60:
                        player.trust_in_agent = "Excellent"
                        game.agent.change_press_reputation(+15)
                        st.success(f"✓ Evidencia de inocencia (${cost:,}, -2 acc). Caso cerrado.")
                    else:
                        player.morale = "Unhappy"
                        game.agent.change_press_reputation(-15)
                        st.warning(f"✗ Sin evidencia concluyente (${cost:,}, -2 acc)")
                else:
                    st.error("✗ Recursos insuficientes.")
                    player.morale = "Unhappy"
                    game.agent.change_press_reputation(-20)
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col2:
            if st.button("💰 Compensación ($30k + 1 acc)", use_container_width=True):
                cost = 30000
                if game.agent.spend_money(cost) and game.agent.actions_remaining >= 1:
                    game.agent.actions_remaining -= 1
                    player.trust_in_agent = "Good"
                    game.agent.change_press_reputation(-10)
                    st.success(f"✓ Cargos retirados (${cost:,}, -1 acc). Prensa sospecha.")
                else:
                    st.error("✗ Recursos insuficientes. Juicio se avecina.")
                    player.morale = "Unhappy"
                    game.agent.change_press_reputation(-25)
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col3:
            if st.button("⏳ Esperar proceso legal", use_container_width=True):
                if random.random() < 0.40:
                    player.morale = "Content"
                    st.success(f"✓ {player.name} fue absuelto. Suerte.")
                else:
                    player.trust_in_agent = "Very Low"
                    player.morale = "Unhappy"
                    game.agent.change_press_reputation(-40)
                    st.error(f"✗ {player.name} fue condenado. Te culpa.")
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
    
    elif event_type == "leaked_video":
        st.markdown(f"""
        🚨 **CRISIS: Un video íntimo de {player.name} fue filtrado en redes sociales.**
        
        Se viraliza rápidamente. El jugador está devastado emocionalmente.
        
        💡 Tu energía: {game.agent.actions_remaining}/{game.agent.actions_per_week}
        """)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💻 Ciberseguridad ($12k + 2 acc)", use_container_width=True):
                cost = 12000
                if game.agent.spend_money(cost) and game.agent.actions_remaining >= 2:
                    game.agent.actions_remaining -= 2
                    player.trust_in_agent = "Excellent"
                    player.morale = "Content"
                    game.agent.change_press_reputation(+10)
                    st.success(f"✓ Video eliminado (${cost:,}, -2 acc). {player.name} agradecido.")
                else:
                    st.error("✗ Recursos insuficientes. Video persiste.")
                    player.morale = "Unhappy"
                    game.agent.change_press_reputation(-20)
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col2:
            if st.button("📢 Víctima ($5k + 1 acc)", use_container_width=True):
                cost = 5000
                if game.agent.spend_money(cost) and game.agent.actions_remaining >= 1:
                    game.agent.actions_remaining -= 1
                    player.trust_in_agent = "Good"
                    player.morale = "Happy"
                    game.agent.change_press_reputation(+15)
                    st.success(f"✓ Declaración emitida (${cost:,}, -1 acc). Prensa apoya.")
                else:
                    st.error("✗ Recursos insuficientes.")
                    player.morale = "Unhappy"
                    game.agent.change_press_reputation(-15)
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
        
        with col3:
            if st.button("🤐 Ignorar y esperar", use_container_width=True):
                player.trust_in_agent = "Low"
                player.morale = "Unhappy"
                game.agent.change_press_reputation(-25)
                st.error(f"✗ {player.name} está devastado. Te culpa por no ayudar.")
                st.session_state.pending_event = None
                time.sleep(2)
                st.rerun()
    
    # Add skip button for testing
    st.markdown("---")
    if st.button("⏭️ Omitir Evento (Testing)", type="secondary"):
        st.session_state.pending_event = None
        st.session_state.event_player = None
        st.session_state.selected_page = "🏠 Inicio"
        st.rerun()

def render_advance_week():
    """Render advance week page"""
    st.title("⏭️ Avanzar Semana")
    
    game = st.session_state.game
    
    st.markdown(f"### Semana Actual: {game.agent.week}")
    st.markdown(f"**Acciones restantes:** {game.agent.actions_remaining}/{game.agent.actions_per_week}")
    
    if game.agent.actions_remaining > 0:
        st.warning(f"⚠️ Tienes {game.agent.actions_remaining} acciones sin usar")
    
    if st.button("⏭️ Avanzar a la Siguiente Semana", type="primary", use_container_width=True):
        with st.spinner("Procesando semana..."):
            # Headless advance without input prompts
            current_week_index = game.agent.week - 1
            game._simulate_week_fixtures(current_week_index)
            game._simulate_client_match_participation(current_week_index)
            game._process_weekly_player_growth(current_week_index)
            # Generar ofertas de la semana (ventana de traspasos y agentes libres)
            game._generate_transfer_offers_for_clients(current_week_index)
            game.event_occurred_this_week = False
            game.agent.advance_week()
            
            # Generate random weekly event
            if game.agent.clients and not game.event_occurred_this_week:
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
                
                total_weight = sum(e["weight"] for e in event_catalog)
                rand = random.random() * total_weight
                cumulative = 0
                selected_event = event_catalog[0]
                
                for event in event_catalog:
                    cumulative += event["weight"]
                    if rand < cumulative:
                        selected_event = event
                        break
                
                affected_client = random.choice(game.agent.clients)
                st.session_state.pending_event = selected_event
                st.session_state.event_player = affected_client
                game.event_occurred_this_week = True

        st.success("¡Semana avanzada!")
        time.sleep(1)
        
        # If event was generated, go to situations page
        if st.session_state.pending_event:
            st.session_state.selected_page = "🎲 Situaciones"
        else:
            st.session_state.selected_page = "📝 Reportes"
        st.rerun()

# Main app
def main():
    render_sidebar()
    
    # Route to selected page
    page = st.session_state.selected_page
    
    if page == "🏠 Inicio":
        render_home()
    elif page == "👤 Mis Clientes":
        render_clients()
    elif page == "📊 Estadísticas":
        render_stats()
    elif page == "📝 Reportes":
        render_reports()
    elif page == "💼 Contratos":
        render_contracts()
    elif page == "📰 Ofertas":
        render_offers()
    elif page == "🔍 Buscar Jugadores":
        render_search_players()
    elif page == "🤝 Interacciones":
        render_interactions()
    elif page == "📈 Liga":
        render_league()
    elif page == "⚙️ Acciones":
        render_actions()
    elif page == "🎲 Situaciones":
        render_situations()
    elif page == "⏭️ Avanzar":
        render_advance_week()

if __name__ == "__main__":
    main()
