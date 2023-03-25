from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.decorators import user_passes_test

app_name = 'materias'

urlpatterns = [
    path('agregar/', 
        user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.agregar_materia), name='agregar'),
    path('editar/<int:pk>', 
        user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.editar_materia), name='editar'),
    path('lista/', 
        user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.lista_materias), name='lista'),
    path('agregar-docente/<int:pk>', 
        user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.agregar_docente), name='agregar_docente'),
    path('buscar-docente/', views.buscar_docente, name='buscar_docente'), # Es una url que retorna json, considero que el implementar permisos puede dar problemas.
    path('eliminar/<int:pk>', 
        user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.eliminar_materia), name='eliminar'),
]
