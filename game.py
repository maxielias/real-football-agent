"""
Main game module - Contains the game loop and core mechanics
"""

import sys
from agent import Agent
from player import Player
from game_data import create_initial_players, create_player_reports, get_clubs, get_club_contacts

class FootballAgentGame:
    """Main game class that manages the game state and flow"""
    
    def __init__(self):
        self.agent = None
        self.all_players = []
        self.available_reports = []
        self.clubs = []
        self.club_contacts = {}
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
        self.clubs = get_clubs()
        self.club_contacts = get_club_contacts()
        
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
        print("7. Advance to Next Week")
        print("8. Save & Quit")
        
        choice = input("\nEnter choice (1-8): ").strip()
        
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
            self.advance_week()
        elif choice == "8":
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
        
        if not self.available_reports:
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
        
        print("\nCLUBS WITH CONTACTS:")
        club_list = list(self.club_contacts.keys())
        for i, club in enumerate(club_list, 1):
            contacts = self.club_contacts[club]
            print(f"{i}. {club} - Director: {contacts['director']}, Coach: {contacts['coach']}")
        
        choice = input("\nSelect club to contact (or 0 to cancel): ").strip()
        if choice.isdigit() and 0 < int(choice) <= len(club_list):
            club = club_list[int(choice) - 1]
            contacts = self.club_contacts[club]
            
            print(f"\nContacting {club}")
            print("1. Speak with Director: " + contacts['director'])
            print("2. Speak with Coach: " + contacts['coach'])
            
            contact_choice = input("\nEnter choice (1-2): ").strip()
            
            if contact_choice == "1":
                print(f"\n{contacts['director']}: 'Hello, always good to hear from agents.'")
                print("'We're always looking for talent. Send over your clients' details.'")
                print("\n[Relationship with " + club + " slightly improved]")
                
                # Update relationship
                current = self.agent.club_relationships.get(club, "Neutral")
                if current == "Neutral":
                    self.agent.club_relationships[club] = "Positive"
                    
            elif contact_choice == "2":
                print(f"\n{contacts['coach']}: 'I'm busy with training, but I can spare a minute.'")
                print("'We need players who fit our system. Quality over quantity.'")
                print("\n[You learned more about " + club + "'s needs]")
            else:
                print("\nInvalid choice.")
                self.agent.actions_remaining += 1  # Refund
        else:
            self.agent.actions_remaining += 1  # Refund
        
        input("\nPress Enter to continue...")
    
    def advance_week(self):
        """Move to the next week"""
        if self.agent.actions_remaining > 0:
            print(f"\nYou have {self.agent.actions_remaining} actions remaining.")
            confirm = input("Are you sure you want to advance? (yes/no): ").strip().lower()
            if confirm not in ['yes', 'y']:
                return
        
        self.agent.advance_week()
        print(f"\n{'='*60}")
        print(f"Advancing to Week {self.agent.week}...")
        print(f"{'='*60}")
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

def main():
    """Main entry point"""
    game = FootballAgentGame()
    game.start_game()

if __name__ == "__main__":
    main()
