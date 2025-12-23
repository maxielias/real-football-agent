"""
Ejemplos prácticos de uso del sistema de personalidades
"""

from player import Player

def ejemplo_1_crear_jugador_model_citizen():
    """Ejemplo 1: Crear un jugador con personalidad Model Citizen"""
    print("\n" + "="*80)
    print("EJEMPLO 1: Model Citizen - El jugador perfecto")
    print("="*80)
    
    player = Player("Cristiano Ronaldo", 28, "Forward")
    player.set_mental_attributes(
        determination=18,    # Excellent
        leadership=17,       # Good
        ambition=16,         # Good
        loyalty=16,          # Good
        pressure=18,         # Excellent
        professionalism=19,  # Excellent
        sportsmanship=17,    # Good
        temperament=16       # Good
    )
    
    print(player.get_mental_attributes_description())
    print("\nComentario: Este jugador es un ejemplo perfecto para cualquier equipo.")
    print("Su profesionalismo excepcional y buenos atributos en todas las áreas")
    print("lo convierten en un Model Citizen que puede ser líder dentro y fuera del campo.")

def ejemplo_2_comparar_personalidades():
    """Ejemplo 2: Comparar diferentes personalidades"""
    print("\n" + "="*80)
    print("EJEMPLO 2: Comparación de Personalidades")
    print("="*80)
    
    # Perfectionist
    p1 = Player("Diego Perfeccionista", 23, "Midfielder")
    p1.set_mental_attributes(
        determination=17, leadership=10, ambition=16, loyalty=10,
        pressure=10, professionalism=16, sportsmanship=10, temperament=8
    )
    
    # Balanced
    p2 = Player("Juan Equilibrado", 23, "Defender")
    p2.set_mental_attributes(
        determination=12, leadership=11, ambition=13, loyalty=12,
        pressure=11, professionalism=13, sportsmanship=12, temperament=11
    )
    
    # Mercenary (regen)
    p3 = Player("Roberto Mercenario", 18, "Forward")
    p3.set_mental_attributes(
        determination=14, leadership=10, ambition=17, loyalty=4,
        pressure=18, professionalism=10, sportsmanship=10, temperament=10
    )
    p3.update_personality(is_regen=True)
    
    print(f"\n{p1.name}:")
    print(f"  Personalidad: {p1.get_personality_description()}")
    print(f"  Pros: Gran determinación y ambición, muy profesional")
    print(f"  Cons: Temperamento bajo, puede ser difícil de manejar bajo estrés")
    
    print(f"\n{p2.name}:")
    print(f"  Personalidad: {p2.get_personality_description()}")
    print(f"  Pros: Equilibrado, confiable, sin grandes debilidades")
    print(f"  Cons: No destaca en ningún área, potencial de desarrollo limitado")
    
    print(f"\n{p3.name}:")
    print(f"  Personalidad: {p3.get_personality_description()}")
    print(f"  Pros: Ambicioso y maneja bien la presión")
    print(f"  Cons: Poca lealtad, probablemente busque mejores ofertas constantemente")

def ejemplo_3_desarrollo_juvenil():
    """Ejemplo 3: Planificación de desarrollo para jóvenes talentos"""
    print("\n" + "="*80)
    print("EJEMPLO 3: Academia Juvenil - Planificación de Desarrollo")
    print("="*80)
    
    jovenes = []
    
    # Joven con gran potencial pero necesita desarrollo mental
    j1 = Player("Marco Talento", 17, "Winger")
    j1.set_mental_attributes(
        determination=11, leadership=8, ambition=14, loyalty=10,
        pressure=9, professionalism=10, sportsmanship=11, temperament=9
    )
    jovenes.append(j1)
    
    # Joven con buena mentalidad desde temprana edad
    j2 = Player("Laura Profesional", 18, "Midfielder")
    j2.set_mental_attributes(
        determination=15, leadership=12, ambition=13, loyalty=14,
        pressure=14, professionalism=17, sportsmanship=15, temperament=14
    )
    jovenes.append(j2)
    
    # Joven con mucha determinación pero necesita trabajo en otras áreas
    j3 = Player("Carlos Luchador", 17, "Defender")
    j3.set_mental_attributes(
        determination=18, leadership=9, ambition=11, loyalty=13,
        pressure=16, professionalism=12, sportsmanship=10, temperament=11
    )
    jovenes.append(j3)
    
    print("\nAnálisis de la cantera:")
    for i, jugador in enumerate(jovenes, 1):
        print(f"\n{i}. {jugador.name} ({jugador.age}) - {jugador.position}")
        print(f"   Personalidad: {jugador.get_personality_description()}")
        print(f"   Determinación: {jugador._classify_attribute(jugador.determination)}")
        print(f"   Profesionalismo: {jugador._classify_attribute(jugador.professionalism)}")
        
        if jugador.determination >= 15 and jugador.professionalism >= 15:
            print(f"   ✓ Recomendación: Priorizar para primer equipo")
        elif jugador.professionalism >= 15:
            print(f"   → Recomendación: Buen potencial, desarrollar determinación")
        else:
            print(f"   ⚠ Recomendación: Necesita más tiempo y mentoría")

def ejemplo_4_construir_equipo_balanceado():
    """Ejemplo 4: Construir un equipo con personalidades complementarias"""
    print("\n" + "="*80)
    print("EJEMPLO 4: Construcción de Equipo Balanceado")
    print("="*80)
    
    equipo = []
    
    # Capitán - Líder
    capitan = Player("Ana Capitana", 28, "Defender")
    capitan.set_mental_attributes(
        determination=17, leadership=19, ambition=14, loyalty=16,
        pressure=17, professionalism=18, sportsmanship=18, temperament=18
    )
    equipo.append(("Capitán", capitan))
    
    # Joven promesa - Ambitious
    promesa = Player("Luis Promesa", 20, "Forward")
    promesa.set_mental_attributes(
        determination=16, leadership=10, ambition=17, loyalty=9,
        pressure=13, professionalism=14, sportsmanship=12, temperament=13
    )
    equipo.append(("Joven Estrella", promesa))
    
    # Veterano leal - Loyal
    veterano = Player("Pedro Veterano", 32, "Midfielder")
    veterano.set_mental_attributes(
        determination=13, leadership=14, ambition=6, loyalty=19,
        pressure=15, professionalism=16, sportsmanship=17, temperament=16
    )
    equipo.append(("Veterano Leal", veterano))
    
    # Profesional confiable - Professional
    profesional = Player("Sandra Confiable", 26, "Midfielder")
    profesional.set_mental_attributes(
        determination=14, leadership=12, ambition=12, loyalty=13,
        pressure=13, professionalism=19, sportsmanship=14, temperament=15
    )
    equipo.append(("Profesional", profesional))
    
    print("\nComposición del equipo:")
    print("\nEste equipo tiene una mezcla balanceada de personalidades:")
    
    for rol, jugador in equipo:
        print(f"\n• {rol}: {jugador.name}")
        print(f"  Personalidad: {jugador.get_personality_description()}")
        print(f"  Edad: {jugador.age}")
        
    print("\n" + "-"*80)
    print("Análisis del equipo:")
    print("\n✓ Liderazgo: Ana Capitana proporciona liderazgo fuerte")
    print("✓ Ambición: Luis Promesa impulsa al equipo a mejorar")
    print("✓ Estabilidad: Pedro Veterano aporta experiencia y lealtad")
    print("✓ Profesionalismo: Sandra Confiable mantiene altos estándares")
    print("\nEste balance crea un ambiente saludable donde:")
    print("- Los jóvenes aprenden de los veteranos")
    print("- Hay líderes que guían al grupo")
    print("- Existe ambición sin sacrificar la unidad del equipo")
    print("- El profesionalismo es el estándar")

def ejemplo_5_identificar_problemas():
    """Ejemplo 5: Identificar jugadores problemáticos antes de ficharlos"""
    print("\n" + "="*80)
    print("EJEMPLO 5: Scouting - Identificar Señales de Alerta")
    print("="*80)
    
    candidatos = []
    
    # Candidato 1: Parece bueno pero es mercenario
    c1 = Player("Victor Mercenario", 22, "Forward")
    c1.set_mental_attributes(
        determination=15, leadership=10, ambition=18, loyalty=3,
        pressure=14, professionalism=11, sportsmanship=10, temperament=12
    )
    c1.update_personality(is_regen=True)
    candidatos.append(c1)
    
    # Candidato 2: Joven con bajo profesionalismo
    c2 = Player("Miguel Casual", 19, "Midfielder")
    c2.set_mental_attributes(
        determination=8, leadership=7, ambition=12, loyalty=10,
        pressure=9, professionalism=5, sportsmanship=11, temperament=8
    )
    c2.update_personality(is_regen=True)
    candidatos.append(c2)
    
    # Candidato 3: Buena opción
    c3 = Player("Sofia Resiliente", 23, "Defender")
    c3.set_mental_attributes(
        determination=16, leadership=13, ambition=14, loyalty=14,
        pressure=16, professionalism=15, sportsmanship=14, temperament=14
    )
    candidatos.append(c3)
    
    print("\nAnálisis de candidatos para fichaje:")
    
    for i, candidato in enumerate(candidatos, 1):
        print(f"\n{'='*80}")
        print(f"Candidato {i}: {candidato.name} ({candidato.age}) - {candidato.position}")
        print(f"Personalidad: {candidato.get_personality_description()}")
        
        # Análisis de red flags
        red_flags = []
        yellow_flags = []
        green_flags = []
        
        if candidato.loyalty < 7:
            red_flags.append(f"⛔ Lealtad muy baja ({candidato._classify_attribute(candidato.loyalty)})")
        if candidato.professionalism < 7:
            red_flags.append(f"⛔ Profesionalismo muy bajo ({candidato._classify_attribute(candidato.professionalism)})")
        if candidato.temperament < 7:
            red_flags.append(f"⛔ Mal temperamento ({candidato._classify_attribute(candidato.temperament)})")
        
        if 7 <= candidato.professionalism < 10:
            yellow_flags.append(f"⚠ Profesionalismo bajo ({candidato._classify_attribute(candidato.professionalism)})")
        if candidato.determination < 10:
            yellow_flags.append(f"⚠ Baja determinación ({candidato._classify_attribute(candidato.determination)})")
        
        if candidato.determination >= 15:
            green_flags.append(f"✓ Buena determinación ({candidato._classify_attribute(candidato.determination)})")
        if candidato.professionalism >= 15:
            green_flags.append(f"✓ Muy profesional ({candidato._classify_attribute(candidato.professionalism)})")
        if candidato.pressure >= 15:
            green_flags.append(f"✓ Maneja bien la presión ({candidato._classify_attribute(candidato.pressure)})")
        
        if red_flags:
            print("\nSeñales de ALERTA ROJA:")
            for flag in red_flags:
                print(f"  {flag}")
        
        if yellow_flags:
            print("\nSeñales de PRECAUCIÓN:")
            for flag in yellow_flags:
                print(f"  {flag}")
        
        if green_flags:
            print("\nPuntos POSITIVOS:")
            for flag in green_flags:
                print(f"  {flag}")
        
        # Recomendación
        if red_flags:
            print("\n❌ RECOMENDACIÓN: NO FICHAR")
            print("   Riesgo alto de problemas en el vestuario o falta de compromiso")
        elif len(yellow_flags) > 2:
            print("\n⚠️  RECOMENDACIÓN: CONSIDERAR CON CUIDADO")
            print("   Necesitará mentoría y supervisión cercana")
        else:
            print("\n✅ RECOMENDACIÓN: BUEN FICHAJE")
            print("   Perfil mental sólido para incorporar al equipo")

def main():
    """Ejecutar todos los ejemplos"""
    ejemplos = [
        ejemplo_1_crear_jugador_model_citizen,
        ejemplo_2_comparar_personalidades,
        ejemplo_3_desarrollo_juvenil,
        ejemplo_4_construir_equipo_balanceado,
        ejemplo_5_identificar_problemas
    ]
    
    print("\n" + "="*80)
    print("EJEMPLOS PRÁCTICOS DEL SISTEMA DE PERSONALIDADES")
    print("="*80)
    print("\nEste script demuestra casos de uso reales del sistema de personalidades")
    print("en el contexto de gestión de un equipo de fútbol.\n")
    
    for i, ejemplo in enumerate(ejemplos, 1):
        print(f"\n\nPresiona Enter para ver el Ejemplo {i}...")
        input()
        ejemplo()
    
    print("\n\n" + "="*80)
    print("FIN DE LOS EJEMPLOS")
    print("="*80)
    print("\n¡Explora el sistema creando tus propios jugadores!")
    print("Usa: python personality_generator.py")

if __name__ == "__main__":
    main()
