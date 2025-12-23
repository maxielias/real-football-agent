# Personality Impact Config

This folder defines small percentage effects for player personalities.

## File
- `data/personality_impacts.json`
  - `levels`: numeric values for performance, cohesion, conflict.
  - `defaults`: fallback per category (Best/Good/Neutral/Bad/Worst).
  - `personalities`: explicit overrides for named personalities.
  - `performance_alias`: mapping for textual labels to levels.
  - `caps`: safety bounds.

## Usage
Import helpers from `personality_impact.py`:

```python
from personality_impact import (
    get_profile,
    performance_multiplier,
    weekly_cohesion_delta,
    weekly_conflict_probability,
    team_morale_delta,
    player_morale_delta,
)
```

### Examples
- See `examples_personality_impact.py` for a quick demo.

### Tuning
- Adjust small percentages in `data/personality_impacts.json`.
- Keep effects small: performance in ±3%, cohesion per-week ≤ 0.6%, conflict weekly ≤ 1%.
- Use `defaults` for entire categories; add specific personalities under `personalities`.

### Notes
- Unpredictable performance uses random spikes/dips within caps.
- Average maps to Moderate.
- Conflict probability is base (0.1% weekly) plus personality extra.
