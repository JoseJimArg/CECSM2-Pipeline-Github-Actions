from django.contrib import admin

from usuarios.models import Docente
from usuarios.models import Alumno, Aspirante


# Register your models here.

admin.site.register(Docente)
admin.site.register(Alumno)
admin.site.register(Aspirante)
