"""
Game data module - Contains initial game data like players, clubs, etc.
"""

import random

from player import Player
from club import Club

_cached_players = []  # Used so reports match the generated players


def get_default_clubs():
    """Return list of 10 default clubs with all required information"""
    clubs = [
        Club("Atlético General Belgrano", "Campeón / Top 3", "4-3-3", "Presion alta", "Ricardo Gareca"),
        Club("Real Porteño FC", "Campeón / Top 3", "4-2-3-1", "Posesion", "Gabriel Milito"),
        Club("Juventud Unida de Cuyo", "Clasificación Libertadores", "4-3-1-2", "Ataque", "Eduardo Domínguez"),
        Club("Estudiantes del Sur", "Clasificación Libertadores", "4-4-2", "Ataque", "Gustavo Alfaro"),
        Club("Huracán del Litoral", "Clasificación Sudamericana", "4-4-1-1", "Contraataque", "Diego Martínez"),
        Club("Sporting Club de la Sierra", "Clasificación Sudamericana", "3-5-2", "Posesion", "Fernando Gago"),
        Club("Unión Ferroviaria de Junín", "Mitad de Tabla", "4-1-4-1", "Presion alta", "Frank Kudelka"),
        Club("Defensores de Malvinas", "Mitad de Tabla", "4-4-2", "Contraataque", "Julio César Falcioni"),
        Club("Deportivo Riachuelo", "No Descender", "5-3-2", "Defensivo", "Leonardo Madelón"),
        Club("S. y D. Pampa Central", "No Descender", "5-4-1", "Catenaccio", "Ricardo Zielinski"),
    ]
    return clubs


def get_international_clubs():
    """Return list of international clubs for playoff competitions"""
    # Map reputation from 1-5 scale to 1-100 scale (multiply by 20)
    international_clubs = [
        Club("Nacional de Montevideo", "Playoff Internacional", "4-3-3", "Presion alta", "Martín Lasarte", 
             is_international=True, country="Uruguay", reputation=100),  # 5/5 = 100
        Club("Unión de Santiago", "Playoff Internacional", "4-3-3", "Posesion", "Manuel Pellegrini",
             is_international=True, country="Chile", reputation=80),  # 4/5 = 80
        Club("Atlético Guayaquil", "Playoff Internacional", "4-2-3-1", "Ataque", "Álex Aguinaga",
             is_international=True, country="Ecuador", reputation=80),  # 4/5 = 80
        Club("Independiente de Medellín", "Playoff Internacional", "4-3-1-2", "Ataque", "H. Darío Gómez",
             is_international=True, country="Colombia", reputation=80),  # 4/5 = 80
        Club("Alianza de Bogotá", "Playoff Internacional", "4-4-2", "Contraataque", "Alberto Gamero",
             is_international=True, country="Colombia", reputation=80),  # 4/5 = 80
        Club("Deportivo Asunción", "Playoff Internacional", "4-4-2", "Defensivo", "Francisco Arce",
             is_international=True, country="Paraguay", reputation=60),  # 3/5 = 60
        Club("Sporting Lima", "Playoff Internacional", "4-2-3-1", "Posesion", "Juan Reynoso",
             is_international=True, country="Perú", reputation=60),  # 3/5 = 60
        Club("Libertad de Quito", "Playoff Internacional", "3-5-2", "Presion alta", "Jorge Célico",
             is_international=True, country="Ecuador", reputation=60),  # 3/5 = 60
        Club("Real Potosino", "Playoff Internacional", "4-4-2", "Contraataque", "Erwin Sánchez",
             is_international=True, country="Bolivia", reputation=40),  # 2/5 = 40
        Club("Caracas Real", "Playoff Internacional", "4-5-1", "Catenaccio", "Noel Sanvicente",
             is_international=True, country="Venezuela", reputation=40),  # 2/5 = 40
    ]
    return international_clubs


def _rand_attr(base=12, spread=4):
    """Generate a random attribute between 1-20 using a normal-like spread."""
    return max(1, min(20, int(random.gauss(base, spread))))


def _generate_random_player():
    """Create a single random player with technical and mental attributes."""
    first_names = ["Juan", "Pedro", "Luis", "Carlos", "Miguel", "Diego", "Andrés", "Sergio"]
    last_names = ["García", "López", "Martínez", "Rodríguez", "Pérez", "Sánchez", "Torres", "Ramírez"]
    positions = [
        "Forward", "Attacking Midfielder", "Winger", "Central Midfielder",
        "Defensive Midfielder", "Center Back", "Full Back", "Wing Back"
    ]

    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    age = random.randint(17, 29)
    position = random.choice(positions)

    player = Player(name, age, position)

    # Technical attributes
    player.set_technical_attributes(
        defending=_rand_attr(),
        aerial=_rand_attr(),
        passing=_rand_attr(),
        technical=_rand_attr(),
        speed=_rand_attr(),
        physical=_rand_attr(),
        shooting=_rand_attr(),
        mental=_rand_attr(),
        intelligence=_rand_attr(),
    )

    # Mental attributes (personality)
    player.set_mental_attributes(
        determination=_rand_attr(13, 3),
        leadership=_rand_attr(12, 3),
        ambition=_rand_attr(13, 3),
        loyalty=_rand_attr(12, 3),
        pressure=_rand_attr(12, 3),
        professionalism=_rand_attr(12, 3),
        sportsmanship=_rand_attr(12, 3),
        temperament=_rand_attr(12, 3),
    )
    
    # Concentration attribute
    player.set_concentration(_rand_attr(12, 3))

    # Recalculate ratings now that mental attributes are set
    player.calculate_ratings()

    # Overall scores (0-100 scale)
    overall_current = int(round(player.current_rating * 100))
    potential_min = min(100, overall_current + 1)
    player.potential_overall_score = random.randint(potential_min, 100)
    player.current_overall_score = overall_current

    # Transfer value rough estimate
    player.transfer_value = max(10000, player.current_overall_score * 500)

    return player


def _format_report(player: Player) -> str:
    """Build a compact scouting report with numeric data only."""
    lines = []
    lines.append(f"PLAYER: {player.name} | Age: {player.age} | Position: {player.position}")
    lines.append(f"Overall: {player.current_overall_score}/100 | Potential: {player.potential_overall_score}/100")
    main_pos_key = Player.POSITION_MAP.get(player.position, 'AVG')
    main_rating = player.position_rating.get(main_pos_key, player.current_rating) * 100
    lines.append(f"Main Position Rating ({main_pos_key}): {main_rating:.1f}/100")
    lines.append("")
    lines.append("TECHNICAL ATTRIBUTES (1-20):")
    lines.append(
        f"DEF {player.defending:2d} | AER {player.aerial:2d} | PAS {player.passing:2d} | "
        f"TEC {player.technical:2d} | SPD {player.speed:2d} | PHY {player.physical:2d} | "
        f"SHO {player.shooting:2d} | MEN {player.mental:2d} | INT {player.intelligence:2d}"
    )
    lines.append("")
    lines.append("MENTAL ATTRIBUTES (1-20):")
    lines.append(
        f"DET {player.determination:2d} | LDR {player.leadership:2d} | AMB {player.ambition:2d} | "
        f"LOY {player.loyalty:2d} | PRE {player.pressure:2d} | PRO {player.professionalism:2d} | "
        f"SPM {player.sportsmanship:2d} | TMP {player.temperament:2d}"
    )
    lines.append("")
    lines.append(f"PERSONALITY: {player.personality}")
    lines.append(f"MEDIA HANDLING: {player.media_handling}")
    lines.append(f"CONCENTRATION: {player.concentration:2d}")
    return "\n".join(lines)


def create_initial_players():
    """Create a pool of initial players for the game (now 3 random players)."""
    global _cached_players
    _cached_players = [_generate_random_player() for _ in range(3)]
    return list(_cached_players)


def create_player_reports():
    """Create scouting reports based on the current generated players."""
    players = _cached_players if _cached_players else create_initial_players()
    reports = []
    for p in players:
        preview = (
            f"{p.name} | {p.position} | Overall {p.current_overall_score}/100 | "
            f"Potential {p.potential_overall_score}/100"
        )
        reports.append(
            {
                "player_name": p.name,
                "preview": preview,
                "full_report": _format_report(p),
            }
        )
    return reports

def get_clubs():
    """Return list of clubs in the game"""
    return [
        "FC Valencia",
        "Athletic Bilbao", 
        "AS Roma",
        "Manchester United",
        "Bayern Munich",
        "Paris Saint-Germain",
        "Ajax Amsterdam",
        "Porto FC",
        "Celtic FC",
        "Sporting Lisbon"
    ]

def get_club_contacts():
    """Return club staff members for interactions"""
    contacts = {
        "FC Valencia": {
            "director": "Carlos Mendez",
            "coach": "Miguel Torres"
        },
        "Athletic Bilbao": {
            "director": "Inaki Azpilicueta",
            "coach": "Javier Clemente"
        },
        "AS Roma": {
            "director": "Giancarlo Rossi",
            "coach": "Roberto Mancini"
        },
        "Manchester United": {
            "director": "David Gill",
            "coach": "Thomas Edwards"
        },
        "Bayern Munich": {
            "director": "Karl-Heinz Rummenigge",
            "coach": "Hans-Dieter Flick"
        },
        "Paris Saint-Germain": {
            "director": "Leonardo Araújo",
            "coach": "Christophe Galtier"
        },
        "Ajax Amsterdam": {
            "director": "Marc Overmars",
            "coach": "Erik ten Hag"
        },
        "Porto FC": {
            "director": "António Silva",
            "coach": "João Santos"
        },
        "Celtic FC": {
            "director": "Peter Lawwell",
            "coach": "Brendan Rodgers"
        },
        "Sporting Lisbon": {
            "director": "Hugo Viana",
            "coach": "Rúben Amorim"
        }
    }
    return contacts
