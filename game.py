"""
Main game module - Contains the game loop and core mechanics
"""

import sys
import random
from agent import Agent
from player import Player
from game_data import (
    create_initial_players,
    create_player_reports,
    get_default_clubs,
    get_international_clubs,
)
from personality_impact import (
    skill_growth_chance,
    renewal_intent_probability,
)

class FootballAgentGame:
    """Main game class that manages the game state and flow"""
    
    def __init__(self):
        self.agent = None
        self.all_players = []
        self.available_reports = []
        self.clubs = []
        self.international_clubs = []
        self.schedule = []  # List of dicts {phase, fixtures}
        self.total_weeks = 0
        self.league_table = {}
        self.club_index = {}
        self.club_rosters = {}  # {club_name: [player_dict]}
        self.growth_log = []  # Track weekly growth events
        self.renewal_log = []  # Track renewal intent at season end
        self.transfer_log = []  # Track transfer offers and decisions
        self.weekly_event_log = []  # Track weekly random events
        self.event_occurred_this_week = False  # Only one event per week
        self.running = True
        
    def start_game(self):
        """Initialize and start the game"""
        self.show_intro()
        agent_name = input("\nEnter your name: ").strip()
        if not agent_name:
            agent_name = "Agent Smith"
        
        # Choose agent type/personality
        agent_type = self._choose_agent_type()
        
        self.agent = Agent(agent_name, agent_type)
        self.all_players = create_initial_players()
        self.available_reports = create_player_reports()
        self.clubs = get_default_clubs()
        self.international_clubs = get_international_clubs()
        self.schedule = self._build_season_schedule()
        self.total_weeks = len(self.schedule)
        self._init_league_table()
        self.club_index = {c.name: c for c in self.clubs}
        self._init_club_rosters()
        
        print(f"\nWelcome, {agent_name}! Your journey as a {agent_type} agent begins now.")
        print(f"Starting money: ${self.agent.money:,}")
        print(f"Actions per week: {self.agent.actions_per_week}")
        print(f"Commission rate: {self.agent.commission_rate*100:.0f}%")
        input("\nPress Enter to begin...")
        
        self.game_loop()
    
    def _choose_agent_type(self):
        """Let player choose their agent personality"""
        print("\n" + "="*60)
        print("CHOOSE YOUR AGENT TYPE")
        print("="*60)
        print("""
1. THE FATHER (Mentor)
   - Starting Money: $45,000
   - Actions/Week: 6
   - Commission: 3% (low)
   - Bonuses: +15% client morale, +10% young player growth
   - Philosophy: Long-term development, loyalty over money

2. THE SHARK (Negotiator)
   - Starting Money: $60,000
   - Actions/Week: 4
   - Commission: 8% (high)
   - Bonuses: +20% transfer fees
   - Penalty: -10% client morale (they feel used)
   - Philosophy: Maximum profit, ruthless efficiency

3. THE DIPLOMAT (Connector)
   - Starting Money: $50,000
   - Actions/Week: 5
   - Commission: 5% (standard)
   - Bonuses: 2x faster club relationships, access to top loans
   - Philosophy: Build network, open doors

4. BALANCED (All-rounder)
   - Starting Money: $50,000
   - Actions/Week: 5
   - Commission: 5% (standard)
   - Philosophy: No specialization, steady growth
        """)
        print("="*60)
        
        choice = input("\nChoose your type (1-4): ").strip()
        type_map = {
            "1": "Father",
            "2": "Shark",
            "3": "Diplomat",
            "4": "Balanced"
        }
        
        agent_type = type_map.get(choice, "Balanced")
        print(f"\n✓ You chose: {agent_type}")
        return agent_type
    
    def show_intro(self):
        """Display game introduction"""
        print("\n" + "="*60)
        print(" "*15 + "FOOTBALL AGENT SIMULATOR")
        print("="*60)
        print("""
You are a football agent starting your career in the competitive 
world of player representation. Your goal is to discover talented 
players, sign them as clients, develop their careers, and earn 
money through commissions.

Each week you have limited actions. Use them to:
- Read scouting reports on potential clients
- Sign promising players
- Interact with your clients (counsel, advise, support)
- Negotiate with clubs and coaches
- Build your reputation and wealth

Remember: Player attributes are described with words, not numbers.
Trust your judgment and instinct!
        """)
        print("="*60)
    
    def game_loop(self):
        """Main game loop"""
        while self.running:
            self.show_week_summary()
            self.show_main_menu()
    
    def show_week_summary(self):
        """Display summary at the start of each week"""
        print("\n" + "="*60)
        print(f"WEEK {self.agent.week}")
        print("="*60)
        print(f"Money: ${self.agent.money:,}")
        print(f"Clients: {len(self.agent.clients)}")
        print(f"Actions Remaining: {self.agent.actions_remaining}/{self.agent.actions_per_week}")
        print("="*60)

        if 1 <= self.agent.week <= self.total_weeks:
            current = self.schedule[self.agent.week - 1]
            print(f"Phase: {current['phase']}")
            if current['fixtures']:
                print("Fixtures this week:")
                for home, away in current['fixtures']:
                    print(f"  - {home} vs {away}")
            else:
                print("No scheduled matches this week.")
        else:
            print("Out of scheduled season window.")
        
        # Show any weekly events
        if self.agent.week > 1:
            self.process_weekly_events()
    
    def process_weekly_events(self):
        """Process events that happen each week"""
        current_week_index = max(0, self.agent.week - 1)

        # Show commission earned
        total_commission = 0
        for client in self.agent.clients:
            if client.signed and client.weekly_wage > 0:
                commission = int(client.weekly_wage * 0.05)
                total_commission += commission
        
        if total_commission > 0:
            print(f"✓ Weekly commissions earned: ${total_commission:,}")
        
        # Check for contract expirations
        for client in self.agent.clients:
            if client.signed and client.contract_length <= 4 and client.contract_length > 0:
                print(f"⚠ {client.name}'s contract expires in {client.contract_length} weeks!")

        # Transfer window logic: generate and review offers for clients
        if self._is_transfer_window(current_week_index):
            self._generate_transfer_offers_for_clients(current_week_index)
            self._handle_transfer_offers_prompt()
        
        # Weekly random situation (only one per week, 40% chance)
        if not self.event_occurred_this_week and self.agent.clients and random.random() < 0.40:
            self._generate_weekly_situation()

    # ========== TRANSFER WINDOW HELPERS ==========

    def _is_transfer_window(self, week_index: int) -> bool:
        """Return True if the current phase is a transfer window."""
        if week_index < 0 or week_index >= len(self.schedule):
            return False
        phase = self.schedule[week_index].get("phase", "")
        return phase.startswith("Pretemporada") or phase.startswith("Descanso")

    def _advance_offer_deadlines(self):
        """Reduce offer deadlines and drop expired ones."""
        kept = []
        for offer in self.agent.pending_offers:
            offer["expires_in_weeks"] -= 1
            if offer["expires_in_weeks"] > 0:
                kept.append(offer)
            else:
                self.transfer_log.append({**offer, "status": "expired", "week": self.agent.week})
        self.agent.pending_offers = kept

    def _create_transfer_offer(self, player: Player) -> dict:
        """Build a single transfer offer for a player."""
        candidates = [c for c in self.clubs if c.name != player.club]
        if not candidates:
            return {}

        club = random.choice(candidates)
        overall = player.current_overall_score or int(player.current_rating * 100)
        base_fee = max(10000, player.transfer_value or overall * 500)
        is_free = not bool(player.club)

        offer = {
            "club": club.name,
            "player": player,
            "player_name": player.name,
            "fee": 0 if is_free else int(base_fee * random.uniform(0.85, 1.15)),
            "wage": max(1200, int(overall * random.uniform(120, 200))),
            "contract_weeks": random.randint(52, 156),  # 1-3 seasons
            "expires_in_weeks": 2,
            "status": "pending",
        }
        return offer

    def _generate_transfer_offers_for_clients(self, week_index: int):
        """Create transfer offers for agent-managed players during window or free agents anytime."""
        self._advance_offer_deadlines()

        new_offers = []
        is_transfer_window = self._is_transfer_window(week_index)
        
        # First: guarantee offers for free agents (no club) - ANY TIME
        for client in self.agent.clients:
            if not client.club:  # Free agent (removed "and not client.signed" to allow any free agent)
                # Free agents get offers even outside transfer window
                existing_offers = [o for o in self.agent.pending_offers if o.get("player") is client]
                if not existing_offers:
                    # Create guaranteed offer with better terms from top club
                    candidates = sorted(self.clubs, key=lambda c: c.reputation, reverse=True)[:5]
                    club = random.choice(candidates)
                    overall = client.current_overall_score or int(client.current_rating * 100)
                    
                    offer = {
                        "club": club.name,
                        "player": client,
                        "player_name": client.name,
                        "fee": 0,  # Free agent
                        "wage": max(1500, int(overall * random.uniform(140, 220))),
                        "contract_weeks": random.randint(52, 104),
                        "expires_in_weeks": 2,  # Short deadline
                        "status": "pending",
                    }
                    self.agent.pending_offers.append(offer)
                    new_offers.append(offer)
                    self.transfer_log.append({**offer, "status": "created_free_agent", "week": self.agent.week})
                    print(f"\n📩 Oferta garantizada para agente libre {client.name}: {offer['club']} - ${offer['wage']:,}/sem")
        
        # Then: regular offers for other clients (only during transfer window)
        if is_transfer_window:
            for client in self.agent.clients:
                # Skip if already has two active offers
                existing = [o for o in self.agent.pending_offers if o.get("player") is client]
                if len(existing) >= 2:
                    continue

                rating = client.current_overall_score or int(client.current_rating * 100)
                if rating >= 80:
                    prob = 0.65
                elif rating >= 70:
                    prob = 0.45
                else:
                    prob = 0.25

                if random.random() > prob:
                    continue

                offer = self._create_transfer_offer(client)
                if offer:
                    self.agent.pending_offers.append(offer)
                    new_offers.append(offer)
                    self.transfer_log.append({**offer, "status": "created", "week": self.agent.week})

        if new_offers:
            print(f"\n📩 Nuevas ofertas de traspaso: {len(new_offers)} (ver abajo)")

    def _handle_transfer_offers_prompt(self):
        """Prompt the user to accept or reject pending offers."""
        if not self.agent.pending_offers:
            return

        print("\nOFERTAS PENDIENTES PARA TUS CLIENTES:")
        for idx, offer in enumerate(self.agent.pending_offers, 1):
            player = offer["player"]
            print(f"{idx}. {player.name} → {offer['club']} | Fee ${offer['fee']:,} | Wage ${offer['wage']:,}/sem | {offer['contract_weeks']} semanas | expira en {offer['expires_in_weeks']} sem")

        for idx, offer in list(enumerate(list(self.agent.pending_offers), 1)):
            player = offer["player"]
            decision = input(f"Aceptar oferta #{idx} para {player.name}? (a)ccept / (r)eject / (s)kip: ").strip().lower()
            if decision.startswith("a"):
                self._accept_transfer_offer(offer)
            elif decision.startswith("r"):
                self.agent.pending_offers.remove(offer)
                self.transfer_log.append({**offer, "status": "rejected", "week": self.agent.week})
                print(f"✗ Rechazada oferta de {offer['club']} para {player.name}.")
            else:
                print(f"↷ Oferta para {player.name} se mantiene pendiente.")

    def _accept_transfer_offer(self, offer: dict):
        """Accept an offer and update agent finances and player contract."""
        player = offer["player"]
        player.sign_with_club(offer["club"], offer["wage"], offer["contract_weeks"])

        # Agent commission: 5% of fee + 2 weeks of wage as bonus proxy
        commission = int(offer["fee"] * 0.05 + offer["wage"] * 2 * 0.05)
        self.agent.earn_commission(commission)

        if offer in self.agent.pending_offers:
            self.agent.pending_offers.remove(offer)

        self.transfer_log.append({**offer, "status": "accepted", "week": self.agent.week, "commission": commission})
        print(f"✓ {player.name} firmó con {offer['club']} por ${offer['wage']:,}/sem. Comisión: ${commission:,}")
    
    # ========== WEEKLY RANDOM SITUATIONS ==========
    
    def _generate_weekly_situation(self):
        """Generate one random situation per week for a client."""
        if not self.agent.clients or self.event_occurred_this_week:
            return
        
        # Event catalog with weights
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
            # CRISIS EVENTS (high impact)
            {"type": "nightclub_scandal", "weight": 6, "title": "🍾 CRISIS: Escándalo nocturno"},
            {"type": "doping_accusation", "weight": 4, "title": "💊 CRISIS: Acusación de doping"},
            {"type": "social_media_disaster", "weight": 7, "title": "📱 CRISIS: Desastre en redes"},
            {"type": "contract_rebellion", "weight": 5, "title": "📄 CRISIS: Rebelión contractual"},
        ]
        
        # Pick random event by weight
        total_weight = sum(e["weight"] for e in event_catalog)
        rand = random.random() * total_weight
        cumulative = 0
        selected_event = event_catalog[0]
        
        for event in event_catalog:
            cumulative += event["weight"]
            if rand < cumulative:
                selected_event = event
                break
        
        # Pick random client
        affected_client = random.choice(self.agent.clients)
        
        self.event_occurred_this_week = True
        self._present_situation(affected_client, selected_event)
    
    def _present_situation(self, player: Player, event: dict):
        """Present situation to user and handle their choice."""
        print("\n" + "="*60)
        print(f"🎲 SITUACIÓN SEMANAL: {event['title']}")
        print("="*60)
        print(f"Jugador: {player.name} ({player.position})")
        print(f"Club: {player.club or 'Libre'}")
        print(f"Morale: {player.morale} | Trust: {player.trust_in_agent}")
        print()
        
        event_type = event["type"]
        
        if event_type == "needs_money":
            print(f"{player.name} necesita un adelanto urgente de ${random.randint(2000, 8000):,}.")
            print("\nOpciones:")
            print("1. Darle adelanto personal (tu dinero)")
            print("2. Negociar con el club un bonus")
            print("3. Negarle el adelanto")
            choice = input("\nElige (1-3): ").strip()
            
            if choice == "1":
                cost = random.randint(2000, 8000)
                if self.agent.spend_money(cost):
                    player.trust_in_agent = "Good" if player.trust_in_agent == "Neutral" else "Excellent"
                    print(f"✓ {player.name} está muy agradecido. Trust mejorado.")
                    self._log_event(player, event_type, "gave_money", {"trust": "+"})
                else:
                    print("✗ No tienes suficiente dinero.")
                    player.trust_in_agent = "Low" if player.trust_in_agent == "Neutral" else "Very Low"
                    self._log_event(player, event_type, "failed_money", {"trust": "-"})
            elif choice == "2":
                if player.club:
                    print(f"✓ Negociaste un bonus con {player.club}. {player.name} está satisfecho.")
                    self._log_event(player, event_type, "negotiated_bonus", {"morale": "+"})
                else:
                    print(f"✗ {player.name} está libre, no hay club con quien negociar.")
                    player.morale = "Unhappy"
                    self._log_event(player, event_type, "no_club", {"morale": "-"})
            else:
                player.trust_in_agent = "Low"
                player.morale = "Unhappy"
                print(f"✗ {player.name} está decepcionado. Trust y morale reducidos.")
                self._log_event(player, event_type, "denied", {"trust": "-", "morale": "-"})
        
        elif event_type == "demotivated":
            print(f"{player.name} se siente desmotivado y sin objetivos claros.")
            print("\nOpciones:")
            print("1. Sesión motivacional intensa")
            print("2. Darle tiempo libre")
            print("3. Presionarlo para que entrene más")
            choice = input("\nElige (1-3): ").strip()
            
            if choice == "1":
                player.morale = "Happy"
                player.trust_in_agent = "Good" if player.trust_in_agent != "Low" else "Neutral"
                print(f"✓ {player.name} recuperó su motivación. Morale mejorado.")
                self._log_event(player, event_type, "motivational_talk", {"morale": "+", "trust": "+"})
            elif choice == "2":
                player.morale = "Content"
                print(f"↷ {player.name} tomó un descanso. Morale estable.")
                self._log_event(player, event_type, "time_off", {"morale": "="})
            else:
                player.morale = "Unhappy"
                player.trust_in_agent = "Low"
                print(f"✗ {player.name} se siente presionado. Morale y trust reducidos.")
                self._log_event(player, event_type, "pressured", {"morale": "-", "trust": "-"})
        
        elif event_type == "not_training":
            print(f"{player.name} no está asistiendo a entrenamientos.")
            print("\nOpciones:")
            print("1. Hablar con él en privado")
            print("2. Alertar al club/entrenador")
            print("3. Darle ultimátum")
            choice = input("\nElige (1-3): ").strip()
            
            if choice == "1":
                player.trust_in_agent = "Good"
                print(f"✓ {player.name} apreció tu apoyo. Volverá a entrenar.")
                self._log_event(player, event_type, "private_talk", {"trust": "+"})
            elif choice == "2":
                if player.club:
                    player.morale = "Content"
                    print(f"↷ {player.club} está al tanto. {player.name} volverá.")
                    self._log_event(player, event_type, "alerted_club", {"morale": "="})
                else:
                    print(f"✗ {player.name} está libre, no hay club.")
                    self._log_event(player, event_type, "no_club", {})
            else:
                player.trust_in_agent = "Low"
                player.morale = "Unhappy"
                print(f"✗ {player.name} se molestó con el ultimátum.")
                self._log_event(player, event_type, "ultimatum", {"trust": "-", "morale": "-"})
        
        elif event_type == "press_rumor":
            rumor_positive = random.random() > 0.5
            if rumor_positive:
                print(f"📰 La prensa habla positivamente de {player.name}.")
                player.morale = "Happy"
                print(f"✓ Morale mejorado.")
                self._log_event(player, event_type, "positive", {"morale": "+"})
            else:
                print(f"📰 La prensa publicó rumores negativos sobre {player.name}.")
                print("\nOpciones:")
                print("1. Emitir comunicado oficial")
                print("2. Ignorar el rumor")
                print("3. Confrontar al periodista")
                choice = input("\nElige (1-3): ").strip()
                
                if choice == "1":
                    player.morale = "Content"
                    print(f"✓ El comunicado calmó la situación.")
                    self._log_event(player, event_type, "statement", {"morale": "="})
                elif choice == "2":
                    player.morale = "Unhappy"
                    print(f"↷ El rumor persiste. {player.name} está molesto.")
                    self._log_event(player, event_type, "ignored", {"morale": "-"})
                else:
                    player.morale = "Content"
                    player.trust_in_agent = "Good"
                    print(f"✓ {player.name} apreció tu defensa agresiva.")
                    self._log_event(player, event_type, "confronted", {"trust": "+"})
        
        elif event_type == "coach_conflict":
            if not player.club:
                print(f"✗ {player.name} está libre, no hay entrenador.")
                self._log_event(player, event_type, "no_club", {})
            else:
                print(f"{player.name} tuvo un conflicto con el entrenador de {player.club}.")
                print("\nOpciones:")
                print("1. Mediar entre ambos")
                print("2. Exigir disculpa del jugador")
                print("3. Buscar transferencia inmediata")
                choice = input("\nElige (1-3): ").strip()
                
                if choice == "1":
                    player.morale = "Content"
                    player.trust_in_agent = "Good"
                    print(f"✓ Mediaste exitosamente. Relación restaurada.")
                    self._log_event(player, event_type, "mediated", {"morale": "=", "trust": "+"})
                elif choice == "2":
                    player.trust_in_agent = "Low"
                    print(f"↷ {player.name} se disculpó pero está resentido contigo.")
                    self._log_event(player, event_type, "forced_apology", {"trust": "-"})
                else:
                    player.morale = "Unhappy"
                    print(f"⚠️ {player.name} quiere irse. Deberás buscar ofertas.")
                    self._log_event(player, event_type, "force_transfer", {"morale": "-"})
        
        elif event_type == "rival_agent":
            print(f"🕴️ Otro agente está intentando seducir a {player.name}.")
            print("\nOpciones:")
            print("1. Renovar compromiso con beneficios")
            print("2. Confiar en la lealtad del jugador")
            print("3. Amenazar con acciones legales")
            choice = input("\nElige (1-3): ").strip()
            
            if choice == "1":
                cost = random.randint(1000, 3000)
                if self.agent.spend_money(cost):
                    player.trust_in_agent = "Excellent"
                    print(f"✓ {player.name} rechazó al otro agente. Trust máximo. Costo: ${cost:,}")
                    self._log_event(player, event_type, "renewed_commitment", {"trust": "++"})
                else:
                    print(f"✗ No tienes dinero para beneficios. {player.name} está dudando.")
                    player.trust_in_agent = "Low"
                    self._log_event(player, event_type, "no_money", {"trust": "-"})
            elif choice == "2":
                loyalty_check = random.random()
                if loyalty_check > 0.3:
                    player.trust_in_agent = "Good"
                    print(f"✓ {player.name} se mantuvo leal.")
                    self._log_event(player, event_type, "stayed_loyal", {"trust": "+"})
                else:
                    self.agent.remove_client(player)
                    print(f"✗ {player.name} decidió cambiar de agente.")
                    self._log_event(player, event_type, "lost_client", {"trust": "--"})
            else:
                player.trust_in_agent = "Very Low"
                print(f"✗ {player.name} se sintió amenazado. Trust muy bajo.")
                self._log_event(player, event_type, "threatened", {"trust": "--"})
        
        elif event_type == "family_issue":
            print(f"{player.name} tiene un problema familiar grave.")
            print("\nOpciones:")
            print("1. Darle permiso y apoyo emocional")
            print("2. Pedirle que se enfoque en el fútbol")
            print("3. Ofrecer ayuda financiera")
            choice = input("\nElige (1-3): ").strip()
            
            if choice == "1":
                player.trust_in_agent = "Excellent"
                player.morale = "Happy"
                print(f"✓ {player.name} agradece tu comprensión. Trust y morale mejorados.")
                self._log_event(player, event_type, "support", {"trust": "++", "morale": "+"})
            elif choice == "2":
                player.trust_in_agent = "Low"
                player.morale = "Unhappy"
                print(f"✗ {player.name} se sintió ignorado. Trust y morale reducidos.")
                self._log_event(player, event_type, "ignored", {"trust": "-", "morale": "-"})
            else:
                cost = random.randint(3000, 7000)
                if self.agent.spend_money(cost):
                    player.trust_in_agent = "Excellent"
                    print(f"✓ Tu ayuda de ${cost:,} fue invaluable. Trust máximo.")
                    self._log_event(player, event_type, "financial_help", {"trust": "++"})
                else:
                    print(f"✗ No tienes dinero suficiente. {player.name} entenderá pero está decepcionado.")
                    self._log_event(player, event_type, "no_money", {})
        
        elif event_type == "injury_scare":
            print(f"{player.name} sufrió una molestia física que lo tiene preocupado.")
            print("\nOpciones:")
            print("1. Consultar médicos especializados (costo)")
            print("2. Descanso preventivo")
            print("3. Ignorar y continuar")
            choice = input("\nElige (1-3): ").strip()
            
            if choice == "1":
                cost = random.randint(1500, 3500)
                if self.agent.spend_money(cost):
                    player.morale = "Happy"
                    player.trust_in_agent = "Good"
                    print(f"✓ Consulta exitosa: ${cost:,}. {player.name} está tranquilo.")
                    self._log_event(player, event_type, "specialist", {"morale": "+", "trust": "+"})
                else:
                    print(f"✗ No tienes dinero. {player.name} está nervioso.")
                    player.morale = "Unhappy"
                    self._log_event(player, event_type, "no_money", {"morale": "-"})
            elif choice == "2":
                player.morale = "Content"
                print(f"↷ {player.name} descansará. Situación estable.")
                self._log_event(player, event_type, "rest", {"morale": "="})
            else:
                injury_risk = random.random()
                if injury_risk < 0.3:
                    player.morale = "Unhappy"
                    print(f"✗ La molestia empeoró. {player.name} podría lesionarse.")
                    self._log_event(player, event_type, "worsened", {"morale": "-"})
                else:
                    print(f"✓ Afortunadamente, la molestia pasó.")
                    self._log_event(player, event_type, "passed", {})
        
        elif event_type == "dressing_room_issue":
            if not player.club:
                print(f"✗ {player.name} está libre, no hay vestuario de equipo.")
                self._log_event(player, event_type, "no_club", {})
            else:
                print(f"{player.name} tiene un conflicto con compañeros en el vestuario de {player.club}.")
                print("\nOpciones:")
                print("1. Organizar reunión de equipo")
                print("2. Apoyar públicamente al jugador")
                print("3. Pedirle que se disculpe con el equipo")
                choice = input("\nElige (1-3): ").strip()
                
                if choice == "1":
                    player.morale = "Content"
                    player.trust_in_agent = "Good"
                    print(f"✓ La reunión ayudó a resolver las tensiones. Vestuario más unido.")
                    self._log_event(player, event_type, "team_meeting", {"morale": "=", "trust": "+"})
                elif choice == "2":
                    player.trust_in_agent = "Excellent"
                    player.morale = "Happy"
                    print(f"✓ {player.name} apreció tu apoyo incondicional, pero algunos compañeros están molestos.")
                    self._log_event(player, event_type, "public_support", {"trust": "++", "morale": "+"})
                else:
                    player.morale = "Unhappy"
                    player.trust_in_agent = "Low"
                    print(f"✗ {player.name} se sintió traicionado. El vestuario mejoró pero perdiste su confianza.")
                    self._log_event(player, event_type, "forced_apology", {"trust": "--", "morale": "-"})
        
        # ========== CRISIS EVENTS ==========
        elif event_type == "nightclub_scandal":
            print(f"🚨 CRISIS: {player.name} fue visto en un boliche a las 4 AM antes de un partido importante.")
            print(f"La prensa ya tiene fotos. El club está furioso.")
            print(f"\nTu energía: {self.agent.actions_remaining}/{self.agent.actions_per_week}")
            print("\nOpciones:")
            print("1. Encubrirlo ($8,000 + prensa baja, no sale en medios)")
            print("2. Regañarlo públicamente (morale --, club +, prensa =)")
            print("3. Decir al club que tú lo manejas (trust +, club -, prensa conoce)")
            choice = input("\nElige (1-3): ").strip()
            
            if choice == "1":
                cost = 8000
                if self.agent.spend_money(cost):
                    self.agent.change_press_reputation(-15)
                    print(f"✓ Pagaste ${cost:,} para encubrir. No salió en medios.")
                    print(f"⚠️  Prensa: {self.agent.press_reputation}/100 (perdiste reputación)")
                    self._log_event(player, event_type, "cover_up", {"press": "-15"})
                else:
                    print(f"✗ No tienes dinero. El escándalo explotó en la prensa.")
                    player.morale = "Unhappy"
                    self.agent.change_press_reputation(-25)
                    self._log_event(player, event_type, "failed_cover", {"morale": "-", "press": "-25"})
            elif choice == "2":
                player.morale = "Unhappy"
                player.trust_in_agent = "Low"
                print(f"✓ El club apreció tu postura firme. {player.name} está molesto contigo.")
                self._log_event(player, event_type, "public_scolding", {"morale": "--", "trust": "-"})
            else:
                player.trust_in_agent = "Good"
                self.agent.change_press_reputation(-10)
                print(f"✓ {player.name} valoró tu apoyo. El club no quedó conforme.")
                print(f"⚠️  Prensa: {self.agent.press_reputation}/100")
                self._log_event(player, event_type, "agent_handling", {"trust": "+", "press": "-10"})
        
        elif event_type == "doping_accusation":
            print(f"🚨 CRISIS: {player.name} fue acusado de doping por un medio amarillista.")
            print(f"No hay pruebas, pero el rumor se expande rápido.")
            print(f"\nTu energía: {self.agent.actions_remaining}/{self.agent.actions_per_week}")
            print("\nOpciones:")
            print("1. Contratar abogados ($12,000, prensa ++, trust ++)")
            print("2. Emitir desmentida rápida (gratis, prensa +, efectividad limitada)")
            print("3. No hacer nada (prensa --, trust -)")
            choice = input("\nElige (1-3): ").strip()
            
            if choice == "1":
                cost = 12000
                if self.agent.spend_money(cost):
                    self.agent.change_press_reputation(+20)
                    player.trust_in_agent = "Excellent"
                    print(f"✓ Demanda exitosa: ${cost:,}. Medio retractado. Reputación mejorada.")
                    print(f"✓ Prensa: {self.agent.press_reputation}/100")
                    self._log_event(player, event_type, "lawsuit", {"press": "+20", "trust": "++"})
                else:
                    print(f"✗ No tienes dinero. El rumor sigue vivo.")
                    self.agent.change_press_reputation(-15)
                    self._log_event(player, event_type, "no_money", {"press": "-15"})
            elif choice == "2":
                self.agent.change_press_reputation(+5)
                player.trust_in_agent = "Good"
                print(f"↷ Desmentida emitida. Daño parcialmente controlado.")
                print(f"Prensa: {self.agent.press_reputation}/100")
                self._log_event(player, event_type, "denial", {"press": "+5", "trust": "+"})
            else:
                self.agent.change_press_reputation(-20)
                player.trust_in_agent = "Low"
                player.morale = "Unhappy"
                print(f"✗ No hiciste nada. {player.name} está furioso y la prensa te odia.")
                print(f"⚠️  Prensa: {self.agent.press_reputation}/100")
                self._log_event(player, event_type, "ignored", {"press": "-20", "trust": "-", "morale": "-"})
        
        elif event_type == "social_media_disaster":
            print(f"🚨 CRISIS: {player.name} publicó un tweet polémico insultando al entrenador.")
            print(f"Está viralizándose. El club exige acción inmediata.")
            print(f"\nTu energía: {self.agent.actions_remaining}/{self.agent.actions_per_week}")
            print("\nOpciones:")
            print("1. Borrar tweet y disculpa pública (morale -, prensa +, club +)")
            print("2. Defenderlo: 'Expresó su opinión' (trust ++, prensa -, club --)")
            print("3. Fingir hackeo ($5,000, todo neutral)")
            choice = input("\nElige (1-3): ").strip()
            
            if choice == "1":
                player.morale = "Content"
                self.agent.change_press_reputation(+10)
                print(f"✓ Tweet borrado. Disculpa emitida. Crisis controlada.")
                print(f"Prensa: {self.agent.press_reputation}/100")
                self._log_event(player, event_type, "public_apology", {"morale": "-", "press": "+10"})
            elif choice == "2":
                player.trust_in_agent = "Excellent"
                self.agent.change_press_reputation(-15)
                print(f"✓ {player.name} agradece tu lealtad. Club y prensa no están contentos.")
                print(f"⚠️  Prensa: {self.agent.press_reputation}/100")
                self._log_event(player, event_type, "defended", {"trust": "++", "press": "-15"})
            else:
                cost = 5000
                if self.agent.spend_money(cost):
                    print(f"✓ Historia de hackeo creíble. Crisis neutralizada (${cost:,}).")
                    self._log_event(player, event_type, "hack_excuse", {})
                else:
                    print(f"✗ No tienes dinero. Tweet sigue visible. Desastre total.")
                    player.morale = "Unhappy"
                    self.agent.change_press_reputation(-20)
                    self._log_event(player, event_type, "failed_excuse", {"morale": "-", "press": "-20"})
        
        elif event_type == "contract_rebellion":
            print(f"🚨 CRISIS: {player.name} está exigiendo renovación YA o amenaza con irse libre.")
            print(f"Club: {player.club or 'Libre'}")
            print(f"\nTu energía: {self.agent.actions_remaining}/{self.agent.actions_per_week}")
            print("\nOpciones:")
            print("1. Negociar mejora ahora (trust ++, club relación -)")
            print("2. Calmarlo: 'Espera al final de temporada' (trust -, morale -)")
            print("3. Filtrar a prensa que club no valora al jugador (prensa --, valor +20%)")
            choice = input("\nElige (1-3): ").strip()
            
            if choice == "1":
                player.trust_in_agent = "Excellent"
                player.morale = "Happy"
                print(f"✓ {player.name} está feliz. Presionarás al club esta semana.")
                self._log_event(player, event_type, "negotiate_now", {"trust": "++", "morale": "+"})
            elif choice == "2":
                player.trust_in_agent = "Neutral"
                player.morale = "Content"
                print(f"↷ {player.name} aceptó esperar, pero no está contento.")
                self._log_event(player, event_type, "delay", {"trust": "-", "morale": "-"})
            else:
                self.agent.change_press_reputation(-15)
                player.transfer_value = int(player.transfer_value * 1.2) if player.transfer_value else 0
                print(f"✓ Rumor plantado. Valor del jugador +20%. Prensa te tiene marcado.")
                print(f"⚠️  Prensa: {self.agent.press_reputation}/100")
                print(f"💰 Nuevo valor: ${player.transfer_value:,}")
                self._log_event(player, event_type, "leak_to_press", {"press": "-15", "value": "+20%"})
        
        print("="*60)
        input("\nPresiona Enter para continuar...")
    
    def _log_event(self, player: Player, event_type: str, resolution: str, effects: dict):
        """Log event with player, type, resolution and effects."""
        self.weekly_event_log.append({
            "week": self.agent.week,
            "player": player.name,
            "event_type": event_type,
            "resolution": resolution,
            "effects": effects,
        })
    
    def show_main_menu(self):
        """Display main menu and handle user choice"""
        print("\nWhat would you like to do?")
        print("1. View Agent Status")
        print("2. View Clients")
        print("3. Read Scouting Reports (1 action)")
        print("4. Sign New Player (1 action)")
        print("5. Interact with Client (1 action)")
        print("6. Offer Player to Clubs (1 action)")
        print("7. Contact Club Staff (1 action)")
        print("8. View League Table")
        print("9. International Playoff (1 action, requiere cliente en club internacional)")
        print("10. Advance to Next Week")
        print("11. Save & Quit")
        
        choice = input("\nEnter choice (1-11): ").strip()
        
        if choice == "1":
            self.view_agent_status()
        elif choice == "2":
            self.view_clients()
        elif choice == "3":
            self.read_reports()
        elif choice == "4":
            self.sign_player()
        elif choice == "5":
            self.interact_with_client()
        elif choice == "6":
            self.offer_player_to_clubs()
        elif choice == "7":
            self.contact_club_staff()
        elif choice == "8":
            self.show_league_table()
        elif choice == "9":
            self.international_playoff()
        elif choice == "10":
            self.advance_week()
        elif choice == "11":
            self.quit_game()
        else:
            print("Invalid choice. Please try again.")
    
    def view_agent_status(self):
        """Display detailed agent status"""
        print(self.agent.get_status())
        if self.agent.clients:
            print("YOUR CLIENTS:")
            for i, client in enumerate(self.agent.clients, 1):
                print(f"{i}. {client.short_description()}")
        else:
            print("You have no clients yet. Read reports and sign players!")
        input("\nPress Enter to continue...")
    
    def view_clients(self):
        """View detailed information about clients"""
        if not self.agent.clients:
            print("\nYou have no clients yet!")
            input("Press Enter to continue...")
            return
        
        print("\nYOUR CLIENTS:")
        for i, client in enumerate(self.agent.clients, 1):
            print(f"{i}. {client.short_description()}")
        
        choice = input("\nEnter number to view details (or 0 to go back): ").strip()
        if choice.isdigit() and 0 < int(choice) <= len(self.agent.clients):
            client = self.agent.clients[int(choice) - 1]
            print(client.describe())
            input("\nPress Enter to continue...")
    
    def read_reports(self):
        """Read scouting reports on potential players"""
        if not self.agent.use_action():
            print("\nNo actions remaining this week!")
            input("Press Enter to continue...")
            return
        
            client_club_names = {client.club for client in self.agent.clients if client.club}
            print("\nNo new reports available this week.")
            input("Press Enter to continue...")
            return
        
        print("\nAVAILABLE SCOUTING REPORTS:")
        for i, report in enumerate(self.available_reports, 1):
            print(f"{i}. {report['preview']}")
        
        choice = input("\nEnter number to read full report (or 0 to go back): ").strip()
        if choice.isdigit() and 0 < int(choice) <= len(self.available_reports):
            report = self.available_reports[int(choice) - 1]
            print("\n" + "="*60)
            print(report['full_report'])
            print("="*60)
            input("\nPress Enter to continue...")
    
    def sign_player(self):
        """Attempt to sign a new player as client"""
        if not self.agent.use_action():
            print("\nNo actions remaining this week!")
            input("Press Enter to continue...")
            return
        
        # Show available players
        available = [p for p in self.all_players if not p.agent_signed]
        
        if not available:
            print("\nNo players available to sign right now!")
            input("Press Enter to continue...")
            return
        
        print("\nAVAILABLE PLAYERS:")
        for i, player in enumerate(available, 1):
            print(f"{i}. {player.short_description()}")
        
        choice = input("\nEnter number to sign (or 0 to cancel): ").strip()
        if choice.isdigit() and 0 < int(choice) <= len(available):
            player = available[int(choice) - 1]
            
            # Calculate signing bonus
            signing_bonus = max(1000, player.transfer_value // 10)
            
            print(f"\nSigning {player.name} requires a bonus of ${signing_bonus:,}")
            print(f"Your current funds: ${self.agent.money:,}")
            
            confirm = input("Proceed with signing? (yes/no): ").strip().lower()
            if confirm in ['yes', 'y']:
                if self.agent.spend_money(signing_bonus):
                    self.agent.add_client(player)
                    print(f"\n✓ {player.name} is now your client!")
                    print(f"Signing bonus paid: ${signing_bonus:,}")
                    print(f"Remaining funds: ${self.agent.money:,}")
                else:
                    print("\n✗ Insufficient funds!")
                    self.agent.actions_remaining += 1  # Refund the action
            else:
                print("\nSigning cancelled.")
                self.agent.actions_remaining += 1  # Refund the action
        
        input("\nPress Enter to continue...")
    
    def interact_with_client(self):
        """Interact with one of your clients"""
        if not self.agent.use_action():
            print("\nNo actions remaining this week!")
            input("Press Enter to continue...")
            return
        
        if not self.agent.clients:
            print("\nYou have no clients to interact with!")
            self.agent.actions_remaining += 1  # Refund the action
            input("Press Enter to continue...")
            return
        
        print("\nYOUR CLIENTS:")
        for i, client in enumerate(self.agent.clients, 1):
            print(f"{i}. {client.short_description()}")
        
        choice = input("\nSelect client to interact with (or 0 to cancel): ").strip()
        if choice.isdigit() and 0 < int(choice) <= len(self.agent.clients):
            client = self.agent.clients[int(choice) - 1]
            
            print(f"\nInteracting with {client.name}")
            print("Choose interaction type:")
            print("1. Career Counseling")
            print("2. Training Advice")
            print("3. Contract Negotiation Discussion")
            print("4. Personal Support")
            print("5. Career Planning Session")
            
            interaction_choice = input("\nEnter choice (1-5): ").strip()
            
            interaction_types = {
                "1": "counsel",
                "2": "training_advice",
                "3": "contract_negotiation",
                "4": "personal_support",
                "5": "career_planning"
            }
            
            if interaction_choice in interaction_types:
                response = client.interact(interaction_types[interaction_choice])
                print(f"\n{response}")
                
                # Small positive effect on relationship
                if client.trust_in_agent == "Neutral":
                    client.trust_in_agent = "Good"
                elif client.trust_in_agent == "Low":
                    client.trust_in_agent = "Neutral"
                
                if client.morale in ["Unhappy", "Content"]:
                    client.morale = "Happy"
            else:
                print("\nInvalid choice.")
                self.agent.actions_remaining += 1  # Refund the action
        else:
            self.agent.actions_remaining += 1  # Refund the action
        
        input("\nPress Enter to continue...")
    
    def offer_player_to_clubs(self):
        """Offer one of your clients to clubs proactively (improves relations but clubs decide)"""
        if not self.agent.use_action():
            print("\nNo actions remaining this week!")
            input("Press Enter to continue...")
            return
        
        if not self.agent.clients:
            print("\nYou have no clients to offer!")
            self.agent.actions_remaining += 1  # Refund
            input("Press Enter to continue...")
            return
        
        print("\n" + "="*60)
        print("OFFER PLAYER TO CLUBS")
        print("="*60)
        print("\nSelect which client to offer:")
        for i, client in enumerate(self.agent.clients, 1):
            print(f"{i}. {client.name} ({client.position}) - Overall: {client.current_overall_score:.0f}")
        
        choice = input("\nEnter number to offer (or 0 to cancel): ").strip()
        if not (choice.isdigit() and 0 < int(choice) <= len(self.agent.clients)):
            self.agent.actions_remaining += 1  # Refund
            input("Press Enter to continue...")
            return
        
        player = self.agent.clients[int(choice) - 1]
        print(f"\n📢 Offering {player.name} ({player.position}) to clubs...")
        print("="*60)
        
        # Improve relationship with all clubs
        for club in self.clubs:
            current = self.agent.club_relationships.get(club.name, "Neutral")
            if current == "Neutral":
                self.agent.club_relationships[club.name] = "Positive"
                print(f"✓ Relationship with {club.name} improved to Positive")
            elif current == "Positive":
                self.agent.club_relationships[club.name] = "Excellent"
                print(f"✓ Relationship with {club.name} improved to Excellent")
        
        # Clubs evaluate and decide to offer or not
        print("\n" + "-"*60)
        print("CLUB EVALUATIONS:")
        print("-"*60)
        
        player_overall = player.current_overall_score or int(player.current_rating * 100)
        has_interest = False
        
        for club in self.clubs:
            # Skip if player already there
            if player.club == club.name:
                continue
            
            # Evaluate if club is interested
            decision = self._club_evaluate_offer(club, player, player_overall)
            
            if decision["interested"]:
                has_interest = True
                print(f"\n✓ {club.name} is interested in {player.name}!")
                print(f"  → They will make an offer")
                
                # Create transfer offer from club
                offer = {
                    "club": club.name,
                    "player": player,
                    "player_name": player.name,
                    "fee": 0 if not player.club else int(player.transfer_value or player_overall * 500),
                    "wage": max(1200, int(player_overall * random.uniform(120, 200))),
                    "contract_weeks": random.randint(52, 156),
                    "expires_in_weeks": 2,
                    "status": "pending",
                }
                self.agent.pending_offers.append(offer)
                self.transfer_log.append({**offer, "status": "created_player_offer", "week": self.agent.week})
            else:
                print(f"\n✗ {club.name} declined: {decision['reason']}")
        
        if not has_interest:
            print("\n" + "-"*60)
            print("⚠️  No clubs showed interest in this player.")
        
        print("\n" + "="*60)
        input("Press Enter to continue...")
    
    def _club_evaluate_offer(self, club, player, player_overall):
        """Evaluate if a club is interested in offering for the player."""
        reasons = []
        
        # Check 1: Overall rating too low
        if player_overall < 50:
            reasons.append("not good enough")
        
        # Check 2: Club has enough budget
        budget = club.budget or 500000
        avg_wage = player_overall * 150
        if budget < avg_wage * 2:
            reasons.append("insufficient budget")
        
        # Check 3: Position fit (club's formation needs)
        position = player.position.lower()
        # Basic check: club prefers certain positions
        formation_positions = getattr(club, 'formation_positions', [])
        if formation_positions and position not in formation_positions:
            reasons.append(f"position mismatch ({position} not in formation)")
        
        # Check 4: Personality compatibility
        player_personality = getattr(player, 'personality', 'Neutral')
        if player_personality in ['Slack', 'Temperamental', 'Spineless', 'Mercenary']:
            reasons.append(f"personality concerns ({player_personality})")
        
        # Decision: if 2+ reasons, reject
        if len(reasons) >= 2:
            return {
                "interested": False,
                "reason": " + ".join(reasons)
            }
        
        # Otherwise interested
        return {
            "interested": True,
            "reason": "suitable profile"
        }

    def contact_club_staff(self):
        """Contact club directors or coaches"""
        if not self.agent.use_action():
            print("\nNo actions remaining this week!")
            input("Press Enter to continue...")
            return
        
        print("\nAVAILABLE CLUBS:")
        for i, club in enumerate(self.clubs, 1):
            print(f"{i}. {club.name} - Manager: {club.manager}, Objective: {club.objective}")
        
        choice = input("\nSelect club to contact (or 0 to cancel): ").strip()
        if choice.isdigit() and 0 < int(choice) <= len(self.clubs):
            club = self.clubs[int(choice) - 1]
            
            print(f"\nContacting {club.name}")
            print(f"1. Speak with Manager: {club.manager}")
            print("2. View Club Info")
            
            contact_choice = input("\nEnter choice (1-2): ").strip()
            
            if contact_choice == "1":
                print(f"\n{club.manager}: 'Hello, always good to hear from agents.'")
                print("'We're always looking for talent. Send over your clients' details.'")
                print(f"\n[Relationship with {club.name} slightly improved]")
                
                # Update relationship
                current = self.agent.club_relationships.get(club.name, "Neutral")
                if current == "Neutral":
                    self.agent.club_relationships[club.name] = "Positive"
                    
            elif contact_choice == "2":
                print(club.describe())
            else:
                print("\nInvalid choice.")
                self.agent.actions_remaining += 1  # Refund
        else:
            self.agent.actions_remaining += 1  # Refund
        
        input("\nPress Enter to continue...")

    def international_playoff(self):
        """Run an international playoff if any client belongs to an international club"""
        if not self.agent.use_action():
            print("\nNo actions remaining this week!")
            input("Press Enter to continue...")
            return

        client_club_names = {client.club for client in self.agent.clients if client.club}
        participating = [c for c in self.international_clubs if c.name in client_club_names]

        if not participating:
            print("\nNo tienes clientes en clubes internacionales. El playoff se activa solo si al menos uno de tus representados juega allí.")
            # Refund action since nothing happened
            self.agent.actions_remaining += 1
            input("Press Enter to continue...")
            return

        print("\n" + "="*60)
        print("PLAYOFF INTERNACIONAL - SOLO CLUBES INTERNACIONALES")
        print("="*60)
        print("Clientes en clubes internacionales:")
        for client in self.agent.clients:
            if client.club in client_club_names:
                print(f"- {client.name} ({client.club})")

        # Seleccionar 8 clubes para el bracket, priorizando el/los clubes de clientes
        pool_sorted = sorted(self.international_clubs, key=lambda c: c.reputation, reverse=True)
        participants = pool_sorted[:8]
        participant_names = {c.name for c in participants}

        # Asegurar inclusión de los clubes de clientes
        for club in pool_sorted:
            if club.name in client_club_names and club.name not in participant_names:
                participants[-1] = club
                participant_names = {c.name for c in participants}

        random.shuffle(participants)

        round_names = ["Cuartos de Final", "Semifinal", "Final"]
        current_round = participants

        for round_name in round_names:
            print(f"\n{round_name.upper()}")
            print("-"*60)
            winners = []
            for i in range(0, len(current_round), 2):
                home = current_round[i]
                away = current_round[i+1]
                home_prob = home.get_win_probability(away)
                away_prob = away.get_win_probability(home)
                total_prob = home_prob + away_prob
                outcome = random.random() * total_prob
                winner = home if outcome <= home_prob else away
                print(f"{home.name} ({home_prob:.1f}%) vs {away.name} ({away_prob:.1f}%) → Gana {winner.name}")
                winners.append(winner)
            current_round = winners

        champion = current_round[0]
        print("\n" + "="*60)
        print(f"CAMPEÓN INTERNACIONAL: {champion.name}")
        print("="*60)
        input("\nPress Enter to continue...")

    # ========== SCHEDULING HELPERS ==========

    def _build_season_schedule(self):
        """Create full season calendar: pre-season, league, break, international playoff"""
        schedule = []

        # 1) Pre-season: 10 weeks
        for _ in range(10):
            schedule.append({"phase": "Pretemporada", "fixtures": []})

        # 2) National league: double round robin ( (n-1)*2 weeks )
        league_rounds = self._generate_league_fixtures(self.clubs)
        for idx, fixtures in enumerate(league_rounds, 1):
            schedule.append({"phase": f"Liga Nacional - Jornada {idx}", "fixtures": fixtures})

        # 3) Break between competitions: 5 weeks
        for _ in range(5):
            schedule.append({"phase": "Descanso entre ligas", "fixtures": []})

        # 4) International playoff: 4 weeks (Octavos, Cuartos, Semifinal, Final)
        playoff_rounds = self._generate_international_playoff_rounds()
        round_names = ["Octavos de Final", "Cuartos de Final", "Semifinal", "Final"]
        for name, fixtures in zip(round_names, playoff_rounds):
            schedule.append({"phase": f"Playoff Internacional - {name}", "fixtures": fixtures})

        return schedule

    def _generate_league_fixtures(self, clubs):
        """Generate double round-robin fixtures for the national league"""
        teams = list(clubs)
        if len(teams) % 2 != 0:
            teams.append(None)  # bye week if odd, though we have 10 teams even

        n = len(teams)
        rounds = []
        # Single round robin using circle method
        for r in range(n - 1):
            pairs = []
            for i in range(n // 2):
                t1 = teams[i]
                t2 = teams[n - 1 - i]
                if t1 and t2:
                    # Alternate home/away by round to balance
                    if r % 2 == 0:
                        pairs.append((t1.name, t2.name))
                    else:
                        pairs.append((t2.name, t1.name))
            # rotate teams (except first)
            teams = [teams[0]] + teams[-1:] + teams[1:-1]
            rounds.append(pairs)

        # Double round robin: add reverse fixtures
        reverse_rounds = []
        for fixtures in rounds:
            reverse_rounds.append([(away, home) for home, away in fixtures])

        return rounds + reverse_rounds

    def _generate_international_playoff_rounds(self):
        """Create bracket fixtures for 16-team playoff (6 national top vs 10 international)"""
        # Pick top 6 national by reputation
        national_sorted = sorted(self.clubs, key=lambda c: c.reputation, reverse=True)
        national_top = national_sorted[:6]

        # Take all international clubs (10 provided)
        international = list(self.international_clubs)

        participants = national_top + international
        random.shuffle(participants)

        # Round of 16 pairings
        r16 = []
        for i in range(0, 16, 2):
            home = participants[i]
            away = participants[i + 1]
            r16.append((home.name, away.name))

        # Placeholder fixtures for later rounds will be determined by winners; for schedule we just show slots
        r8 = [("Ganador R16-1", "Ganador R16-2"), ("Ganador R16-3", "Ganador R16-4"),
              ("Ganador R16-5", "Ganador R16-6"), ("Ganador R16-7", "Ganador R16-8")]
        r4 = [("Ganador QF-1", "Ganador QF-2"), ("Ganador QF-3", "Ganador QF-4")]
        r2 = [("Ganador SF-1", "Ganador SF-2")]

        return [r16, r8, r4, r2]

    # ========== LEAGUE TABLE & SIMULATION ==========

    def _init_league_table(self):
        self.league_table = {}
        for c in self.clubs:
            self.league_table[c.name] = {
                "points": 0,
                "played": 0,
                "wins": 0,
                "draws": 0,
                "losses": 0,
                "gf": 0,
                "ga": 0,
                "gd": 0,
            }

    def _simulate_week_fixtures(self, week_index):
        if week_index < 0 or week_index >= len(self.schedule):
            return
        fixtures = self.schedule[week_index].get("fixtures", [])
        phase = self.schedule[week_index].get("phase", "")

        # Only update league table for national league phase
        if not phase.startswith("Liga Nacional"):
            return

        for home_name, away_name in fixtures:
            home = self.club_index.get(home_name)
            away = self.club_index.get(away_name)
            if not home or not away:
                continue

            home_prof = home.get_quick_profile()
            away_prof = away.get_quick_profile()

            # Combine probabilities (simplified): average win prob adjusted
            home_win = (home_prof["win_prob"] + (100 - away_prof["win_prob"])) / 2
            away_win = (away_prof["win_prob"] + (100 - home_prof["win_prob"])) / 2
            draw_prob = (home_prof["draw_prob"] + away_prof["draw_prob"]) / 2
            total = home_win + away_win + draw_prob
            if total == 0:
                continue
            home_win /= total
            draw_prob /= total
            away_win /= total

            outcome = random.random()
            if outcome < home_win:
                result = "home_win"
            elif outcome < home_win + draw_prob:
                result = "draw"
            else:
                result = "away_win"

            def sample_goals(xg):
                return max(0, int(round(random.gauss(xg, 0.9))))

            home_goals = sample_goals(home_prof["xg"])
            away_goals = sample_goals(away_prof["xg"])

            # Align goals with outcome
            if result == "home_win" and home_goals <= away_goals:
                home_goals = away_goals + 1
            if result == "away_win" and away_goals <= home_goals:
                away_goals = home_goals + 1
            if result == "draw":
                away_goals = home_goals

            self._update_league_table(home_name, away_name, home_goals, away_goals)

    def _update_league_table(self, home, away, hg, ag):
        for name in [home, away]:
            if name not in self.league_table:
                return
        ht = self.league_table[home]
        at = self.league_table[away]

        ht["played"] += 1
        at["played"] += 1
        ht["gf"] += hg
        ht["ga"] += ag
        at["gf"] += ag
        at["ga"] += hg
        ht["gd"] = ht["gf"] - ht["ga"]
        at["gd"] = at["gf"] - at["ga"]

        if hg > ag:
            ht["wins"] += 1
            at["losses"] += 1
            ht["points"] += 3
        elif ag > hg:
            at["wins"] += 1
            ht["losses"] += 1
            at["points"] += 3
        else:
            ht["draws"] += 1
            at["draws"] += 1
            ht["points"] += 1
            at["points"] += 1

    def show_league_table(self):
        table = sorted(
            self.league_table.items(),
            key=lambda kv: (kv[1]["points"], kv[1]["gd"], kv[1]["gf"]),
            reverse=True,
        )
        print("\n" + "="*60)
        print("TABLA DE LA LIGA NACIONAL")
        print("="*60)
        print(f"{'Pos':<4}{'Club':<28}{'Pts':>5}{'P':>4}{'W':>4}{'D':>4}{'L':>4}{'GF':>5}{'GA':>5}{'GD':>5}")
        for i, (name, stats) in enumerate(table, 1):
            print(f"{i:<4}{name:<28}{stats['points']:>5}{stats['played']:>4}{stats['wins']:>4}{stats['draws']:>4}{stats['losses']:>4}{stats['gf']:>5}{stats['ga']:>5}{stats['gd']:>5}")
        input("\nPress Enter to continue...")
    
    def advance_week(self):
        """Move to the next week and simulate scheduled fixtures"""
        if self.agent.actions_remaining > 0:
            print(f"\nYou have {self.agent.actions_remaining} actions remaining.")
            confirm = input("Are you sure you want to advance? (yes/no): ").strip().lower()
            if confirm not in ['yes', 'y']:
                return

        # Simulate fixtures for the current week before moving forward
        current_week_index = self.agent.week - 1
        self._simulate_week_fixtures(current_week_index)
        
        # Simulate client participation in their club matches
        self._simulate_client_match_participation(current_week_index)
        
        # Process player growth and contract countdown
        self._process_weekly_player_growth(current_week_index)
        
        # Reset weekly event flag for next week
        self.event_occurred_this_week = False

        self.agent.advance_week()
        print(f"\n{'='*60}")
        print(f"Advancing to Week {self.agent.week}...")
        print(f"{'='*60}")
        
        if self.agent.week > self.total_weeks:
            print("\nSeason complete. Thanks for playing!")
            self._process_season_end_renewals()
            self.running = False
            sys.exit(0)
        input("\nPress Enter to continue...")
    
    def quit_game(self):
        """Exit the game"""
        print("\nThank you for playing Football Agent Simulator!")
        print(f"Final Stats - Week {self.agent.week}")
        print(f"Money: ${self.agent.money:,}")
        print(f"Clients: {len(self.agent.clients)}")
        print("\nYour progress has been saved.")
        self.running = False
        sys.exit(0)

    # ========== CLIENT MATCH PARTICIPATION ==========
    
    def _simulate_client_match_participation(self, week_index: int):
        """Simulate agent clients playing in their club matches this week."""
        if week_index < 0 or week_index >= len(self.schedule):
            return
        
        phase = self.schedule[week_index].get('phase', '')
        if not phase.startswith('Liga Nacional'):
            return
        
        fixtures = self.schedule[week_index].get('fixtures', [])
        
        # Find which clients played this week
        for client in self.agent.clients:
            if not client.club or not client.signed:
                continue
            
            # Check if client's club played this week
            client_played = False
            client_home = False
            opponent_name = None
            
            for home_name, away_name in fixtures:
                if client.club == home_name:
                    client_played = True
                    client_home = True
                    opponent_name = away_name
                    break
                elif client.club == away_name:
                    client_played = True
                    client_home = False
                    opponent_name = home_name
                    break
            
            if not client_played:
                continue
            
            # Simulate match performance
            client.appearances += 1
            
            # Base performance based on position
            position_goal_prob = {
                'Forward': 0.35, 'Striker': 0.35, 'FW': 0.35, 'ST': 0.35,
                'Winger': 0.25, 'Wing Forward': 0.25, 'WF': 0.25,
                'Attacking Midfielder': 0.20, 'AM': 0.20,
                'Midfielder': 0.10, 'Central Midfielder': 0.10, 'CM': 0.10,
                'Defensive Midfielder': 0.05, 'DM': 0.05,
            }
            
            goal_prob = position_goal_prob.get(client.position, 0.08)
            assist_prob = goal_prob * 1.2  # Slightly higher chance of assist
            
            # Goals
            if random.random() < goal_prob:
                goals = 1
                if random.random() < 0.15:  # 15% chance of brace
                    goals = 2
                client.goals += goals
            else:
                goals = 0
            
            # Assists
            if random.random() < assist_prob:
                assists = 1
                if random.random() < 0.10:  # 10% chance of double assist
                    assists = 2
                client.assists += assists
            else:
                assists = 0
            
            # Cards (yellow/red)
            yellow_card = random.random() < 0.12  # 12% chance
            red_card = random.random() < 0.02 if not yellow_card else False  # 2% chance if no yellow
            
            # Match rating (1-10)
            base_rating = 6.0
            rating_bonus = goals * 1.5 + assists * 1.0
            if yellow_card:
                rating_bonus -= 0.3
            if red_card:
                rating_bonus -= 1.5
            
            match_rating = max(1.0, min(10.0, base_rating + rating_bonus + random.uniform(-0.5, 0.5)))
            
            # Show match performance if something noteworthy happened
            if goals > 0 or assists > 0 or yellow_card or red_card:
                print(f"\n⚽ ACTUACIÓN DE {client.name} vs {opponent_name}:")
                if goals > 0:
                    print(f"   🎯 Goles: {goals}")
                if assists > 0:
                    print(f"   🅰️ Asistencias: {assists}")
                if yellow_card:
                    print(f"   🟨 Tarjeta amarilla")
                if red_card:
                    print(f"   🟥 Tarjeta roja")
                print(f"   ⭐ Rating: {match_rating:.1f}/10")
                
                # Morale effect
                if goals >= 2 or (goals >= 1 and assists >= 1):
                    client.morale = "Happy"
                    print(f"   ✓ {client.name} está feliz con su actuación!")
                elif red_card:
                    client.morale = "Unhappy"
                    print(f"   ✗ {client.name} está molesto por la expulsión.")
    
    # ========== PLAYER ROSTER & GROWTH TRACKING ==========

    def _init_club_rosters(self):
        """Initialize simple rosters for tracking growth and renewals"""
        personalities = [
            ('Leader', 'Good'), ('Ambitious', 'Best'), ('Perfectionist', 'Best'),
            ('Resolute', 'Good'), ('Light-Hearted', 'Moderate'), ('Professional', 'Good'),
            ('Team Player', 'Good'), ('Temperamental', 'Bad'), ('Selfish', 'Bad'),
            ('Arrogant', 'Bad'), ('Lazy', 'Bad'),
        ]
        
        for club in self.clubs:
            # Create 11 players per club
            roster = []
            for i in range(11):
                pers, cat = personalities[i % len(personalities)]
                player = {
                    'name': f'{club.name}_Player_{i+1}',
                    'personality': pers,
                    'category': cat,
                    'skill_rating': round(random.uniform(60.0, 85.0), 1),
                    'contract_weeks_remaining': random.randint(20, 80),
                    'cohesion_index': 60.0,
                    'morale': 60.0,
                }
                roster.append(player)
            self.club_rosters[club.name] = roster

    def _process_weekly_player_growth(self, week_index):
        """Process skill growth for all players based on match performance"""
        if week_index < 0 or week_index >= len(self.schedule):
            return
            
        phase = self.schedule[week_index].get('phase', '')
        if not phase.startswith('Liga Nacional'):
            return
            
        fixtures = self.schedule[week_index].get('fixtures', [])
        week_growth_count = 0
        
        # Get client names for filtering output
        client_names = {client.name for client in self.agent.clients}
        
        print("\n" + "="*60)
        print(f"CRECIMIENTO SEMANAL - Semana {self.agent.week}")
        print("="*60)
        
        for home_name, away_name in fixtures:
            home_result = self.league_table.get(home_name, {})
            away_result = self.league_table.get(away_name, {})
            
            # Determinar resultado aproximado para rating_vs_avg
            home_last_gf = home_result.get('gf', 0)
            home_last_ga = home_result.get('ga', 0)
            away_last_gf = away_result.get('gf', 0)
            away_last_ga = away_result.get('ga', 0)
            
            # Simplificación: si GF > GA en histórico reciente, rating positivo
            home_rating_diff = +5 if home_last_gf > home_last_ga else -5 if home_last_gf < home_last_ga else 0
            away_rating_diff = +5 if away_last_gf > away_last_ga else -5 if away_last_gf < away_last_ga else 0
            
            # Process home club roster
            if home_name in self.club_rosters:
                club = self.club_index[home_name]
                for player in self.club_rosters[home_name]:
                    growth_prob = skill_growth_chance(
                        player['personality'],
                        player['category'],
                        rating_vs_team_avg=home_rating_diff,
                        training_quality=club.training_quality
                    )
                    
                    if random.random() < growth_prob:
                        old_rating = player['skill_rating']
                        improvement = round(random.uniform(0.1, 0.3), 1)
                        player['skill_rating'] = min(99.0, player['skill_rating'] + improvement)
                        week_growth_count += 1
                        
                        self.growth_log.append({
                            'week': self.agent.week,
                            'club': home_name,
                            'player': player['name'],
                            'personality': player['personality'],
                            'old_rating': old_rating,
                            'new_rating': player['skill_rating'],
                            'improvement': improvement,
                            'growth_prob': growth_prob,
                        })
                        
                        # Show only if it's an agent client
                        if player['name'] in client_names:
                            print(f"✓ {player['name']} ({player['personality']}): {old_rating} → {player['skill_rating']} (+{improvement}) [prob: {growth_prob:.3f}]")
                    
                    # Countdown contract
                    player['contract_weeks_remaining'] -= 1
            
            # Process away club roster
            if away_name in self.club_rosters:
                club = self.club_index[away_name]
                for player in self.club_rosters[away_name]:
                    growth_prob = skill_growth_chance(
                        player['personality'],
                        player['category'],
                        rating_vs_team_avg=away_rating_diff,
                        training_quality=club.training_quality
                    )
                    
                    if random.random() < growth_prob:
                        old_rating = player['skill_rating']
                        improvement = round(random.uniform(0.1, 0.3), 1)
                        player['skill_rating'] = min(99.0, player['skill_rating'] + improvement)
                        week_growth_count += 1
                        
                        self.growth_log.append({
                            'week': self.agent.week,
                            'club': away_name,
                            'player': player['name'],
                            'personality': player['personality'],
                            'old_rating': old_rating,
                            'new_rating': player['skill_rating'],
                            'improvement': improvement,
                            'growth_prob': growth_prob,
                        })
                        
                        # Show only if it's an agent client
                        if player['name'] in client_names:
                            print(f"✓ {player['name']} ({player['personality']}): {old_rating} → {player['skill_rating']} (+{improvement}) [prob: {growth_prob:.3f}]")
                    
                    # Countdown contract
                    player['contract_weeks_remaining'] -= 1
        
        client_improvements = sum(1 for log in self.growth_log if log['week'] == self.agent.week and log['player'] in client_names)
        if client_improvements == 0:
            print("Ninguno de tus clientes mejoraron esta semana.")
        else:
            print(f"\nTotal de mejoras: {week_growth_count}")
        print("="*60)

    def _process_season_end_renewals(self):
        """Calculate renewal intent for players with expiring contracts"""
        print("\n" + "="*60)
        print("INTENCIÓN DE RENOVACIÓN - FIN DE TEMPORADA")
        print("="*60)
        
        renewal_candidates = []
        
        for club_name, roster in self.club_rosters.items():
            club = self.club_index[club_name]
            club_stats = self.league_table.get(club_name, {})
            
            # Club performance metrics
            club_position = sorted(
                self.league_table.items(),
                key=lambda kv: (kv[1]['points'], kv[1]['gd']),
                reverse=True
            ).index((club_name, club_stats)) + 1
            
            meets_objective = club_position <= 3  # Top 3 = success
            avg_club_rating = sum(p['skill_rating'] for p in roster) / len(roster)
            
            for player in roster:
                # Only consider players with contracts ending soon (< 10 weeks)
                if player['contract_weeks_remaining'] > 10:
                    continue
                    
                performance_diff = player['skill_rating'] - avg_club_rating
                
                renewal_prob = renewal_intent_probability(
                    player['personality'],
                    player['category'],
                    cohesion_index=player['cohesion_index'],
                    meets_objective=meets_objective,
                    performance_diff=performance_diff,
                    player_morale=player['morale']
                )
                
                wants_renewal = random.random() < renewal_prob
                
                renewal_candidates.append({
                    'club': club_name,
                    'player': player['name'],
                    'personality': player['personality'],
                    'weeks_left': player['contract_weeks_remaining'],
                    'renewal_prob': renewal_prob,
                    'wants_renewal': wants_renewal,
                    'cohesion': player['cohesion_index'],
                    'morale': player['morale'],
                    'performance_diff': performance_diff,
                })
                
                self.renewal_log.append(renewal_candidates[-1])
        
        # Display renewal summary
        for candidate in sorted(renewal_candidates, key=lambda x: x['renewal_prob'], reverse=True):
            icon = "✓" if candidate['wants_renewal'] else "✗"
            print(f"{icon} {candidate['player']} ({candidate['club']}) - {candidate['personality']}")
            print(f"   Prob: {candidate['renewal_prob']:.3f} | Cohesión: {candidate['cohesion']:.1f} | Moral: {candidate['morale']:.1f} | Perf diff: {candidate['performance_diff']:+.1f}")
        
        print(f"\nTotal candidatos: {len(renewal_candidates)}")
        want_renew = sum(1 for c in renewal_candidates if c['wants_renewal'])
        print(f"Quieren renovar: {want_renew} ({want_renew/len(renewal_candidates)*100:.1f}%)")
        print("="*60)
        
        # Export logs summary
        self._export_growth_summary()

    def _export_growth_summary(self):
        """Export growth statistics summary"""
        if not self.growth_log:
            return
            
        print("\n" + "="*60)
        print("RESUMEN DE CRECIMIENTO DE LA TEMPORADA")
        print("="*60)
        
        # Top improvers
        by_player = {}
        for entry in self.growth_log:
            key = entry['player']
            if key not in by_player:
                by_player[key] = {'count': 0, 'total_improvement': 0.0, 'personality': entry['personality']}
            by_player[key]['count'] += 1
            by_player[key]['total_improvement'] += entry['improvement']
        
        top_improvers = sorted(
            by_player.items(),
            key=lambda x: x[1]['total_improvement'],
            reverse=True
        )[:10]
        
        print("\nTop 10 Jugadores con Mayor Crecimiento:")
        for player_name, stats in top_improvers:
            print(f"  {player_name} ({stats['personality']}): +{stats['total_improvement']:.1f} en {stats['count']} mejoras")
        
        # By personality
        by_personality = {}
        for entry in self.growth_log:
            pers = entry['personality']
            if pers not in by_personality:
                by_personality[pers] = {'count': 0, 'total': 0.0}
            by_personality[pers]['count'] += 1
            by_personality[pers]['total'] += entry['improvement']
        
        print("\nCrecimiento por Personalidad:")
        for pers, stats in sorted(by_personality.items(), key=lambda x: x[1]['total'], reverse=True):
            avg = stats['total'] / stats['count'] if stats['count'] > 0 else 0
            print(f"  {pers}: {stats['count']} mejoras, promedio +{avg:.2f}")
        
        print("="*60)

def main():
    """Main entry point"""
    game = FootballAgentGame()
    game.start_game()

if __name__ == "__main__":
    main()
