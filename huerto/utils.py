from .models import Compatibilidad
import math
import random

def obtener_relacion(planta_a, planta_b, mapa_compatibilidad):
    """ Busca la relación en el mapa cacheado, bidireccional """
    if planta_a.id == planta_b.id:
        return 'NEUTRA'
    
    # Buscar A->B
    if planta_a.id in mapa_compatibilidad and planta_b.id in mapa_compatibilidad[planta_a.id]:
        return mapa_compatibilidad[planta_a.id][planta_b.id]
    
    # Buscar B->A
    if planta_b.id in mapa_compatibilidad and planta_a.id in mapa_compatibilidad[planta_b.id]:
        return mapa_compatibilidad[planta_b.id][planta_a.id]

    return 'NEUTRA'

def generar_grilla_distribucion(ancho, largo, plantas_cantidades):
    """
    Algoritmo de distribución espacial 2D basado en cantidades, distancias y compatibilidad.
    Busca coordenadas válidas evitando superposiciones y alejando plantas rivales.
    """
    ancho_cm = ancho * 100
    largo_cm = largo * 100

    # Expandir la lista: Si el usuario pidió 3 tomates, guardamos 3 objetos "Tomate"
    lista_a_plantar = []
    for item in plantas_cantidades:
        for _ in range(item['cantidad']):
            lista_a_plantar.append(item['planta'])

    # Pre-cargar relaciones de compatibilidad en un diccionario para acceso rápido (Cache)
    relaciones = Compatibilidad.objects.all()
    mapa_comp = {}
    for r in relaciones:
        if r.planta_a.id not in mapa_comp: mapa_comp[r.planta_a.id] = {}
        mapa_comp[r.planta_a.id][r.planta_b.id] = r.tipo_relacion

    # MEJORA DEL ALGORITMO: Ordenar las plantas de mayor a menor tamaño (distancia requerida)
    # Es mucho más fácil ubicar las plantas pequeñas en los huecos que dejen las grandes.
    lista_a_plantar.sort(key=lambda p: p.distancia_minima_separacion, reverse=True)

    distribucion = {
        "dimensiones": {"ancho_cm": ancho_cm, "largo_cm": largo_cm},
        "coordenadas": [],
        "no_ubicadas": []
    }

    # Resolución de la cuadrícula base en cm
    PASO = 5 
    
    # MEJORA ORGÁNICA: Generar malla de puntos y ordenarlos desde el CENTRO hacia afuera.
    # Así el huerto crecerá desde el medio de la parcela en círculos como la naturaleza.
    centro_x = ancho_cm / 2
    centro_y = largo_cm / 2
    puntos_grilla = []
    
    for y in range(0, int(largo_cm), PASO):
        for x in range(0, int(ancho_cm), PASO):
            puntos_grilla.append((x, y))
            
    puntos_grilla.sort(key=lambda p: math.sqrt((p[0] - centro_x)**2 + (p[1] - centro_y)**2))

    # Contador para numerar las plantas (Ej: Tomate 1, Tomate 2)
    conteo_ubicadas = {}

    for nueva_planta in lista_a_plantar:
        ubicada = False
        dist_nueva = nueva_planta.distancia_minima_separacion
        radio_nueva = dist_nueva / 2
        
        # Buscar en los puntos desde el centro hacia los bordes
        for px, py in puntos_grilla:
            # 1. Validar que la planta no se salga de los bordes del terreno (caja invisible)
            if px - radio_nueva < 0 or px + radio_nueva > ancho_cm or py - radio_nueva < 0 or py + radio_nueva > largo_cm:
                continue

            posicion_invalida = False
            
            # 2. Checkear contra todas las plantas ya ubicadas
            for plantada in distribucion["coordenadas"]:
                dx = px - plantada["x"]
                dy = py - plantada["y"]
                distancia_euclidiana = math.sqrt(dx**2 + dy**2)
                
                radio_plantada = plantada["radio_necesario"] / 2
                distancia_requerida = radio_plantada + radio_nueva
                
                relacion = obtener_relacion(nueva_planta, plantada["_objeto"], mapa_comp)
                
                if relacion == 'COMPITEN':
                    distancia_requerida *= 1.8 
                elif relacion == 'AYUDA':
                    distancia_requerida *= 0.85
                
                if distancia_euclidiana < distancia_requerida:
                    posicion_invalida = True
                    break 
            
            if not posicion_invalida:
                # Actualizar el conteo para esta especie
                conteo_ubicadas[nueva_planta.nombre] = conteo_ubicadas.get(nueva_planta.nombre, 0) + 1
                nombre_numerado = f"{nueva_planta.nombre} {conteo_ubicadas[nueva_planta.nombre]}"
                
                # Le agregamos un levísimo "temblor" o "ruido" aleatorio a las coordenadas finales
                # para romper la perfección de la cuadrícula y parezca sembrado a mano por un humano.
                jitter_x = random.uniform(-2.5, 2.5)
                jitter_y = random.uniform(-2.5, 2.5)
                
                final_x = round(px + jitter_x, 1)
                final_y = round(py + jitter_y, 1)
                
                # Asegurar de que ese "temblor" no lo saque del límite
                final_x = max(radio_nueva, min(final_x, ancho_cm - radio_nueva))
                final_y = max(radio_nueva, min(final_y, largo_cm - radio_nueva))
                
                # Encontramos un lugar válido
                distribucion["coordenadas"].append({
                    "planta": nueva_planta.nombre,
                    "planta_display": nombre_numerado,
                    "x": final_x,
                    "y": final_y,
                    "radio_necesario": dist_nueva,
                    "_objeto": nueva_planta 
                })
                ubicada = True
                break 
                
        if not ubicada:
            distribucion["no_ubicadas"].append(nueva_planta.nombre)

    # Limpiar el objeto oculto _objeto para poder parsear a JSON en la Base de Datos
    for c in distribucion["coordenadas"]:
        del c["_objeto"]

    return distribucion
