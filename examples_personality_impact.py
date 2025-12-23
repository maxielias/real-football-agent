from personality_impact import (
    weekly_cohesion_delta,
    performance_multiplier,
    weekly_conflict_probability,
)

# Example XI with mixed personalities
starters = [
    {'personality_name': 'Leader', 'category': 'Good'},
    {'personality_name': 'Ambitious', 'category': 'Best'},
    {'personality_name': 'Perfectionist', 'category': 'Good'},
    {'personality_name': 'Resolute', 'category': 'Good'},
    {'personality_name': 'Driven', 'category': 'Good'},
    {'personality_name': 'Light-Hearted', 'category': 'Neutral'},
    {'personality_name': 'Lazy', 'category': 'Bad'},
    {'personality_name': 'Temperamental', 'category': 'Worst'},
    {'personality_name': 'Unambitious', 'category': 'Bad'},
    {'personality_name': 'Unknown', 'category': 'Neutral'},
    {'personality_name': 'Unknown', 'category': 'Neutral'},
]

print('Cohesion weekly delta:', weekly_cohesion_delta(starters))

for s in starters[:6]:
    name = s['personality_name']
    cat = s['category']
    pm = performance_multiplier(name, cat)
    cp = weekly_conflict_probability(name, cat)
    print(f"{name} ({cat}): perf_mult={pm:.4f}, conflict_prob={cp:.4f}")
