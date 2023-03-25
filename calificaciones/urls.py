from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.decorators import user_passes_test

app_name = 'calificaciones'

urlpatterns = [
    path('registrar/<int:id_clase>/<int:id_parcial>',
         user_passes_test(lambda u: u.has_perm('usuarios.docente_permiso'))(views.registrar_calificaciones), name='registrar'),
    path('consulta/', views.consulta_calificaciones_alumno, # No requiere ni login, no tiene caso ponerle un permiso requerido.
         name='consulta'),
]
