from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from calificaciones.models import Periodo
from ciclos.models import TipoCiclo, CicloEscolar
from test.helpers.permissions import Permissions
from usuarios.models import Docente, Alumno
from grupos.models import Letra, Semestre, Grupo
from materias.models import Materia
from clases.models import Clase


class TestViewsCalificaciones(TestCase):

    @classmethod
    def setUpTestData(cls):
        Permissions.create_permissions()

    def setUp(self):
        self.ciclo = self.crearCicloEscolar('par', '2021', '2022')
        self.grupo = self.crearGrupo('3', 'B')
        self.materia = self.crearMateria('Blockchain', 'La nueva materia')
        self.docente = self.crearDocente(
            'profe5',
            'Alonso',
            'Gonzalez',
            'profe5@gmail.com',
            'Profesor.5',
            '12345672'
        )
        self.docente.save()
        docente_grupo=Group.objects.get(name="Docente_Grupo")
        self.docente.groups.add(docente_grupo)
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
        self.client.login(username=self.docente.username,
                          password='Profesor.5')

    def test_views_calificaciones_registrar_url(self):
        response = self.client.get(
            f'/calificaciones/registrar/{self.clase.id}/{self.periodo.id}')
        self.assertEqual(response.status_code, 200)

    def test_views_calificaciones_registrar_login_requerido(self):
        self.client.logout()
        response = self.client.get(
            f'/calificaciones/registrar/{self.clase.id}/{self.periodo.id}')
        self.assertEqual(response.status_code, 302)

    def test_views_calificaciones_registrar_nombre_url(self):
        response = self.client.get(
            reverse('calificaciones:registrar', args=[self.clase.id, self.periodo.id]))
        self.assertEqual(response.status_code, 200)

    def test_views_calificaciones_registrar_periodo_no_valido(self):
        response = self.client.get(
            reverse('calificaciones:registrar', args=[self.clase.id, 0]))
        self.assertContains(response, 'El parcial no existe')

    def test_views_calificaciones_registrar_clase_no_existe(self):
        response = self.client.get(
            f'/calificaciones/registrar/2/{self.periodo.id}')
        self.assertEqual(response.status_code, 404)

    def test_views_calificaciones_registrar_exitosamente(self):
        response = self.client.post(
            f'/calificaciones/registrar/{self.clase.id}/{self.periodo.id}',
            data={
                self.alumno.id: '8'
            }
        )
        self.assertContains(response, 'Se registraron 1 calificaciones')

    def test_views_calificaciones_registrar_modificacion_exitosa(self):
        self.client.post(
            f'/calificaciones/registrar/{self.clase.id}/{self.periodo.id}',
            data={
                self.alumno.id: '9'
            }
        )
        response = self.client.post(
            f'/calificaciones/registrar/{self.clase.id}/{self.periodo.id}',
            data={
                self.alumno.id: '7'
            }
        )
        self.assertContains(response, 'Se registraron 1 calificaciones')

    def test_views_calificaciones_registrar_no_mandar_calificacion(self):
        response = self.client.post(
            f'/calificaciones/registrar/{self.clase.id}/{self.periodo.id}',
            data={
                self.alumno.id: ''
            }
        )
        self.assertContains(response, 'Se registraron 0 calificaciones')

    def test_views_calificaciones_registrar_alumno_no_pertenece_clase(self):
        alumno2 = self.crearAlumno(
            'alumno2',
            'Javier2',
            'Chavez',
            'alumno2@gmail.com',
            'alumno2',
            '87654322'
        )
        response = self.client.post(
            f'/calificaciones/registrar/{self.clase.id}/{self.periodo.id}',
            data={
                alumno2.id: '10'
            }
        )
        self.assertContains(response, 'Se registraron 0 calificaciones')

    def test_views_calificaciones_registrar_calificacion_menos_de_5(self):
        response = self.client.post(
            f'/calificaciones/registrar/{self.clase.id}/{self.periodo.id}',
            data={
                self.alumno.id: '4.9'
            }
        )
        self.assertContains(response, 'Se registraron 0 calificaciones')

    def test_views_calificaciones_registrar_calificacion_mayor_a_10(self):
        response = self.client.post(
            f'/calificaciones/registrar/{self.clase.id}/{self.periodo.id}',
            data={
                self.alumno.id: '10.1'
            }
        )
        self.assertContains(response, 'Se registraron 0 calificaciones')

    # Tests for Consultar calificaciones of Alumno
    def test_responde_url_consultar_calificaciones(self):
        response = self.client.get('/calificaciones/consulta/')
        self.assertEqual(response.status_code, 200)

    def test_nombre_url_consulta_calificaciones(self):
        response = self.client.get(
            reverse('calificaciones:consulta'))
        self.assertEqual(response.status_code, 200)

    def test_obtiene_template_consulta_calificaciones(self):
        response = self.client.get('/calificaciones/consulta/')
        self.assertTemplateUsed(
            response, 'consulta_calificaciones_alumno.html')

    def test_hay_titulo_de_pagina_consulta_calificaciones(self):
        response = self.client.get('/calificaciones/consulta/')
        self.assertContains(response, 'Consulta de Calificaciones')

    def test_hay_titulo_campo_ingresar_matricula(self):
        response = self.client.get('/calificaciones/consulta/')
        self.assertContains(response, 'Matricula del Alumno:')

    def test_hay_campo_ingresar_matricula_alumno(self):
        response = self.client.get('/calificaciones/consulta/')
        self.assertContains(response, 'name="matricula_alumno"')

    def test_muestra_tabla_calificaciones(self):
        self.alumno.save()
        data = {
            'matricula_alumno': '87654321'
        }
        response = self.client.post(
            '/calificaciones/consulta/', data=data)
        self.assertContains(response, 'name="tabla_calificaciones"')

    def test_muestra_mensaje_cuando_no_encuentra_matricula(self):
        self.alumno.save()
        data = {
            'matricula_alumno': '11111111'
        }
        response = self.client.post(
            '/calificaciones/consulta/', data=data)
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Alumno no encontrado.')

    # **********************TestHelpers*****************************

    def crearMateria(self, nombre, descripcion):
        materia = Materia.objects.create(
            nombre=nombre, descripcion=descripcion)
        return materia

    def crearDocente(self, username, first_name, last_name, email, password, matricula):
        docente = Docente.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            matricula=matricula
        )
        docente.set_password(password)
        docente.save()
        return docente

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

    def crearAdmin(self):
        admin = User.objects.create_superuser(
            username='admin', password='admin.123')
        return admin

    def crearPeriodo(self, nombre):
        return Periodo.objects.create(
            nombre=nombre
        )
