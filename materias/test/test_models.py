from django.test import TestCase
from materias.models import Materia
from usuarios.models import Docente
from django.core.exceptions import ValidationError
from django.db import IntegrityError
# from sqlite3 import IntegrityError


class TestModels(TestCase):
    def setUp(self):
        self.datos = {
            'nombre': 'Anatomia',
            'descripcion': 'Estudio de las partes y funcionamiento del cuerpo humano',
        }
        self.materia = Materia(
            nombre='Anatomia',
            descripcion='Estudio de las partes y funcionamiento del cuerpo humano'
        )

    def test_return_objeto_materia(self):
        self.materia.full_clean()
        self.materia.save()
        self.assertEqual(Materia.objects.all().count(), 1)

    def test_guarda_nombre_correctamente(self):
        self.materia.full_clean()
        self.materia.save()
        self.assertEqual(Materia.objects.first().nombre, self.materia.nombre)

    def test_guarda_descripcion_correctamente(self):
        self.materia.full_clean()
        self.materia.save()
        self.assertEqual(Materia.objects.first().descripcion,
                         self.materia.descripcion)

    def test_no_nombre_largo_materia(self):
        self.materia.nombre = 'asdasdasdasdasdasdasdasdasdaasdasdasdasdasdasdasdaasdasdasdasdasdasdasdasdasdaasdasdasdasdasdasdasdaasdasdasdasdasdasdasdasdasdaasdasdasdasdasdasdasdaasdasdasdasdasdasdasdasdasdaasdasdasdasdasdasdasda'
        with self.assertRaises(ValidationError):
            self.materia.full_clean()

    def test_no_nombre_vacio(self):
        self.materia.nombre = ''
        with self.assertRaises(ValidationError):
            self.materia.full_clean()

    def test_no_descripcion_vacia(self):
        self.materia.descripcion = ''
        with self.assertRaises(ValidationError):
            self.materia.full_clean()

    def test_nombre_materia_unique(self):
        materia1 = Materia(
            nombre="Nombre repetido",
            descripcion="Diferente decripcion"
        )
        materia1.full_clean()
        materia1.save()
        materia2 = Materia(
            nombre="Nombre repetido",
            descripcion="Diferente descripcion 2"
        )

        with self.assertRaises(ValidationError):
            materia2.full_clean()

    def test_model_materia_docente_permitido_materia_sin_docentes(self):
        Materia.objects.create(
            nombre="Nombre repetido",
            descripcion="Diferente decripcion"
        )
        self.assertEqual(Materia.objects.all().count(), 1)

    def test_model_materia_docente_docente_no_repetido(self):
        materia1 = Materia.objects.create(
            nombre="Nombre repetido",
            descripcion="Diferente decripcion"
        )
        docente = self.crear_docente(
            'profe1', 'Alonso', 'Gonzalez', 'profe1@gmail.com', 'profe1', '12345678')
        materia1.docente.add(docente)
        materia1.docente.add(docente)
        self.assertEqual(materia1.docente.all().count(), 1)

    # ************************* Help test *************************

    def crear_docente(self, username, first_name, last_name, email, password, matricula):
        return Docente.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            matricula=matricula
        )
