from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.decorators import user_passes_test

app_name = 'ciclos'

urlpatterns = [
    path('nuevo', 
        user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.nuevo_ciclo), name='nuevo_ciclo'),
    path('activar/<int:id>', 
        user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.activar_ciclo), name='activar'),
]