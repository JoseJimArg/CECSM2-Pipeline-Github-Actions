from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.http import response
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from materias.models import Materia
from test.helpers.permissions import Permissions
from usuarios.models import Docente


class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        Permissions.create_permissions()

    def setUp(self):
        self.data = {
            'nombre': 'Materia de prueba',
            'descripcion': 'Descripcion de prueba.',
        }
        self.materia_defatult = Materia.objects.create(
            nombre='Nombre materia default',
            descripcion='Descripcion de la materia por defecto'
        )
        self.usuario = self.login_admin()

    def test_test(self):
        self.assertEqual(2, 2)

    def test_responde_url_agregar_materia(self):
        response = self.client.get('/materias/agregar/')
        self.assertEqual(response.status_code, 200)

    def test_nombre_url_agregar_materia(self):
        response = self.client.get(reverse('materias:agregar'))
        self.assertEqual(response.status_code, 200)

    def test_obtiene_template_agregar_materia(self):
        response = self.client.get('/materias/agregar/')
        self.assertTemplateUsed(response, 'agregar_materia.html')

    def test_hay_titulo_del_campo_para_agregar_nombre(self):
        response = self.client.get('/materias/agregar/')
        self.assertContains(response, 'Nombre')

    def test_hay_campo_para_agregar_nombre(self):
        response = self.client.get('/materias/agregar/')
        self.assertContains(response, '<input type="text" name="nombre"')

    def test_hay_titulo_del_campo_para_agregar_descripcion(self):
        response = self.client.get('/materias/agregar/')
        self.assertContains(response, 'Descripcion')

    def test_hay_campo_para_agregar_descripcion(self):
        response = self.client.get('/materias/agregar/')
        self.assertContains(response, '<textarea name="descripcion"')

    def test_hay_boton_guardar_materia(self):
        response = self.client.get('/materias/agregar/')
        self.assertContains(response, '<button id="id_btn_guardar"')

    def test_agrega_materia(self):
        response = self.client.post('/materias/agregar/', data=self.data)
        self.assertEqual(Materia.objects.all().count(), 2)

    def test_muestra_mensaje_error_longitud_nombre_tempalte(self):
        self.data['nombre'] = 'asdasdasdasdasdasdasdasdasdaasdasdasdasdasdasdasdaasdasdasdasdasdasdasdasdasdaasdasdasdasdasdasdasdaasdasdasdasdasdasdasdasdasdaasdasdasdasdasdasdasdaasdasdasdasdasdasdasdasdasdaasdasdasdasdasdasdasda'
        response = self.client.post('/materias/agregar/', data=self.data)
        self.assertContains(
            response, 'Asegúrese de que este valor tenga como máximo 60 caracteres (tiene 200).')

    def test_muestra_mensaje_error_nombre_vacio_tempalte(self):
        self.data['nombre'] = ''
        response = self.client.post('/materias/agregar/', data=self.data)
        self.assertContains(response, 'Este campo es obligatorio.')

    def test_muestra_mensaje_error_descripcion_vacio_tempalte(self):
        self.data['descripcion'] = ''
        response = self.client.post('/materias/agregar/', data=self.data)
        self.assertContains(response, 'Este campo es obligatorio.')

    def test_muestra_mensaje_error_nombre_duplicado(self):
        materia_original = Materia(
            nombre='Materia de prueba',
            descripcion='Dddddesssscrrrripppcciiioon.'
        )
        materia_original.full_clean()
        materia_original.save()
        response = self.client.post('/materias/agregar/', data=self.data)
        self.assertContains(
            response, 'Ya existe un/a Materia con este/a Nombre.')

    # Test for edit Materia.

    def test_responde_url_editar_materia(self):
        materia = Materia.objects.first()
        response = self.client.get(f'/materias/editar/{materia.id}')
        self.assertEqual(response.status_code, 200)

    def test_nombre_url_editar_materia(self):
        materia = Materia.objects.first()
        response = self.client.get(
            reverse('materias:editar', kwargs={'pk': materia.id}))
        self.assertEqual(response.status_code, 200)

    def test_obtiene_template_editar_materia(self):
        materia = Materia.objects.first()
        response = self.client.get(f'/materias/editar/{materia.id}')
        self.assertTemplateUsed(response, 'editar_materia.html')

    def test_hay_titulo_del_campo_para_ver_nombre(self):
        materia = Materia.objects.first()
        response = self.client.get(f'/materias/editar/{materia.id}')
        self.assertContains(response, 'Nombre')

    def test_hay_titulo_del_campo_para_editar_descripcion(self):
        materia = Materia.objects.first()
        response = self.client.get(f'/materias/editar/{materia.id}')
        self.assertContains(response, 'Descripcion')

    def test_hay_campo_para_editar_descripcion(self):
        materia = Materia.objects.first()
        response = self.client.get(f'/materias/editar/{materia.id}')
        self.assertContains(response, 'name="descripcion"')

    def test_hay_boton_guardar_edicion_materia(self):
        materia = Materia.objects.first()
        response = self.client.get(f'/materias/editar/{materia.id}')
        self.assertContains(response, '<button id="id_btn_guardar"')

    def test_campo_ver_nombre_esta_desabilitado(self):
        materia = Materia.objects.first()
        response = self.client.get(f'/materias/editar/{materia.id}')
        self.assertContains(
            response, '<input type="text" name="nombre" id="id_nombre_input" disabled')

    def test_edita_materia(self):
        # Create a new Materia to edit him latter.
        materia_a_editar = Materia.objects.first()
        # Set the new data to edit the descripcion field.
        data = {
            'nombre': materia_a_editar.nombre,
            'descripcion': 'Decripcion nueva y editada EDITADA'
        }
        # Send the request to edit Materia.
        self.client.post(f'/materias/editar/{materia_a_editar.id}', data=data)
        self.assertEqual(Materia.objects.get(
            id=materia_a_editar.id).descripcion, data['descripcion'])

    def test_muestra_mensaje_error_descripcion_vacio_template_editar(self):
        materia = Materia.objects.first()
        self.data['descripcion'] = ''
        response = self.client.post(f'/materias/editar/{materia.id}', data=self.data)
        self.assertContains(response, 'Este campo es obligatorio.')

    # Tests for view a list of Materias.add()

    def test_responde_url_lista_materias(self):
        response = self.client.get('/materias/lista/')
        self.assertEqual(response.status_code, 200)

    def test_nombre_url_lista_materias(self):
        response = self.client.get(reverse('materias:lista'))
        self.assertEqual(response.status_code, 200)

    def test_obtiene_template_lista_materias(self):
        response = self.client.get('/materias/lista/')
        self.assertTemplateUsed(response, 'lista_materias.html')

    def test_hay_titulo_de_la_tabla_materias(self):
        response = self.client.get('/materias/lista/')
        self.assertContains(response, '<h1>Lista de materias</h1>')

    def test_muestra_materias_en_lista(self):
        response = self.client.get('/materias/lista/')
        self.assertContains(response, 'Nombre materia default')

    def test_login_necesario_lista_materias(self):
        self.client.logout()
        response = self.client.get('/materias/lista/')
        self.assertEqual(response.status_code, 302)

    # Tests for agregar_docente - Añadir docentes a una materia

    def test_views_agregar_docente_materia_url(self):
        materia = self.crear_materia('Blockchain', 'Una nueva materia')
        response = self.client.get(f'/materias/agregar-docente/{materia.id}')
        self.assertEqual(response.status_code, 200)

    def test_views_agregar_docente_materia_url_nombre(self):
        materia = self.crear_materia('Blockchain', 'Una nueva materia')
        response = self.client.get(
            reverse('materias:agregar_docente', kwargs={'pk': materia.id}))
        self.assertEqual(response.status_code, 200)

    def test_views_agregar_docente_login_requerido(self):
        materia = self.crear_materia('Blockchain', 'Una nueva materia')
        self.client.logout()
        response = self.client.get(
            reverse('materias:agregar_docente', kwargs={'pk': materia.id}))
        self.assertEqual(response.status_code, 302)

    def test_views_agregar_docente_template(self):
        materia = self.crear_materia('Blockchain', 'Una nueva materia')
        response = self.client.get(
            reverse('materias:agregar_docente', kwargs={'pk': materia.id}))
        self.assertTemplateUsed(response, 'agregar_docente.html')

    def test_views_agregar_docente_titulo_pagina_debe_tener_la_materia(self):
        materia = self.crear_materia('Blockchain', 'Una nueva materia')
        response = self.client.get(
            reverse('materias:agregar_docente', kwargs={'pk': materia.id}))
        self.assertContains(response, f'Asignar docente a {materia.nombre}')

    def test_views_agregar_docente_pagina_debe_contener_la_lista_de_docentes(self):
        materia = self.crear_materia('Blockchain', 'Una nueva materia')
        docente = self.crear_docente(
            'profe1', 'Alonso', 'Gonzalez', 'profe1@gmail.com', 'profe1', '12345678')
        materia.docente.add(docente)
        response = self.client.get(
            reverse('materias:agregar_docente', kwargs={'pk': materia.id}))
        self.assertContains(response, 'Docentes que imparten esta materia')

    def test_views_agregar_docente_pagina_no_debe_contener_la_lista_de_docentes(self):
        materia = self.crear_materia('Blockchain', 'Una nueva materia')
        response = self.client.get(
            reverse('materias:agregar_docente', kwargs={'pk': materia.id}))
        self.assertNotContains(response, 'Docentes que imparten esta materia')

    def test_views_agregar_docente_mensaje_de_exito(self):
        materia = self.crear_materia('Blockchain', 'Una nueva materia')
        docente = self.crear_docente(
            'profe1', 'Alonso', 'Gonzalez', 'profe1@gmail.com', 'profe1', '12345678')
        response = self.client.post(
            reverse('materias:agregar_docente', kwargs={
                'pk': materia.id
            }),
            data={
                'id': docente.id,
                'matricula_input': docente.matricula,
            }
        )
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Docente asignado correctamente')

    def test_views_agregar_docente_mensaje_de_error_falta_matricula(self):
        materia = self.crear_materia('Blockchain', 'Una nueva materia')
        docente = self.crear_docente(
            'profe1', 'Alonso', 'Gonzalez', 'profe1@gmail.com', 'profe1', '12345678')
        response = self.client.post(
            reverse('materias:agregar_docente', kwargs={
                'pk': materia.id
            }),
            data={
                'id': docente.id,
            }
        )
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'La matrícula no puede estar vacia')

    def test_views_agregar_docente_mensaje_de_error_falta_id_docente(self):
        materia = self.crear_materia('Blockchain', 'Una nueva materia')
        docente = self.crear_docente(
            'profe1', 'Alonso', 'Gonzalez', 'profe1@gmail.com', 'profe1', '12345678')
        response = self.client.post(
            reverse('materias:agregar_docente', kwargs={
                'pk': materia.id
            }),
            data={
                'matricula_input': docente.matricula,
            }
        )
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         'No se selecionó docente de la lista')

    def test_views_agregar_docente_mensaje_de_error_docente_ya_asignado(self):
        materia = self.crear_materia('Blockchain', 'Una nueva materia')
        docente = self.crear_docente(
            'profe1', 'Alonso', 'Gonzalez', 'profe1@gmail.com', 'profe1', '12345678')
        materia.docente.add(docente)
        response = self.client.post(
            reverse('materias:agregar_docente', kwargs={
                'pk': materia.id
            }),
            data={
                'matricula_input': docente.matricula,
                'id': docente.id,
            }
        )
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), 'EL docente ya tiene asignada la materia')

    def test_views_agregar_docente_mensaje_de_error_docente_no_existe(self):
        materia = self.crear_materia('Blockchain', 'Una nueva materia')
        response = self.client.post(
            reverse('materias:agregar_docente', kwargs={
                'pk': materia.id
            }),
            data={
                'matricula_input': 12345678,
                'id': 10
            }
        )
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'El docente no existe')

    def test_views_materias_buscar_docente_get(self):
        docente = self.crear_docente(
            'profe1', 'Alonso', 'Gonzalez', 'profe1@gmail.com', 'profe1', '12345678')
        response = self.client.get(
            f'/materias/buscar-docente/?docente={docente.id}/')
        self.assertEqual(response.status_code, 200)

    # ********************** Tests helpers **************************

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

    def crear_materia(self, nombre, descripcion):
        materia = Materia.objects.create(
            nombre=nombre, descripcion=descripcion)
        materia.save()
        return materia

    def crear_docente(self, username, first_name, last_name, email, password, matricula):
        return Docente.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            matricula=matricula
        )
