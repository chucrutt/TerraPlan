from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import PlanificadorForm
from .utils import generar_grilla_distribucion
from .models import Planificacion, Planta

def registro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            # Iniciar sesión automáticamente al registrarse
            login(request, usuario)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'huerto/registro.html', {'form': form})


@login_required(login_url='/login/')
def dashboard_view(request):
    """Panel principal que lista todos los huertos del usuario logueado"""
    huertos = Planificacion.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'huerto/dashboard.html', {'huertos': huertos})


@login_required(login_url='/login/')
def eliminar_huerto_view(request, plan_id):
    """Permite eliminar permanentemente un huerto creado"""
    if request.method == 'POST':
        huerto = get_object_or_404(Planificacion, id=plan_id, usuario=request.user)
        huerto.delete()
    return redirect('dashboard')


def catalogo_plantas_view(request):
    """Catálogo interactivo con filtros y búsqueda de especies y compatibilidades"""
    plantas = Planta.objects.all().order_by('nombre')
    
    # Parámetros de búsqueda GET
    query = request.GET.get('q', '')
    sol_filtro = request.GET.get('sol', '')
    
    if query:
        plantas = plantas.filter(nombre__icontains=query)
    if sol_filtro:
        plantas = plantas.filter(necesidad_sol=sol_filtro)
        
    # Agrupar datos de compatibilidad para evitar costosas sentencias SQL en el template
    catalogo_data = []
    for p in plantas:
        ayudan = [rel.planta_b.nombre for rel in p.relacion_origen.filter(tipo_relacion='AYUDA')]
        compiten = [rel.planta_b.nombre for rel in p.relacion_origen.filter(tipo_relacion='COMPITEN')]
        catalogo_data.append({
            'planta': p,
            'ayudan': ayudan,
            'compiten': compiten
        })

    return render(request, 'huerto/catalogo.html', {
        'catalogo_data': catalogo_data,
        'query': query,
        'sol_filtro': sol_filtro,
        'opciones_sol': Planta.NECESIDAD_SOL_CHOICES
    })


@login_required(login_url='/login/')
def planificador_view(request, plan_id=None):
    """Vista compartida para CREAR y EDITAR un huerto"""
    
    # 1. Determinar si estamos creando uno nuevo o abriendo uno existente
    if plan_id:
        planificacion = get_object_or_404(Planificacion, id=plan_id, usuario=request.user)
    else:
        planificacion = None
        
    resultado = planificacion # Si estamos editando, ya pre-cargamos la visualización generada previamente
    
    if request.method == 'POST':
        form = PlanificadorForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            ancho = form.cleaned_data['ancho_terreno']
            largo = form.cleaned_data['largo_terreno']
            
            # Extraer plantas del formulario
            plantas_cantidades = []
            registro_solicitadas = {} 
            for nombre_campo, cantidad in form.cleaned_data.items():
                if nombre_campo.startswith('planta_') and cantidad is not None and cantidad > 0:
                    planta_id = int(nombre_campo.split('_')[1])
                    try:
                        p_obj = Planta.objects.get(id=planta_id)
                        plantas_cantidades.append({'planta': p_obj, 'cantidad': int(cantidad)})
                        registro_solicitadas[p_obj.nombre] = int(cantidad)
                    except Planta.DoesNotExist:
                        pass
            
            # Recalcular la matemática biológica del terreno
            matriz_coords = generar_grilla_distribucion(ancho, largo, plantas_cantidades)
            
            # Guardar o Actualizar el modelo asociado al usuario
            if planificacion:
                # Actualizando huerto existente
                planificacion.nombre = nombre
                planificacion.ancho_terreno = ancho
                planificacion.largo_terreno = largo
                planificacion.plantas_solicitadas = registro_solicitadas
                planificacion.distribucion_calculada = matriz_coords
                planificacion.save()
            else:
                # Creando nuevo huerto
                planificacion = Planificacion.objects.create(
                    usuario=request.user,
                    nombre=nombre,
                    ancho_terreno=ancho,
                    largo_terreno=largo,
                    plantas_solicitadas=registro_solicitadas,
                    distribucion_calculada=matriz_coords
                )
            
            # Redirigimos siempre a la variante de "Edición" para ver los resultados permanentemente
            return redirect('editar_huerto', plan_id=planificacion.id)
            
    else:
        # Petición GET: Cargar el formulario
        # Si estamos abriendo un huerto existente, auto-rellenamos el formulario con sus datos históricos
        initial_data = {}
        if planificacion:
            initial_data = {
                'nombre': planificacion.nombre,
                'ancho_terreno': planificacion.ancho_terreno,
                'largo_terreno': planificacion.largo_terreno,
            }
            if planificacion.plantas_solicitadas:
                for p_nombre, cant in planificacion.plantas_solicitadas.items():
                    try:
                        p_obj = Planta.objects.get(nombre=p_nombre)
                        initial_data[f'planta_{p_obj.id}'] = cant
                    except Planta.DoesNotExist:
                        pass
                        
        form = PlanificadorForm(initial=initial_data)

    return render(request, 'huerto/planificador.html', {
        'form': form,
        'resultado': resultado,
        'es_edicion': planificacion is not None
    })

