from django.shortcuts import redirect, render, get_object_or_404
from .forms import FormMateria, FormMateriaEditar
from .models import Materia
from usuarios.models import Docente
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def buscar_docente(request):
    docente = request.GET.get('docente')
    docentes = []
    if docente:
        docentes_encontrados = Docente.objects.filter(
            matricula__icontains=docente).values("id", "matricula", "first_name", "last_name")
        for d in docentes_encontrados:
            docentes.append(d)
        return JsonResponse({'status': 200, 'data': docentes})
    return JsonResponse({'status': 404, 'data': docentes})


@login_required
def agregar_docente(request, pk):
    materia = Materia.objects.get(id=pk)
    docentes = materia.docente.all()
    nombre_materia = materia.nombre
    context = {
        'docentes': docentes,
        'materia': nombre_materia
    }

    if request.method == 'POST':
        id = request.POST.get('id')
        matricula = request.POST.get('matricula_input')

        # Si no se ha seleccionado un docente de la lista
        if id:
            docente = Docente.objects.filter(id=id).first()
        else:
            messages.error(request, 'No se selecionó docente de la lista')
            return render(request, 'agregar_docente.html', context)

        # Si no se escribió matricula en el input
        if not matricula:
            messages.error(request, 'La matrícula no puede estar vacia')
            return render(request, 'agregar_docente.html', context)

        # Si el docente existe
        if docente:
            # Si el docente ya está asignado a la materia
            if Materia.objects.filter(id=materia.id, docente=docente).exists():
                messages.error(
                    request, 'EL docente ya tiene asignada la materia')
                return render(request, 'agregar_docente.html', context)
            else:
                materia.docente.add(docente)
                messages.success(request, 'Docente asignado correctamente')
                return render(request, 'agregar_docente.html', context)
        else:
            messages.error(request, 'El docente no existe')
            return render(request, 'agregar_docente.html', context)

    return render(request, 'agregar_docente.html', context)


@login_required
def agregar_materia(request):
    if request.method == "POST":
        form = FormMateria(request.POST)

        if form.is_valid():
            form.save()
            # Success message
            # Premiliminar url
            messages.success(request, "Materia agregada correctamente")
            return redirect('materias:agregar')
        else:

            context = {
                "form": form
            }
            # Error message
            return render(request, "agregar_materia.html", context)

    form = FormMateria()
    context = {
        "form": form
    }
    return render(request, "agregar_materia.html", context)


@login_required
def editar_materia(request, pk):
    # Get the instance of materia who we want to edit
    materia = get_object_or_404(Materia, id=pk)
    # If the method of request is from a form.
    if request.method == "POST":
        # Build form whit data from POST request.
        form = FormMateriaEditar(request.POST, instance=materia)
        # Validate the data integrity
        if form.is_valid():
            form.save()
            messages.success(request, "Materia editada correctamente.")
            return redirect("materias:agregar")
        else:
            context = {
                'form': form,
                'nombre': materia.nombre
            }
            return render(request, "editar_materia.html", context)
    # If the request come from GET method.
    context = {
        # Add to context the name of Materia who they whant edit.
        'nombre': materia.nombre
    }
    return render(request, "editar_materia.html", context)


@login_required
def lista_materias(request):
    materias = Materia.objects.all()

    context = {
        'materias': materias
    }

    return render(request, 'lista_materias.html', context)

@login_required
def eliminar_materia(request, pk):
    materia = get_object_or_404(Materia, id=pk)
    if materia.delete():
        messages.success(request, 'Materia eliminada correctamente')
        return redirect('materias:lista')
    else:
        messages.error(request, 'No se pudo eliminar la materia')
        return redirect('materias:lista')
