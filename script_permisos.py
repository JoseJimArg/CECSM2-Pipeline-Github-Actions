import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CECSM2.settings')
django.setup()

from django.contrib.auth.models import Permission, Group, User
from django.contrib.contenttypes.models import ContentType

from usuarios.models import Docente, Aspirante, Alumno

Administrador_Grupo = Group.objects.create(name='Administrador_Grupo')
Aspirante_Grupo = Group.objects.create(name='Aspirante_Grupo')
Docente_Grupo = Group.objects.create(name='Docente_Grupo')
Alumno_Grupo = Group.objects.create(name='Alumno_Grupo')


content_type_aspirante = ContentType.objects.get_for_model(Aspirante)
content_type_administrador = ContentType.objects.get_for_model(User)
content_type_alumno = ContentType.objects.get_for_model(Alumno)
content_type_docente = ContentType.objects.get_for_model(Docente)



aspirante_permiso = Permission.objects.create(
    codename = 'aspirante_permiso',
    name = 'Permiso requerido para aspirantes',
    content_type = content_type_aspirante
)
administrador_permiso = Permission.objects.create(
    codename = 'administrador_permiso',
    name = 'Permiso requerido para administradores',
    content_type = content_type_administrador
)
docente_permiso = Permission.objects.create(
    codename = 'docente_permiso',
    name = 'Permiso requerido para docentes',
    content_type = content_type_docente
)
alumno_permiso = Permission.objects.create(
    codename = 'alumno_permiso',
    name = 'Permiso requerido para alumnos',
    content_type = content_type_alumno
)


Administrador_Grupo.permissions.add(administrador_permiso)
Administrador_Grupo.permissions.add(alumno_permiso)

Docente_Grupo.permissions.add(docente_permiso)

Alumno_Grupo.permissions.add(alumno_permiso)

Aspirante_Grupo.permissions.add(aspirante_permiso)
