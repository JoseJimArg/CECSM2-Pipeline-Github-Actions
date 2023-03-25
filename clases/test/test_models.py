from django.test import TestCase
from django.core.exceptions import ValidationError


from clases.models import Clase
from usuarios.models import Docente
from materias.models import Materia
from grupos.models import Semestre, Letra, Grupo
from ciclos.models import CicloEscolar, TipoCiclo


class TestModel(TestCase):
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
            'docente': self.docente,
            'materia': self.materia,
            'ciclo': self.ciclo,
            'grupo': self.grupo
        }

    def test_modelo_clase_correcto(self):
        clase = Clase(
            docente=self.data_clase['docente'],
            materia=self.data_clase['materia'],
            ciclo=self.data_clase['ciclo'],
            grupo=self.data_clase['grupo'],
        )
        clase.full_clean()
        clase.save()
        self.assertEqual(Clase.objects.all().count(), 1)

    def test_modelo_clase_profesor_vacio(self):
        clase = Clase(
            materia=self.data_clase['materia'],
            ciclo=self.data_clase['ciclo'],
            grupo=self.data_clase['grupo'],
        )
        with self.assertRaises(ValidationError):
            clase.full_clean()

    def test_modelo_clase_materia_vacia(self):
        clase = Clase(
            docente=self.data_clase['docente'],
            ciclo=self.data_clase['ciclo'],
            grupo=self.data_clase['grupo'],
        )
        with self.assertRaises(ValidationError):
            clase.full_clean()

    def test_modelo_clase_ciclo_vacio(self):
        clase = Clase(
            docente=self.data_clase['docente'],
            materia=self.data_clase['materia'],
            grupo=self.data_clase['grupo'],
        )
        with self.assertRaises(ValidationError):
            clase.full_clean()

    def test_modelo_clase_grupo_vacio(self):
        clase = Clase(
            docente=self.data_clase['docente'],
            materia=self.data_clase['materia'],
            ciclo=self.data_clase['ciclo'],
        )
        with self.assertRaises(ValidationError):
            clase.full_clean()

    def test_modelo_clase_to_string(self):
        clase = Clase(
            docente=self.data_clase['docente'],
            materia=self.data_clase['materia'],
            ciclo=self.data_clase['ciclo'],
            grupo=self.data_clase['grupo'],
        )
        self.assertEqual(str(
            clase), f"{self.data_clase['docente']} {self.data_clase['materia']} {self.data_clase['grupo']} {self.data_clase['ciclo']}")
