from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from ciclos.models import CicloEscolar

from clases.models import Clase
from clases.forms import FormClase
from materias.models import Materia
from usuarios.models import Alumno, Docente
from grupos.models import Grupo
# Create your views here.


@login_required
def nueva_clase(request):
    if request.method == "POST":
        form = FormClase(request.POST)
        form.instance.cupo_restante = request.POST['cupo_total']

        if form.is_valid():
            docente = get_object_or_404(Docente, id=request.POST['docente'])
            materia = get_object_or_404(Materia, id=request.POST['materia'])

            # Validation for teacher teach te course selected.
            try:
                Materia.objects.get(
                    id=materia.id, docente=docente.id)
            except:
                messages.error(
                    request, f"La materia {materia} no es impartida por {docente}.")
                context = {
                    "form": form
                }
                return render(request, "nueva_clase.html", context)

            # Validation for cupo in clase for semestre cero
            if validar_cupo(request):
                form.save()
                messages.success(request, "Clase agregada correctamente")
                
                # Set the new form to the render
                form = FormClase()
                context = {
                    'form': form
                }
                return render(request, 'nueva_clase.html', context)
            else:
                ciclo = get_object_or_404( CicloEscolar , id = request.POST['ciclo'] )
                primera_clase = Clase.objects.filter( grupo = request.POST['grupo'] , ciclo = ciclo.id ).first()
                messages.error(request, f"La clase no tiene el mismo cupo que las clases de semestre 0 ya asignadas al grupo ({primera_clase.cupo_total})")
                context = {
                    "form": form
                }
                return render(request, "nueva_clase.html", context)

        else:
            context = {
                "form": form
            }
            return render(request, "nueva_clase.html", context)

    form = FormClase()
    context = {
        'form': form
    }
    return render(request, "nueva_clase.html", context)

@login_required
def eliminar_clase(request, pk):
    clase = get_object_or_404(Clase, pk=pk)
    if clase.delete():
        messages.success(request, 'Clase eliminada correctamente')
    else:
        messages.error(request, 'No se pudo eliminar la clase')
    return redirect('clases:lista_clases')

@login_required
def lista_clases(request):
    clases = Clase.objects.order_by("-ciclo__anio_inicio")
    context = {}
    if any(clases):
        context = {
            "clases": clases
        }
    return render(request, "lista_clases.html", context)


@login_required
def buscar_clase(request):
    nombre_clase = request.GET.get("clase")
    clases = []
    if nombre_clase:
        clases_encontradas = Clase.objects.filter(
            materia__nombre__icontains=nombre_clase).values("id", "materia", "docente", "ciclo")
        for clase in clases_encontradas:
            materia_encontrada = Materia.objects.get(id=clase['materia'])
            docente = Docente.objects.get(id=clase['docente'])
            ciclo = CicloEscolar.objects.get(id=clase['ciclo'])
            clase['materia'] = materia_encontrada.nombre
            clase['docente'] = f"{docente.last_name} {docente.first_name}"
            clase['ciclo'] = str(ciclo)
            clases.append(clase)
    return JsonResponse({"status": 200, "data": clases})


def recuperar_clases_asignadas(alumno):
    clases_lleva_alumno = Clase.objects.filter(
        alumno=alumno)
    return clases_lleva_alumno


@login_required
def asignar_clase(request, pk):
    try:
        alumno = Alumno.objects.get(id=pk)
    except:
        messages.error(request, "El alumno ingresado no existe.")
        return redirect('/alumnos/')
    if request.method == "POST":
        clase = request.POST.get('id_clase')
        if clase:
            clase = Clase.objects.get(id=clase)
            if Clase.objects.filter(
                materia=clase.materia,
                ciclo=clase.ciclo,
                alumno=alumno
            ).exists():
                messages.error(
                    request, "Este alumno ya está inscrito a esta materia")
            else:
                if validar_cupo_restante(clase):
                    clase.alumno.add(alumno)
                    clase.cupo_restante -= 1
                    clase.save()
                    messages.success(
                        request, f"Se registró la materia {clase} al alumno {alumno.first_name}")
                else:
                    messages.error(
                        request, f"No quedan cupos disponibles")
        else:
            messages.error(request, "No se seleccionó una clase de la lista.")
    clases_lleva_alumno = recuperar_clases_asignadas(alumno)
    context = {
        "alumno": alumno,
        "clases_lleva": clases_lleva_alumno
    }
    return render(request, "asignar_clase.html", context)

@login_required
def desasignar_clase(request, alumno, clase):
    clase = get_object_or_404(Clase, id=clase)
    alumno = get_object_or_404(Alumno, id=alumno)
    clase.cupo_restante += 1
    clase.alumno.remove(alumno)
    clase.save()
    messages.success(request, f"Se desasignó la materia {clase} al alumno {alumno.first_name}")
    return redirect('clases:agregar_clase_alumno', pk=alumno.id)

@login_required
def lista_alumnos_de_clase(request, pk):
    clase = get_object_or_404(Clase, pk=pk)
    if clase.grupo.semestre.numero == 0:
        alumnos = clase.aspirantes.all()
    else:
        alumnos = clase.alumno.all()

    context = {
        "clase": clase,
        "alumnos": alumnos
    }
    return render(request, "lista_alumnos_de_clase.html", context)


# HELPERS
def validar_cupo(request):
    grupo = get_object_or_404( Grupo, id = request.POST['grupo'] )
    ciclo = get_object_or_404( CicloEscolar, id = request.POST['ciclo'] )

    if (grupo.semestre.numero == 0):
        primera_clase = Clase.objects.filter( grupo = grupo.id , ciclo = ciclo.id).first()
        if primera_clase:
            if int(primera_clase.cupo_total) != int(request.POST['cupo_total']):
                return False
    return True

def validar_cupo_restante(clase):
    if clase.cupo_restante > 0:
        return True
    return False