# -*- coding: utf-8 -*-

from django import forms
from django.core.validators import RegexValidator
from app_HOI.models import Categoria,Item, Departamento
from django.forms import ModelChoiceField
from django.utils.translation import ugettext, ugettext_lazy as _
from django.forms.extras.widgets import SelectDateWidget
from functools import partial
import datetime


class iniciarSesionForm(forms.Form):
    cedula = forms.CharField(
                    max_length = 11,
                    required = True,
                    label = "Cédula de Identidad",
                    widget=forms.TextInput(attrs={'style': 'width:100%'}),
                    validators = [
                        RegexValidator(
                            regex = '^([1-9][0-9]{0,2})([0-9]{3}){0,3}$',
                            message = 'Formato erróneo.'
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
                            message = 'Formato erróneo.'
                        )
                    ]
            )
    nombre = forms.CharField(max_length = 30, 
                    required = True, 
                    label = "Nombre", 
                    widget=forms.TextInput(attrs={'style': 'width:100%'}),
                    validators = [
                          RegexValidator(
                                regex = '^[a-zA-ZáéíóúñÑÁÉÍÓÚ][a-zA-ZáéíóúñÑÁÉÍÓÚ ]+$',
                                message = 'Sólo debe contener letras.'
                        )])
    apellido = forms.CharField(max_length = 30, 
                    required = True, 
                    label = "Apellido", 
                    widget=forms.TextInput(attrs={'style': 'width:100%'}),
                    validators = [
                          RegexValidator(
                                regex = '^[a-zA-ZáéíóúñÑÁÉÍÓÚ][a-zA-ZáéíóúñÑÁÉÍÓÚ ]+$',
                                message = 'Sólo debe contener letras.'
                        )
                    ])
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
                            message = 'Formato erróneo.'
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

class cambiarContraseñaForm(forms.Form):
    contraseñaActual = forms.CharField(
                     max_length = 25,
                     required = True,
                     label = "Contraseña actual", 
                     widget=forms.PasswordInput(attrs={'style': 'width:100%'}))
    contraseña1 = forms.CharField(max_length = 25,
                     required = True,
                     label = "Contraseña nueva", 
                     widget=forms.PasswordInput(attrs={'style': 'width:100%'}))
    contraseña2 = forms.CharField(max_length = 25,
                     required = True,
                     label = "Confirmar contraseña", 
                     widget=forms.PasswordInput(attrs={'style': 'width:100%'}))

class perfilForm(forms.Form):
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

class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "My Object #%i" % obj.nombre

class itemForm(forms.Form):
    nombre = forms.CharField(max_length = 100, 
                    required = True, 
                    label = "Nombre", 
                    widget = forms.TextInput(attrs={'style': 'width:100%'}),
                    validators = [
                                RegexValidator(
                                    regex = '^[^ ].*$',
                                    message = 'Formato erróneo.'
                                )])
    cantidad = forms.IntegerField(max_value = 2147483647, 
                    min_value = 0, 
                    required = True, 
                    label = "Cantidad", 
                    widget=forms.NumberInput(attrs={'style': 'width:100%'}))
    categoria = forms.ModelChoiceField(label = "Categoría",
        widget=forms.Select(attrs={'style':'width:100%; background-color:white'}), 
        queryset=Categoria.objects.filter(estado=1).order_by('nombre'))
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
 
 # Cantidad de items a ingresar o retirar
class item_cantidadForm(forms.Form):
    cantidad = forms.IntegerField(max_value = 2147483647, 
                    min_value = 0, 
                    required = True, 
                    label = "Cantidad", 
                    widget=forms.NumberInput(attrs={'style': 'width:100%'}))

class categoriaForm(forms.Form):
    nombre = forms.CharField(max_length = 100, 
                    required = True, 
                    label = "Nombre", 
                    widget = forms.TextInput(attrs={'style': 'width:100%'}),
                    validators = [
                                RegexValidator(
                                    regex = '^[^ ].*$',
                                    message = 'Formato erróneo.'
                                )])

# Form para editar categorias, hereda de categoriaForm
class categoria_editarForm(categoriaForm):
    opciones_estado = (('0', 'Inactivo',), ('1', 'Activo'))
    estado = forms.ChoiceField(required = True,
                    widget=forms.RadioSelect(attrs={'style': 'width:100%; background-color:white'}), 
                    label = "Estado",
                    choices=opciones_estado)

#class categoria_estadoForm(categoria_editarForm):

class solicitudForm(forms.Form):
    # categoria = forms.ModelChoiceField(
    #                 label = "Categoría",
    #                 widget = forms.Select(attrs={'style':'width:100%; background-color:white'}), 
    #                 queryset = Categoria.objects.order_by('nombre'))

    # item = forms.ModelChoiceField(
    #                 label = "Item",
    #                 widget = forms.Select(attrs={'style':'width:100%; background-color:white'}), 
    #                 queryset = Item.objects.order_by('nombre'))

    cantidad = forms.IntegerField(
                    max_value = 2147483647, 
                    min_value = 0, 
                    required = True, 
                    label = "Cantidad",
                    widget=forms.NumberInput(attrs={'style': 'width:100%'}))
    
    opciones_dpto = (('0', 'Dpto 1'),       # No estoy segura de qué va aqui
                 ('1', 'Dpto 2'),
                 ('2', 'Dpto 3'))
    dpto = forms.ModelChoiceField(label = "Departamento que lo solicita",
        widget=forms.Select(attrs={'style':'width:100%; background-color:white'}), 
        queryset=Departamento.objects.filter(estado=1).order_by('nombre'),
        required = True)

class reportesForm(forms.Form):
    DateInput = partial(forms.DateInput, {'class': 'datepicker','style':'width:100%'})
    fechaInicio = forms.DateField(
                        label = "Fecha inicial",
                        required = True,
                        widget = DateInput(),
                        input_formats = ['%d/%m/%Y'])
    
    fechaFin = forms.DateField(
                       label = "Fecha final",
                       required = True,
                       widget = DateInput(),
                       input_formats = ['%d/%m/%Y'])
    
class editarUsuarioForm(forms.Form):
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
                    widget=forms.TextInput(attrs={'style': 'width:100%'}),
                    validators = [
                          RegexValidator(
                                regex = '^[a-zA-ZáéíóúñÑÁÉÍÓÚ][a-zA-ZáéíóúñÑÁÉÍÓÚ ]+$',
                                message = 'Sólo debe contener letras.'
                        )])
    apellido = forms.CharField(max_length = 30, 
                    required = True, 
                    label = "Apellido", 
                    widget=forms.TextInput(attrs={'style': 'width:100%'}),
                    validators = [
                          RegexValidator(
                                regex = '^[a-zA-ZáéíóúñÑÁÉÍÓÚ][a-zA-ZáéíóúñÑÁÉÍÓÚ ]+$',
                                message = 'Sólo debe contener letras.'
                        )])
    correo = forms.EmailField(required = False, 
                    label = "Correo electrónico", 
                    widget=forms.EmailInput(attrs={'style': 'width:100%'}))
    tipoEmpleado = (("tecnico","Técnico"), ("almacenista", "Almacenista"),("administrador","Administrador"))
    tipo = forms.ChoiceField(required = True, 
                    choices = tipoEmpleado, 
                    widget = forms.Select(attrs={'style': 'width:100%; background-color:white'}), 
                    label = "Cargo")
    opciones_estado = (('0', 'Inactivo',), ('1', 'Activo'))
    estado = forms.ChoiceField(required = True,
                    widget=forms.RadioSelect(attrs={'style': 'width:100%; background-color:white'}), 
                    label = "Estado",
                    choices=opciones_estado)

class registroAdminForm(registroForm):
    correo = forms.EmailField(required = True, 
                    label = "Correo electrónico", 
                    widget=forms.EmailInput(attrs={'style': 'width:100%'}))
    tipoEmpleado = (("tecnico","Técnico"), ("almacenista", "Almacenista"),("administrador","Administrador"))
    tipo = forms.ChoiceField(required = True, 
                    choices = tipoEmpleado, 
                    widget = forms.Select(attrs={'style': 'width:100%; background-color:white'}), 
                    label = "Cargo")
    opciones_estado = (('0', 'Inactivo',), ('1', 'Activo'))
    estado = forms.ChoiceField(required = True,
                    widget=forms.RadioSelect(attrs={'style': 'width:100%; background-color:white'}), 
                    label = "Estado",
                    choices=opciones_estado)
    
class departamentoForm(forms.Form):
    nombre = forms.CharField(max_length = 500, 
                    required = True, 
                    label = "Nombre", 
                    widget = forms.TextInput(attrs={'style': 'width:100%'}),
                    validators = [
                                RegexValidator(
                                    regex = '^[^ ].*$',
                                    message = 'Formato erróneo.'
                                )])

class editarDptoForm(departamentoForm):
    opciones_estado = (('0', 'Inactivo',), ('1', 'Activo'))
    estado = forms.ChoiceField(required = True,
                    widget=forms.RadioSelect(attrs={'style': 'width:100%; background-color:white'}), 
                    label = "Estado",
                    choices=opciones_estado)