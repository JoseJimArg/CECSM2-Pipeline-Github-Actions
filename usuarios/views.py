from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.http import Http404
from django.db import transaction
from CECSM2.settings import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER
from calificaciones.models import Periodo
from clases.models import Clase
from usuarios.forms import AlumnoEditForm, AlumnoForm, AspiranteCorregirForm, DocenteEditForm, DocenteForm, AspiranteForm
from .models import Alumno, Docente, Aspirante
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.views.generic.edit import CreateView
from .filters import AspiranteFilter
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone
from django.contrib.auth.models import update_last_login

from ciclos.models import CicloEscolar
from grupos.models import Grupo, Semestre
from materias.models import Materia


# Create your views here.

from django.utils.decorators import method_decorator


def home(request):
    return render(request, "home.html")

@method_decorator(login_required, name='dispatch')
class ListaDocentes(ListView):
    model = Docente
    context_object_name = 'docentes'
    template_name = 'docentes/lista_docentes.html'


@method_decorator(login_required, name='dispatch')
class NuevoDocente(CreateView):
    model = Docente
    form_class = DocenteForm
    template_name = "docentes/nuevo_docente.html"
    success_url = reverse_lazy('usuarios:lista_docentes')

@login_required
def eliminar_docente(request, pk):
    docente = get_object_or_404(Docente, pk=pk)
    if docente.delete():
        messages.success(request, 'Docente eliminado correctamente')
    else:
        messages.error(request, 'No se pudo eliminar el docente')
    return redirect('usuarios:lista_docentes')

class Login(LoginView):
    model = User
    template_name = 'login.html'

def logout_view(request):
    logout(request)
    return redirect('usuarios:login')

@method_decorator(login_required, name='dispatch')
class EditarDocente(UpdateView):
    model = Docente
    template_name = "docentes/nuevo_docente.html"
    form_class = DocenteEditForm
    extra_context = {'etiqueta': 'Actualizar', 'boton': 'Guardar'}
    success_url = reverse_lazy('usuarios:lista_docentes')

@login_required
def ver_docente(request, pk):
    if request.method == 'GET':
        docente = get_object_or_404(Docente, pk=pk)
        materias = Materia.objects.filter(docente=docente)
        context = {
            'docente': docente,
            'materias': materias
        }
        return render(request, 'docentes/detalle.html', context)
    else:
        return redirect('usuarios:lista_docentes')

@method_decorator(login_required, name='dispatch')
class NuevoAlumno(CreateView):
    model = Alumno
    form_class = AlumnoForm
    template_name = "alumnos/nuevo_alumno.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        return redirect('usuarios:lista_alumnos')

@method_decorator(login_required, name='dispatch')
class EditarAlumno(UpdateView):
    model = Alumno
    template_name = "alumnos/nuevo_alumno.html"
    form_class = AlumnoEditForm
    extra_context = {'etiqueta': 'Actualizar', 'boton': 'Guardar'}
    success_url = reverse_lazy('usuarios:lista_alumnos')

@login_required
def eliminar_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    if alumno.delete():
        messages.success(request, 'Alumno eliminado correctamente')
    else:
        messages.error(request, 'No se pudo eliminar el alumno')
    return redirect('usuarios:lista_alumnos')


@login_required
def lista_alumnos(request):
    alumnos = Alumno.objects.all()
    context = {}
    if any(alumnos):
        context = {
            "alumnos": alumnos
        }
    return render(request, "alumnos/lista_alumnos.html", context)

@login_required
def ver_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    clases = alumno.clase_set.all().order_by('-ciclo')
    context = {
        'alumno': alumno,
        'clases': clases
    }
    return render(request, 'alumnos/ver_alumno.html', context)

@login_required
def ver_clases(request):
    context = {}
    profe = Docente.objects.filter(id=request.user.id).first()
    if not profe:
        context = {
            'clases': [],
        }
        return render(request, 'docentes/lista_clases_docente.html', context)
    clases = Clase.objects.filter(docente=profe)
    primer_parcial = get_object_or_404(Periodo, nombre='Primer Parcial')
    segundo_parcial = get_object_or_404(Periodo, nombre='Segundo Parcial')
    tercer_parcial = get_object_or_404(Periodo, nombre='Tercer Parcial')
    ordinario = get_object_or_404(Periodo, nombre='Ordinario')
    extraordinario = get_object_or_404(Periodo, nombre='Extraordinario')
    context = {
        'clases': clases,
        'primer_parcial': primer_parcial,
        'segundo_parcial': segundo_parcial,
        'tercer_parcial': tercer_parcial,
        'ordinario': ordinario,
        'extraordinario': extraordinario,
        'docente': profe
    }
    return render(request, 'docentes/lista_clases_docente.html', context)


def nuevo_aspirante(request):
    if request.method == "POST":
        form = AspiranteForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic(): #Transaccion
                    aspirante = form.save()
                    aspirante.is_active=False
                    aspirante.valido_comprobante_pago = False
                    aspirante_grupo=Group.objects.get(name="Aspirante_Grupo")
                    aspirante.groups.add(aspirante_grupo)
                    aspirante.save()
                    
                    mensaje = render_to_string(request=request, template_name='aspirantes/aviso_registro_correo.html')
                    asunto = 'Registro preinscripciones CECS'
                    correo = aspirante.email
                    email = EmailMessage(
                        asunto,
                        mensaje,
                        to=[correo]
                    )
                    email.content_subtype = 'html'
                    email.send()
                    if request.user.is_authenticated:
                        # Es admin
                        messages.success(request,"Aspirante registrado satisfactoriamente.")
                        form = AspiranteForm()
                    else: # Es un aspirante registrandose.
                        return render(request,"aspirantes/aviso_registro.html")
            except Exception as e:
                raise Http404
        context={
            "form":form
        }
        return render(request,"aspirantes/nuevo_aspirante.html", context)
    form= AspiranteForm()
    context={
        "form":form
    }
    return render(request, "aspirantes/nuevo_aspirante.html",context)

@login_required
def aceptar_aspirante(request, id):
    aspirante = get_object_or_404(Aspirante, id=id)
    # Actualizar el estado del aspirante para que pueda entonces iniciar sesión en el sistema.
    aspirante.is_active=True
    aspirante.valido_comprobante_pago = True
    aspirante.status = 1
    aspirante.save()

    # mandar correo
    if notificar_cambio_aspirante(request, aspirante.email, "Se ha aceptado tu registro. Puedes entrar al sistema e inscribirte a un grupo."):
        messages.success(request, "El estudiante ha sido Aceptado y ha sido notificado con un correo.")
    else:
        messages.error(request, "Hubo un error al enviar la notificación de actualización al aspirante. Intentar contactarse con el Aspirante para notificarle de su cambio y/o problema.")

    return redirect("usuarios:ver_aspirante", pk=id)

@login_required
def rechazar_aspirante(request, id):
    aspirante = get_object_or_404(Aspirante, id=id)
    # Actualizar el estado del aspirante para que pueda entonces iniciar sesión en el sistema.
    aspirante.is_active=False
    aspirante.valido_comprobante_pago = False
    aspirante.status = 2
    aspirante.save()

    if notificar_cambio_aspirante(request, aspirante.email, "Tu registro ha pasado de aceptado a rechazado. Comunícate con la administración para saber qué es lo que pasa."):
        messages.success(request, "El estudiante ha pasado de Aceptado a Rechazado y ha sido notificado con un correo.")
    else:
        messages.error(request, "Hubo un error al enviar la notificación de actualización al aspirante. Intentar contactarse con el Aspirante para notificarle de su cambio y/o problema.")

    return redirect("usuarios:ver_aspirante", pk=id)

@login_required
def avisar_comprobante_erroneo(request, id):
    aspirante = get_object_or_404(Aspirante, id=id)
    aspirante.valido_comprobante_pago = False
    aspirante.save()

    # Crear token temporal
    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(aspirante)

    # Mandar correo
    if notificar_cambio_aspirante(request, aspirante.email, f"Se te notifica sobre un error en tu comprobante de pago. Por favor subir tu documentación correcta en el siguiente enlace: {settings.URL_SISTEMA}aspirantes/corregir/{token}/{aspirante.id}/"):
        messages.success(request, "Se ha enviado un correo al aspirante para que pueda subir nuevamente su comprobante de pago.")
    else:
        messages.error(request, "Hubo un problema al enviar el correo al aspirante, favor de avisarle del problema de documentación por medio de un correo.")

    return redirect("usuarios:ver_aspirante", pk=id)

def corregir(request, token, id):
    token_generator = PasswordResetTokenGenerator()
    aspirante = get_object_or_404(Aspirante, id=id)
    token_valido = token_generator.check_token(aspirante,token)
    
    if not token_valido:
        messages.error(request, "El enlace ha expirado o ya se ha utlizado para corregir documentación.")
        return redirect("usuarios:login")

    if request.method == "POST":
        form = AspiranteCorregirForm(instance = aspirante, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            update_last_login(None, aspirante) # Se actualiza la fecha de last_login para que el token no tenga más función.
            messages.success(request, "Documentos actualizados. Espera a las indicaciones de la administración.")
            notificar_cambio_aspirante(request, aspirante.email, "Se ha actualizado tu documentación en la plataforma. Espera las indicaciones de la administración.")
            return redirect("usuarios:login")
        context={
            "form":form
        }
        return render(request, "aspirantes/corregir_documentos.html", context)

    context={
        "form":AspiranteCorregirForm()
    }
    return render(request, "aspirantes/corregir_documentos.html", context)

def notificar_cambio_aspirante(request, email, mensaje):
    try:
        mensaje = render_to_string(request=request, template_name='aspirantes/aviso_actualizacion_registro.html', context={"mensaje":mensaje, "url":settings.URL_SISTEMA})
        asunto = 'Actualización del registro preinscripciones CECS'
        correo = email
        email = EmailMessage(
            asunto,
            mensaje,
            to=[correo]
        )
        email.content_subtype = 'html'
        email.send()
        return True
    except Exception as e:
        return False



@login_required
def lista_aspirantes(request):
    aspirantes = AspiranteFilter(request.GET, queryset=Aspirante.objects.all())

    context = {
        "filter": aspirantes
    }
    
    return render(request, "aspirantes/lista_aspirantes.html", context)

@login_required
def ver_aspirante(request, pk):
    aspirante = get_object_or_404(Aspirante, pk=pk)
    tipoDocumento=str(aspirante.comprobante_pago)[-3:]
    context = {
        'aspirante': aspirante,
        "tipoDocumento":tipoDocumento
    }
    return render(request, 'aspirantes/ver_aspirante.html', context)

@login_required
def eliminar_aspirante(request, pk):
    aspirante = get_object_or_404(Aspirante, pk=pk)
    if aspirante.delete():
        messages.success(request, 'Aspirante eliminado correctamente')
    else:
        messages.error(request, 'No se pudo eliminar el aspirante')
    return redirect('usuarios:lista_aspirantes')

@login_required
def inscribir_aspirante(request, id):
    aspirante = get_object_or_404(Aspirante, id=request.user.id)

    ciclo = CicloEscolar.objects.filter( activo = True ).first()
    if not ciclo:
        messages.error(request, "!Error! No hay ciclo escolar activo")
        return redirect('grupos:lista_semestre_cero')

    # Check if the aspirante is on any grupo of semestre 0
    esta_inscrito = validar_aspirante_no_inscrito(aspirante, ciclo)
    if esta_inscrito:
        # aspirante is allready in one grupo of semestre cero
        messages.error(request, f"!Error! Ya estás inscrito en el grupo {esta_inscrito.grupo.letra}")
        return redirect('grupos:lista_semestre_cero')
    else:
        # aspirante is't enrolled
        grupo = get_object_or_404( Grupo, id = id )
        clases = Clase.objects.filter( ciclo = ciclo, grupo = grupo )

        for clase in clases:
            if not (aspirante in clase.aspirantes.all()):
                if clase.cupo_restante != 0:
                    clase.aspirantes.add(aspirante)
                    clase.cupo_restante = int(clase.cupo_restante) - 1
                    clase.save()
                else:
                    messages.error(request, f"!Error! El grupo {grupo.letra} ya no tiene cupo")
                    return redirect('grupos:lista_semestre_cero')
            else:
                messages.error(request, f"!Error! Ya estás inscrito en el grupo {grupo.letra}")
                return redirect('grupos:lista_semestre_cero')
        
        
        messages.success(request, f"Alumno {aspirante.first_name} {aspirante.last_name} con número {aspirante.num_aspirante} inscrito correctamente en el grupo {grupo}")
        return redirect('grupos:lista_semestre_cero')


# Helpers
def validar_aspirante_no_inscrito(aspirante, ciclo):
    semestre_cero = get_object_or_404( Semestre, numero = 0 )
    grupos_semestre_cero = Grupo.objects.filter( semestre = semestre_cero.id ) 
    
    # Get all clases of all of the grupos of semestre cero
    clases = []
    for grupo in grupos_semestre_cero:
        clases_grupo = Clase.objects.filter( grupo = grupo, ciclo = ciclo )
        for clase in clases_grupo:
            clases.append(clase)
    
    # Check if the aspirante is in any clase of any grupo of semestre cero
    for clase in clases:
        if aspirante in clase.aspirantes.all():
            return clase
    
    return False
