# Sistema de Ratings por Posición

## Descripción General

El sistema de ratings calcula el puntaje de un jugador basado en **9 atributos técnicos** (escala 1-20) ponderados según su posición. Cada posición valora diferentes atributos de manera distinta.

## Atributos Técnicos

Cada jugador tiene 9 atributos técnicos en escala 1-20:

| Atributo | Código | Descripción |
| ---------- | -------- | ------------- |
| **Defending** | DEF | Capacidad defensiva, tackles, marcaje |
| **Aerial** | AER | Juego aéreo, cabezazos |
| **Passing** | PAS | Precisión y visión de pase |
| **Technical** | TEC | Habilidad técnica, control de balón |
| **Speed** | SPD | Velocidad y aceleración |
| **Physical** | PHY | Fuerza física, resistencia |
| **Shooting** | SHO | Precisión y potencia de tiro |
| **Mental** | MEN | Fortaleza mental en el juego |
| **Intelligence** | INT | Inteligencia táctica, posicionamiento |

### Clasificaciones

| Rating | Clasificación |
| -------- | --------------- |
| 1-6 | **Terrible** |
| 7-9 | **Poor** |
| 10-14 | **Average** |
| 15-17 | **Good** |
| 18-20 | **Excellent** |

## Posiciones y Ponderadores

El sistema soporta **9 posiciones principales**, cada una con ponderadores específicos:

### Posiciones Defensivas

#### **CB (Center Back / Centro de Defensa)**

- **Prioridades**: Defending (1.10%), Aerial (0.83%), Intelligence (1.59%)
- **Menos importante**: Shooting (0.00%), Technical (0.08%)
- **Características**: Especialista en defensa aérea y terrestre

#### **FB (Full Back / Lateral)**

- **Prioridades**: Intelligence (1.23%), Speed (0.99%), Defending (0.77%)
- **Menos importante**: Shooting (0.00%), Aerial (0.02%)
- **Características**: Combinación de defensa y velocidad

#### **WB (Wing Back / Carrilero)**

- **Prioridades**: Speed (1.26%), Intelligence (0.98%), Physical (0.71%)
- **Menos importante**: Shooting (0.01%), Aerial (0.00%)
- **Características**: Muy ofensivo, prioriza velocidad

### Posiciones de Mediocampo

#### **DM (Defensive Midfielder / Mediocentro Defensivo)**

- **Prioridades**: Intelligence (1.66%), Mental (0.93%), Defending (0.75%)
- **Menos importante**: Aerial (0.01%), Shooting (0.09%)
- **Características**: Cerebro defensivo del equipo

#### **CM (Central Midfielder / Mediocentro)**

- **Prioridades**: Intelligence (1.62%), Technical (0.95%), Mental (0.77%)
- **Menos importante**: Aerial (0.00%), Shooting (0.05%)
- **Características**: Organizador y creador de juego

#### **SM (Side Midfielder / Interior)**

- **Prioridades**: Technical (1.03%), Intelligence (1.06%), Speed (0.90%)
- **Menos importante**: Defending (0.13%), Aerial (0.00%)
- **Características**: Creativo desde los costados

### Posiciones Ofensivas

#### **WF (Wing Forward / Extremo)**

- **Prioridades**: Speed (1.44%), Technical (1.23%), Shooting (1.11%)
- **Menos importante**: Defending (0.00%), Aerial (0.08%)
- **Características**: Velocidad y desborde

#### **AM (Attacking Midfielder / Mediapunta)**

- **Prioridades**: Intelligence (1.78%), Technical (1.40%), Passing (0.45%)
- **Menos importante**: Defending (0.00%), Aerial (0.00%)
- **Características**: Enganche, creador de juego ofensivo

#### **FW (Forward / Delantero)**

- **Prioridades**: Intelligence (1.23%), Speed (0.94%), Technical (0.79%)
- **Menos importante**: Defending (0.00%), Passing (0.09%)
- **Características**: Finalizador, goleador

## Cálculo de Ratings

### Current Rating (Rating Actual)

```text
Rating = Σ (Atributo × Ponderador de Posición)
```

Ejemplo para un CM con todos los atributos en 15:

```text
Rating = (15 × 0.0027) + (15 × 0.0000) + (15 × 0.0061) + 
                 (15 × 0.0095) + (15 × 0.0035) + (15 × 0.0039) + 
                 (15 × 0.0005) + (15 × 0.0077) + (15 × 0.0162)
             = 0.75
```

### Potential Rating (Rating Potencial)

El rating potencial se calcula como:

- **Mínimo**: Current Rating + 0.01
- **Máximo**: Basado en el potencial teórico con mejora de atributos
- Se añade aleatoriedad para simular variabilidad en desarrollo

### Overall Rating (Rating General)

Calculado usando los ponderadores AVG (promedio de todas las posiciones):

```text
AVG Weights:
- DEF: 0.39%, AER: 0.14%, PAS: 0.37%
- TEC: 0.76%, SPD: 0.80%, PHY: 0.48%
- SHO: 0.10%, MEN: 0.64%, INT: 1.33%
```

### Rating Máximo Posible

Con todos los atributos en 20, el rating máximo es **1.00** para cualquier posición.

## Uso del Sistema

### Crear Jugador y Establecer Atributos

```python
from player import Player

# Crear jugador
player = Player("Lionel Messi", 24, "Attacking Midfielder")

# Establecer atributos técnicos
player.set_technical_attributes(
    defending=10,
    aerial=8,
    passing=19,
    technical=20,
    speed=15,
    physical=11,
    shooting=17,
    mental=18,
    intelligence=19
)

# Los ratings se calculan automáticamente
print(f"Rating Actual: {player.current_rating:.2f}")
print(f"Rating Potencial: {player.potential_rating:.2f}")
```

### Ver Atributos y Ratings

```python
# Ver todos los atributos técnicos
print(player.get_technical_attributes_description())

# Ver perfil completo
print(player.describe())

# Ver mejores posiciones
best_positions = player.get_best_positions(3)
for pos, rating in best_positions:
    print(f"{pos}: {rating:.2f}")
```

### Generar Jugadores Aleatorios

```python
from player_generator import generate_player

# Generar jugador de calidad específica
player = generate_player(
    name="Carlos Silva",
    age=25,
    position="Center Back",
    quality='good',        # poor, average, good, excellent, world_class
    specialist=True        # True = especializado en posición
)
```

### Generar Escuadra Completa

```python
from player_generator import create_squad_by_quality, display_squad_summary

# Generar equipo de calidad 'good'
squad = create_squad_by_quality('good')
display_squad_summary(squad)
```

## Ejemplos por Posición

### Centro Defensivo Elite (CB)

```python
cb = Player("Sergio Ramos", 28, "Center Back")
cb.set_technical_attributes(
    defending=19,    # ★ Prioridad
    aerial=18,       # ★ Prioridad
    passing=11,
    technical=10,
    speed=12,
    physical=18,
    shooting=6,
    mental=17,
    intelligence=18  # ★ Prioridad
)
# Rating esperado: ~0.85-0.90
```

### Mediapunta de Clase Mundial (AM)

```python
am = Player("Kevin De Bruyne", 27, "Attacking Midfielder")
am.set_technical_attributes(
    defending=8,
    aerial=7,
    passing=19,
    technical=20,    # ★ Prioridad
    speed=14,
    physical=12,
    shooting=17,
    mental=18,
    intelligence=19  # ★ Prioridad
)
# Rating esperado: ~0.90-0.95
```

### Delantero Goleador (FW)

```python
fw = Player("Robert Lewandowski", 29, "Forward")
fw.set_technical_attributes(
    defending=5,
    aerial=14,
    passing=12,
    technical=17,
    speed=16,        # ★ Prioridad
    physical=16,
    shooting=19,
    mental=18,
    intelligence=19  # ★ Prioridad
)
# Rating esperado: ~0.80-0.85
```

## Versatilidad de Posiciones

El sistema calcula automáticamente el rating del jugador en **todas las posiciones**:

```python
player = Player("Versatile Player", 25, "Midfielder")
player.set_technical_attributes(
    defending=14, aerial=12, passing=15, technical=16,
    speed=15, physical=14, shooting=13, mental=15, intelligence=16
)

# Ver ratings en todas las posiciones
for pos, rating in player.position_rating.items():
    print(f"{pos}: {rating:.2f}")

# Ver las 3 mejores posiciones
best = player.get_best_positions(3)
```

## Mapeo de Nombres de Posición

El sistema reconoce múltiples nombres para cada posición:

| Nombres Reconocidos | Posición |
| --------------------- | ---------- |
| Goalkeeper, GK | CB* |
| Center Back, Centre Back, CB, Defender | CB |
| Full Back, Fullback, FB, LB, RB, Left Back, Right Back | FB |
| Wing Back, Wingback, WB, LWB, RWB | WB |
| Defensive Midfielder, DM, CDM | DM |
| Central Midfielder, Centre Midfielder, CM, Midfielder | CM |
| Side Midfielder, SM, Wide Midfielder, LM, RM | SM |
| Winger, Wing Forward, WF, LW, RW | WF |
| Attacking Midfielder, AM, CAM | AM |
| Forward, Striker, FW, ST, CF | FW |

*Nota: Los porteros usan ponderadores CB como aproximación

## Herramientas de Generación

### Generador de Jugadores

```bash
python player_generator.py
```

Opciones:

1. Generar jugador aleatorio
2. Generar escuadra por calidad (poor/average/good/excellent/world_class)
3. Creador interactivo
4. Salir

### Tests del Sistema

```bash
python test_rating_system.py
```

Ejecuta pruebas completas del sistema de ratings con ejemplos de todos los tipos de jugadores.

## Niveles de Calidad

| Nivel | Rating Esperado | Descripción |
| ------- | ----------------- | ------------- |
| **Poor** | 0.35-0.50 | Jugador de categorías inferiores |
| **Average** | 0.50-0.70 | Jugador profesional estándar |
| **Good** | 0.70-0.85 | Jugador de buen nivel |
| **Excellent** | 0.85-0.95 | Jugador de élite |
| **World Class** | 0.95-1.00 | Jugador de clase mundial |

## Integración con Sistema de Personalidades

El sistema de ratings se integra completamente con el sistema de personalidades:

```python
player = Player("Complete Player", 25, "Midfielder")

# Atributos técnicos
player.set_technical_attributes(
    defending=14, aerial=12, passing=16, technical=17,
    speed=15, physical=14, shooting=13, mental=16, intelligence=17
)

# Atributos mentales (personalidad)
player.set_mental_attributes(
    determination=17, leadership=16, ambition=16, loyalty=15,
    pressure=17, professionalism=18, sportsmanship=16, temperament=16
)

# Ver perfil completo con ratings y personalidad
print(player.describe())
```

## Notas Técnicas

### Suma de Ponderadores

Todos los ponderadores de cada posición suman **0.05** (5%), lo que significa:

- Rating máximo (todos 20s) = 20 × 0.05 = **1.00**
- Rating con todos en 10 = 10 × 0.05 = **0.50**

### Cálculo de Potencial

El potencial se calcula considerando:

1. Rating actual como base
2. Espacio de mejora hasta el máximo teórico
3. Factor aleatorio para variabilidad realista
4. Multiplicador basado en rating actual (jugadores con mejor base tienen más potencial)

### Especialización vs Generalización

- **Especialistas**: Atributos focalizados en las necesidades de su posición
- **Generalistas**: Atributos balanceados, versátiles en múltiples posiciones

## Conclusión

Este sistema proporciona:

- ✅ Evaluación precisa basada en posición
- ✅ Cálculo de potencial realista
- ✅ Identificación de mejores posiciones
- ✅ Generación de jugadores especializados
- ✅ Integración con sistema de personalidades
- ✅ Herramientas de creación y visualización
