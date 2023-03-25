import mock
from django.test import TestCase
from ..forms import AlumnoForm, DocenteForm, AspiranteForm
from django.contrib.auth.models import User
from django.core.files import File
from ..models import Alumno, Docente


class TestFormUsuario(TestCase):

    def setUp(self, nombre_usuario="corverin2", nombre='Oscar Leonardo', apellidos="Corvera Espinosa", correo='oscar6rock@gmail.com',
              password='Corverita#1', matricula="35166865"):
        self.data = {
            'username': nombre_usuario,
            'first_name': nombre,
            'last_name': apellidos,
            'email': correo,
            'password': password,
            'matricula': matricula
        }

        file_mock = mock.MagicMock(spec=File, name='FileMock')
        file_mock.name = 'comprobajte.jpg'
        self.data_aspirante = {
            'username': nombre_usuario,
            'first_name': nombre,
            'last_name': apellidos,
            'email': correo,
            'password': password,
            'password2': 'Corverita#1',
            'num_aspirante': matricula,
            'comprobante_pago': file_mock,
        }

    # Tests para cuenta de usuario

    def test_docente_form_valido(self):
        form = DocenteForm(self.data)
        self.assertTrue(form.is_valid())

    def test_docente_form_save(self):
        form = DocenteForm(self.data)
        form.full_clean()
        form.save()
        self.assertEqual(Docente.objects.first().first_name,
                         self.data['first_name'])

    def test_docente_form_matricula_no_repetida(self):
        alumno_form = AlumnoForm(self.data)
        alumno_form.full_clean()
        alumno_form.save()
        self.data['username'] = "docente"
        self.data['email'] = "docente@gmail.com"
        self.data['matricula'] = "35166869"
        docente_form = DocenteForm(self.data)
        docente_form.full_clean()
        self.assertTrue(docente_form.is_valid())

    def test_docente_form_matricula_repetida(self):
        alumno_form = AlumnoForm(self.data)
        alumno_form.full_clean()
        alumno_form.save()
        self.data['username'] = "docente"
        self.data['email'] = "docente@gmail.com"
        docente_form = DocenteForm(self.data)
        docente_form.full_clean()
        self.assertFalse(docente_form.is_valid())

    def test_docente_form_mensaje_matricula_repetida(self):
        alumno_form = AlumnoForm(self.data)
        alumno_form.full_clean()
        alumno_form.save()

        self.data['username'] = "docente"
        self.data['email'] = "docente@gmail.com"
        docente_form = DocenteForm(self.data)
        docente_form.full_clean()
        self.assertEqual(docente_form.errors['matricula'], [
                         'La matrícula ya está en uso por un alumno'])

    def test_docente_form_nombre_invalido(self):
        self.data['first_name'] = ''
        form = DocenteForm(self.data)
        self.assertFalse(form.is_valid())

    def test_docente_form_nombre_vacio_mensaje(self):
        self.data['first_name'] = ''
        form = DocenteForm(self.data)
        self.assertEqual(form.errors['first_name'], [
                         'Este campo es obligatorio.'])

    def test_docente_form_apellido_invalido(self):
        self.data['last_name'] = ''
        form = DocenteForm(self.data)
        self.assertFalse(form.is_valid())

    def test_docente_form_apellido_vacio_mensaje(self):
        self.data['last_name'] = ''
        form = DocenteForm(self.data)
        self.assertEqual(form.errors['last_name'], [
                         'Este campo es obligatorio.'])

    def test_docente_form_matricula_invalido(self):
        self.data['matricula'] = "3516686"
        form = DocenteForm(self.data)
        self.assertFalse(form.is_valid())

    def test_docente_form_matricula_invalido(self):
        self.data['matricula'] = "3516686"
        form = DocenteForm(self.data)
        self.assertEqual(form.errors['matricula'], [
                         'El tamaño mínimo debe ser de 8'])

    def test_docente_form_password_sin_digitos(self):
        self.data['password'] = "Corverita#"
        form = DocenteForm(self.data)
        self.assertFalse(form.is_valid())

    def test_docente_form_password_sin_digitos_mensaje(self):
        self.data['password'] = "Corverita#"
        form = DocenteForm(self.data)
        self.assertEqual(form.errors['password'], [
                         'La contraseña debe tener mínimamente un número, 0-9.'])

    def test_docente_form_password_sin_simbolos(self):
        self.data['password'] = "Corverita1"
        form = DocenteForm(self.data)
        self.assertFalse(form.is_valid())

    def test_docente_form_password_sin_simbolos_mensaje(self):
        self.data['password'] = "Corverita1"
        form = DocenteForm(self.data)
        self.assertEqual(form.errors['password'], [
                         'La contraseña debe contener un carácter especial: ()[]{}|\\`~!@#$%^&*_-+=;:\'",<>./?'])

    def test_docente_form_password_sin_mayusculas(self):
        self.data['password'] = "corverita#1"
        form = DocenteForm(self.data)
        self.assertFalse(form.is_valid())

    def test_docente_form_password_sin_mayusculas_mensaje(self):
        self.data['password'] = "corverita#1"
        form = DocenteForm(self.data)
        self.assertEqual(form.errors['password'], [
                         'La contraseña debe contener al menos una mayúscula, A-Z.'])

    def test_docente_form_password_sin_minusculas(self):
        self.data['password'] = "CORVERITA#1"
        form = DocenteForm(self.data)
        self.assertFalse(form.is_valid())

    def test_docente_form_password_sin_minusculas_mensaje(self):
        self.data['password'] = "CORVERITA#1"
        form = DocenteForm(self.data)
        self.assertEqual(form.errors['password'], [
                         'La contraseña debe contener al menos 1 minúscula, a-z.'])

    def test_docente_form_password_min_8(self):
        self.data['password'] = "Corv3#"
        form = DocenteForm(self.data)
        self.assertFalse(form.is_valid())

    def test_docente_form_password_min_8_mensaje(self):
        self.data['password'] = "Corv3#"
        form = DocenteForm(self.data)
        self.assertEqual(form.errors['password'], [
                         'La contraseña es muy corta. Debe contener al menos 8 caracteres.'])

    def test_formulario_DocenteForm_funciona(self):
        form = DocenteForm(
            data={
                'username': 'Ricardo2',
                'first_name': 'Ricardo',
                'last_name': 'Ricardo',
                'email': 'profesor@gmail.com',
                'password': 'Profesor#1',
                'matricula': '35166007',
            }
        )
        self.assertTrue(form.is_valid())

    def test_nombre_profesor_vacio(self):
        form = DocenteForm(
            data={
                'username': '',
                'email': 'profesor@gmail.com',
                'password': 'profe',
                'matricula': '35166006',
            }
        )
        self.assertFalse(form.is_valid())

    def test_profesor_sin_nombre(self):
        form = DocenteForm(
            data={
                'email': 'profesor@gmail.com',
                'password': 'profe',
                'matricula': '35166006',
            }
        )
        self.assertFalse(form.is_valid())

    def test_profesor_con_password_vacia(self):
        form = DocenteForm(
            data={
                'username': 'Ricardo',
                'email': 'profe@gmail.com',
                'password': '',
                'matricula': '35166006',
            }
        )
        self.assertFalse(form.is_valid())

    def test_profesor_sin_password(self):
        form = DocenteForm(
            data={
                'username': 'Ricardo',
                'email': 'profe@gmail.com',
                'matricula': '35166006',
            }
        )
        self.assertFalse(form.is_valid())

    def test_alumno_form_valido(self):
        form = AlumnoForm(self.data)
        self.assertTrue(form.is_valid())

    def test_alumno_form_save(self):
        form = AlumnoForm(self.data)
        form.full_clean()
        form.save()
        self.assertEqual(Alumno.objects.first().first_name,
                         self.data['first_name'])

    def test_alumno_form_matricula_no_repetida(self):
        docente_form = DocenteForm(self.data)
        docente_form.full_clean()
        docente_form.save()
        self.data['username'] = "alumno"
        self.data['email'] = "alumno@gmail.com"
        self.data['matricula'] = "35166869"
        alumno_form = AlumnoForm(self.data)
        self.assertTrue(alumno_form.is_valid())

    def test_alumno_form_matricula_repetida(self):
        docente_form = DocenteForm(self.data)
        docente_form.full_clean()
        docente_form.save()
        self.data['username'] = "alumno"
        self.data['email'] = "alumno@gmail.com"
        alumno_form = AlumnoForm(self.data)
        self.assertFalse(alumno_form.is_valid())

    def test_alumno_form_mensaje_matricula_repetida(self):
        docente_form = DocenteForm(self.data)
        docente_form.full_clean()
        docente_form.save()
        self.data['username'] = "alumno"
        self.data['email'] = "alumno@gmail.com"
        alumno_form = AlumnoForm(self.data)
        alumno_form.full_clean()
        self.assertEqual(alumno_form.errors['matricula'], [
                         'La matrícula ya está en uso por un docente'])

    def test_alumno_form_nombre_invalido(self):
        self.data['first_name'] = ''
        form = AlumnoForm(self.data)
        self.assertFalse(form.is_valid())

    def test_alumno_form_nombre_vacio_mensaje(self):
        self.data['first_name'] = ''
        form = AlumnoForm(self.data)
        self.assertEqual(form.errors['first_name'], [
                         'Este campo es obligatorio.'])

    def test_alumno_form_apellido_invalido(self):
        self.data['last_name'] = ''
        form = AlumnoForm(self.data)
        self.assertFalse(form.is_valid())

    def test_alumno_form_apellido_vacio_mensaje(self):
        self.data['last_name'] = ''
        form = AlumnoForm(self.data)
        self.assertEqual(form.errors['last_name'], [
                         'Este campo es obligatorio.'])

    def test_alumno_form_matricula_invalido(self):
        self.data['matricula'] = "3516686"
        form = AlumnoForm(self.data)
        self.assertFalse(form.is_valid())

    def test_alumno_form_matricula_invalido(self):
        self.data['matricula'] = "3516686"
        form = AlumnoForm(self.data)
        self.assertEqual(form.errors['matricula'], [
                         'El tamaño mínimo debe ser de 8'])

    def test_alumno_form_password_sin_digitos(self):
        self.data['password'] = "Corverita#"
        form = AlumnoForm(self.data)
        self.assertFalse(form.is_valid())

    def test_alumno_form_password_sin_digitos_mensaje(self):
        self.data['password'] = "Corverita#"
        form = AlumnoForm(self.data)
        self.assertEqual(form.errors['password'], [
                         'La contraseña debe tener mínimamente un número, 0-9.'])

    def test_alumno_form_password_sin_simbolos(self):
        self.data['password'] = "Corverita1"
        form = AlumnoForm(self.data)
        self.assertFalse(form.is_valid())

    def test_alumno_form_password_sin_simbolos_mensaje(self):
        self.data['password'] = "Corverita1"
        form = AlumnoForm(self.data)
        self.assertEqual(form.errors['password'], [
                         'La contraseña debe contener un carácter especial: ()[]{}|\\`~!@#$%^&*_-+=;:\'",<>./?'])

    def test_alumno_form_password_sin_mayusculas(self):
        self.data['password'] = "corverita#1"
        form = AlumnoForm(self.data)
        self.assertFalse(form.is_valid())

    def test_alumno_form_password_sin_mayusculas_mensaje(self):
        self.data['password'] = "corverita#1"
        form = AlumnoForm(self.data)
        self.assertEqual(form.errors['password'], [
                         'La contraseña debe contener al menos una mayúscula, A-Z.'])

    def test_alumno_form_password_sin_minusculas(self):
        self.data['password'] = "CORVERITA#1"
        form = AlumnoForm(self.data)
        self.assertFalse(form.is_valid())

    def test_alumno_form_password_sin_minusculas_mensaje(self):
        self.data['password'] = "CORVERITA#1"
        form = AlumnoForm(self.data)
        self.assertEqual(form.errors['password'], [
                         'La contraseña debe contener al menos 1 minúscula, a-z.'])

    def test_alumno_form_password_min_8(self):
        self.data['password'] = "Corv3#"
        form = AlumnoForm(self.data)
        self.assertFalse(form.is_valid())

    def test_alumno_form_password_min_8_mensaje(self):
        self.data['password'] = "Corv3#"
        form = AlumnoForm(self.data)
        self.assertEqual(form.errors['password'], [
                         'La contraseña es muy corta. Debe contener al menos 8 caracteres.'])

    def test_aspirante_form_paswords_no_coinciden(self):
        self.data_aspirante['password2'] = "Corverita1"
        form = AspiranteForm(self.data_aspirante)
        self.assertEqual(form.errors['password'], ['Las contraseñas no coinciden'])
    