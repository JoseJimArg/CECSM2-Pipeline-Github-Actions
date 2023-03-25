from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from calificaciones.models import Calificacion, Periodo
from ciclos.models import TipoCiclo, CicloEscolar
from usuarios.models import Docente, Alumno
from grupos.models import Letra, Semestre, Grupo
from materias.models import Materia
from clases.models import Clase


class TestModelCalificaciones(TestCase):

    def setUp(self):
        self.ciclo = self.crearCicloEscolar('par', '2021', '2022')
        self.grupo = self.crearGrupo('3', 'B')
        self.materia = self.crearMateria('Blockchain', 'La nueva materia')
        self.docente = self.crearDocente(
            'profe1',
            'Alonso',
            'Gonzalez',
            'profe1@gmail.com',
            'profe1',
            '12345678'
        )
        self.materia.docente.add(self.docente)
        self.alumno = self.crearAlumno(
            'alumno1',
            'Javier',
            'Chavez',
            'alumno1@gmail.com',
            'alumno1',
            '87654321'
        )
        self.clase = self.crearClase(
            self.materia,
            self.docente,
            self.ciclo,
            self.grupo
        )
        self.periodo = self.crearPeriodo('Primer Parcial')
        self.clase.alumno.add(self.alumno)

    def test_models_periodo_string_retorna_nombre_del_periodo(self):
        periodo = Periodo.objects.create(
            nombre='Segundo Parcial'
        )
        self.assertEqual(str(periodo), 'Segundo Parcial')

    def test_models_periodo_periodo_no_valido(self):
        periodo = Periodo.objects.create(
            nombre='Parcial 1'
        )
        with self.assertRaises(ValidationError):
            periodo.full_clean()

    def test_models_periodo_periodo_valido(self):
        Periodo.objects.create(
            nombre='Segundo Parcial'
        )
        self.assertEqual(Periodo.objects.all().count(), 2)

    def test_models_periodo_unico(self):
        with self.assertRaises(IntegrityError):
            Periodo.objects.create(
                nombre='Primer Parcial'
            )

    def test_models_calif_no_permitir_misma_calificacion_2_veces(self):
        Calificacion.objects.create(
            clase=self.clase,
            alumno=self.alumno,
            tipo=self.periodo,
            calificacion=10
        )
        with self.assertRaises(IntegrityError):
            Calificacion.objects.create(
                clase=self.clase,
                alumno=self.alumno,
                tipo=self.periodo,
                calificacion=9
            )

    def test_models_calificaciones_mayor_a_10(self):
        calificacion = Calificacion.objects.create(
            clase=self.clase,
            alumno=self.alumno,
            tipo=self.periodo,
            calificacion=10.1
        )
        with self.assertRaises(ValidationError):
            calificacion.full_clean()

    def test_models_calificaciones_menor_a_5(self):
        calificacion = Calificacion.objects.create(
            clase=self.clase,
            alumno=self.alumno,
            tipo=self.periodo,
            calificacion=4.9
        )
        with self.assertRaises(ValidationError):
            calificacion.full_clean()

    def test_models_calificaciones_permite_decimales(self):
        Calificacion.objects.create(
            clase=self.clase,
            alumno=self.alumno,
            tipo=self.periodo,
            calificacion=9.5
        )
        self.assertEqual(Calificacion.objects.count(), 1)

    def test_models_calificaciones_no_permite_mas_de_un_decimal(self):
        calificacion = Calificacion.objects.create(
            clase=self.clase,
            alumno=self.alumno,
            tipo=self.periodo,
            calificacion=9.55
        )
        with self.assertRaises(ValidationError):
            calificacion.full_clean()

    def test_models_calificaciones_acepta_numeros_sin_decimal(self):
        Calificacion.objects.create(
            clase=self.clase,
            alumno=self.alumno,
            tipo=self.periodo,
            calificacion=5
        )
        self.assertEqual(Calificacion.objects.count(), 1)

    def test_models_calificaciones_acepta_numeros_sin_decimal_dos_digitos(self):
        Calificacion.objects.create(
            clase=self.clase,
            alumno=self.alumno,
            tipo=self.periodo,
            calificacion=10
        )
        self.assertEqual(Calificacion.objects.count(), 1)

    def test_models_calificaciones_calificacion_diferente_parcial(self):
        Calificacion.objects.create(
            clase=self.clase,
            alumno=self.alumno,
            tipo=self.periodo,
            calificacion=10
        )
        periodo2 = self.crearPeriodo('Segundo Parcial')
        Calificacion.objects.create(
            clase=self.clase,
            alumno=self.alumno,
            tipo=periodo2,
            calificacion=10
        )
        self.assertEqual(Calificacion.objects.count(), 2)

    def test_models_calificaciones_modelo_string_es_calificacion(self):
        Calificacion.objects.create(
            clase=self.clase,
            alumno=self.alumno,
            tipo=self.periodo,
            calificacion=10
        )
        self.assertEqual(
            str(Calificacion.objects.first()),
            f'{self.clase.materia} - {self.alumno} - {self.periodo} - {float(10)}')

    # **********************TestHelpers*****************************

    def crearMateria(self, nombre, descripcion):
        materia = Materia.objects.create(
            nombre=nombre, descripcion=descripcion)
        return materia

    def crearDocente(self, username, first_name, last_name, email, password, matricula):
        return Docente.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            matricula=matricula
        )

    def crearCicloEscolar(self, tipo, anio_inicio, anio_fin):
        tipo_ciclo = tipo_ciclo = TipoCiclo.objects.create(nombre=tipo)
        return CicloEscolar.objects.create(
            anio_inicio=anio_inicio,
            anio_fin=anio_fin,
            tipo_ciclo=tipo_ciclo
        )

    def crearAlumno(self, username, first_name, last_name, email, password, matricula):
        return Alumno.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            matricula=matricula
        )

    def crearGrupo(self, semestre, letra):
        letra1 = Letra.objects.create(letra=letra)
        semestre1 = Semestre.objects.create(numero=semestre)
        return Grupo.objects.create(
            letra=letra1,
            semestre=semestre1
        )

    def crearClase(self, materia, docente, ciclo, grupo):
        return Clase.objects.create(
            materia=materia,
            docente=docente,
            ciclo=ciclo,
            grupo=grupo,
        )

    def crearPeriodo(self, nombre):
        return Periodo.objects.create(
            nombre=nombre
        )
