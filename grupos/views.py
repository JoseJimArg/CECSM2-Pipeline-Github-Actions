from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib import messages

from ciclos.models import CicloEscolar
from clases.models import Clase
from .models import Grupo, Semestre, Letra
from .forms import GrupoForm
from usuarios.views import validar_aspirante_no_inscrito
from usuarios.models import Aspirante


@login_required
def nuevo_grupo(request):
    form = GrupoForm()

    if request.method == 'POST':
        form = GrupoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grupo agregado correctamente')
            return redirect('grupos:lista_grupos')
        else:
            messages.error(request, 'No se pudo crear el grupo')
            return render(request, 'nuevo_grupo.html', {'form': form})
    else:
        context = {
            'form': form,
            'titulo': 'Nuevo Grupo'
        }
        return render(request, 'nuevo_grupo.html', context)


@login_required
def lista_grupos(request):
    grupos = Grupo.objects.all()
    return render(request, 'lista_grupos.html', {'grupos': grupos})


@login_required
def editar_grupo(request, id_grupo):
    # Se obtiene el grupo y se crea el form a partir de la instacia
    grupo = Grupo.objects.get(id=id_grupo)
    form = GrupoForm(instance=grupo)

    # Si es por POST
    if request.method == 'POST':
        # Se crea el from a partir de los datos enviados
        form = GrupoForm(request.POST, instance=grupo)

        # Si los datos son validos
        if form.is_valid():
            form.save()
            messages.success(request, 'Grupo editado correctamente')
            return redirect('grupos:lista_grupos')

        # Si los datos no son validos se manda un mensaje
        messages.error(request, 'No fue posible editar el grupo')

    # Si los datos no son validos o es una consulta GET se vuelve a renderizar el form
    context = {
        'form': form,
        'titulo': 'Editar Grupo'
    }
    return render(request, 'nuevo_grupo.html', context)

@login_required
def lista_grupos_semestre_cero(request):
    semestre_cero = get_object_or_404( Semestre, numero = 0 )
    ciclo = get_object_or_404( CicloEscolar, activo = True )
    clases_semestre_cero_ciclo_activo = Clase.objects.filter( ciclo = ciclo.id, grupo__semestre = semestre_cero.id )

    # Si hay clases en semestre 0 en el ciclo activo
    if clases_semestre_cero_ciclo_activo.first():
        grupos_semestre_cero = Grupo.objects.filter( semestre = semestre_cero.id )

        # Filtrar los grupos de semestre 0 que tengan clases asignada
        # Si no tiene clase asignada no se mostrará en la lista de grupos de semestre 0
        lista_grupos=[]
        for grupo in grupos_semestre_cero:
            grupo_con_clase = clases_semestre_cero_ciclo_activo.filter(grupo=grupo)
            if grupo_con_clase.exists():
                lista_grupos.append(grupo)
        
        # Obtener los cupos de los grupos en base a la primer clase que tiene asignada
        cupos_totales = []
        cupos_restantes = []
        for grupo in lista_grupos:
            primera_clase = Clase.objects.filter( grupo = grupo.id , ciclo = ciclo.id ).first()
            cupos_totales.append(primera_clase.cupo_total)
            cupos_restantes.append(primera_clase.cupo_restante)
        
        # Mandar los grupos y sus cupos en una sola lista para iterarlas juntas
        lista = zip(lista_grupos, cupos_totales, cupos_restantes)
    else:
        # No hay clases en el ciclo activo ni en semestre 0, por lo tanto no hay grupos de semestre 0
        lista = []

    # Verificar si el aspirante logeado ya está inscrito a algun grupo
    aspirante = get_object_or_404( Aspirante, id=request.user.id )
    grupo_inscrito = validar_aspirante_no_inscrito(aspirante, ciclo)

    context = {
        'grupos' : lista, 
        'ciclo' : ciclo,
        'grupo_inscrito' : grupo_inscrito,
    }

    return render(request, 'lista_grupos_semestre_cero.html', context)

@login_required
def lista_alumnos_grupo_semestre_cero(request, id_grupo):
    ciclo = get_object_or_404( CicloEscolar, activo = True )
    grupo = get_object_or_404( Grupo, id = id_grupo)

    clase = Clase.objects.filter( ciclo = ciclo.id, grupo = grupo.id ).first()
    aspirantes = clase.aspirantes.all().order_by('last_name')

    context = {
        'grupo' : grupo,
        'aspirantes' : aspirantes,
    }

    return render(request, 'lista_aspirantes_grupo_semestre_cero.html', context)

@login_required
def lista_clases_grupo_semestre_cero(request, id_grupo):
    ciclo = get_object_or_404( CicloEscolar, activo = True )
    grupo = get_object_or_404( Grupo, id = id_grupo)

    clases = Clase.objects.filter( ciclo = ciclo.id, grupo = grupo.id )

    context = {
        'grupo' : grupo,
        'clases' : clases,
    }

    return render(request, 'lista_clases_grupo_semestre_cero.html', context)