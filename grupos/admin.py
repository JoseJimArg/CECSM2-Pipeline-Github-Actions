from django.contrib import admin
from .models import Letra, Grupo, Semestre

# Register your models here.
admin.site.register(Grupo)
admin.site.register(Letra)
admin.site.register(Semestre)
