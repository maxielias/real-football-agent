"""
Personality Impact module - loads configuration and provides helper functions
for team cohesion, conflict probability, and performance influence.
"""

import json
import os
import random
from typing import Dict, Optional, List

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'data', 'personality_impacts.json')


def _load_config() -> Dict:
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


_CONFIG = _load_config()
_LEVELS = _CONFIG['levels']
_DEFAULTS = _CONFIG['defaults']
_PERSONALITIES = _CONFIG['personalities']
_ALIAS = _CONFIG['performance_alias']
_CAPS = _CONFIG['caps']
_DEV = _CONFIG['development']
_RENEW = _CONFIG['renewal']


def get_profile(personality_name: str, category: Optional[str] = None) -> Dict:
    """Return impact profile (levels) for a personality, falling back to category defaults."""
    p = _PERSONALITIES.get(personality_name)
    if p:
        perf_level = p.get('performance_level')
        if perf_level in _ALIAS:
            perf_level = _ALIAS[perf_level]
        return {
            'performance': _LEVELS.get(perf_level, _LEVELS['Moderate']),
            'cohesion': _LEVELS.get(p.get('cohesion_level', 'Moderate'), _LEVELS['Moderate']),
            'conflict': _LEVELS.get(p.get('conflict_level', 'Medium'), _LEVELS['Medium']),
        }
    # fallback to category defaults
    cat = category or 'Neutral'
    defaults = _DEFAULTS.get(cat, _DEFAULTS['Neutral'])
    perf_level = defaults['performance_level']
    return {
        'performance': _LEVELS.get(perf_level, _LEVELS['Moderate']),
        'cohesion': _LEVELS.get(defaults['cohesion_level'], _LEVELS['Moderate']),
        'conflict': _LEVELS.get(defaults['conflict_level'], _LEVELS['Medium']),
    }


def performance_multiplier(personality_name: str, category: Optional[str] = None) -> float:
    """Compute small performance multiplier for a match, bounded by caps."""
    prof = _PERSONALITIES.get(personality_name)
    level_map = get_profile(personality_name, category)
    # Special handling for 'Unpredictable'
    if prof and prof.get('performance_level') == 'Unpredictable':
        # 10% spike, 10% dip, else normal around 0 within caps
        r = random.random()
        if r < 0.10:
            delta = _CAPS['performance_max']
        elif r < 0.20:
            delta = _CAPS['performance_min']
        else:
            delta = max(_CAPS['performance_min'], min(_CAPS['performance_max'], random.gauss(0.0, 0.01)))
        return delta
    # Normal mapping
    delta = level_map['performance']['performance']
    return max(_CAPS['performance_min'], min(_CAPS['performance_max'], delta))


def weekly_cohesion_delta(starters: List[Dict]) -> float:
    """Compute weekly cohesion delta from starters' profiles.
    starters: list of dicts with keys {'personality_name', 'category'}
    """
    if not starters:
        return 0.0
    total = 0.0
    for s in starters:
        prof = get_profile(s.get('personality_name', ''), s.get('category'))
        total += prof['cohesion']['cohesion']
    avg = total / max(1, len(starters))
    # cap weekly
    return max(-_CAPS['cohesion_weekly_cap'], min(_CAPS['cohesion_weekly_cap'], avg))


def weekly_conflict_probability(personality_name: str, category: Optional[str] = None) -> float:
    """Compute probability of conflict event for a player in a given week."""
    base = _CAPS['conflict_base_weekly']
    prof = get_profile(personality_name, category)
    extra = prof['conflict']['conflict']
    return max(0.0005, min(0.010, base + extra))


def skill_growth_chance(personality_name: str,
                        category: Optional[str] = None,
                        rating_vs_team_avg: float = 0.0,
                        training_quality: int = 12) -> float:
    """Weekly probability of skill improvement.
    - Base from development weekly per level (mapped from performance level).
    - Boosts: positive performance diff (>= +5) adds small bonus; negative lowers.
    - Training quality (1-20) scaled by small factor.
    """
    prof = _PERSONALITIES.get(personality_name)
    perf_level = None
    if prof:
        perf_level = prof.get('performance_level')
        if perf_level in _ALIAS:
            perf_level = _ALIAS[perf_level]
    if not perf_level:
        perf_level = _DEFAULTS.get(category or 'Neutral', _DEFAULTS['Neutral'])['performance_level']

    base = _DEV['weekly_base'].get(perf_level, _DEV['weekly_base']['Moderate'])
    boost = 0.0
    if rating_vs_team_avg >= 5.0:
        boost += _DEV['boosts']['positive_performance']
    elif rating_vs_team_avg <= -5.0:
        boost += _DEV['boosts']['negative_performance']
    # training scaling
    boost += (max(1, min(20, training_quality)) - 10) * _DEV['boosts']['training_quality_scale']
    prob = base + boost
    return max(_DEV['caps']['weekly_min'], min(_DEV['caps']['weekly_max'], prob))


def renewal_intent_probability(personality_name: str,
                               category: Optional[str] = None,
                               cohesion_index: float = 60.0,
                               meets_objective: bool = False,
                               performance_diff: float = 0.0,
                               player_morale: float = 60.0) -> float:
    """Probability the player wants to renew, based on personality and happiness metrics.
    Returns a probability in [min, max]. Intended to be evaluated near contract end.
    """
    base = _RENEW['base_by_personality'].get(personality_name)
    if base is None:
        cat = category or 'Neutral'
        base = _RENEW['base_by_category'].get(cat, 0.06)

    w = _RENEW['weights']
    delta = 0.0
    # Normalize indices
    delta += (cohesion_index - 50.0) * w['cohesion_index']  # above average adds
    delta += (w['meets_objective'] if meets_objective else -w['meets_objective'])
    delta += performance_diff * w['performance_diff']
    delta += (player_morale - 50.0) * w['player_morale']

    prob = base + delta
    return max(_RENEW['caps']['min'], min(_RENEW['caps']['max'], prob))


def team_morale_delta(result: str, meets_objective: bool, cohesion_monthly_change: float) -> float:
    """Return team morale delta based on result, objective status and cohesion trend.
    result: 'win'|'draw'|'loss'
    cohesion_monthly_change: accumulated change in the last ~4 weeks
    """
    delta = 0.0
    if result == 'win':
        delta += 0.8
    elif result == 'draw':
        delta += 0.2
    elif result == 'loss':
        delta -= 0.8
    if meets_objective:
        delta += 0.3
    else:
        delta -= 0.3
    if cohesion_monthly_change > 0.005:  # ~+0.5%
        delta += 0.2
    elif cohesion_monthly_change < -0.005:
        delta -= 0.2
    return max(-3.0, min(3.0, delta))


def player_morale_delta(rating_vs_team_avg: float, personality_name: str) -> float:
    """Return per-player morale delta based on rating diff and personality."""
    delta = 0.0
    if rating_vs_team_avg >= 5.0:
        delta += 0.5
        if personality_name in ('Ambitious', 'Perfectionist', 'Resolute'):
            delta += 0.1
    elif rating_vs_team_avg <= -5.0:
        delta -= 0.5
        if personality_name in ('Lazy', 'Unambitious'):
            delta -= 0.1
    # Clamp monthly per player
    return max(-4.0, min(4.0, delta))


if __name__ == '__main__':
    # Simple demo
    demo_players = [
        {'personality_name': 'Leader', 'category': 'Good'},
        {'personality_name': 'Temperamental', 'category': 'Bad'},
        {'personality_name': 'Ambitious', 'category': 'Best'},
        {'personality_name': 'Unknown', 'category': 'Neutral'},
    ]
    print('Weekly cohesion delta (XI):', weekly_cohesion_delta(demo_players))
    for p in demo_players:
        name = p['personality_name']
        print(name, 'perf_mult:', performance_multiplier(name, p['category']), 'conflict_prob:', weekly_conflict_probability(name, p['category']))
    # Growth & renewal examples
    print('Growth Leader:', skill_growth_chance('Leader', 'Good', rating_vs_team_avg=6, training_quality=16))
    print('Renew Ambitious:', renewal_intent_probability('Ambitious', 'Best', cohesion_index=70, meets_objective=True, performance_diff=6, player_morale=72))
