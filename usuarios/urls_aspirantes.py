from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.decorators import user_passes_test

urlpatterns = [
    path('registro', views.nuevo_aspirante, name='nuevo_aspirante'), # En esta vista participan tanto admin como un usuario no logeado.
    path('', user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.lista_aspirantes), name='lista_aspirantes'),
    path('<int:pk>/', user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.ver_aspirante), name='ver_aspirante'),
    path('eliminar/<int:pk>', user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.eliminar_aspirante), name = 'eliminar_aspirante'),
    path("aceptar-aspirante/<int:id>/", user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.aceptar_aspirante), name="aceptar_aspirante"),
    path("rechazar-aspirante/<int:id>/", user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.rechazar_aspirante), name="rechazar_aspirante"),
    path("notificar-comprobante-erroneo/<int:id>/", user_passes_test(lambda u: u.has_perm('auth.administrador_permiso'))(views.avisar_comprobante_erroneo), name="notificar_comprobante_erroneo"),
    path("corregir/<slug:token>/<int:id>/",views.corregir, name="corregir_aspirante"), # Esta no requiere permiso, esta simplemente es para corregir documentos.
    path("inscribir/<int:id>/", user_passes_test(lambda u: u.has_perm('usuarios.aspirante_permiso'))(views.inscribir_aspirante), name="inscribir") # Tengo mis dudas porque el aspirante sí se puede inscribir.
]