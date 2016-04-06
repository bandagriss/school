#-*- encoding:utf-8 -*-
from django import forms
from models import Libro
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect, render_to_response

class LibroForm(forms.ModelForm):

   class Meta:
      model = Libro
      widgets = {
            'codigo': forms.TextInput(attrs={'class' : 'form-control col-md-7 col-xs-12'}),
            'titulo': forms.TextInput(attrs={'class' : 'form-control col-md-7 col-xs-12'}),




      }
      fields = ['codigo', 'titulo', 'autor', 'ejemplares', 'editor', 'fecha_publicacion', 'estado', 'area', 'tipo_documento', 'notas']

   #Validamos que el autor no sea menor a 3 caracteres
   def clean_codigo(self):
      codigo = self.cleaned_data.get('codigo')
      if len(codigo) < 3:
         raise forms.ValidationError("El autor debe contener mas de tres caracteres")

      return codigo

   def clean_titulo(self):
      titulo = self.cleaned_data.get('titulo')
      if len(titulo)>150:
         raise forms.ValidationError("El titulo es muy extenso porfavor introduzca un titulo menor a 150 caracteres")
      return titulo

