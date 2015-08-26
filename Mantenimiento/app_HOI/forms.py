# -*- coding: utf-8 -*-

from django import forms
from django.core.validators import RegexValidator
from app_HOI.models import Categoria
from django.forms import ModelChoiceField

class iniciarSesionForm(forms.Form):
    cedula = forms.CharField(
                    max_length = 11,
                    required = True,
                    label = "Cédula de Identidad",
                    widget=forms.TextInput(attrs={'style': 'width:100%'}),
                    validators = [
                        RegexValidator(
                            regex = '^([1-9][0-9]{0,2})([0-9]{3}){0,3}$',
                            message = 'Formato erróneo'
                        )
                    ]
            )
    contraseña = forms.CharField(max_length = 25,
                                 required = True,
                                 label = "Contraseña", widget=forms.PasswordInput(attrs={'style': 'width:100%'}))
    
class registroForm(forms.Form):
    cedula = forms.CharField(
                    max_length = 11,
                    required = True,
                    label = "Cédula de Identidad",
                    widget=forms.TextInput(attrs={'style': 'width:100%'}),
                    validators = [
                        RegexValidator(
                            regex = '^([1-9][0-9]{0,2})([0-9]{3}){0,3}$',
                            message = 'Formato erróneo'
                        )
                    ]
            )
    nombre = forms.CharField(max_length = 30, required = True, label = "Nombre", widget=forms.TextInput(attrs={'style': 'width:100%'}))
    apellido = forms.CharField(max_length = 30, required = True, label = "Apellido", widget=forms.TextInput(attrs={'style': 'width:100%'}))
    correo = forms.EmailField(required = False, label = "Correo electrónico", widget=forms.EmailInput(attrs={'style': 'width:100%'}))
    tipoEmpleado = (("tecnico","Técnico"), ("almacenista", "Almacenista"), ("admin", "Administrador"))
    tipo = forms.ChoiceField(required = True, choices = tipoEmpleado, 
                             widget = forms.Select(attrs={'style': 'width:100%; background-color:white'}), label = "Cargo")
    contraseña1 = forms.CharField(max_length = 25,
                                 required = True,
                                 label = "Contraseña", widget=forms.PasswordInput(attrs={'style': 'width:100%'}))
    contraseña2 = forms.CharField(max_length = 25,
                                 required = True,
                                 label = "Confirmar contraseña", widget=forms.PasswordInput(attrs={'style': 'width:100%'}))

class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "My Object #%i" % obj.nombre

class itemForm(forms.Form):
    nombre = forms.CharField(max_length = 100, required = True, label = "Nombre", widget = forms.TextInput(attrs={'style': 'width:100%'}))
    cantidad = forms.IntegerField(max_value = 2147483647, min_value = 0, required = True, label = "Cantidad", widget=forms.NumberInput(attrs={'style': 'width:100%'}))
    # Categoria.objects.none() creo que porque no hay nada,  si no seria Categoria.objects.all()
    categoria = forms.ModelChoiceField(widget=forms.Select(attrs={'style': 'width:100%; background-color:white'}), queryset=Categoria.objects.order_by('nombre'), label = "Categoría")
    opciones_prioridad = (("baja", "Baja"),("media", "Media"), ("alta", "Alta"))
    prioridad = forms.ChoiceField(required = True, choices = opciones_prioridad, widget = forms.Select(attrs={'style': 'width:100%; background-color:white'}), label = "Prioridad")
    minimo = forms.IntegerField(max_value = 2147483647, min_value = 0, required = True, label = "Mínimo valor para alerta", widget=forms.NumberInput(attrs={'style': 'width:100%'}))

class categoriaForm(forms.Form):
    nombre = forms.CharField(max_length = 100, required = True, label = "Nombre", widget = forms.TextInput(attrs={'style': 'width:100%'}))