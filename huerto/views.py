from django.shortcuts import render
from .forms import PlanificadorForm
from .utils import generar_grilla_distribucion
from .models import Planificacion, Planta

def planificador_view(request):
    resultado = None
    
    if request.method == 'POST':
        form = PlanificadorForm(request.POST)
        if form.is_valid():
            # 1. Capturar dimensiones
            ancho = form.cleaned_data['ancho_terreno']
            largo = form.cleaned_data['largo_terreno']
            
            # 2. Extraer cantidades de cada planta
            plantas_cantidades = []
            registro_solicitadas = {} # Para guardar en la BD
            
            for nombre_campo, cantidad in form.cleaned_data.items():
                if nombre_campo.startswith('planta_') and cantidad is not None and cantidad > 0:
                    planta_id = int(nombre_campo.split('_')[1])
                    try:
                        planta_obj = Planta.objects.get(id=planta_id)
                        plantas_cantidades.append({
                            'planta': planta_obj,
                            'cantidad': int(cantidad)
                        })
                        registro_solicitadas[planta_obj.nombre] = int(cantidad)
                    except Planta.DoesNotExist:
                        continue
            
            # 3. Pasar las variables al algoritmo matemático de cálculo
            matriz_coords = generar_grilla_distribucion(ancho, largo, plantas_cantidades)
            
            # 4. Guardar el resultado en la base de datos (Historial de planificaciones)
            planificacion = Planificacion.objects.create(
                ancho_terreno=ancho,
                largo_terreno=largo,
                plantas_solicitadas=registro_solicitadas,
                distribucion_calculada=matriz_coords
            )
            
            resultado = planificacion
    else:
        # Si es GET, mostrar el formulario vacío
        form = PlanificadorForm()

    return render(request, 'huerto/planificador.html', {
        'form': form,
        'resultado': resultado
    })

