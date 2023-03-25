from django.test import TestCase
from materias.forms import FormMateria, FormMateriaEditar
from materias.models import Materia


class TestFormMateria(TestCase):

    def setUp(self):
        self.materia_data = {
            'nombre': "Anatomia",
            'descripcion': "Estudio del cuerpo humano"
        }

    # Test for US about add some Materias to field.add()

    def test_form_materia_correcto(self):
        form = FormMateria(self.materia_data)
        self.assertTrue(form.is_valid)

    def test_form_nombre_largo(self):
        self.materia_data['nombre'] = "asdasdasdasdasdasdasdasdasdaasdasdasdasdasdasdasdaasdasdasdaasd"
        form = FormMateria(self.materia_data)
        self.assertEqual(form.errors['nombre'], [
                         'Asegúrese de que este valor tenga como máximo 60 caracteres (tiene 63).'])

    def test_form_nombre_vacio(self):
        self.materia_data['nombre'] = ""
        form = FormMateria(self.materia_data)
        self.assertEqual(form.errors['nombre'], ['Este campo es obligatorio.'])

    def test_form_descripcion_vacia(self):
        self.materia_data['descripcion'] = ""
        form = FormMateria(self.materia_data)
        self.assertEqual(form.errors['descripcion'], [
                         'Este campo es obligatorio.'])

    # Test for FormMateriEditar form.

    def test_form_edicion_materia_correcto(self):
        form = FormMateriaEditar(self.materia_data)
        self.assertTrue(form.is_valid)

    def test_form_editar_descripcion_vacia(self):
        self.materia_data['descripcion'] = ""
        form = FormMateriaEditar(self.materia_data)
        self.assertEqual(form.errors['descripcion'], [
                         'Este campo es obligatorio.'])
