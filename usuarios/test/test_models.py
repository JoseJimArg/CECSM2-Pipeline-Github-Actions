from django.test import TestCase
from ..models import Alumno, Docente, Aspirante
from django.core.exceptions import ValidationError
from django.db import IntegrityError


class TestModels(TestCase):

    def setUp(self, username="Corverita", first_name='Oscar', last_name="Corvera",
              correo='oscar6rock@gmail.com', password='Corverita#1', matricula="35166865"):
        self.docente = Docente(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=correo,
            password=password,
            matricula=matricula
        )
        self.alumno = Alumno(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=correo,
            password=password,
            matricula=matricula
        )

        self.aspirante = Aspirante(
            username='Ricardo',
            first_name='Ricardo',
            last_name='Ricardo',
            email='ricardo@mail.com',
            password='ricardo',
            num_aspirante='12345678',
            comprobante_pago='/comprobante/comprobante.jpg'
        )

    def test_return_object_docente(self):
        self.docente.full_clean()
        self.docente.save()
        self.assertEqual(f'{Docente.objects.first().last_name} {Docente.objects.first().first_name}',
                         self.docente.__str__())

    def test_edita_nombre_profesor(self):
        profe = Docente.objects.create(
            username='Ricardo',
            email='profe@gmail.com',
            password='profe',
            matricula='35166006'
        )
        profe.username = 'Ricardo_nuevo'
        profe.save()
        profesor = Docente.objects.first()
        self.assertEqual(profesor.username, 'Ricardo_nuevo')

    def test_edita_email_profesor(self):
        profe = Docente.objects.create(
            username='Ricardo',
            email='profe@gmail.com',
            password='profe',
            matricula='35166006'
        )
        profe.email = 'profe2@gmail.com'
        profe.save()
        profesor = Docente.objects.first()
        self.assertEqual(profesor.email, 'profe2@gmail.com')

    def test_edita_matricula_profesor(self):
        profe = Docente.objects.create(
            username='Ricardo',
            email='profe@gmail.com',
            password='profe',
            matricula='35166006'
        )
        profe.matricula = '35000000'
        profe.save()
        profesor = Docente.objects.first()
        self.assertEqual(profesor.matricula, '35000000')

    def test_edita_matricula_con_19_caracteres_excediendose(self):
        profe = Docente.objects.create(
            username='Ricardo',
            email='profe@gmail.com',
            password='profe',
            matricula='35166006'
        )
        profe.matricula = '3516600600000000000'
        with self.assertRaisesMessage(ValidationError, 'Asegúrese de que este valor tenga como máximo 8 caracteres (tiene 19).'):
            profe.full_clean()

    def test_return_object_alumno(self):
        self.alumno.full_clean()
        self.alumno.save()
        self.assertEqual(f'{Alumno.objects.first().last_name} {Alumno.objects.first().first_name}',
                         self.alumno.__str__())

    def test_agregar_alumno_no_nombre(self):
        self.alumno.first_name = ""
        self.alumno.save()
        with self.assertRaisesMessage(ValidationError, 'Este campo no puede estar en blanco.'):
            self.alumno.full_clean()

    def test_agregar_alumno_no_apellidos(self):
        self.alumno.last_name = ""
        self.alumno.save()
        with self.assertRaisesMessage(ValidationError, 'Este campo no puede estar en blanco.'):
            self.alumno.full_clean()

    def test_agregar_alumno_no_correo(self):
        self.alumno.email = ""
        self.alumno.save()
        with self.assertRaisesMessage(ValidationError, 'Este campo no puede estar en blanco.'):
            self.alumno.full_clean()

    def test_agregar_alumno_no_matricula(self):
        self.alumno.matricula = ""
        self.alumno.save()
        with self.assertRaisesMessage(ValidationError, 'Este campo no puede estar en blanco.'):
            self.alumno.full_clean()

    def test_registrar_aspirante_correctamente(self):
        Aspirante.objects.create(
            username='Ricardo',
            first_name='Ricardo',
            last_name='Ricardo',
            email='ricardo@mail.com',
            password='ricardo',
            num_aspirante='12345678',
            comprobante_pago='/comprobante/comprobante.jpg'
        )
        self.assertEqual(Aspirante.objects.all().count(), 1)

    def test_registrar_aspirante_no_nombre(self):
        self.aspirante.first_name = ""
        self.aspirante.save()
        with self.assertRaisesMessage(ValidationError, 'Este campo no puede estar en blanco.'):
            self.aspirante.full_clean()

    def test_registrar_aspirante_no_username(self):
        self.aspirante.username = ""
        self.aspirante.save()
        with self.assertRaises(ValidationError):
            self.aspirante.full_clean()

    def test_registrar_aspirante_no_apellidos(self):
        self.aspirante.last_name = ""
        self.aspirante.save()
        with self.assertRaisesMessage(ValidationError, 'Este campo no puede estar en blanco.'):
            self.aspirante.full_clean()
    
    def test_registrar_aspirante_no_num_aspiratne(self):
        self.aspirante.num_aspirante = None
        with self.assertRaises(IntegrityError):
            self.aspirante.save()

    def test_registrar_aspirante_no_comprobante_pago(self):
        self.aspirante.comprobante_pago = None
        self.aspirante.save()
        with self.assertRaises(ValidationError):
            self.aspirante.full_clean()

    def test_estatus_aspirante_no_valido(self):
        self.aspirante.save()
        self.aspirante.status = 3
        with self.assertRaises(ValidationError):
            self.aspirante.full_clean()
        
        self.aspirante.status = -1
        with self.assertRaises(ValidationError):
            self.aspirante.full_clean()

    

