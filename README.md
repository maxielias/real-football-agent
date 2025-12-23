# Football Agent Simulator

An immersive text-based game where you play as a football (soccer) agent, managing player careers and building your agency's reputation and wealth.

## Game Overview

As a football agent, your goal is to:
- Scout and sign talented players as clients
- Develop their careers through guidance and support
- Negotiate contracts with clubs
- Build relationships with club directors and coaches
- Earn money through commissions
- Grow your reputation in the football world

## Key Features

### Player Rating System
Advanced position-based rating system with 9 technical attributes (1-20 scale):
- **9 Technical Attributes**: Defending, Aerial, Passing, Technical, Speed, Physical, Shooting, Mental, Intelligence
- **Position-Specific Weights**: Each position values attributes differently
- **Current & Potential Ratings**: Track player quality and growth potential
- **Versatility Analysis**: See how players perform in different positions
- **9 Positions Supported**: FB, CB, WB, DM, SM, CM, WF, AM, FW

See [RATING_SYSTEM.md](RATING_SYSTEM.md) for detailed information about the rating system.

### Player Personality System
Each player has a unique personality based on their mental attributes (1-20 scale):
- **8 Mental Attributes**: Determination, Leadership, Ambition, Loyalty, Pressure, Professionalism, Sportsmanship, Temperament
- **5 Personality Categories**: Best, Good, Neutral, Bad, Worst
- **30+ Different Personalities**: From Model Citizen to Temperamental
- Personalities influence player development, behavior, and career decisions

See [PERSONALITY_SYSTEM.md](PERSONALITY_SYSTEM.md) for detailed information about the personality system.

### Turn-Based Gameplay
Each week you have **5 actions** to use wisely:
- Read scouting reports on potential clients
- Sign new players (requires signing bonus)
- Interact with clients (counseling, advice, support)
- Contact club staff (directors, coaches)
- Build relationships and reputation

### Dynamic Player Development
- Players grow and develop over time
- Your interactions affect their morale and trust
- Contract management and negotiations
- Performance tracking (appearances, goals, assists)

## How to Play

### Requirements
- Python 3.6 or higher

### Running the Game

```bash
python3 main.py
```

Or:

```bash
python3 game.py
```

### Gameplay Tips

1. **Start Small**: Begin with affordable young prospects rather than expensive established players
2. **Read Reports**: Use actions to read scouting reports - knowledge is power
3. **Build Trust**: Regular interactions with clients improve their trust and morale
4. **Manage Resources**: Balance action points, money, and time effectively
5. **Network**: Build relationships with clubs to create opportunities for your clients
6. **Long-Term Thinking**: Young players with high potential can become very valuable

### Game Actions

- **View Agent Status**: Check your money, reputation, and clients (free)
- **View Clients**: See detailed information about your signed players (free)
- **Read Scouting Reports**: Learn about available players (1 action)
- **Sign New Player**: Add a player to your client roster (1 action + signing bonus)
- **Interact with Client**: Counsel, advise, or support your clients (1 action)
- **Contact Club Staff**: Network with directors and coaches (1 action)
- **Advance to Next Week**: Progress time and earn commissions (free)

### Earning Money

- **Weekly Commissions**: Earn 5% of each signed client's weekly wage
- **Transfer Commissions**: Earn when clients sign new contracts (coming soon)
- **Performance Bonuses**: Additional earnings based on client success (coming soon)

## Game Structure

The game consists of several modules:

- `main.py` - Entry point for the game
- `game.py` - Main game loop and mechanics
- `agent.py` - Agent (player character) class
- `player.py` - Football player class with text-based attributes and personality system
- `game_data.py` - Initial players, clubs, and scouting reports
- `player_generator.py` - Tool to generate players with rating system
- `test_rating_system.py` - Test script for the rating system
- `test_personality.py` - Test script for the personality system
- `personality_generator.py` - Interactive tool to generate players with personalities
- `RATING_SYSTEM.md` - Complete documentation of the rating system
- `PERSONALITY_SYSTEM.md` - Complete documentation of the personality system

## Testing the Systems

### Rating System

Run the rating system test suite to see examples of different player types:

```bash
python test_rating_system.py
```

Or use the interactive player generator:

```bash
python player_generator.py
```

The generator allows you to:
- Generate random players with realistic attributes
- Create full squads by quality level (poor, average, good, excellent, world class)
- Manually create players with specific attributes

### Personality System

Run the personality test suite to see examples of all personality types:

```bash
python test_personality.py
```

Or use the interactive personality generator:

```bash
python personality_generator.py
```

The interactive generator allows you to:
- Generate random players with personalities
- Create a full squad and analyze personality distribution
- Manually set mental attributes and see the resulting personality

## Development

This is a Python-based text game with no external dependencies. All game logic is self-contained.

## Future Enhancements

Potential features for future versions:
- Save/load game functionality
- More detailed contract negotiations
- Player transfers between clubs
- Reputation system affecting available players
- Random events and storylines
- More clubs and league systems
- Retirement and end-game conditions

## License

Open source - feel free to modify and extend!

## Credits

Created as a game design project focusing on text-based attribute systems and turn-based gameplay mechanics.
