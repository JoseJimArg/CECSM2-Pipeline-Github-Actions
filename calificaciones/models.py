from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


class Calificacion(models.Model):

    # Campos en el modelo
    clase = models.ForeignKey('clases.Clase', on_delete=models.CASCADE)
    alumno = models.ForeignKey('usuarios.Alumno', on_delete=models.CASCADE)
    tipo = models.ForeignKey('calificaciones.Periodo',
                             on_delete=models.CASCADE)
    calificacion = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MaxValueValidator(10), MinValueValidator(5)]
    )

    class Meta:
        unique_together = ('clase', 'alumno', 'tipo')

    def __str__(self):
        return f'{self.clase.materia } - {self.alumno} - {self.tipo} - {self.calificacion}'


periodos = ['Primer Parcial', 'Segundo Parcial',
            'Tercer Parcial', 'Ordinario', 'Extraordinario']


def validar_periodo(periodo):
    if periodo in periodos:
        return periodo
    else:
        raise ValidationError(
            'Los periosdos solo pueden ser Primer Parcial, Segundo Parcial, Tercer Parcial, Ordinario, Extraordinario')


class Periodo(models.Model):
    nombre = models.CharField(
        max_length=30, unique=True, validators=[validar_periodo])

    def __str__(self):
        return self.nombre
