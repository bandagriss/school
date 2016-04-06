#-*- encoding : utf-8 -*-

from django.shortcuts import *
from twilio.rest import TwilioRestClient

from forms import LibroForm
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf


# Create your views here.


def index(request):
    return render(request, "libro/index.html")


def create(request):
    if request.POST:
        form = LibroForm(request.POST)
        print form
        if form.is_valid():
            return HttpResponse("dis que es valido")
            form.save()

            return HttpResponseRedirect('/libro/index/')
    else:
        form = LibroForm()

    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('libro/create.html', args)




















def IndexSms(request):
    return render(request, 'libro/sms.html')


def twiliosms(request):
    status = []
    if request.method == 'POST':
        mensaje = request.POST['mensaje']
        numero = request.POST['numero']
        status.append("Mensaje enviado satisfactoriamente...")
        account = 'AC7e64c1517222d432aff27fe731d86892'
        token = '4a6d6c2ed182df6d1ff765fed09c9bfd'
        client = TwilioRestClient(account, token)
        number = "+591"+numero
        # print number
        # return HttpResponse(number)
        print status
        message = client.messages.create(to=number, from_="+19016228015", body=mensaje)
        return render(request, 'libro/sms.html',  {'status' : status})
