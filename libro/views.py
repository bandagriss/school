from django.shortcuts import *
from twilio.rest import TwilioRestClient

# Create your views here.

def index(request):
    return render(request, "base.html")

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
