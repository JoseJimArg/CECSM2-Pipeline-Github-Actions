from django.test import TestCase


from clases.forms import FormClase
from usuarios.models import Docente
from materias.models import Materia
from grupos.models import Semestre, Letra, Grupo
from ciclos.models import CicloEscolar, TipoCiclo


class TestForm(TestCase):
    # Create Dcente
    def setUp(self):
        self.docente = Docente.objects.create(
            username='profechido',
            first_name='Mauricio',
            last_name='Martinez',
            email='docente@test.com',
            matricula='35166865',)
        self.docente.set_password('Clavecita123k.')
        self.docente.save()

        # Create Materia
        self.materia = Materia(
            nombre='Testing',
            descripcion='Materia para aprender a hacer testing chido.',
        )
        self.materia.save()

        # Create Semestre
        self.semestre = Semestre.objects.create(numero=3)
        self.semestre.save()

        # Create Letra
        self.letra = Letra.objects.create(letra="B")
        self.letra.save()

        # Create grupo
        self.grupo = Grupo.objects.create(
            semestre=self.semestre,
            letra=self.letra
        )
        self.grupo.save()

        # Create tipo ciclo
        self.tipo_ciclo = TipoCiclo.objects.create(nombre="par")
        self.tipo_ciclo.save()

        # Create ciclo
        self.ciclo = CicloEscolar.objects.create(
            anio_inicio="2020",
            anio_fin="2021",
            tipo_ciclo=self.tipo_ciclo
        )
        self.ciclo.save()

        # Assing materia to docente
        self.materia.docente.add(self.docente)

        # Clase data
        self.data_clase = {
            'docente': self.docente.id,
            'materia': self.materia.id,
            'ciclo': self.ciclo.id,
            'grupo': self.grupo.id
        }

    # Test for FormClase to add a new clase
    def test_form_clase_correcto(self):
        form = FormClase(self.data_clase)
        self.assertTrue(form.is_valid())

    def test_form_clase_docente_vacio(self):
        self.data_clase['docente'] = None
        form = FormClase(self.data_clase)
        self.assertFalse(form.is_valid())

    def test_form_clase_materia_vacio(self):
        self.data_clase['materia'] = None
        form = FormClase(self.data_clase)
        self.assertFalse(form.is_valid())

    def test_form_clase_ciclo_vacio(self):
        self.data_clase['ciclo'] = None
        form = FormClase(self.data_clase)
        self.assertFalse(form.is_valid())

    def test_form_clase_grupo_vacio(self):
        self.data_clase['grupo'] = None
        form = FormClase(self.data_clase)
        self.assertFalse(form.is_valid())

    # Methods to help tests
