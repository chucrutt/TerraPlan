from django.contrib import admin
from .models import Planta, Compatibilidad, Planificacion

@admin.register(Planta)
class PlantaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'distancia_minima_separacion', 'ph_optimo_suelo', 'necesidad_sol')
    search_fields = ('nombre',)
    list_filter = ('necesidad_sol',)

@admin.register(Compatibilidad)
class CompatibilidadAdmin(admin.ModelAdmin):
    list_display = ('planta_a', 'planta_b', 'tipo_relacion')
    list_filter = ('tipo_relacion',)
    search_fields = ('planta_a__nombre', 'planta_b__nombre')

@admin.register(Planificacion)
class PlanificacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_creacion', 'ancho_terreno', 'largo_terreno')
    list_filter = ('fecha_creacion',)

