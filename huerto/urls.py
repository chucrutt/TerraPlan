from django.urls import path
from . import views

urlpatterns = [
    path('', views.planificador_view, name='planificador'),
]