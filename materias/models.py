from pyexpat import model
from django.db import models

# Create your models here.

class TipoMateria(models.Model):
    tipo = models.CharField(verbose_name="Tipo de Materia", max_length=100, unique=True)
    
    def __str__(self):
        return self.tipo

class Materia(models.Model):
    tipo = models.ForeignKey(TipoMateria, verbose_name="Tipo de Materia", on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField("Nombre", max_length=60, unique=True)
    descripcion = models.CharField("Descripcion", max_length=350)
    docente = models.ManyToManyField('usuarios.Docente', blank=True)

    def __str__(self):
        return self.nombre

    