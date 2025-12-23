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
        self.running = True
        
    def start_game(self):
        """Initialize and start the game"""
        self.show_intro()
        agent_name = input("\nEnter your name: ").strip()
        if not agent_name:
            agent_name = "Agent Smith"
        
        self.agent = Agent(agent_name)
        self.all_players = create_initial_players()
        self.available_reports = create_player_reports()
        self.clubs = get_default_clubs()
        self.international_clubs = get_international_clubs()
        self.schedule = self._build_season_schedule()
        self.total_weeks = len(self.schedule)
        self._init_league_table()
        self.club_index = {c.name: c for c in self.clubs}
        self._init_club_rosters()
        
        print(f"\nWelcome, {agent_name}! Your journey as a football agent begins now.")
        print("You have $50,000 to start your agency.")
        print("Each week, you can perform 5 actions. Choose wisely!")
        input("\nPress Enter to begin...")
        
        self.game_loop()
    
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
    
    def show_main_menu(self):
        """Display main menu and handle user choice"""
        print("\nWhat would you like to do?")
        print("1. View Agent Status")
        print("2. View Clients")
        print("3. Read Scouting Reports (1 action)")
        print("4. Sign New Player (1 action)")
        print("5. Interact with Client (1 action)")
        print("6. Contact Club Staff (1 action)")
        print("7. View League Table")
        print("8. International Playoff (1 action, requiere cliente en club internacional)")
        print("9. Advance to Next Week")
        print("10. Save & Quit")
        
        choice = input("\nEnter choice (1-10): ").strip()
        
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
            self.contact_club_staff()
        elif choice == "7":
            self.show_league_table()
        elif choice == "8":
            self.international_playoff()
        elif choice == "9":
            self.advance_week()
        elif choice == "10":
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
        
        # Process player growth and contract countdown
        self._process_weekly_player_growth(current_week_index)

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
                        
                        print(f"✓ {player['name']} ({player['personality']}): {old_rating} → {player['skill_rating']} (+{improvement}) [prob: {growth_prob:.3f}]")
                    
                    # Countdown contract
                    player['contract_weeks_remaining'] -= 1
        
        if week_growth_count == 0:
            print("No hubo mejoras esta semana.")
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
