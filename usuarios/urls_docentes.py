from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.decorators import user_passes_test


urlpatterns = [
    path('', user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.ListaDocentes.as_view()), name='lista_docentes'),
    path('nuevo/', user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.NuevoDocente.as_view()), name='nuevo_docente'),
    path('editar/<int:pk>', user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.EditarDocente.as_view()), name='editar'),
    path("ver/<int:pk>", user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.ver_docente), name="ver_docente"),
    path('ver-clases/', user_passes_test(lambda u: u.has_perm('usuarios.docente_permiso'))(views.ver_clases), name='ver_clases'), # Supongo que son las clases de sí mismo
    path('eliminar/<int:pk>', user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.eliminar_docente), name='eliminar_docente'),
]
