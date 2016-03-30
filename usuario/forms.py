from django import forms


class Autor_Update(forms.Form):
    usuario = forms.CharField(max_length=30, initial="Tu Nombre")
    apellido = forms.CharField(max_length=40)
    email = forms.EmailField()