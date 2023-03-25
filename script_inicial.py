import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CECSM2.settings')
django.setup()

from ciclos.models import TipoCiclo
from grupos.models import Letra, Semestre
from calificaciones.models import Periodo
from materias.models import TipoMateria

semestres = ['0','1','2','3','4','5','6','7','8','9','10']
letras = ['A','B','C','D','E','F']
tipos_ciclos = ['par', 'non']
periodos = ['Primer Parcial', 'Segundo Parcial', 'Tercer Parcial', 'Ordinario', 'Extraordinario']
tipos_materias = ['Curricular', 'Optativa', 'PACDI']

for semestre in semestres:
    if not Semestre.objects.filter(numero=semestre).first():
        Semestre.objects.create(numero=semestre)

for letra in letras:
    if not Letra.objects.filter(letra=letra).first():
        Letra.objects.create(letra=letra)
        
for tipo in tipos_ciclos:
    if not TipoCiclo.objects.filter(nombre=tipo).first():
        TipoCiclo.objects.create(nombre=tipo)

for perodo in periodos:
    if not Periodo.objects.filter(nombre=perodo).first():
        Periodo.objects.create(nombre=perodo)

for tipo in tipos_materias:
    if not TipoMateria.objects.filter(tipo=tipo).first():
        TipoMateria.objects.create(tipo=tipo)
