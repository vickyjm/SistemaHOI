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
                                 label = "Contraseña1", widget=forms.PasswordInput)
    contraseña2 = forms.CharField(max_length = 25,
                                 required = True,
                                 label = "Contraseña2", widget=forms.PasswordInput)