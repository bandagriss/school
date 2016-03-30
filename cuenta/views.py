# -*- encoding: utf-8 -*-
from django.shortcuts import *
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives

# Create your views here.


def login(request):
    return render(request, 'cuenta/login.html')


def auth_view(request):

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/inicio/')
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


@login_required(login_url='/auth_view')
def home(request):
    return render(request, 'cuenta/dashboard.html')


def crear(request):
    return render(request, "cuenta/register.html")


def register_account(request):
    errors = []
    if request.method == 'POST':
        # return HttpResponse('<h1>es metodo post</h1>')
        if not request.POST.get('username', ''):
            errors.append('Por favor Introduce el Usuario')
        duplicado = User.objects.filter(username = request.POST.get('username'))
        if duplicado:
            errors.append('El Usuario ya Existe.')
        if not request.POST.get('password', ''):
            errors.append('Por favor Introduce la Contraseña')
        if (len(request.POST.get('password'))<5):
            errors.append('La Contraseña debe tener minimamente 5 caracteres.')
        if(request.POST.get('password') != request.POST.get('password2')):
            errors.append('Las Contraseñas no coinciden vuelva a intentarlo')
        if not request.POST.get('firstname', ''):
            errors.append('Por favor Introduce tu Nombre')
        if not request.POST.get('matricula',''):
            errors.append('Por favor Introduce tu Número de Matricula.')
        duplicadoMatricula = request.POST.get('matricula','')
        if duplicadoMatricula:
            if not duplicadoMatricula.isdigit():
                errors.append('Por favor llene Matricula solo con números.')
            else:
                duMA = User.objects.filter(matricula = duplicadoMatricula)
                if duMA:
                    errors.append('La Matricula ya existe')

        if not request.POST.get('ci',''):
            errors.append('Por favor Introduce tu Número de CI.')
        duplicadoCI =  request.POST.get('ci','')
        if duplicadoCI:
            if not duplicadoCI.isdigit():
                errors.append('Por favor Introduce CI solo con números')
            else:
                duCI = User.objects.filter(ci = duplicadoCI)
                if duCI:
                    errors.append('El CI ya existe.')
        if request.POST.get('email') and '@' not in request.POST['email']:
            errors.append('Por favor Introduce una dirección de correo válida')
        if not errors:
            usuario = request.POST['username']
            contrasenia = request.POST['password']
            nombre = request.POST['firstname']
            apellido = request.POST['lastname']
            correo = request.POST['email']
            matricula = request.POST['matricula']
            ci = request.POST['ci']
            direccion = request.POST['direccion']
            # fecha = time.strftime("%y/%m/%d %H:%M:%S")
            account = User.objects.create_user(usuario, correo, contrasenia)
            account.first_name = nombre
            account.last_name = apellido
            account.matricula = matricula
            account.ci = ci
            account.direccion = direccion
            account.save()
            # return HttpResponse('<h1>usuario Creado Correctamente</h1>')

            enviaCorreo(usuario, contrasenia, correo)
            ok = 'Cuenta creada Éxitosamente'
            return render(request, 'cuenta/login.html', {'ok': ok})
        return render(request, 'cuenta/register.html', {'errors': errors,
         'username': request.POST.get('username',''),
         'password':request.POST.get('password',''),
         'password2':request.POST.get('password2',''),
         'firstname':request.POST.get('firstname',''),
         'lastname':request.POST.get('lastname',''),
         'email': request.POST.get('email',''),
         'matricula': request.POST.get('matricula',''),
         'ci': request.POST.get('ci',''),
         'direccion': request.POST.get('direccion','')})


def enviaCorreo(usuario, contrasenia, correo):
    # return HttpResponse('la contrasenia es: %s'%contrasenia)
    subject, from_email, to = 'Creacion de Cuenta', 'Biblioteca Virtual', correo
    text_content = 'This is an important message.'
    html_content = '<h1>Creaci&oacute;n de Cuenta &Eacute;xitosa</h1><br><p>Bienvenido al Sistema de Biblioteca Virtual<br>Usuario: <strong>'+usuario+'</strong><br>Contrase&ntilde;a: <strong>'+contrasenia+'</strong><br><br>ahora puede dirigirse a <a href="http://192.168.1.4:8000">Biblioteca Virtual</a> .</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@login_required(login_url='/auth_view')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')