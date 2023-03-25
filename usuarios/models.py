from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator

# Create your models here.

User._meta.get_field('email')._unique = True
User._meta.get_field('email').null = False
User._meta.get_field('first_name').blank = False
User._meta.get_field('first_name').null = False
User._meta.get_field('last_name').blank = False
User._meta.get_field('last_name').null = False
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False


class Docente(User):
    class Meta:
        verbose_name = "Docente"
    matricula = models.CharField(
        "Matrícula", unique=True,
        max_length=8,
        validators=[
            RegexValidator(
                regex='^.{8}$',
                message='El tamaño mínimo debe ser de 8',
                code='nomatch'
            )
        ]
    )

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Alumno(User):
    class Meta:
        verbose_name = "Alumno"
    matricula = models.CharField(
        "Matrícula",
        unique=True,
        max_length=8,
        validators=[
            RegexValidator(
                regex='^.{8}$',
                message='El tamaño mínimo debe ser de 8',
                code='nomatch'
            )
        ]
    )

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

class Aspirante(User):
    class Meta:
        verbose_name = "Aspirante"

    num_aspirante=models.IntegerField()
    comprobante_pago=models.FileField(upload_to="aspirantes/comprobante_pago/")
    valido_comprobante_pago = models.BooleanField(unique=False, blank=True, null=True, default=None) # Ayuda para saber si su documentación es válida.
    status=models.SmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(2)]) # 0 pendiente, 1 aceptado, 2 rechazado
    grupo = models.ForeignKey("grupos.Grupo", verbose_name = 'Grupo', on_delete = models.CASCADE, default=None, null=True, blank=True)
    
    def __str__(self):
        return self.num_aspirante

    def get_grupo(self):
        return self.grupo
