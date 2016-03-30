# -*- encoding: utf-8 -*-
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect, render_to_response
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from usuario.forms import Autor_Update
from django.http import HttpResponseRedirect

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from libro.models import Libro, Editor, TipoDocumento, Area, Estado, Autor, Prestamo, Devolucion

from django_datatables_view.base_datatable_view import BaseDatatableView


# Create your views here.
class OrderListJson(BaseDatatableView):
    # The model we're going to show
    model = User

    columns = ['id', 'first_name', 'matricula', 'email', 'accion']

    order_columns = ['id', 'first_name', 'matricula', 'email', 'accion']
    max_display_length = 500

    def render_column(self, row, column):
        # We want to render user as a custom column

        if column == 'accion':
            # return '{0} {1}'.format(row.first_name, row.last_name)
            # return '{0} {1}'.format(row.first_name, row.id)

            # return '{0}'.format("<button>"+ str(row.id) +"</button>")
            return '{0}'.format(
                '<div class="btn-group"><button type="button" class="btn btn-success">Action</button><button type="button" class="btn btn-success dropdown-toggle" data-toggle="dropdown" aria-expanded="false"><span class="caret"></span><span class="sr-only">Toggle Dropdown</span></button><ul class="dropdown-menu" role="menu"><li><a href="/usuario/ver/' + str(
                    row.id) + '/"></a></li><li><a href="/usuario/ver/' + str(
                    row.id) + '/">Ver </a></li><li><a href="/usuario/editar/' + str(
                    row.id) + '/">Editar</a></li><li class="divider"></li><li><a href="/usuario/ver/' + str(
                    row.id) + '/">Eliminar</a></li></ul></div>')
        else:
            return super(OrderListJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset

        # simple example:
        search = self.request.GET.get(u'search[value]', None)

        if search:
            qs = qs.filter(first_name__istartswith=search) or qs.filter(id__istartswith=search) or qs.filter(
                matricula__istartswith=search) or qs.filter(email__istartswith=search)





            # more advanced example using extra parameters
            # filter_customer = self.request.GET.get(u'customer', None)
            #
            # if filter_customer:
            #     customer_parts = filter_customer.split(' ')
            #     qs_params = None
            #     for part in customer_parts:
            #         q = Q(name__istartswith=part)|Q(name__istartswith=part)
            #         qs_params = qs_params | q if qs_params else q
            #     qs = qs.filter(qs_params)
        return qs


def index(request):
    return render(request, "usuario/index.html")


def show(request, id):
    user = User.objects.get(id__exact=id)
    return render(request, "usuario/show.html", {'user': user})


def edit(request, id):
    user = User.objects.get(id__exact=id)
    return render(request, "usuario/edit.html", {'user': user})


def update(request, id):
    errors = []
    datos = User.objects.get(id = id)

    if request.method == 'POST':
        if not request.POST.get('username', ''):
            errors.append('Por favor Introduce el Usuario')
        duplicado = User.objects.filter(username=request.POST.get('username', ''))
        if duplicado:
            if str(duplicado[0]) != str(datos.username):
                errors.append('El Usuario ya Existe.')
        if not request.POST.get('password', ''):
            errors.append('Por favor Introduce la Contraseña')
        if (len(request.POST.get('password'))<5):
            errors.append('La Contraseña debe tener minimamente 5 caracteres.')
        if(request.POST.get('password') != request.POST.get('password2')):
            errors.append('Las Contraseñas no coinciden vuelva a intentarlo')
        if not request.POST.get('firstname', ''):
            errors.append('Por favor Introduce tu Nombre')
        if not request.POST.get('lastname', ''):
            errors.append('Por favor Introduce tu Apellido')
        if not request.POST.get('matricula',''):
            errors.append('Por favor Introduce tu Número de Matricula.')
        duplicadoMatricula = request.POST.get('matricula','')
        if duplicadoMatricula:
            if not duplicadoMatricula.isdigit():
                errors.append('Por favor llene Matricula solo con números.')
            else:

                duMA = User.objects.filter(matricula=duplicadoMatricula)
                if duMA:
                    if str(duMA[0]) != str(datos.username):
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
                    if str(duCI[0]) != str(datos.username):
                        errors.append('El CI ya existe.')
        if request.POST.get('email') and '@' not in request.POST['email']:
            errors.append('Por favor Introduce una dirección de correo válida')
        else:
            duplicadoEmail = request.POST.get('email', '')
            duEmail = User.objects.filter(email=duplicadoEmail)
            if duEmail:
                if str(duEmail[0]) != str(datos.username):
                    errors.append('El Email ya existe')
        if not errors:
            usuario = request.POST['username']
            contrasenia = request.POST['password']
            nombre = request.POST['firstname']
            apellido = request.POST['lastname']
            correo = request.POST['email']
            matricula = request.POST['matricula']
            ci = request.POST['ci']
            direccion = request.POST['direccion']

            datos.username = usuario
            datos.email = correo
            if contrasenia != "********":
                datos.password = make_password(contrasenia)
            datos.first_name = nombre
            datos.last_name = apellido
            datos.matricula = matricula
            datos.ci = ci
            datos.direccion = direccion
            datos.save()
            # return HttpResponse('<h1>usuario Creado Correctamente</h1>')
            ok = 'Usuario Modificado Éxitosamente'
            return render(request, 'usuario/index.html', {'ok': ok})

        user = User.objects.get(id__exact=id)
        user.username = request.POST.get('username','')
        # user.password = request.POST.get('password','')
        # user.password2 = request.POST.get('password2','')
        user.first_name = request.POST.get('firstname','')
        user.last_name = request.POST.get('lastname','')
        user.email =  request.POST.get('email','')
        user.matricula =  request.POST.get('matricula','')
        user.ci =  request.POST.get('ci','')
        user.direccion =  request.POST.get('direccion','')
 
        return render(request, 'usuario/edit.html', {'errors': errors, 'user': user})

# def update(request, id):
#     if request.method == 'POST':
#         formulario = Autor_Update(request.POST)
#         print formulario
#         if formulario.is_valid():
#             usuario = User.objects.get(id=id)
#             usuario.username=request.POST['usuario']
#             usuario.first_name = request.POST['apellido']
#             usuario.email = request.POST['email']
#             usuario.save()
#             return HttpResponseRedirect('/usuario/index/')
#     else:
#         formulario=Autor_Update()
#
#     ##  Agarra formulario: de esta manera agarramos el formulario para ponerle css
#     args = {}
#     args.update(csrf(request))
#     args['formulario'] = UserCreationForm()
#     datos = User.objects.get(id = id)
#     return render_to_response('usuario/update.html', args)
#     # return render_to_response('usuario/update.html', args)
#
#     #return render_to_response('updateAutor.html', {'formulario':formulario},context_instance=RequestContext(request))
