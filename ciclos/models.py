from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.core.exceptions import ValidationError


# Método para validar que el tipo de ciclo solo pueda ser non o par
def validateTypeName(nombre):
    if nombre == 'par' or nombre == 'non':
        return nombre
    else:
        raise ValidationError('El tipo solo puede ser par o non')


class TipoCiclo(models.Model):
    nombre = models.CharField(
        unique=True, max_length=50, validators=[validateTypeName])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.nombre


class CicloEscolar(models.Model):
    anio_inicio = models.IntegerField(
        validators=[MinValueValidator(2015), MaxValueValidator(2099)])
    anio_fin = models.IntegerField(
        validators=[MinValueValidator(2016), MaxValueValidator(2100)])
    tipo_ciclo = models.ForeignKey(TipoCiclo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    class Meta:
        unique_together = ('anio_inicio', 'anio_fin', 'tipo_ciclo')


    def is_active(self):
        return self.activo


    def update_active(self, active=False):
        self.activo = active
        self.save()


    # Retorne como string 2021-2022non
    def __str__(self):
        return f'{self.anio_inicio}-{self.anio_fin}{self.tipo_ciclo}'
