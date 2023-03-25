from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from ciclos.models import CicloEscolar, TipoCiclo


class TestModelsCiclos(TestCase):

    def setUp(self):
        self.tipo_ciclo = TipoCiclo.objects.create(nombre='par')
        self.ciclo_escolar = CicloEscolar.objects.create(
            anio_inicio=2021, anio_fin=2022, tipo_ciclo=self.tipo_ciclo)

    # ********************* Test TipoCiclo model **********************

    def test_model_tipo_ciclo_solo_puede_ser_par_o_non(self):
        tipo = TipoCiclo.objects.create(nombre='otro')
        with self.assertRaises(ValidationError):
            tipo.full_clean()

    def test_model_tipo_ciclo_unicos(self):
        with self.assertRaises(IntegrityError):
            TipoCiclo.objects.create(nombre='par')

    def test_model_tipo_ciclo_agregar_exitosamente_non(self):
        tipo = TipoCiclo.objects.create(nombre='non')
        self.assertEqual(tipo.nombre, 'non')

    def test_model_tipo_ciclo_agregar_exitosamente_par(self):
        ciclo = TipoCiclo.objects.get(nombre='par')
        ciclo.delete()
        tipo = TipoCiclo.objects.create(nombre='par')
        self.assertEqual(tipo.nombre, 'par')

    # ********************* Test CicloEscolar model **********************

    def test_model_ciclo_escolar_anio_no_mayor_a_2100(self):
        self.ciclo_escolar.anio_fin = 2101
        with self.assertRaises(ValidationError):
            self.ciclo_escolar.full_clean()

    def test_model_ciclo_escolar_anios_y_tipo_unicos(self):
        with self.assertRaises(IntegrityError):
            CicloEscolar.objects.create(
                anio_inicio=2021, anio_fin=2022, tipo_ciclo=self.tipo_ciclo)

    def test_model_ciclo_escolar_anios_minimo_2015(self):
        self.ciclo_escolar.anio_inicio = 2014
        with self.assertRaises(ValidationError):
            self.ciclo_escolar.full_clean()

    def test_model_ciclo_escolar_string(self):
        self.assertEqual(str(self.ciclo_escolar), '2021-2022par')
