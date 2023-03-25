from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.decorators import user_passes_test

urlpatterns = [
    path('', user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.lista_alumnos), name="lista_alumnos"),
    path('nuevo/', user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.NuevoAlumno.as_view()), name='nuevo_alumno'),
    path('<int:pk>/', user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.ver_alumno), name='ver_alumno'),
    path('editar/<int:pk>', user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.EditarAlumno.as_view()), name='editar_alumno'),
    path('eliminar/<int:pk>', user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.eliminar_alumno), name='eliminar_alumno'),
]
