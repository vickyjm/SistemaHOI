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
                                 label = "Contraseña")