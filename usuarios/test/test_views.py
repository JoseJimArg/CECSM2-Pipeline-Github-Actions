from django.contrib.auth.models import User
from django.test import TestCase
from django.urls.base import reverse
from django.contrib.auth.models import Group
from ciclos.models import CicloEscolar, TipoCiclo
from grupos.models import Grupo, Letra, Semestre
from clases.models import Clase
from calificaciones.models import Periodo

from materias.models import Materia
from ..models import Alumno, Docente, Aspirante
from test.helpers.permissions import Permissions


class TestViews(TestCase):
    # Tests para nuevo docente
    @classmethod
    def setUpTestData(cls):
        Permissions.create_permissions()

    def test_accesso_url_docente_nuevo(self):
        self.login_admin()
        response = self.client.get('/docentes/nuevo/')
        self.assertEqual(response.status_code, 200)

    def test_acceso_alias_docente_nuevo(self):
        self.login_admin()
        response = self.client.get(reverse('usuarios:nuevo_docente'))
        self.assertEqual(response.status_code, 200)

    def test_template_docente_nuevo(self):
        self.login_admin()
        response = self.client.get('/docentes/nuevo/')
        self.assertTemplateUsed(
            response, "docentes/nuevo_docente.html", "base.html")

    def test_titulo_se_encuentra_en_template_docente_nuevo(self):
        self.login_admin()
        response = self.client.get('/docentes/nuevo/')
        self.assertContains(response, "<title>Nuevo Docente</title>")

    def test_campo_username_se_encuentra_en_el_template_docente_nuevo(self):
        self.login_admin()
        response = self.client.get('/docentes/nuevo/')
        formulario = 'id_username'
        self.assertContains(response, formulario)

    def test_campo_nombre_se_encuentra_en_el_template_docente_nuevo(self):
        self.login_admin()
        response = self.client.get('/docentes/nuevo/')
        formulario = 'id_first_name'
        self.assertContains(response, formulario)

    def test_campo_apellidos_se_encuentra_en_el_template_docente_nuevo(self):
        self.login_admin()
        response = self.client.get('/docentes/nuevo/')
        formulario = 'id_last_name'
        self.assertContains(response, formulario)

    def test_campo_correo_se_encuentra_en_el_template_docente_nuevo(self):
        self.login_admin()
        response = self.client.get('/docentes/nuevo/')
        formulario = 'id_email'
        self.assertContains(response, formulario)

    def test_campo_password_se_encuentra_en_el_template_docente_nuevo(self):
        self.login_admin()
        response = self.client.get('/docentes/nuevo/')
        formulario = 'id_password'
        self.assertContains(response, formulario)

    def test_campo_matricula_se_encuentra_en_el_template_docente_nuevo(self):
        self.login_admin()
        response = self.client.get('/docentes/nuevo/')
        formulario = 'id_matricula'
        self.assertContains(response, formulario)

    def test_boton_guardar_se_encuentra_en_el_template_docente_nuevo(self):
        self.login_admin()
        response = self.client.get('/docentes/nuevo/')
        formulario = 'Guardar'
        self.assertContains(response, formulario)

    # Tests para lista docentes

    def test_accesso_url_lista_docentes(self):
        self.login_admin()
        response = self.client.get('/docentes/')
        self.assertEqual(response.status_code, 200)

    def test_acceso_alias_lista_docentes(self):
        self.login_admin()
        response = self.client.get(reverse('usuarios:lista_docentes'))
        self.assertEqual(response.status_code, 200)

    def test_template_lista_docentes(self):
        self.login_admin()
        response = self.client.get('/docentes/')
        self.assertTemplateUsed(
            response, "docentes/lista_docentes.html", "base.html")

    def test_titulo_se_encuentra_en_template_lista_docentes(self):
        self.login_admin()
        response = self.client.get('/docentes/')
        self.assertContains(response, "Lista de docentes")

    def test_url_editar_usuario(self):
        self.login_admin()
        self.agrega_profe()
        usuario = Docente.objects.get(first_name="Ricardo")
        response = self.client.get(f'/docentes/editar/{usuario.id}')
        self.assertEqual(response.status_code, 200)

    def test_editar_profe_y_se_encuentre_en_template_lista_docentes(self):
        self.login_admin()
        profe = self.agrega_profe()
        profe.first_name = 'Armando'
        profe.save()
        response = self.client.get('/docentes/')
        self.assertContains(response, 'Armando')

    # Login docente
    def test_login_docente(self):
        docente = self.agregar_docente()
        login = self.client.login(
            username=docente.username, password="Docente#1")
        self.assertTrue(login)

    # Login admin
    def test_login_admin(self):
        admin = self.agregar_admin()
        login = self.client.login(
            username=admin.username, password="Corverita#1")
        self.assertTrue(login)

    def test_login_alumno(self):
        alumno = self.agregar_alumno()
        login = self.client.login(
            username=alumno.username, password="Alumno#1")
        self.assertFalse(login)

    def test_logout(self):
        admin = self.agregar_admin()
        login = self.client.login(
            username=admin.username, password="Corverita#1")
        logout = self.client.logout()
        self.assertIsNone(logout)

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

    def agrega_profe(self):
        profe = Docente(
            username='profe',
            first_name="Ricardo",
            last_name="Ricardo",
            email='profe@gmail.com',
            password='Corverita#1',
            matricula='35166006',
        )
        profe.save()
        return profe

    def agregar_docente(self):
        username = 'docente'
        first_name = 'Docente'
        last_name = 'Docente'
        email = 'docente@test.com'
        password = 'Docente#1'
        matricula = '35166865'
        user = Docente(username=username, first_name=first_name,
                       last_name=last_name, matricula=matricula, email=email)
        user.set_password(password)
        user.save()
        return user

    def agregar_alumno(self):
        username = 'alumno1'
        first_name = 'alumno1'
        last_name = 'alumno1'
        email = 'alumno1@test.com'
        password = 'Alumno#1'
        matricula = '35166865'
        user = Alumno(username=username, first_name=first_name,
                      last_name=last_name, matricula=matricula, email=email)
        user.set_password(password)
        user.is_active = False
        user.save()
        return user

    # ver docente
    def test_ver_usuario_url_id_1(self):
        self.login_admin()
        docente = self.agregar_docente()
        response = self.client.get(f'/docentes/ver/{docente.id}')
        self.assertEqual(response.status_code, 200)

    def test_ver_datos_profe_Docente(self):
        self.login_admin()
        profe = self.agregar_docente()
        profe = Docente.objects.get(first_name='Docente')

        response = self.client.get(f'/docentes/ver/{profe.id}')
        self.assertEqual(response.status_code, 200)

    # Tests para nuevo alumno

    def test_crear_alumno(self):
        self.login_admin()
        data = {
            "username": 'alumno',
            "first_name": 'alumno',
            "last_name": "alumno",
            "email": "alumno@gmail.com",
            "password": "Corverita#1",
            "matricula": "35166865"
        }
        response = self.client.post('/alumnos/nuevo/', data=data)
        alumno = Alumno.objects.all().first()
        self.assertEqual(alumno.username, data['username'])

    def test_campo_matricula_se_encuentra_en_el_template_alumno_nuevo(self):
        self.login_admin()
        response = self.client.get('/alumnos/nuevo/')
        formulario = 'id_matricula'
        self.assertContains(response, formulario)

    def test_campo_password_se_encuentra_en_el_template_alumno_nuevo(self):
        self.login_admin()
        response = self.client.get('/alumnos/nuevo/')
        formulario = 'id_password'
        self.assertContains(response, formulario)

    def test_campo_correo_se_encuentra_en_el_template_alumno_nuevo(self):
        self.login_admin()
        response = self.client.get('/alumnos/nuevo/')
        formulario = 'id_email'
        self.assertContains(response, formulario)

    def test_campo_apellidos_se_encuentra_en_el_template_alumno_nuevo(self):
        self.login_admin()
        response = self.client.get('/alumnos/nuevo/')
        formulario = 'id_last_name'
        self.assertContains(response, formulario)

    def test_campo_username_Se_encuentra_en_el_template_alumno_nuevo(self):
        self.login_admin()
        response = self.client.get('/alumnos/nuevo/')
        formulario = 'id_username'
        self.assertContains(response, formulario)

    def test_titulo_se_encuentra_en_template_alumno_nuevo(self):
        self.login_admin()
        response = self.client.get('/alumnos/nuevo/')
        self.assertContains(response, '<title>Nuevo Alumno</title>')

    def test_template_alumno_nuevo(self):
        self.login_admin()
        response = self.client.get('/alumnos/nuevo/')
        self.assertTemplateUsed(
            response, "alumnos/nuevo_alumno.html", "base.html")

    def test_acceso_alias_alumno_nuevo(self):
        self.login_admin()
        response = self.client.get(reverse('usuarios:nuevo_alumno'))
        self.assertEqual(response.status_code, 200)

    def test_acceso_url_alumno_nuevo(self):
        self.login_admin()
        response = self.client.get('/alumnos/nuevo/')
        self.assertEqual(response.status_code, 200)

    # Tests para listar alumnos

    def test_acceso_alias_lista_alumnos(self):
        self.login_admin()
        response = self.client.get(reverse('usuarios:lista_alumnos'))
        self.assertEqual(response.status_code, 200)

    def test_acceso_url_lista_alumnos(self):
        self.login_admin()
        response = self.client.get('/alumnos/')
        self.assertEqual(response.status_code, 200)

    def test_utiliza_template_correcto_lista_alumnos(self):
        self.login_admin()
        response = self.client.get(reverse('usuarios:lista_alumnos'))
        self.assertTemplateUsed(
            response, "alumnos/lista_alumnos.html", "base.html")

    def test_titulo_lista_alumnos(self):
        self.login_admin()
        response = self.client.get(reverse('usuarios:lista_alumnos'))
        self.assertContains(response, "<title>Lista de Alumnos</title>")

# Ver clases de un docente en particular
    def agrega_profesor(self):
        profe = Docente(
            id=100,
            username='profe',
            first_name="Ricardo",
            last_name="Ricardo",
            email='profe@gmail.com',
            password='Corverita#1',
            matricula='35166006',
        )
        profe.save()
        return profe

    def agrega_materia(self):
        materia = Materia(
            nombre='Materia de prueba',
            descripcion='Materia usada para hacer test',
        )
        materia.save()
        return materia

    def agrega_tipo_ciclo(self):
        tipo = TipoCiclo(
            nombre='par',
        )
        tipo.save()
        return tipo

    def agrega_ciclo_escolar(self):
        tipo = self.agrega_tipo_ciclo()
        ciclo = CicloEscolar(
            anio_inicio=2021,
            anio_fin=2022,
            tipo_ciclo=tipo,
        )
        ciclo.save()
        return ciclo

    def agrega_semestre(self):
        semestre = Semestre(
            numero=1,
        )
        semestre.save()
        return semestre

    def agrega_letra(self):
        l = Letra(
            letra='A',
        )
        l.save()
        return l

    def agrega_grupo(self):
        sem = self.agrega_semestre()
        let = self.agrega_letra()
        grupo = Grupo(
            semestre=sem,
            letra=let,
        )
        grupo.save()
        return grupo

    def agrega_clase(self):
        mat = self.agrega_materia()
        profe = self.agrega_profesor()
        ciclo_escolar = self.agrega_ciclo_escolar()
        grupo_creado = self.agrega_grupo()
        clase = Clase(
            docente=profe,
            materia=mat,
            ciclo=ciclo_escolar,
            grupo=grupo_creado,
        )
        clase.save()
        return clase

    def crearPeriodo(self, nombre):
        return Periodo.objects.create(
            nombre=nombre
        )

    def test_url_ver_clases_docente_admin(self):
        self.login_admin()
        self.agrega_clase()
        response = self.client.get('/docentes/ver-clases/')
        self.assertContains(response, "Clases")

    def test_aspirante_rechazado_aceptado_icon(self):
        aspirante = self.crearAspirante()
        aspirante.save()
        self.login_admin()
        response = self.client.get('/aspirantes/')
        self.assertContains(response, "status-pending")

        aspirante.status = 1
        aspirante.save()
        response = self.client.get('/aspirantes/')
        self.assertContains(response, "status-success")

        aspirante.status = 2
        aspirante.save()
        response = self.client.get('/aspirantes/')
        self.assertContains(response, "status-error")

    def test_lista_aspirantes_login_required(self):
        response = self.client.get('/aspirantes/')
        self.assertEquals(response.status_code, 302)

    def test_detalle_aspirantes_login_required(self):
        aspirante = self.crearAspirante()
        aspirante.save()
        response = self.client.get(f'/aspirantes/{aspirante.id}/')
        self.assertEquals(response.status_code, 302)
    
    def test_eliminar_aspirante(self):
        aspirante = self.crearAspirante()
        aspirante.save()
        response = self.client.get(reverse('usuarios:eliminar_aspirante', args=[aspirante.id]))
        self.assertEquals(response.status_code, 302)

        self.login_admin()
        self.client.get(reverse(f'usuarios:eliminar_aspirante', args=[aspirante.id]))
        self.assertEquals(Aspirante.objects.all().count(), 0)

    # def test_ver_clases_profesor_existente_con_clases(self):
    #     # docente2 = Docente.objects.create(
    #     #     username='profe',
    #     #     first_name="Jose",
    #     #     last_name="´Jimenez",
    #     #     email='profe@gmail.com',
    #     #     matricula='35166006',
    #     # )
    #     # docente2.save()

    #     # docente2.set_password('Corverita#1')

    #     # docente = Docente.objects.filter(id=docente2.id).first()
    #     self.crearPeriodo("Primer Parcial")
    #     self.crearPeriodo("Segundo Parcial")
    #     self.crearPeriodo("Tercer Parcial")
    #     self.crearPeriodo("Ordinario")
    #     self.crearPeriodo("Extraordinario")
    #     docente=self.agregar_docente()
    #     login=self.client.login(username=docente.username,password="Docente#1")

    #     response = self.client.get('/docentes/ver-clases/')

    #     print(login)
    #     print(response.content)
    #     self.assertContains(response, f'Clases de {docente.first_name} {docente.last_name}')


    # helpers

    def crearAspirante(self):
        return Aspirante(
            username='Ricardo',
            first_name='Ricardo',
            last_name='Ricardo',
            email='ricardo@mail.com',
            password='ricardo',
            num_aspirante='12345678',
            comprobante_pago='/comprobante/comprobante.jpg'
        )