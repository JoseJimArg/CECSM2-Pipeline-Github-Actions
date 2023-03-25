from django.db import models

from django.core.validators import MinValueValidator
# Create your models here.


# M0odel to Clase entity.
class Clase(models.Model):

    class Meta:
        unique_together = [['materia', 'ciclo', 'grupo']]

    docente = models.ForeignKey(
        "usuarios.Docente", verbose_name="Docente", on_delete=models.CASCADE)
    materia = models.ForeignKey(
        "materias.Materia", verbose_name="Materia", on_delete=models.CASCADE)
    ciclo = models.ForeignKey('ciclos.CicloEscolar',
                              verbose_name="Ciclo", on_delete=models.CASCADE)
    grupo = models.ForeignKey(
        'grupos.Grupo', verbose_name="Grupo", on_delete=models.CASCADE)
    alumno = models.ManyToManyField('usuarios.Alumno', blank=True)
    aspirantes = models.ManyToManyField('usuarios.Aspirante', blank=True)
    cupo_total = models.IntegerField(default=0, blank=True, validators=[MinValueValidator(0)])
    cupo_restante = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.docente} {self.materia} {self.grupo} {self.ciclo}'
