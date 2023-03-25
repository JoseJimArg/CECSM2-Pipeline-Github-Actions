from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from ..models import Semestre, Letra


class TestModels(TestCase):

    # ************* Test Semestre ****************

    def test_numero_semestre_obligatorio(self):
        with self.assertRaises(IntegrityError):
            Semestre.objects.create(numero=None)

    def test_numero_semestre_no_mayor_a_10(self):
        semestre = Semestre.objects.create(numero=11)
        with self.assertRaises(ValidationError):
            semestre.full_clean()

    def test_numero_semestre_no_menor_a_0(self):
        semestre = Semestre.objects.create(numero=-1)
        with self.assertRaises(ValidationError):
            semestre.full_clean()

    def test_numero_semestre_no_decimal(self):
        semestre = Semestre.objects.create(numero=1.5)
        semestre = Semestre.objects.first()
        resultado = float(semestre.numero) % 1
        self.assertEqual(resultado, 0)

    def test_numero_semestre_unico(self):
        Semestre.objects.create(numero=1)
        with self.assertRaises(IntegrityError):
            Semestre.objects.create(numero=1)

    def test_semestre_creado_exitosamente(self):
        semestre = Semestre.objects.create(numero=1)
        self.assertEqual(semestre.numero, 1)

    def test_semestre_guardado_exitosamente(self):
        semestre = Semestre.objects.create(numero=1)
        self.assertEqual(
            semestre.numero, Semestre.objects.get(numero=1).numero)

    # ************* Test Letra ****************}

    def test_letra_letra_obligatoria(self):
        with self.assertRaises(IntegrityError):
            Letra.objects.create(letra=None)

    def test_letra_no_permitida(self):
        letra = Letra.objects.create(letra='G')
        with self.assertRaises(ValidationError):
            letra.full_clean()

    def test_letra_no_minusculas(self):
        letra = Letra.objects.create(letra='g')
        with self.assertRaises(ValidationError):
            letra.full_clean()

    def test_letra_creada_exitosamente(self):
        letra = Letra.objects.create(letra='A')
        letra.save()
        self.assertEqual(Letra.objects.all().count(), 1)

    def test_letra_unica(self):
        letra = Letra.objects.create(letra='A')
        with self.assertRaises(IntegrityError):
            Letra.objects.create(letra='A')

    def test_letra_guardada_exitosamente(self):
        letra = Letra.objects.create(letra='A')
        self.assertEqual(letra.letra, Letra.objects.get(letra='A').letra)
