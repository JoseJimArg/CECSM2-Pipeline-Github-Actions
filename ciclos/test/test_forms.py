from django.test import TestCase
from ciclos.forms import CicloEscolarForm
from ciclos.models import TipoCiclo

class TestFormsCiclos(TestCase):
    
    def setUp(self):
        self.tipo_ciclo = TipoCiclo.objects.create(nombre='par')
        self.ciclo_escolar = CicloEscolarForm(data={
            'anio_inicio': 2021,
            'anio_fin': 2022,
            'tipo_ciclo': self.tipo_ciclo,
        })
        
    def test_form_ciclo_escolar_años_deben_ser_diferentes(self):
        self.ciclo_escolar.data['anio_inicio'] = 2022
        self.assertFalse(self.ciclo_escolar.is_valid())
        
    def test_form_ciclo_escolar_año_inicio_debe_ser_menor_a_año_fin(self):
        self.ciclo_escolar.data['anio_fin'] = 2020
        self.assertFalse(self.ciclo_escolar.is_valid())
        
    def test_form_ciclo_escolar_diferiencia_de_años_debe_ser_1(self):
        self.ciclo_escolar.data['anio_fin'] = 2023
        self.assertFalse(self.ciclo_escolar.is_valid())