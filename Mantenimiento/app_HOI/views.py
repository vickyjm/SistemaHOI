# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from app_HOI.forms import * 
from app_HOI.models import *

def basecol1(request):
	return render(request, 'base-col1.html')
	
def basecol21(request):
	return render(request, 'base-col21.html')

def basecol22(request):
	return render(request, 'base-col22.html')

def basecol3(request):
	return render(request, 'base-col3.html')

def verperfil(request):
	return render(request, 'verperfil.html')

# Vista usada al iniciar el sistema
def inicio_sesion(request):
    if request.method == 'POST':
        form = iniciarSesionForm(request.POST)
        if form.is_valid():
            # Verifico si el usuario existe, esté activo o no
            user = authenticate(username = form.cleaned_data['cedula'],password = form.cleaned_data['contraseña'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('verperfil')
                else:
                    msg = "Su usuario se encuentra inactivo. Contacte al administrador"
                    return render(request,'inicio_sesion.html',{'form': form, 'msg': msg})
            else:
                msg = "Usuario o contraseña incorrecta"
                return render(request,'inicio_sesion.html',{'form': form, 'msg': msg})
    else:
        form = iniciarSesionForm()
    return render(request, 'inicio_sesion.html', {'form': form})

def registro(request):
    if request.method == "POST":
        form = registroForm(request.POST)
    else:
        form = registroForm()
    return render(request,'registro.html', {'form': form})

def crearItem(request):
    if request.method == "POST":
        form = itemForm(request.POST)
        if form.is_valid():
            inombre = form.cleaned_data['nombre']
            icategoria = form.cleaned_data['categoria']
            idcat = Categoria.objects.get(nombre = icategoria)
            print (idcat.id)
            print (icategoria)
            try: 
                item = Item.objects.get(nombre = inombre)
                #item = Item.objects.get(id_categoria = idcat)
                if item.filter(id_categoria = idcat.id).exists():
                #if item.nombre.filter(nombre='inombre').exists():
                    print ("Ya existe")
                #except: 
                else:
                    obj = Item(nombre = inombre,
                                cantidad = form.cleaned_data['cantidad'],
                                id_categoria = idcat,
                                prioridad = form.cleaned_data['prioridad'],
                                minimo = form.cleaned_data['minimo']
                                )
                    obj.save()
                    print("Crea item")
            except:
                print ("No hay items")
                obj = Item(nombre = inombre,
                                cantidad = form.cleaned_data['cantidad'],
                                id_categoria = idcat,
                                prioridad = 1,
                                minimo = form.cleaned_data['minimo']
                                )
                obj.save()
    else:
        form = itemForm(initial={'cantidad': '0', 'minimo': '5'})
    return render(request,'crearItem.html', {'form': form})

def categoria(request):
    if request.method == "POST":
        form = categoriaForm(request.POST)
    
        if form.is_valid():
            catnombre = form.cleaned_data['nombre']
            try: 
                cat = Categoria.objects.get(nombre = catnombre)
                # Verifica si el nombre de la categoria ya existe
                if Categoria.objects.filter(pk=cat.pk).exists():
                    mensaje = "Categoría '%s' ya existe" % (catnombre)
            # Si no existe, crea el objeto y lo guarda
            except ObjectDoesNotExist:
                obj = Categoria(nombre = catnombre)
                obj.save()
                mensaje = "Categoría '%s' creada existosamente" % (catnombre)
            categorias = Categoria.objects.order_by('nombre')
    else:
        form = categoriaForm()
        mensaje = None    
        categorias = Categoria.objects.order_by('nombre')
    return render(request,'categoria.html', {'form': form, 'categorias': categorias, 'mensaje': mensaje})

def inventario(request):
    items = Item.objects.order_by('nombre')
    if request.method == "POST":
        pass  
    else:
        pass
    return render(request,'inventario.html', {'items': items})