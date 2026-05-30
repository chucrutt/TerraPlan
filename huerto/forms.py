from django import forms
from .models import Planta

class PlanificadorForm(forms.Form):
    nombre = forms.CharField(
        label='Nombre de tu Huerto', 
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'margin-bottom:15px; width: 100%;', 'placeholder': 'Ej. Mi primer huerto'})
    )
    ancho_terreno = forms.FloatField(
        label='Ancho del terreno (m)', 
        min_value=0.1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'style': 'margin-bottom:15px;'})
    )
    largo_terreno = forms.FloatField(
        label='Largo del terreno (m)', 
        min_value=0.1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'style': 'margin-bottom:15px;'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Generar dinámicamente un campo de cantidad por cada planta en la BD
        for planta in Planta.objects.all():
            self.fields[f'planta_{planta.id}'] = forms.IntegerField(
                label=planta.nombre,
                min_value=0,
                initial=0,
                required=False,
                widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 80px;'})
            )

