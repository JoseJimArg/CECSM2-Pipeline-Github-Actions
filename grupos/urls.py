from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.decorators import user_passes_test

app_name = 'grupos'

urlpatterns = [
    path('', 
        user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.lista_grupos), name='lista_grupos'),
    path('nuevo', 
        user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.nuevo_grupo), name='nuevo_grupo'),
    path('editar/<int:id_grupo>', 
        user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.editar_grupo), name='editar_grupo'),
    path('lista-semestre-cero', 
        user_passes_test(lambda u: u.has_perm('usuarios.aspirante_permiso'))(views.lista_grupos_semestre_cero), name='lista_semestre_cero'),
    path('lista-aspirantes-grupo/<int:id_grupo>', 
        user_passes_test(lambda u: u.has_perm('usuarios.aspirante_permiso'))(views.lista_alumnos_grupo_semestre_cero), name='lista_aspirantes_grupo'),
    path('lista-clases-grupo/<int:id_grupo>', 
        user_passes_test(lambda u: u.has_perm('usuarios.aspirante_permiso'))(views.lista_clases_grupo_semestre_cero), name='lista_clases_grupo'),
]
