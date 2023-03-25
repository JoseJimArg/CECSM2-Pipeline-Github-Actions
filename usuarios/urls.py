from django.urls import path
from django.urls.conf import include
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('docentes/', include('usuarios.urls_docentes')),
    path("home/", views.home, name="home"),
    path('', views.Login.as_view(), name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('alumnos/', include('usuarios.urls_alumnos')),
    path('aspirantes/', include('usuarios.urls_aspirantes')),
]
