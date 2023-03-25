from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


class Semestre(models.Model):
    numero = models.IntegerField(unique=True,
                                 validators=[MinValueValidator(0), MaxValueValidator(10)])

    def __str__(self):
        return str(self.numero)


letras_permitidas = ['A', 'B', 'C', 'D', 'E', 'F']


def letra_validaciones(letra):
    if letra in letras_permitidas:
        return letra
    else:
        raise ValidationError('Letra no permitida')


class Letra(models.Model):
    letra = models.CharField(max_length=1, unique=True,
                             validators=[letra_validaciones])

    def __str__(self):
        return str(self.letra)


class Grupo(models.Model):

    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    letra = models.ForeignKey(Letra, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('semestre', 'letra')

    def __str__(self):
        return f'{self.semestre.numero}{self.letra.letra}'
