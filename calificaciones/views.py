from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from clases.models import Clase
from calificaciones.models import Calificacion, Periodo
from usuarios.models import Alumno


@login_required
def registrar_calificaciones(request, id_clase, id_parcial):
    context = {}

    # Verificar si el id del parcial es valido
    parcial = Periodo.objects.filter(id=id_parcial).first()
    if not parcial:
        messages.error(request, 'El parcial no existe')
        return render(request, 'registrar_calificaciones.html', context)

    clase = get_object_or_404(Clase, id=id_clase)
    calificaciones = obtener_calificaciones(clase, parcial)

    context = {
        'clase': clase,
        'calificaciones': calificaciones,
        'parcial': parcial
    }

    if request.method == 'POST':
        calificaciones = guardar_calificacion(
            request, clase, parcial, calificaciones)
        context['calificaciones'] = calificaciones
        return render(request, 'registrar_calificaciones.html', context)

    return render(request, 'registrar_calificaciones.html', context)


def guardar_calificacion(request, clase, parcial, calificaciones):
    cont = 0
    for llave, alumno in calificaciones.items():
        calificacion = request.POST.get(str(alumno['id']))
        # verificar si viene la calificacion del alumno
        if calificacion and float(calificacion) >= 5 and float(calificacion) <= 10:
            # Verificar si el alumno pertenece a la clase
            if Clase.objects.filter(id=clase.id, alumno=alumno['id']).first():
                existe_calificacion = Calificacion.objects.filter(
                    alumno=Alumno.objects.get(id=alumno['id']),
                    clase=clase,
                    tipo=parcial
                ).first()
                # Verificar si el alumno ya tiene calificacion en el parcial y actualizarla
                if existe_calificacion:
                    if (existe_calificacion.calificacion != float(calificacion)):
                        existe_calificacion.calificacion = calificacion
                        existe_calificacion.save()
                        alumno['calificacion'] = float(calificacion)
                        cont += 1
                else:
                    # Sino se crea la nueva calificacion
                    reg_calificacion = Calificacion.objects.create(
                        alumno=Alumno.objects.get(id=alumno['id']),
                        clase=clase,
                        calificacion=calificacion,
                        tipo=parcial
                    )
                    if reg_calificacion:
                        reg_calificacion.save()
                        alumno['calificacion'] = float(calificacion)
                        cont += 1
    messages.success(request, f'Se registraron {cont} calificaciones')
    return calificaciones


def obtener_calificaciones(clase, parcial):
    alumnos = clase.alumno.all()
    calificaciones = {}

    if not parcial:
        return False

    for alumno in alumnos:
        calificacion = Calificacion.objects.filter(
            alumno=alumno,
            clase=clase,
            tipo=parcial
        ).first()
        # Si tiene una calificacion obtenerla
        if calificacion:
            calificaciones[alumno.id] = {
                'calificacion': calificacion.calificacion,
                'id': alumno.id,
                'first_name': alumno.first_name,
                'last_name': alumno.last_name,
            }
        else:
            # Si no tiene calificacion no se pone nada
            calificaciones[alumno.id] = {
                'calificacion': '',
                'id': alumno.id,
                'first_name': alumno.first_name,
                'last_name': alumno.last_name,
            }
    return calificaciones


def consulta_calificaciones_alumno(request):
    if request.method == "POST":
        # Validation for matricula do not exists
        try:
            alumno = Alumno.objects.get(
                matricula=request.POST['matricula_alumno'])
        except:
            messages.error(request, "Alumno no encontrado.")
            context = {
                'matricula_alumno': request.POST['matricula_alumno']
            }
            return render(request, "consulta_calificaciones_alumno.html", context)
        clases = Clase.objects.filter(alumno=alumno.id)

        calificaciones = []
        for clase in clases:
            calificacion = Calificacion.objects.filter(
                alumno=alumno.id, clase=clase.id)
            calificaciones.append(calificacion)

        context = {
            'matricula_alumno': request.POST['matricula_alumno'],
            'clases': clases,
            'calificaciones': calificaciones,
            'alumno': alumno,
            'consulta': True
        }
        return render(request, "consulta_calificaciones_alumno.html", context)

    # request method is GET
    context = {}
    return render(request, "consulta_calificaciones_alumno.html", context)
