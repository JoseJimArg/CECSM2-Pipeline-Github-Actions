from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.urls import reverse
from test.helpers.permissions import Permissions

from usuarios.models import Alumno, Docente
from materias.models import Materia
from grupos.models import Grupo, Letra, Semestre
from ciclos.models import CicloEscolar, TipoCiclo
from clases.models import Clase


class TestViws(TestCase):

    @classmethod
    def setUpTestData(cls):
        Permissions.create_permissions()
        
    def setUp(self):
        # Create Dcente
        self.docente = Docente.objects.create(
            username='profechido',
            first_name='Mauricio',
            last_name='Martinez',
            email='docente@test.com',
            matricula='35166865',)
        self.docente.set_password('Clavecita123k.')
        self.docente.save()

        self.alumno = Alumno.objects.create(
            username="alumno",
            first_name="Oscar",
            last_name="Corvera",
            email="alumno@gmail.com",
            matricula="35166866"
        )
        self.alumno.set_password("Alumno#1")
        self.alumno.save()

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

        self.data_clase = {
            'docente': self.docente.id,
            'materia': self.materia.id,
            'ciclo': self.ciclo.id,
            'grupo': self.grupo.id,
            'cupo_total': 50
        }

        # Set materia to docente who teach that materia.
        self.materia.docente.add(self.docente)

        # Login before execute any test
        self.admin = self.login_admin()

    # Tests for add a new Clase

    def test_responde_url_agregar_clase(self):
        response = self.client.get('/clases/nueva/')
        self.assertEqual(response.status_code, 200)

    def test_nombre_url_agregar_clase(self):
        response = self.client.get(reverse('clases:nueva'))
        self.assertEqual(response.status_code, 200)

    def test_obtiene_template_nueva_clase(self):
        response = self.client.get('/clases/nueva/')
        self.assertTemplateUsed(response, 'nueva_clase.html')

    def test_hay_titulo_de_pagina_Crear_nueva_clase(self):
        response = self.client.get('/clases/nueva/')
        self.assertContains(response, 'Crear nueva clase')

    def test_hay_titulo_campo_agregar_docente(self):
        response = self.client.get('/clases/nueva/')
        self.assertContains(response, 'Docente:')

    def test_hay_select_agregar_docente(self):
        response = self.client.get('/clases/nueva/')
        self.assertContains(response, '<select name="docente"')

    def test_hay_titulo_campo_agregar_materia(self):
        response = self.client.get('/clases/nueva/')
        self.assertContains(response, 'Materia:')

    def test_hay_select_agregar_materia(self):
        response = self.client.get('/clases/nueva/')
        self.assertContains(response, '<select name="materia"')

    def test_hay_titulo_campo_agregar_ciclo(self):
        response = self.client.get('/clases/nueva/')
        self.assertContains(response, 'Ciclo:')

    def test_hay_select_agregar_ciclo(self):
        response = self.client.get('/clases/nueva/')
        self.assertContains(response, '<select name="ciclo"')

    def test_hay_titulo_campo_agregar_grupo(self):
        response = self.client.get('/clases/nueva/')
        self.assertContains(response, 'Grupo:')

    def test_hay_select_agregar_grupo(self):
        response = self.client.get('/clases/nueva/')
        self.assertContains(response, '<select name="grupo"')

    def test_hay_boton_guardar_clase(self):
        response = self.client.get('/clases/nueva/')
        self.assertContains(
            response, '<button type="submit" id="submit_button"')

    def test_crear_clase_satisfactoriamente(self):
        response = self.client.post('/clases/nueva/', data=self.data_clase)
        self.assertEqual(Clase.objects.all().count(), 1)

    def test_no_crea_la_misma_clase_dos_veces(self):
        self.client.post('/clases/nueva/', data=self.data_clase)
        self.client.post('/clases/nueva/', data=self.data_clase)
        self.assertEqual(Materia.objects.all().count(), 1)

    def test_muestra_mensaje_materia_ya_registrada(self):
        self.client.post('/clases/nueva/', data=self.data_clase)
        response = self.client.post('/clases/nueva/', data=self.data_clase)
        self.assertContains(response, 'La clase ya está registrada.')

    def test_muestra_mensaje_creado_satisfactoriamente(self):
        # Create Dcente
        docente2 = Docente.objects.create(
            username='profechido2',
            first_name='Mauricio2',
            last_name='Martinez2',
            email='docente2@test.com',
            matricula='35166065',)
        docente2.set_password('Clavecita123k.')
        docente2.save()
        # Set docente to materia
        self.materia.docente.add(docente2)
        # Set the new data to clase
        data_clase2 = {
            'docente': docente2.id,
            'materia': self.materia.id,
            'ciclo': self.ciclo.id,
            'grupo': self.grupo.id,
            'cupo_total': 50
        }
        response = self.client.post('/clases/nueva/', data=data_clase2)
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Clase agregada correctamente')

    def test_muestra_mensaje_profesor_no_imparte_materia(self):
        # Create Dcente
        docente2 = Docente.objects.create(
            username='profechido2',
            first_name='Mauricio2',
            last_name='Martinez2',
            email='docente2@test.com',
            matricula='35166065',)
        docente2.set_password('Clavecita123k.')
        docente2.save()
        # Set the new data to clase
        data_clase2 = {
            'docente': docente2.id,
            'materia': self.materia.id,
            'ciclo': self.ciclo.id,
            'grupo': self.grupo.id,
            'cupo_total': 50,
        }
        response = self.client.post('/clases/nueva/', data=data_clase2)
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), f'La materia {self.materia} no es impartida por {docente2}.')

    # Class assign

    def test_responde_url_asignar_clase(self):
        alumno = Alumno.objects.get(first_name='Oscar')
        self.client.post('/clases/nueva/', data=self.data_clase)
        response = self.client.get(f"/clases/agregar-clase/{alumno.id}")
        self.assertEqual(response.status_code, 200)

    def test_login_required_asignar_clase(self):
        self.client.post('/clases/nueva/', data=self.data_clase)
        self.client.logout()
        response = self.client.get("/clases/agregar-clase/2")
        self.assertEqual(response.status_code, 302)

    def test_utiliza_template_correcta_asignar_clase(self):
        alumno = Alumno.objects.get(first_name='Oscar')
        self.client.post('/clases/nueva/', data=self.data_clase)
        response = self.client.get(f"/clases/agregar-clase/{alumno.id}")
        self.assertTemplateUsed(response, "asignar_clase.html")

    def test_recupera_clases_asignadas_asignar_clase(self):
        self.client.post('/clases/nueva/', data=self.data_clase)
        clase = Clase.objects.first()
        alumno = Alumno.objects.get(first_name='Oscar')
        clase.alumno.add(alumno)
        response = self.client.get(f"/clases/agregar-clase/{alumno.id}")
        self.assertContains(response, "Testing")

    def test_mensaje_clase_no_seleccionada_asignar_clase(self):
        self.client.post('/clases/nueva/', data=self.data_clase)
        alumno = Alumno.objects.get(first_name='Oscar')
        response = self.client.post(
            f'/clases/agregar-clase/{alumno.id}',
            data={
                "nombre_materia_input": "anatomia"
            }
        )
        mensajes = list(response.context.get("messages"))
        self.assertEqual(
            str(mensajes[0]), "No se seleccionó una clase de la lista.")

    def test_mensaje_clase_repetida_asignar_clase(self):
        self.client.post('/clases/nueva/', data=self.data_clase)
        clase = Clase.objects.first()
        alumno = Alumno.objects.get(first_name='Oscar')
        clase.alumno.add(alumno)
        response = self.client.post(
            f'/clases/agregar-clase/{alumno.id}',
            data={
                "nombre_materia_input": "Testing",
                "id_clase": clase.id
            }
        )
        mensajes = list(response.context.get("messages"))
        self.assertEqual(
            str(mensajes[0]), "Este alumno ya está inscrito a esta materia")

    def test_recupera_clases_asignar_clase(self):
        self.client.post('/clases/nueva/', data=self.data_clase)
        response = self.client.get('/clases/buscar-clase/?clase=Test')
        self.assertContains(response, "Testing")

    def test_recupera_clases_vacio_asignar_clase(self):
        self.client.post('/clases/nueva/', data=self.data_clase)
        response = self.client.get('/clases/buscar-clase/?')
        self.assertContains(response, "[]")

    def test_asigna_correctamente_asignar_clase(self):
        self.client.post('/clases/nueva/', data=self.data_clase)
        clase = Clase.objects.first()
        alumno = Alumno.objects.get(first_name='Oscar')
        response = self.client.post(
            f'/clases/agregar-clase/{alumno.id}',
            data={
                "nombre_materia_input": "Testing",
                "id_clase": clase.id
            }
        )
        mensajes = list(response.context.get("messages"))
        self.assertEqual(str(
            mensajes[0]), f"Se registró la materia {clase} al alumno {alumno.first_name}")

    def test_alumno_inexistente_asignar_clase(self):
        self.client.post('/clases/nueva/', data=self.data_clase)
        response = self.client.post(
            '/clases/agregar-clase/5',
            data={
                "nombre_materia_input": "Testing",
                "id_clase": 1
            }
        )
        response = self.client.get("/alumnos/")
        mensajes = list(response.context.get("messages"))
        self.assertEqual(str(mensajes[0]), f"El alumno ingresado no existe.")

    # Class list

    def test_responde_url_lista_clases(self):
        response = self.client.get('/clases/')
        self.assertEqual(response.status_code, 200)

    def test_hay_boton_nueva_lista_clases(self):
        response = self.client.get('/clases/')
        self.assertContains(response, 'Nueva')

    def test_utiliza_template_correcta_lista_clases(self):
        response = self.client.get('/clases/')
        self.assertTemplateUsed(response, "lista_clases.html")

    def test_muestra_mensaje_no_clases_lista_clases(self):
        response = self.client.get('/clases/')
        self.assertContains(response, "No hay clases registradas")

    def test_muestra_clase_lista_clases(self):
        self.client.post('/clases/nueva/', data=self.data_clase)
        response = self.client.get('/clases/')
        self.assertContains(response, "Testing")

    # Methods to help tests

    def login_admin(self):
        admin = self.agregar_admin()
        self.client.login(username=admin.username, password="Corverita#1")

    def agregar_admin(self):
        username = 'corveritaAdmin'
        email = 'corveritaAdmin@test.com'
        password = 'Corverita#1'
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        admin_grupo=Group.objects.get(name="Administrador_Grupo")
        user.groups.add(admin_grupo)
        return user
