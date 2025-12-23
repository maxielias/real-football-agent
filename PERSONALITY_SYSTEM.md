# Sistema de Personalidades de Jugadores

## Descripción General

El sistema de personalidades evalúa los atributos mentales de un jugador (en una escala de 1-20) y determina su personalidad, que influye en su comportamiento dentro y fuera del campo.

## Atributos Mentales

Cada jugador tiene 8 atributos mentales que se clasifican en rangos:

| Rating | Clasificación |
|--------|---------------|
| 1-6    | Terrible      |
| 7-9    | Poor          |
| 10-14  | Average       |
| 15-17  | Good          |
| 18-20  | Excellent     |

### Atributos:
- **Determination**: Determinación del jugador para mejorar y dar lo mejor
- **Leadership**: Capacidad de liderazgo dentro del equipo
- **Ambition**: Ambición profesional y deseo de éxito
- **Loyalty**: Lealtad al club y compromiso a largo plazo
- **Pressure**: Capacidad de manejar la presión en situaciones difíciles
- **Professionalism**: Profesionalismo en entrenamiento y preparación
- **Sportsmanship**: Deportividad y respeto por rivales y árbitros
- **Temperament**: Control del temperamento y disciplina

## Categorías de Personalidad

### Best Personalities (Mejores)
Personalidades ideales para cualquier equipo:
- **Model Citizen**: Jugador ejemplar en todos los aspectos
- **Model Professional**: Profesional excepcional (solo 23+ años)

### Good Personalities (Buenas)
Personalidades positivas con características destacadas:
- **Perfectionist**: Determinado y ambicioso, pero temperamental
- **Resolute**: Determinado y profesional
- **Professional**: Muy profesional con buen temperamento
- **Iron Willed**: Gran determinación bajo presión
- **Resilient**: Determinado y maneja bien la presión
- **Driven/Determined**: Máxima determinación
- **Charismatic Leader**: Líder carismático (23+ años)
- **Born Leader**: Líder nato (23+ años)
- **Leader**: Gran liderazgo (23+ años)
- **Ambitious**: Ambicioso con poca lealtad

### Neutral Personalities (Neutrales)
Personalidades balanceadas sin extremos:
- **Balanced**: Atributos equilibrados sin destacar
- **Light-Hearted**: Alegre y maneja bien la presión
- **Jovial**: Jovial pero poco profesional
- **Loyal**: Muy leal pero poco ambicioso
- **Honest/Sporting**: Deportivo y honesto

### Bad Personalities (Malas)
Solo para regens - personalidades problemáticas:
- **Fickle**: Voluble, puede cambiar de club fácilmente
- **Mercenary**: Mercenario, solo piensa en dinero
- **Unambitious**: Sin ambición de mejorar
- **Unsporting**: Antideportivo

### Worst Personalities (Peores)
Solo para regens - personalidades muy problemáticas:
- **Slack/Casual**: Poco profesional y sin determinación
- **Temperamental**: Mal temperamento
- **Spineless**: Sin carácter bajo presión
- **Low Determination**: Poca determinación

## Uso del Sistema

### Inicializar un Jugador

```python
from player import Player

# Crear jugador
player = Player("Juan Pérez", 22, "Midfielder")

# Establecer atributos mentales
player.set_mental_attributes(
    determination=16,
    leadership=14,
    ambition=15,
    loyalty=12,
    pressure=15,
    professionalism=17,
    sportsmanship=14,
    temperament=13
)

# La personalidad se calcula automáticamente
print(player.personality)  # Imprime la personalidad calculada
```

### Ver Atributos Mentales

```python
# Ver todos los atributos mentales con clasificaciones
print(player.get_mental_attributes_description())
```

Salida ejemplo:
```
============================================================
MENTAL ATTRIBUTES: Juan Pérez
============================================================
Determination:    16 (Good)
Leadership:       14 (Average)
Ambition:         15 (Good)
Loyalty:          12 (Average)
Pressure:         15 (Good)
Professionalism:  17 (Good)
Sportsmanship:    14 (Average)
Temperament:      13 (Average)

Personality: Resilient (Good)
============================================================
```

### Ver Perfil Completo

```python
# Ver perfil completo del jugador incluyendo personalidad
print(player.describe())
```

### Actualizar Personalidad

```python
# Actualizar personalidad manualmente (normalmente se hace automáticamente)
# is_regen=True permite personalidades negativas
# plays_for_favourite=True para detectar "Devoted" vs "Very Loyal"
player.update_personality(is_regen=False, plays_for_favourite=False)
```

### Modificar Atributos Individualmente

```python
# Modificar solo algunos atributos
player.set_mental_attributes(
    determination=18,  # Solo cambiar determinación
    ambition=12        # Y ambición
)
# Los demás atributos mantienen sus valores anteriores
```

## Impacto de la Personalidad

La personalidad del jugador puede influir en:
- **Desarrollo**: Jugadores con mejor determinación y profesionalismo mejoran más rápido
- **Moral**: Personalidades positivas mantienen mejor la moral
- **Negociaciones**: La lealtad y ambición afectan las negociaciones de contrato
- **Rendimiento bajo presión**: Afecta el rendimiento en momentos críticos
- **Relaciones con el equipo**: El liderazgo y deportividad influyen en la química del equipo

## Ejemplos de Personalidades

### Model Citizen (Mejor)
```python
player.set_mental_attributes(
    determination=16, leadership=17, ambition=12,
    loyalty=16, pressure=16, professionalism=18,
    sportsmanship=16, temperament=15
)
# Resultado: Model Citizen (Best)
```

### Perfectionist (Buena)
```python
player.set_mental_attributes(
    determination=17, ambition=16, professionalism=16,
    temperament=8  # Temperamento bajo
)
# Resultado: Perfectionist (Good)
```

### Ambitious (Buena/Neutral)
```python
player.set_mental_attributes(
    determination=14, ambition=17, loyalty=8
)
# Resultado: Ambitious (Good)
```

### Mercenary (Mala - solo regens)
```python
player.set_mental_attributes(
    determination=14, ambition=17, loyalty=4
)
player.update_personality(is_regen=True)
# Resultado: Mercenary (Bad)
```

## Notas Importantes

1. **Regens**: Las personalidades "Bad" y "Worst" solo se asignan a jugadores regenerados (is_regen=True)
2. **Edad**: Algunas personalidades de liderazgo requieren edad 23+
3. **Orden de evaluación**: Las personalidades se evalúan en orden de prioridad (peores primero, luego mejores)
4. **Default**: Si no se cumple ningún criterio, se asigna "Balanced"
5. **Atributos automáticos**: Al usar `set_mental_attributes()`, la personalidad se recalcula automáticamente

## Testing

Ejecutar el script de prueba para ver ejemplos de todas las personalidades:

```bash
python test_personality.py
```

Este script muestra ejemplos de diferentes personalidades con sus atributos correspondientes.
