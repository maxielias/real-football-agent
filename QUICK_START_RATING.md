# 🚀 Guía Rápida - Sistema de Ratings

## Inicio Rápido (5 minutos)

### 1. Crear un Jugador Simple

```python
from player import Player

# Crear jugador
player = Player("Lionel Messi", 30, "Attacking Midfielder")

# Configurar atributos técnicos (1-20)
player.set_technical_attributes(
    defending=10,      # DEF - Defensa
    aerial=8,          # AER - Juego aéreo
    passing=20,        # PAS - Pase ★★★
    technical=20,      # TEC - Técnica ★★★
    speed=15,          # SPD - Velocidad
    physical=12,       # PHY - Físico
    shooting=18,       # SHO - Disparo ★
    mental=19,         # MEN - Mental
    intelligence=20    # INT - Inteligencia ★★★
)

# Ver ratings
print(f"Rating: {player.current_rating:.2f}")           # 0.95
print(f"Potencial: {player.potential_rating:.2f}")      # 0.98
```

### 2. Ver Perfil Completo

```python
# Ver todos los atributos y ratings
print(player.get_technical_attributes_description())

# Ver perfil resumido
print(player.describe())
```

### 3. Generar Jugador Aleatorio

```python
from player_generator import generate_player

# Generar delantero de élite
striker = generate_player(
    name="Erling Haaland",
    age=23,
    position="Forward",
    quality='excellent',      # poor / average / good / excellent / world_class
    specialist=True           # True = especializado en su posición
)

print(striker.describe())
```

### 4. Generar Equipo Completo

```python
from player_generator import create_squad_by_quality, display_squad_summary

# Generar equipo de calidad 'good'
squad = create_squad_by_quality('good')
display_squad_summary(squad)
```

---

## Comandos Rápidos

### Probar el Sistema
```bash
# Test completo del sistema
python test_rating_system.py

# Generador interactivo
python player_generator.py

# Ver documentación
cat RATING_SYSTEM.md
```

---

## Atributos por Posición

### Delantero (FW) - Prioridades
```python
shooting=19      # ★★★ Máxima prioridad
speed=18         # ★★★ Máxima prioridad
intelligence=18  # ★★★ Máxima prioridad
technical=16     # ★ Importante
```

### Centro Defensivo (CB) - Prioridades
```python
defending=19     # ★★★ Máxima prioridad
aerial=18        # ★★★ Máxima prioridad
intelligence=18  # ★★★ Máxima prioridad
physical=17      # ★ Importante
```

### Mediapunta (AM) - Prioridades
```python
intelligence=20  # ★★★ Máxima prioridad
technical=20     # ★★★ Máxima prioridad
passing=19       # ★ Importante
shooting=17      # ★ Importante
```

### Mediocentro (CM) - Prioridades
```python
intelligence=18  # ★★★ Máxima prioridad
technical=17     # ★★ Muy importante
passing=16       # ★★ Muy importante
mental=16        # ★ Importante
```

---

## Escala de Ratings

| Rating | Nivel | Ejemplos |
|--------|-------|----------|
| **0.95-1.00** | 🌟 World Class | Messi, CR7, Mbappé |
| **0.85-0.95** | 💎 Excellent | De Bruyne, Van Dijk |
| **0.70-0.85** | ⭐ Good | Jugadores top de ligas menores |
| **0.50-0.70** | ✓ Average | Jugadores profesionales estándar |
| **0.35-0.50** | ↓ Poor | División inferior, juveniles |

---

## Clasificación de Atributos

| Valor | Clasificación |
|-------|---------------|
| **18-20** | Excellent ⭐⭐⭐ |
| **15-17** | Good ⭐⭐ |
| **10-14** | Average ⭐ |
| **7-9** | Poor ⚠ |
| **1-6** | Terrible ❌ |

---

## Ejemplo Completo: Crear Cristiano Ronaldo

```python
from player import Player

# Crear jugador
cr7 = Player("Cristiano Ronaldo", 30, "Forward")

# Atributos técnicos
cr7.set_technical_attributes(
    defending=8,       # Poor - No es su fuerte
    aerial=17,         # Good - Excelente cabeza
    passing=14,        # Average
    technical=18,      # Excellent - Gran técnica
    speed=16,          # Good - Rápido
    physical=18,       # Excellent - Muy físico
    shooting=19,       # Excellent - Goleador
    mental=19,         # Excellent - Mentalidad ganadora
    intelligence=18    # Excellent - Gran posicionamiento
)

# Atributos mentales (personalidad)
cr7.set_mental_attributes(
    determination=20,       # Excellent
    leadership=19,          # Excellent
    ambition=18,           # Excellent
    loyalty=16,            # Good
    pressure=19,           # Excellent
    professionalism=20,    # Excellent
    sportsmanship=17,      # Good
    temperament=18         # Excellent
)

# Resultados
print(cr7.describe())
# Rating: 0.89 (Excellent)
# Potential: 0.96 (World Class potential)
# Personality: Model Citizen (Best)
# Best Positions: FW (0.89), AM (0.88), WF (0.86)
```

---

## Análisis de Versatilidad

```python
# Ver mejores 3 posiciones
best_positions = player.get_best_positions(3)
for pos, rating in best_positions:
    print(f"{pos}: {rating:.2f}")

# Ver rating en todas las posiciones
for pos in ['FB', 'CB', 'WB', 'DM', 'SM', 'CM', 'WF', 'AM', 'FW']:
    rating = player.position_rating[pos]
    print(f"{pos}: {rating:.2f}")
```

---

## Generar por Calidad

```python
from player_generator import generate_player

# Poor (0.35-0.50)
poor_player = generate_player("Young Prospect", 17, "Forward", 'poor')

# Average (0.50-0.70)
avg_player = generate_player("Squad Player", 25, "Midfielder", 'average')

# Good (0.70-0.85)
good_player = generate_player("Starter", 26, "Center Back", 'good')

# Excellent (0.85-0.95)
elite_player = generate_player("Star", 27, "Attacking Midfielder", 'excellent')

# World Class (0.95-1.00)
worldclass = generate_player("Superstar", 28, "Forward", 'world_class')
```

---

## Tips Útiles

### ✅ Para Delanteros
- Prioriza: Shooting (19+), Speed (17+), Intelligence (17+)
- Ignora: Defending, Aerial (a menos que juegue como target man)

### ✅ Para Defensas
- Prioriza: Defending (18+), Intelligence (17+), Physical (16+)
- Para CB: Aerial (17+) es crítico
- Para FB/WB: Speed (15+) es importante

### ✅ Para Mediocampistas
- Prioriza: Intelligence (17+), Technical (16+), Passing (15+)
- Para DM: Defending (14+) adicional
- Para AM: Shooting (15+) adicional

### ✅ Para Crear Versátiles
- Balancea todos los atributos (12-15)
- No especialices demasiado
- Intelligence alto ayuda en todas las posiciones

---

## Integración con Personalidad

```python
# Sistema completo: Ratings + Personalidad
player = Player("Complete Player", 25, "Midfielder")

# Técnicos
player.set_technical_attributes(
    defending=14, aerial=12, passing=16, technical=17,
    speed=15, physical=14, shooting=13, mental=16, intelligence=17
)

# Mentales (personalidad)
player.set_mental_attributes(
    determination=17, leadership=16, ambition=16, loyalty=15,
    pressure=17, professionalism=18, sportsmanship=16, temperament=16
)

# Ver todo
print(player.describe())
# Muestra: Ratings, Mejores posiciones, Atributos clave, Personalidad
```

---

## 🎯 Comenzar Ahora

```bash
# Método 1: Generador interactivo
python player_generator.py

# Método 2: Tests
python test_rating_system.py

# Método 3: Python interactivo
python
>>> from player import Player
>>> p = Player("Test", 25, "Forward")
>>> p.set_technical_attributes(shooting=20, speed=19, intelligence=18)
>>> print(p.current_rating)
```

---

**¡Listo para usar!** 🚀

Para más detalles, consulta:
- [RATING_SYSTEM.md](RATING_SYSTEM.md) - Documentación completa
- [RATING_IMPLEMENTATION.md](RATING_IMPLEMENTATION.md) - Detalles de implementación
