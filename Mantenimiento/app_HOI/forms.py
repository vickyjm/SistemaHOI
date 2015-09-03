# -*- coding: utf-8 -*-

from django import forms
from django.core.validators import RegexValidator
from app_HOI.models import Categoria,Item
from django.forms import ModelChoiceField
from django.utils.translation import ugettext, ugettext_lazy as _

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
                    label = "Contraseña", 
                    widget=forms.PasswordInput(attrs={'style': 'width:100%'}))
    
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
    nombre = forms.CharField(max_length = 30, 
                    required = True, 
                    label = "Nombre", 
                    widget=forms.TextInput(attrs={'style': 'width:100%'}))
    apellido = forms.CharField(max_length = 30, 
                    required = True, 
                    label = "Apellido", 
                    widget=forms.TextInput(attrs={'style': 'width:100%'}))
    correo = forms.EmailField(required = False, 
                    label = "Correo electrónico", 
                    widget=forms.EmailInput(attrs={'style': 'width:100%'}))
    tipoEmpleado = (("tecnico","Técnico"), ("almacenista", "Almacenista"))
    tipo = forms.ChoiceField(required = True, 
                    choices = tipoEmpleado, 
                    widget = forms.Select(attrs={'style': 'width:100%; background-color:white'}), 
                    label = "Cargo")

    contraseña1 = forms.CharField(max_length = 25,
                     required = True,
                     label = "Contraseña", 
                     widget=forms.PasswordInput(attrs={'style': 'width:100%'}))
    contraseña2 = forms.CharField(max_length = 25,
                     required = True,
                     label = "Confirmar contraseña", 
                     widget=forms.PasswordInput(attrs={'style': 'width:100%'}))

class recuperarContraseñaForm(forms.Form):
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
    contraseña1 = forms.CharField(max_length = 25,
                     required = True,
                     label = "Contraseña", 
                     widget=forms.PasswordInput(attrs={'style': 'width:100%'}))
    contraseña2 = forms.CharField(max_length = 25,
                     required = True,
                     label = "Confirmar contraseña", 
                     widget=forms.PasswordInput(attrs={'style': 'width:100%'}))

class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "My Object #%i" % obj.nombre

class itemForm(forms.Form):
    nombre = forms.CharField(max_length = 100, 
                    required = True, 
                    label = "Nombre", 
                    widget = forms.TextInput(attrs={'style': 'width:100%'}))
    cantidad = forms.IntegerField(max_value = 2147483647, 
                    min_value = 0, 
                    required = True, 
                    label = "Cantidad", 
                    widget=forms.NumberInput(attrs={'style': 'width:100%'}))
    categoria = forms.ModelChoiceField(label = "Categoría",
        widget=forms.Select(attrs={'style':'width:100%; background-color:white'}), 
        queryset=Categoria.objects.order_by('nombre'))
    opciones_prioridad = ((0, "Baja"),(1, "Media"), (2, "Alta"))
    prioridad = forms.ChoiceField(required = True, 
                    choices = opciones_prioridad, 
                    widget = forms.Select(attrs={'style': 'width:100%; background-color:white'}), 
                    label = "Prioridad")
    minimo = forms.IntegerField(max_value = 2147483647, 
                    min_value = 0, 
                    required = True, 
                    label = "Mínimo valor para alerta", 
                    widget=forms.NumberInput(attrs={'style': 'width:100%'}))

# Form para editar items, hereda de itemForm
class item_editarForm(itemForm):
    opciones_estado = (('0', 'Inactivo',), ('1', 'Activo'))
    estado = forms.ChoiceField(required = True,
                    widget=forms.RadioSelect(attrs={'style': 'width:100%; background-color:white'}), 
                    label = "Estado",
                    choices=opciones_estado)
 

class categoriaForm(forms.Form):
    nombre = forms.CharField(max_length = 100, 
                    required = True, 
                    label = "Nombre", 
                    widget = forms.TextInput(attrs={'style': 'width:100%'}))

# Form para editar categorias, hereda de categoriaForm
class categoria_editarForm(categoriaForm):
    opciones_estado = (('0', 'Inactivo',), ('1', 'Activo'))
    estado = forms.ChoiceField(required = True,
                    widget=forms.RadioSelect(attrs={'style': 'width:100%; background-color:white'}), 
                    label = "Estado",
                    choices=opciones_estado)

class solicitudForm(forms.Form):
    opciones_dpto = (('0', 'Dpto 1'),
                     ('1', 'Dpto 2'),
                     ('2', 'Dpto 3'))
    dpto = forms.ChoiceField(required = True,
                             widget=forms.Select(attrs={'style':'width:100%; background-color:white'}),
                             label= "Departamento",
                             choices = opciones_dpto)

    item = forms.ModelChoiceField(label = "Item",
                                  widget=forms.Select(attrs={'style':'width:100%; background-color:white'}), 
                                  queryset = Item.objects.order_by('nombre'))

    cantidad = forms.IntegerField(max_value = 2147483647, 
                                  min_value = 0, 
                                  required = True, 
                                  label = "Cantidad", 
                                  widget=forms.NumberInput(attrs={'style': 'width:100%'}))