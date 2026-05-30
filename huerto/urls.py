from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('catalogo/', views.catalogo_plantas_view, name='catalogo'),
    path('crear/', views.planificador_view, name='crear_huerto'),
    path('editar/<int:plan_id>/', views.planificador_view, name='editar_huerto'),
    path('eliminar/<int:plan_id>/', views.eliminar_huerto_view, name='eliminar_huerto'),
    path('registro/', views.registro_view, name='registro'),
    path('login/', LoginView.as_view(template_name='huerto/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]