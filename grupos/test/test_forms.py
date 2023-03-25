from django.test import TestCase
from ..forms import GrupoForm
from ..models import Semestre, Letra


class FormsTestCase(TestCase):

    def setUp(self):
        self.letra = Letra.objects.create(letra='A')
        self.semestre = Semestre.objects.create(numero='1')
        self.grupo_form_data = {
            'semestre': self.semestre,
            'letra': self.letra,
        }

    def test_formulario_grupo_valido(self):
        form = GrupoForm(self.grupo_form_data)
        self.assertTrue(form.is_valid())

    def test_grupo_unico(self):
        form = GrupoForm(self.grupo_form_data)
        form.save()
        form = GrupoForm(self.grupo_form_data)
        self.assertFalse(form.is_valid())

    def test_semestre_requerido(self):
        self.grupo_form_data.pop('semestre')
        form = GrupoForm(self.grupo_form_data)
        self.assertFalse(form.is_valid())

    def test_letra_requerida(self):
        self.grupo_form_data.pop('letra')
        form = GrupoForm(self.grupo_form_data)
        self.assertFalse(form.is_valid())

    def test_semestre_letra_requeridos(self):
        self.grupo_form_data.pop('semestre')
        self.grupo_form_data.pop('letra')
        form = GrupoForm(self.grupo_form_data)
        self.assertFalse(form.is_valid())

    def test_dos_grupos_diferentes(self):
        form = GrupoForm(self.grupo_form_data)
        form.save()
        self.grupo_form_data['letra'] = Letra.objects.create(letra='B')
        form = GrupoForm(self.grupo_form_data)
        self.assertTrue(form.is_valid())

    def test_opcion_semestre_no_existente(self):
        self.grupo_form_data['semestre'] = '3'
        form = GrupoForm(self.grupo_form_data)
        self.assertFalse(form.is_valid())

    def opcion_letra_no_existente(self):
        self.grupo_form_data['letra'] = 'B'
        form = GrupoForm(self.grupo_form_data)
        self.assertFalse(form.is_valid())
