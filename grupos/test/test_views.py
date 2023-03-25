from django.http import response
from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.urls import reverse
from test.helpers.permissions import Permissions
from ..models import Semestre, Letra, Grupo


class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        Permissions.create_permissions()

    def setUp(self):
        self.create_user()
        self.user_login()

    def test_url_nuevo_grupo(self):
        response = self.client.get('/grupos/nuevo')
        self.assertEqual(response.status_code, 200)

    def test_login_requerido(self):
        self.client.logout()
        response = self.client.get('/grupos/nuevo')
        self.assertEqual(response.status_code, 302)

    def test_nombre_url_nuevo_grupo(self):
        response = self.client.get(reverse('grupos:nuevo_grupo'))
        self.assertEqual(response.status_code, 200)

    def test_nombre_template_nuevo_grupo(self):
        response = self.client.get(reverse('grupos:nuevo_grupo'))
        self.assertTemplateUsed(response, 'nuevo_grupo.html')

    def test_tener_label_semestre(self):
        response = self.client.get(reverse('grupos:nuevo_grupo'))
        self.assertContains(response, 'Semestre')

    def test_tener_label_letra(self):
        response = self.client.get(reverse('grupos:nuevo_grupo'))
        self.assertContains(response, 'Letra')

    def test_tener_boton_guardar(self):
        response = self.client.get(reverse('grupos:nuevo_grupo'))
        self.assertContains(response, 'Guardar')

    def test_crear_nuevo_grupo_correcto(self):
        semestre = self.crear_semestre("1")
        letra = self.crear_letra("C")
        self.client.post(
            reverse('grupos:nuevo_grupo'), data={'semestre': semestre.id, 'letra': letra.id})
        self.assertEqual(Grupo.objects.all().count(), 1)

    def test_no_permitir_crear_grupos_de_opciones_no_existentes(self):
        letra = self.crear_letra("B")
        self.client.post(
            reverse('grupos:nuevo_grupo'), data={'semestre': 'B', 'letra': letra.id})
        self.assertEqual(Grupo.objects.all().count(), 0)
        
        
    # *****************   Test views lista grupos  *****************
    
    def test_existe_url_lista_grupos(self):
        response = self.client.get('/grupos/')
        self.assertEqual(response.status_code, 200)
        
    def test_url_lista_grupos_es_lista_grupos(self):
        response = self.client.get(reverse('grupos:lista_grupos'))
        self.assertEqual(response.status_code, 200)
        
    def test_template_nombre_es_lista_grupos_html(self):
        response = self.client.get(reverse('grupos:lista_grupos'))
        self.assertTemplateUsed(response, 'lista_grupos.html')
    
    def test_logueado_obligatirio_para_accesar(self):
        self.client.logout()
        response = self.client.get(reverse('grupos:lista_grupos'))
        self.assertEqual(response.status_code, 302)
        
    def test_titulo_de_la_pagina_lista_de_grupos(self):
        response = self.client.get(reverse('grupos:lista_grupos'))
        self.assertContains(response, '<title>Lista de Grupos</title>')
        
    def test_se_encuentra_un_grupo_en_lista_grupos(self):
        semestre = self.crear_semestre("1")
        letra = self.crear_letra("B")
        grupo = self.crear_grupo(semestre, letra)
        response = self.client.get(reverse('grupos:lista_grupos'))
        self.assertContains(response, grupo), f"Se esperaba {grupo}, se encontró {response}"
        
    def test_mensaje_no_hay_grupos_agregados_cuando_no_hay_grupos(self):
        response = self.client.get(reverse('grupos:lista_grupos'))
        self.assertContains(response, 'No hay grupos agregados')
        
    # *****************   Test views editar grupo  *****************
    
    def test_existe_url_editar_grupo(self):
        grupo = self.crear_grupo(self.crear_semestre("1"), self.crear_letra("A"))
        response = self.client.get(f'/grupos/editar/{grupo.id}')
        self.assertEqual(response.status_code, 200)
        
    def test_nombre_url_editar_grupo(self):
        grupo = self.crear_grupo(self.crear_semestre("1"), self.crear_letra("A"))
        response = self.client.get(reverse(f'grupos:editar_grupo', args=[grupo.id]))
        self.assertEqual(response.status_code, 200)
    
    def test_editar_grupo_mismo_template_nuevo_grupo(self):
        grupo = self.crear_grupo(self.crear_semestre("1"), self.crear_letra("A"))
        response = self.client.get(reverse(f'grupos:editar_grupo', args=[grupo.id]))
        self.assertTemplateUsed(response, 'nuevo_grupo.html')
        
    def test_editar_grupo_login_requerido(self):
        self.client.logout()
        grupo = self.crear_grupo(self.crear_semestre("1"), self.crear_letra("A"))
        response = self.client.get(reverse(f'grupos:editar_grupo', args=[grupo.id]))
        self.assertEqual(response.status_code, 302)
        
    def test_editar_grupo_titulo_editar_grupo(self):
        grupo = self.crear_grupo(self.crear_semestre("1"), self.crear_letra("A"))
        response = self.client.get(reverse(f'grupos:editar_grupo', args=[grupo.id]))
        self.assertContains(response, '<title>Editar Grupo</title>')
        
    def test_editar_grupo_edicion_exitosa(self):
        grupo = self.crear_grupo(self.crear_semestre("1"), self.crear_letra("A"))
        semestre = self.crear_semestre("2")
        letra = self.crear_letra("B")
        self.client.post(
            reverse(f'grupos:editar_grupo', args=[grupo.id]),
            data = {
                'semestre': semestre.id,
                'letra': letra.id
            }    
        )
        grupo = Grupo.objects.first()
        self.assertEqual(f'{grupo.semestre} {grupo.letra}', f'{semestre} {letra}')
        

    # *****************   Test Helpers  *****************

    def create_user(self):
        admin = User.objects.create_user(
            username='gerardo', password='gera.123')
        admin_grupo=Group.objects.get(name="Administrador_Grupo")
        admin.groups.add(admin_grupo)
        return admin

    def user_login(self):
        self.client.login(username='gerardo', password='gera.123')

    def crear_semestre(self, semestre=None):
        semestre = Semestre.objects.create(numero=semestre)
        return semestre

    def crear_letra(self, letra=None):
        letra = Letra.objects.create(letra=letra)
        return letra
    
    def crear_grupo(self, semestre = None, letra = None):
        grupo = Grupo.objects.create(semestre=semestre, letra=letra)
        return grupo
        
