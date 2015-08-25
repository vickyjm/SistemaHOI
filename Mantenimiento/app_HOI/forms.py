# -*- coding: utf-8 -*-

from django import forms
from django.core.validators import RegexValidator

class iniciarSesionForm(forms.Form):
    cedula = forms.CharField(
                    max_length = 11,
                    required = True,
                    label = "Cédula de Identidad",
                    validators = [
                        RegexValidator(
                            regex = '^([1-9][0-9]{0,2})([0-9]{3}){0,3}$',
                            message = 'Formato erróneo'
                        )
                    ]
            )
    contraseña = forms.CharField(max_length = 25,
                                 required = True,
                                 label = "Contraseña", widget=forms.PasswordInput)
    
class registroForm(forms.Form):
    cedula = forms.CharField(
                    max_length = 11,
                    required = True,
                    label = "Cédula de Identidad",
                    validators = [
                        RegexValidator(
                            regex = '^([1-9][0-9]{0,2})([0-9]{3}){0,3}$',
                            message = 'Formato erróneo'
                        )
                    ]
            )
    nombre = forms.CharField(max_length = 30, required = True, label = "Nombre")
    apellido = forms.CharField(max_length = 30, required = True, label = "Apellido")
    correo = forms.EmailField(required = False, label = "Correo electrónico")
    tipoEmpleado = (("tecnico","Técnico"), ("almacenista", "Almacenista"), ("admin", "Administrador"))
    tipo = forms.ChoiceField(required = True, choices = tipoEmpleado, 
                             widget = forms.Select(), label = "Cargo")
    contraseña1 = forms.CharField(max_length = 25,
                                 required = True,
                                 label = "Contraseña", widget=forms.PasswordInput)
    contraseña2 = forms.CharField(max_length = 25,
                                 required = True,
                                 label = "Confirmar contraseña", widget=forms.PasswordInput)

class itemForm(forms.Form)
    nombre = forms.CharField(max_length = 60, required = True, label = "Nombre")
    cantidad = forms.IntegerField(max_value = 2147483647, min_value = 0, required = True, label = "Cantidad")
    categoria = forms.ModelChoiceField(queryset = Categoria.objects.all())
    opciones_prioridad = (("baja", "Baja"),("media", "Media"), ("alta", "Alta"))
    prioridad = forms.ChoiceField(required = True, choices = opciones_prioridad, widget = forms.Select(), label = "Prioridad")
    minimo = forms.IntegerField(max_value = 2147483647, min_value = 0, required = True, label = "Mínimo valor para alerta")