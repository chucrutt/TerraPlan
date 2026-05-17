from django.db import models

class Planta(models.Model):
    NECESIDAD_SOL_CHOICES = [
        ('ALTA', 'Sol directo pleno'),
        ('MEDIA', 'Sombra parcial'),
        ('BAJA', 'Sombra total'),
    ]

    nombre = models.CharField(max_length=100)
    distancia_minima_separacion = models.FloatField(help_text="Distancia en centímetros")
    ph_optimo_suelo = models.FloatField(help_text="pH ideal")
    necesidad_sol = models.CharField(max_length=10, choices=NECESIDAD_SOL_CHOICES)
    compatibilidades = models.ManyToManyField(
        'self',
        through='Compatibilidad',
        symmetrical=False,
        related_name='compatible_con'
    )

    def __str__(self):
        return self.nombre


class Compatibilidad(models.Model):
    RELACION_CHOICES = [
        ('AYUDA', 'Se ayudan (Asociación benéfica)'),
        ('COMPITEN', 'Compiten (Asociación perjudicial)'),
        ('NEUTRA', 'Neutra'),
    ]

    planta_a = models.ForeignKey(Planta, related_name='relacion_origen', on_delete=models.CASCADE)
    planta_b = models.ForeignKey(Planta, related_name='relacion_destino', on_delete=models.CASCADE)
    tipo_relacion = models.CharField(max_length=15, choices=RELACION_CHOICES)

    class Meta:
        verbose_name_plural = "Compatibilidades"
        unique_together = ('planta_a', 'planta_b')

    def __str__(self):
        return f"{self.planta_a} -> {self.planta_b} ({self.tipo_relacion})"


class Planificacion(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ancho_terreno = models.FloatField(help_text="Ancho del terreno en metros")
    largo_terreno = models.FloatField(help_text="Largo del terreno en metros")
    plantas_solicitadas = models.JSONField(null=True, blank=True, help_text="Diccionario con las cantidades pedidas originalmente")
    distribucion_calculada = models.JSONField(help_text="Almacena el JSON de la matriz o posiciones calculadas")

    class Meta:
        verbose_name_plural = "Planificaciones"

    def __str__(self):
        return f"Planificación #{self.id} - {self.fecha_creacion.strftime('%Y-%m-%d %H:%M')}"


