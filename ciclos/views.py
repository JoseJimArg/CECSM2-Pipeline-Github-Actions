from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CicloEscolarForm
from .models import CicloEscolar
from .utils import desactivar_ciclo_activo


@login_required
def nuevo_ciclo(request):
    form = CicloEscolarForm(request.POST or None)
    title = 'Nuevo Ciclo'
    titulo = 'Nuevo ciclo escolar'
    ciclos = CicloEscolar.objects.all()

    if request.method == 'POST':
        if form.is_valid():
            desactivar_ciclo_activo()
            form.save()
            messages.success(request, 'Ciclo escolar creado con éxito')
            return redirect('ciclos:nuevo_ciclo')
        else:
            messages.error(
                request, 'Algunos datos son incorrectos, no se pudo crear el ciclo escolar')

    context = {
        'form': form,
        'title': title,
        'titulo': titulo,
        'ciclos': ciclos,
    }
    return render(request, 'nuevo_ciclo.html', context)

@login_required
def activar_ciclo(request, id):
    ciclo_activar = get_object_or_404(CicloEscolar, id = id)

    if not ciclo_activar.is_active():
        desactivar_ciclo_activo()
        ciclo_activar.update_active(True)
    
    return redirect('ciclos:nuevo_ciclo')
