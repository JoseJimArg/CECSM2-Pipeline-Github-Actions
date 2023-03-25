from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.models import Group
from ciclos.models import TipoCiclo, CicloEscolar
from test.helpers.permissions import Permissions


class TestViewsCiclos(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        Permissions.create_permissions()
    
    def setUp(self):
        admin = User.objects.create_user(
            username='gerardo', password='gera.123')
        admin_grupo=Group.objects.get(name="Administrador_Grupo")
        admin.groups.add(admin_grupo)
        self.user_login()

    def test_views_ciclo_escolar_url_nuevo_ciclo_escolar(self):
        response = self.client.get('/ciclos/nuevo')
        self.assertEqual(response.status_code, 200)

    def test_views_ciclo_escolar_login_requerido(self):
        self.client.logout()
        response = self.client.get('/ciclos/nuevo')
        self.assertEqual(response.status_code, 302)

    def test_views_ciclo_escolar_nombre_url(self):
        response = self.client.get(reverse('ciclos:nuevo_ciclo'))
        self.assertEqual(response.status_code, 200)

    def test_views_ciclo_escolar_titulo_pagina(self):
        response = self.client.get(reverse('ciclos:nuevo_ciclo'))
        self.assertContains(response, 'Nuevo ciclo escolar')

    def test_views_ciclo_escolar_template_usado(self):
        response = self.client.get(reverse('ciclos:nuevo_ciclo'))
        self.assertTemplateUsed(response, 'nuevo_ciclo.html')

    def test_views_ciclo_escolar_label_anio_inicio(self):
        response = self.client.get(reverse('ciclos:nuevo_ciclo'))
        self.assertContains(response, 'Año de inicio:')

    def test_views_ciclo_escolar_label_anio_fin(self):
        response = self.client.get(reverse('ciclos:nuevo_ciclo'))
        self.assertContains(response, 'Año de término:')

    def test_views_ciclo_escolar_label_tipo_ciclo(self):
        response = self.client.get(reverse('ciclos:nuevo_ciclo'))
        self.assertContains(response, 'Tipo:')

    def test_views_ciclo_escolar_se_puede_crear_ciclo_escolar(self):
        tipo = TipoCiclo.objects.create(nombre='par')
        self.client.post(
            reverse('ciclos:nuevo_ciclo'),
            data={'anio_inicio': 2021, 'anio_fin': 2022, 'tipo_ciclo': tipo.id})
        self.assertEqual(CicloEscolar.objects.all().count(), 1)

    # *****************   Test Lista Ciclos  *****************

    def test_views_lista_ciclo_debe_estar_en_mismo_template_de_nuevo_ciclo(self):
        self.user_login()
        self.crear_ciclo(2021, 2022, 'par')
        response = self.client.get(reverse('ciclos:nuevo_ciclo'))
        self.assertContains(response, 'Lista de ciclos')

    def test_views_lista_ciclo_no_mostrar_lista_si_no_hay_ciclos(self):
        self.user_login()
        response = self.client.get(reverse('ciclos:nuevo_ciclo'))
        self.assertNotContains(response, 'Lista de ciclos')

    def test_views_lista_ciclo_se_muestra_nombre_del_ciclo(self):
        self.user_login()
        self.crear_ciclo(2021, 2022, 'par')
        response = self.client.get(reverse('ciclos:nuevo_ciclo'))
        self.assertContains(response, '2021-2022par')

    # *****************   Test Helpers  *****************

    def user_login(self):
        self.client.login(username='gerardo', password='gera.123')

    def crear_ciclo(self, anio_inico, anio_fin, tipo):
        tipo = TipoCiclo.objects.create(nombre=tipo)
        CicloEscolar.objects.create(
            anio_inicio=anio_inico, anio_fin=anio_fin, tipo_ciclo=tipo)
