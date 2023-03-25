from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.decorators import user_passes_test

app_name = 'clases'

urlpatterns = [
    path("agregar-clase/<int:pk>", 
        user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.asignar_clase), name="agregar_clase_alumno"),
    path("buscar-clase/", views.buscar_clase, name="buscar_clase"), # Este es una petición para json, no sé si debería de pedir permisos, no lo considero muy importante y no sé si pueda validar.
    path("nueva/", 
        user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.nueva_clase), name="nueva"),
    path("", 
        user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.lista_clases), name="lista_clases"),
    path("eliminar/<int:pk>", 
        user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.eliminar_clase), name="eliminar_clase"),
    path("alumnos/<int:pk>", 
        user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.lista_alumnos_de_clase), name="lista_alumnos_de_clase"),
    path("quitar-clase/<int:alumno>/<int:clase>", 
        user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.desasignar_clase), name="quitar_clase_alumno"),
]
