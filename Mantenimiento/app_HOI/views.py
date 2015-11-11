# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from app_HOI.forms import * 
from app_HOI.models import *
from django.contrib.auth.decorators import login_required 
from app_HOI.generarPdf import *
from io import BytesIO
import datetime
from django.http.response import HttpResponse
from django.shortcuts import render_to_response #For error handling
from django.template import RequestContext      #For error handling
from django.core.exceptions import PermissionDenied # Forbiddden

red = "color:#CC0000"
black = "color:#000000"
green = "color:#009900"

def page_not_found(request):
    response = render_to_response('404.html',
                                    context_instance=RequestContext(request)
    )
    response.status_code = 404
    return response

def permission_denied(request):
    response = render_to_response('403.html',
                                    context_instance=RequestContext(request)
    )
    response.status_code = 403
    return response

@login_required
def verperfil(request):
    grupo = request.user.groups.values('name')
    if (not grupo) and request.user.is_superuser:
        request.user.groups.add(Group.objects.get(name='Administradores'))
        request.user.groups.add(Group.objects.get(name='Almacenistas'))
        request.user.groups.add(Group.objects.get(name='Técnicos'))

    crear = Crea.objects.filter(id_usuario = request.user).order_by('-fecha')
    crear_todos = Crea.objects.all()
    aprobar = Aprueba.objects.filter(id_usuario = request.user).order_by('-fecha')
    ingresar = Ingresa.objects.filter(id_usuario = request.user).order_by('-fecha')
    latest =  list(crear) + list(aprobar) + list(ingresar)
    latest_sorted = sorted(latest, key=lambda x: x.fecha, reverse=True)

    return render(request, 'verperfil.html',{'user': request.user,
                                             'crear':crear,
                                             'crear_todos': crear_todos,
                                             'latest': latest_sorted})

@login_required
def perfil_editar(request, _id):

    mensaje = None
    if request.method == "POST":
        form = perfilForm(request.POST)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['nombre']
            request.user.last_name = form.cleaned_data['apellido']
            request.user.email = form.cleaned_data['correo']
            request.user.save()
            mensaje = "Perfil editado exitosamente."
            #return HttpResponseRedirect('/verperfil')
            if "Guardar" in request.POST:
                aprobar = Aprueba.objects.filter(id_usuario = request.user)
                crear = Crea.objects.all()
                return render(request,'verperfil.html', {'user': request.user, 
                                                    'aprobar': aprobar,
                                                    'mensaje': mensaje, 
                                                    'crear': crear})
    else:

        form = perfilForm(initial = {'nombre':request.user.first_name,
                                     'apellido':request.user.last_name,
                                     'correo':request.user.email})

    return render(request, 'perfil_editar.html', {'form': form,
                                                  'mensaje' : mensaje,
                                                  'user': request.user})

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
                    msg = "Su usuario se encuentra inactivo. Contacte al administrador."
                    return render(request,'inicio_sesion.html',{'form': form, 'msg': msg})
            else:
                msg = "Usuario o contraseña incorrecta."
                return render(request,'inicio_sesion.html',{'form': form, 'msg': msg})
    else:
        form = iniciarSesionForm()
    return render(request, 'inicio_sesion.html', {'form': form})

def registro(request):
    if request.method == "POST":
        if (request.user.groups.filter(name = "Administradores").exists()):
            form = registroAdminForm(request.POST)
        else:
            form = registroForm(request.POST)

        if form.is_valid():
            ci = form.cleaned_data['cedula']
            if User.objects.filter(username=ci).exists():
                msg = "Esta cédula ya se encuentra registrada."
                color = red
                return render(request,'registro.html',{'form' : form, 
                                                       'msg' : msg,
                                                       'color': color})

            if (form.cleaned_data['contraseña1']!= form.cleaned_data['contraseña2']):
                msg = "Las contraseñas no coinciden. Intente de nuevo."
                color = red
                return render(request,'registro.html',{'form' : form, 
                                                       'msg' : msg,
                                                       'color': color})

            user = User.objects.create_user(username=ci,
                                 password=form.cleaned_data['contraseña1'])
            user.first_name = form.cleaned_data['nombre']
            user.last_name = form.cleaned_data['apellido']
            if (form.cleaned_data['correo']!=""):
                user.email = form.cleaned_data['correo']

            if (form.cleaned_data['tipo'] == "tecnico"):
                user.groups.add(Group.objects.get(name='Técnicos'))
            else:
                user.groups.add(Group.objects.get(name='Almacenistas'))
                user.groups.add(Group.objects.get(name='Técnicos'))
                            
            print(user.groups.values('name'))
            print(user.groups.values_list('name',flat=True))
            if (request.user.groups.filter(name = "Administradores").exists()):
                user.is_active = int(form.cleaned_data['estado'])
            else:
                user.is_active = True
            user.save()
            msg = "El usuario fue registrado exitosamente."
            color = green
            form = registroForm()

            if "Guardar" in request.POST and (request.user.groups.filter(name = "Administradores").exists()):
                usuarios = User.objects.order_by('first_name')        
                return render(request,'adminUsuarios.html', {'usuarios': usuarios, 'mensaje': msg})
            else:
                return render(request,'registro.html',{'form': form, 
                                                   'msg': msg,
                                                   'color':color})
    else:
        if (request.user.groups.filter(name = "Administradores").exists()):
            form = registroAdminForm(initial = {'estado':'1'})
        else:
            form = registroForm()
    return render(request,'registro.html', {'form': form})
   
@login_required
def cambiarContraseña(request):
    if request.method == "POST":
        form = cambiarContraseñaForm(request.POST)
        if form.is_valid():
            actual = form.cleaned_data['contraseñaActual']
            
            if request.user.check_password(actual):
                if (form.cleaned_data['contraseña1']!= form.cleaned_data['contraseña2']):
                    mensaje = "Las nuevas contraseñas no coinciden. Intente de nuevo."
                    return render(request,'contrasenia_cambiar.html',{'form' : form, 'mensaje' : mensaje})

                request.user.set_password(form.cleaned_data['contraseña1'])
                request.user.save()
                mensaje = "Contraseña cambiada exitosamente."
                if "Guardar" in request.POST:
                    aprobar = Aprueba.objects.filter(id_usuario = request.user)
                    crear = Crea.objects.all()
                    return render(request,'verperfil.html', {'user': request.user, 
                                                             'aprobar': aprobar,
                                                             'mensaje': mensaje, 
                                                             'crear': crear})
            else:
                mensaje = "La contraseña actual no coincide."
                return render(request,'contrasenia_cambiar.html',{'form' : form, 'mensaje' : mensaje})
    else:
        form = cambiarContraseñaForm()
    return render(request,'contrasenia_cambiar.html',{'form': form})

def recuperarContraseña(request):
    if request.method == "POST":
        form = recuperarContraseñaForm(request.POST)
        if form.is_valid():
            ci = form.cleaned_data['cedula']
            if User.objects.filter(username=ci).exists():
                if (form.cleaned_data['contraseña1']!= form.cleaned_data['contraseña2']):
                    msg = "Las contraseñas no coinciden. Intente de nuevo."
                    return render(request,'recuperarContrasenia.html',{'form' : form, 'msg' : msg})
                user = User.objects.get(username=ci)
                user.set_password(form.cleaned_data['contraseña1'])
                user.save()
                msg = "Su contraseña fue cambiada."
                return render(request,'recuperarContrasenia.html',{'form' : form, 'msg' : msg})  
            else:
                msg = "La cédula ingresada no se encuentra registrada."
                return render(request,'recuperarContrasenia.html',{'form' : form, 'msg' : msg})
    else:
        form = recuperarContraseñaForm()
    return render(request,'recuperarContrasenia.html',{'form': form})

def cerrarSesion(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def crearItem(request):
    if not request.user.groups.filter(name = "Administradores").exists():
        raise PermissionDenied
    
    color = black
    mensaje = None
    
    if request.method == "POST":
        form = itemForm(request.POST)

        if form.is_valid():
            inombre = form.cleaned_data['nombre']
            inombre = inombre.upper()
            icategoria = form.cleaned_data['categoria']
            icategoria = icategoria.nombre.upper()
            idcat = Categoria.objects.get(nombre = icategoria)
            # Verifica si ya existe un item con el mismo nombre y categoria
            itemexiste = Item.objects.filter(nombre = inombre, 
                                            id_categoria = idcat.id).exists()
            # Si el item ya existe
            if itemexiste:
                mensaje = "Ítem '%s' ya existe en la categoría '%s'." % (inombre,icategoria)
                color = red
            # Si el item no existe, lo crea
            else:
                obj = Item(nombre = inombre,
                            cantidad = form.cleaned_data['cantidad'],
                            id_categoria = idcat,
                            minimo = form.cleaned_data['minimo']
                            )
                obj.save()
                mensaje = "Ítem '%s' creado exitosamente." % (inombre)
                color = green 

                if "Guardar" in request.POST:
                    items = Item.objects.order_by('nombre')
                    return render(request,'inventario.html', {'items': items, 'mensaje': mensaje})
                else:
                    form = itemForm(initial={'cantidad': '0', 'minimo': '5'})   
    else:
        form = itemForm(initial={'cantidad': '0', 'minimo': '5'})

    return render(request,'crearItem.html', {'form': form, 
                                             'mensaje': mensaje,
                                             'color' : color})

# Vista utilizada para editar un item en el sistema
def item_editar(request, _id):
    if not request.user.groups.filter(name = "Administradores").exists():
        raise PermissionDenied

    # Obtiene el objeto de item a editar
    color = black
    item = Item.objects.get(id = _id)
    nombre = item.nombre
    mensaje = None

    if request.method == "POST":
        form = item_editarForm(request.POST)

        if form.is_valid():
            # Obtiene los datos del formulario
            inombre = form.cleaned_data['nombre']
            inombre = inombre.upper()
            icategoria = form.cleaned_data['categoria']
            icategoria = icategoria.nombre.upper()
            idcat = Categoria.objects.get(nombre = icategoria)

            try:
                itemexiste = Item.objects.get(nombre = inombre, 
                                              id_categoria = idcat.id)
                if int(itemexiste.id) == int(_id): 
                    iestado = form.cleaned_data['estado']
                    
                    if int(itemexiste.estado) != int(iestado):
                        # Si cambia a activo
                        if int(iestado) == 1:
                            # Si cambia a una categoria activa
                            if int(idcat.estado) == 1 :
                                pass
                            elif int(idcat.estado) == 0:

                                mensaje = "La categoría '%s' se encuentra inactiva por lo que no\
                                           se puede cambiar el estado del ítem '%s' a activo." %(icategoria,nombre)
                                color = red
                                return render(request, 'item_editar.html', {'form' : form, 
                                                                            'item' : item,
                                                                            'nombre' : nombre,
                                                                            'mensaje': mensaje,
                                                                            'color': color})
                        # Si cambia a inactivo
                        elif int(iestado) == 0:
                            pass

                    item.cantidad = form.cleaned_data['cantidad']
                    item.minimo = form.cleaned_data['minimo']
                    item.estado = iestado
                    item.save()
                    mensaje = "Ítem '%s' editado exitosamente." % nombre
                    color = green
                    
                    if "Guardar" in request.POST:
                        items = Item.objects.order_by('nombre')
                        return render(request,'inventario.html', {'items': items, 'mensaje': mensaje})
                else:
                    mensaje = "Ítem '%s' ya existe en la categoría '%s'." %(inombre, idcat)
                    color = red
                    
            except ObjectDoesNotExist:


                iestado = form.cleaned_data['estado']
                
                #if int(item.estado) != int(iestado):
                # Si cambia a una categoria activa
                if int(idcat.estado) == 1 :
                        pass
                # Si se cambia a una categoria inactiva
                elif int(idcat.estado) == 0:
                    # Si cambia a activo
                    if int(iestado) == 1:
                        mensaje = "La categoría '%s' está inactiva, al cambiar el ítem '%s'\
                                   a esta categoría, también será desactivado.\n \
                                   ¿Está seguro de que desea editar el ítem '%s'?" %(icategoria,nombre,nombre)
                        print (mensaje)
                        cantidad = form.cleaned_data['cantidad']
                        minimo = form.cleaned_data['minimo']
                        form = item_editarForm(request.POST)

                        return render (request, 'item_estado.html', {'mensaje': mensaje,
                                                                'form': form,
                                                                'item': item,
                                                                'nombre': inombre,
                                                                'cantidad': cantidad,
                                                                'categoria':idcat,
                                                                'minimo': minimo})
                    # Si cambia a inactivo
                    elif int(iestado) == 0:
                        pass

                item.nombre = inombre
                item.cantidad = form.cleaned_data['cantidad']
                item.id_categoria = idcat
                item.minimo = form.cleaned_data['minimo']
                item.estado = iestado
                item.save()
                mensaje = "Ítem '%s' editado exitosamente." %nombre
                color = green
                nombre = inombre

                if "Guardar" in request.POST:
                    items = Item.objects.order_by('nombre')
                    return render(request,'inventario.html', {'items': items, 'mensaje': mensaje})
    else: 
        # Formulario con los datos del item a editar
        form = item_editarForm(initial = {'nombre': item.nombre, 
                                        'cantidad': item.cantidad,
                                        'categoria': item.id_categoria,
                                        'minimo': item.minimo,
                                        'estado': item.estado})

    return render(request, 'item_editar.html', {'form' : form, 
                                                'item' : item,
                                                'nombre' : nombre,
                                                'mensaje': mensaje,
                                                'color': color})

def item_estado(request, _id):
    if not request.user.groups.filter(name = "Administradores").exists():
        raise PermissionDenied
    mensaje = None
    item = Item.objects.get(id = _id)

    if request.method == "POST":
        form = item_editarForm(request.POST)
        if form.is_valid():

            inombre = form.cleaned_data['nombre']
            inombre = inombre.upper()
            icategoria = form.cleaned_data['categoria']
            icategoria = icategoria.nombre.upper()
            idcat = Categoria.objects.get(nombre = icategoria)
            item.nombre = inombre
            item.cantidad = form.cleaned_data['cantidad']
            item.id_categoria = idcat
            item.minimo = form.cleaned_data['minimo']
            item.estado = 0
            item.save()
            mensaje = "Ítem '%s' editado exitosamente." %inombre
            color = green

            items = Item.objects.order_by('nombre')
            return render (request, 'inventario.html', {'items': items})

    else:
        pass

    return render(request, 'item_estado.html',{'mensaje':mensaje,
                                               'item': item})


@login_required
def categoria(request):

    color = black
    mensaje = None

    if request.method == "POST":
        form = categoriaForm(request.POST)

        if form.is_valid():
            catnombre = form.cleaned_data['nombre']
            catnombre = catnombre.upper()
        
            try: 
                cat = Categoria.objects.get(nombre = catnombre)
                # Verifica si el nombre de la categoria ya existe
                if Categoria.objects.filter(pk=cat.pk).exists():
                    mensaje = "La categoría '%s' ya existe." % (catnombre)
                    color = red
            # Si no existe, crea el objeto y lo guarda
            except ObjectDoesNotExist:
                obj = Categoria(nombre = catnombre,
                                estado = 1)
                obj.save()
                mensaje = "Categoría '%s' creada exitosamente." % (catnombre)
                color = green
                form = categoriaForm()
        categorias = Categoria.objects.order_by('nombre')

    else:
        form = categoriaForm()
        categorias = Categoria.objects.order_by('nombre')

    return render(request,'categoria.html', {'form': form, 
                                             'categorias': categorias, 
                                             'mensaje': mensaje,
                                             'color': color})

# Vista creada para editar una categoria en el sistema
def categoria_editar(request, _id):
    if not request.user.groups.filter(name = "Administradores").exists():
        raise PermissionDenied

    color = black
    categoria = Categoria.objects.get(id = _id)
    nombre = categoria.nombre
    mensaje = None
    items = Item.objects.filter(id_categoria = _id)
    cantidad = items.count()

    if request.method == "POST":
        
        form = categoria_editarForm(request.POST)
        
        if form.is_valid():
            #Obtiene datos del formulario
            cnombre = form.cleaned_data['nombre']
            cnombre = cnombre.upper()
            cestado = form.cleaned_data['estado']

            try:
                # Obtiene la categoria con el nombre del formulario
                cat = Categoria.objects.get(nombre = cnombre)
                # Si la categoria es la misma a editar
                if int(cat.pk) == int(_id):
                    pass  
                 # Si la categoria no es la misma a editar
                else:
                    mensaje = "La categoría '%s' ya existe." % cnombre
                    color = red
            # Si no existe una categoria con el nombre introducido
            except:
                pass

            # si la categoria tiene items
            if cantidad != 0:
                # si hubo cambio de estado
                if int(categoria.estado) != int(cestado):
                    # si se activo
                    if int(cestado) == 1:
                        accion = "Activar"
                        mensaje = "Al activar la categoría '%s' también se \
                                   activarán todos los ítems (%i) que le pertenecen.\
                                   ¿Está seguro de que desea activar la categoría %s?" \
                                   % (categoria.nombre,cantidad,categoria.nombre)
                    # si se desactivo
                    elif int(cestado) == 0:
                        accion = "Desactivar"
                        mensaje = "Al desactivar la categoría '%s' también se \
                                   desactivarán todos los ítems (%i) que le pertenecen.\
                                   ¿Está seguro de que desea desactivar la categoría %s?" \
                                   % (categoria.nombre,cantidad,categoria.nombre)

                    form = categoria_editarForm(request.POST)
                    return render (request, 'categoria_estado.html', {'form': form,
                                                                      'accion': accion,
                                                                      'mensaje': mensaje,
                                                                      'categoria': categoria,
                                                                      'nombre': cnombre,
                                                                      'estado': int(cestado)})

            categoria.nombre = cnombre
            categoria.estado = cestado
            categoria.save()
            mensaje = "Categoría '%s' editada exitosamente." % nombre
            color = green

            if "Guardar" in request.POST:
                form = categoriaForm
                categorias = Categoria.objects.order_by('nombre')
                return render(request,'categoria.html', {'form': form, 
                                         'categorias': categorias, 
                                         'mensaje': None,
                                         'mensaje2': mensaje,
                                         'color': color})

    else:
        # Formulario con los datos a editar
        form = categoria_editarForm(initial={'nombre': categoria.nombre,
                                             'cantidad': cantidad, 
                                             'estado': categoria.estado})
        mensaje = None
    return render(request,'categoria_editar.html', {'categoria': categoria, 
                                                    'form': form,
                                                    'mensaje': mensaje,
                                                    'cantidad': cantidad,
                                                    'color':color})


def categoria_estado(request, _id):
    if not request.user.groups.filter(name = "Administradores").exists():
        raise PermissionDenied      
    mensaje = None
    categoria = Categoria.objects.get(id = _id)

    if request.method == "POST":
        
        form = categoria_editarForm(request.POST)
        if form.is_valid():
            cnombre = form.cleaned_data['nombre']
            cnombre = cnombre.upper()
            cestado = form.cleaned_data['estado']

            categoria.nombre = cnombre
            categoria.estado = cestado
            categoria.save()
            mensaje = "Categoría '%s'editada exitosamente." % cnombre
            color = green

            items = Item.objects.filter(id_categoria = _id)
            for i in items:
                i.estado = cestado
                i.save()

            if "Guardar" in request.POST:
                form = categoriaForm
                categorias = Categoria.objects.order_by('nombre')
                return render(request,'categoria.html', {'form': form, 
                                      'categorias': categorias, 
                                      'mensaje': None,
                                      'mensaje2': mensaje,
                                      'color': color})
    else:
        pass
    return render(request,'categoria_estado.html', {'mensaje': mensaje, 'categoria': categoria})
           
# Vista utilizada para mostrar los items del inventario
@login_required
def inventario(request):
    items = Item.objects.order_by('nombre')
    mensaje = None
    if request.method == "POST":
        pass  
    else:
        pass
    return render(request,'inventario.html', {'items': items, 'mensaje':mensaje})

def item_ingresar(request, _id):
    if not request.user.groups.filter(name = "Almacenistas").exists():
        raise PermissionDenied
    item = Item.objects.get(pk = _id)
    
    if request.method == "POST":
        form = item_cantidadForm(request.POST)
        
        if form.is_valid():
            fecha = datetime.datetime.now()
            icantidad = form.cleaned_data['cantidad']            
            item.cantidad = item.cantidad + icantidad
            item.save()
            
            obj = Ingresa(id_usuario = request.user,
                          id_item = item,
                          fecha = fecha,
                          cantidad = icantidad)
            obj.save()
            
            mensaje = "Cantidad ingresada exitosamente."
            color = green
    else:
        mensaje = None
        color = black
        form = item_cantidadForm(initial={'cantidad': '1'})

    return render(request,'item_ingresar.html', {'form': form, 
                                                 'item': item,
                                                 'mensaje': mensaje,
                                                 'color': color})

@login_required
def solicitud(request):
    solic_creadas = Crea.objects.order_by('-fecha')

    # Si es un técnico, solo puede ver sus solicitudes
    if not request.user.groups.filter(name = "Almacenistas").exists():
        solicitudes = solic_creadas.filter(id_usuario = request.user)
    # Si es almacenista o administrador, solo ve las solicitudes de los técnicos
    else:
    #    solicitudes = solic_creadas.exclude(id_usuario = request.user)
        solicitudes = solic_creadas.all()
    if request.method == "POST":
        pass  
    else:
        pass
    return render(request,'solicitud.html', {'user' : request.user,
                                             'solicitudes': solicitudes})

# Actualiza el estado de las solicitudes de un técnico
def solicitud_estado(request, _id, _nuevo_estado):
    if not request.user.groups.filter(name = "Almacenistas").exists():
        raise PermissionDenied    
    solic_creadas = Crea.objects.order_by('-fecha')

    # Si es un técnico, solo puede ver sus solicitudes
    if not request.user.groups.filter(name = "Almacenistas").exists():
        solicitudes = solic_creadas.filter(id_usuario = request.user)
    # Si es almacenista o administrador, solo ve las solicitudes de los técnicos
    else:
        solicitudes = solic_creadas.exclude(id_usuario = request.user)

    if request.method == "GET":
        obj = Crea.objects.get(pk=_id)
        solicitud = Solicitud.objects.get(pk = obj.id_solicitud.pk)        
        solicitud.estado = _nuevo_estado
        solicitud.save()
        
        for s in solic_creadas: 
            if s.id_solicitud == solicitud:
                item = Item.objects.get(pk = s.id_item.pk)

        if _nuevo_estado == "A":
            aprobado = Aprueba(id_usuario = request.user,
                               id_solicitud = solicitud,
                               fecha = datetime.datetime.now())
            aprobado.save()

            # Si la solicitud se aprobó, se reduce la cantidad de ese item del inventario    
            item.cantidad = item.cantidad - solicitud.cantidad
            item.save()
        
        else:
            # Si la solicitud se rechazó, se suma al inventario la cantidad que se había reservado
            item.cantidad = item.cantidad + solicitud.cantidad
            item.save()
    else:
        pass
    return render(request,'solicitud_estado.html', {'solicitudes':solicitudes})

@login_required
def crearSolicitud(request):
    categorias = Categoria.objects.values_list('nombre', flat = True)
    items = Item.objects.order_by('nombre') 
    falta_item = None
    falta_categoria = None
    color = red   # Color rojo para los errores

    if request.method == "POST":
        mensaje = None
        form = solicitudForm(request.POST)

        if form.is_valid():

            fecha = datetime.datetime.now()
            scategoria = request.POST.get("role")
            sitem = request.POST.get(scategoria)
            scantidad = form.cleaned_data['cantidad']
            sdpto = form.cleaned_data['dpto']

            # Si el técnico no seleccionó ninguna categoría
            if scategoria == "":
                form = solicitudForm(initial={'cantidad': scantidad,
                                              'dpto': sdpto})
                falta_categoria = "Este campo es obligatorio."
            
            # Si el técnico no seleccionó ningún ítem
            if sitem == None:
                form = solicitudForm(initial={'cantidad': scantidad,
                                              'dpto': sdpto})
                falta_item = "Este campo es obligatorio."


            if (scategoria != "") and (sitem != ""):
                cat = Categoria.objects.get(nombre = scategoria)
                item = Item.objects.filter(id_categoria = cat).get(nombre = sitem)

                # Si el técnico pide más items de los disponibles
                if scantidad > item.cantidad:
                    if item.cantidad == 0:
                        mensaje = "La solicitud no se puede realizar. No quedan unidades de este ítem."    
                    else:
                        mensaje = "La solicitud no se puede realizar. Solo quedan '%d' unidades de este ítem." % (item.cantidad)
                    color = red

                # Si el técnico pide 0 items
                elif scantidad == 0:
                    mensaje = "La cantidad de ítems a solicitar debe ser mayor a cero."
                    color = red

                # Si no hay errores
                else:
                    if request.user.groups.filter(name = "Almacenistas").exists():
                        sestado = "A"
                    else:
                        sestado = "E"

                    nueva_solicitud = Solicitud(fecha = fecha,
                                                dpto = sdpto,
                                                cantidad = scantidad,
                                                estado = sestado)
                    nueva_solicitud.save()

                    obj = Crea(id_usuario = request.user,
                               id_item = item,
                               id_solicitud = nueva_solicitud,
                               fecha = fecha)
                    obj.save()

                    if request.user.groups.filter(name = "Almacenistas").exists():
                        aprobar = Aprueba(id_usuario = request.user,
                                          id_solicitud = nueva_solicitud,
                                          fecha = fecha)
                        aprobar.save() 
                    
                    # Se hace una reserva hasta que "A" o "R"
                    item.cantidad = item.cantidad - scantidad
                    item.save()

                    mensaje = "Solicitud creada exitosamente."
                    color = green

                    if "Guardar" in request.POST:
                        solic_creadas = Crea.objects.order_by('-fecha')
                        # Si es un técnico, solo puede ver sus solicitudes
                        if not request.user.groups.filter(name = "Almacenistas").exists():
                            solicitudes = solic_creadas.filter(id_usuario = request.user)
                        # Si es almacenista o administrador, solo ve las solicitudes de los técnicos
                        else:
                            solicitudes = solic_creadas.exclude(id_usuario = request.user)

                        return render(request,'solicitud.html', {'user' : request.user,
                                                         'mensaje': mensaje,
                                                         'solicitudes': solicitudes})

                    form = solicitudForm(initial={'cantidad': '1'})
    else:
        mensaje = None
        form = solicitudForm(initial={'cantidad': '1'})
    
    return render(request,'crearSolicitud.html', {'form': form,
                                                  'mensaje': mensaje,
                                                  'color': color,
                                                  'falta_categoria': falta_categoria,
                                                  'falta_item': falta_item,
                                                  'categorias': categorias,
                                                  'items':items})
@login_required
def solicitud_editar(request, _id):
    obj = Crea.objects.get(pk = _id)
    solicitud = Solicitud.objects.get(pk = obj.id_solicitud.pk)
    item = Item.objects.get(pk = obj.id_item.pk)
    categoria = item.id_categoria.nombre
    color = green

    if request.method == "POST":
        form = solicitudForm(request.POST)

        if form.is_valid():
            scantidad = form.cleaned_data['cantidad']
            sdpto = form.cleaned_data['dpto']
            
            if scantidad > item.cantidad:
                if item.cantidad == 0:

                    mensaje = "La solicitud no se puede modificar. No quedan unidades de este ítem."
                else:
                    mensaje = "La solicitud no se puede editar. Solo quedan '%d' unidades de este ítem." % (item.cantidad)
                    color = red

            elif scantidad == 0:
                mensaje = "La cantidad de ítems a solicitar debe ser mayor a cero."

                color = red

            # Si no hay errores
            else:
                solicitud.cantidad = scantidad
                solicitud.dpto = sdpto
                solicitud.save()

                mensaje = "Solicitud editada exitosamente."

                if "Guardar" in request.POST:
                    solic_creadas = Crea.objects.order_by('-fecha')
                    # Si es un técnico, solo puede ver sus solicitudes
                    if not request.user.groups.filter(name = "Almacenistas").exists():
                        solicitudes = solic_creadas.filter(id_usuario = request.user)
                    # Si es almacenista o administrador, solo ve las solicitudes de los técnicos
                    else:
                        solicitudes = solic_creadas.exclude(id_usuario = request.user)

                    return render(request,'solicitud.html', {'user' : request.user,
                                                             'mensaje': mensaje,
                                                             'solicitudes': solicitudes})

    else:
        mensaje = None
        form = solicitudForm(initial = {'cantidad': solicitud.cantidad,
                                        'dpto': solicitud.dpto})

    return render(request, 'solicitud_editar.html', {'item': item,
                                                     'categoria': categoria,
                                                     'form': form,
                                                     'mensaje': mensaje,
                                                     'color': color})

@login_required
def solicitud_eliminar(request, _id):
    if request.method == "GET":
        return render(request,'solicitud_eliminar.html')
    else:
        obj = Crea.objects.get(pk=_id)

        solicitud = Solicitud.objects.get(pk = obj.id_solicitud.pk)
        solicitud.delete()
    
        obj.delete()
    return HttpResponseRedirect('/solicitud')

def imprimirReporte(request):
    if not request.user.groups.filter(name = "Administradores").exists():
        raise PermissionDenied
    msg = None
    if request.method == 'POST':
        form = reportesForm(request.POST)
        
        if form.is_valid():
            fechaIni = form.cleaned_data['fechaInicio']
            fechaFin = form.cleaned_data['fechaFin']
            
            if (fechaFin < fechaIni):
                msg = "Fechas inválidas. Intente de nuevo."
                
            else:
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="Inventario_'+str(fechaIni)+'_'+str(fechaFin)+'.pdf"'
                buffer = BytesIO()
                report = MiPDF(buffer,'Letter')
                usuario = request.user
                pdf = report.imprimir_reporte(usuario,fechaIni,fechaFin)
                response.write(pdf)
                return response
        
    else:
        form = reportesForm()
    return render(request,'reporte.html',{'form':form,'msg':msg})

def adminUsuarios(request):
    if not request.user.groups.filter(name = "Administradores").exists():
        raise PermissionDenied
    usuarios = User.objects.order_by('first_name')
    if request.method == "POST":
        pass
    else:
        pass
    return render(request,'adminUsuarios.html',{'usuarios':usuarios})

def editarUsuario(request,_id):
    if not request.user.groups.filter(name = "Administradores").exists():
        raise PermissionDenied
    usuario = User.objects.get(id = _id)
    nombre = usuario.first_name + " " + usuario.last_name
    color = black
    msg = None
    if request.method == "POST":
        form = editarUsuarioForm(request.POST)
        if form.is_valid():
            if (usuario.username != form.cleaned_data['cedula']):
                try:
                    ciNueva = User.objects.get(username=form.cleaned_data['cedula'])
                    msg = "La cédula ingresada ya existe. Intente de nuevo."
                    color = red
                    return render(request,'editarUsuario.html',{'form':form,
                                                                'usuario': usuario,
                                                                'nombre':nombre,
                                                                'mensaje':msg,
                                                                'color':color})
                except User.DoesNotExist:
                    usuario.username = form.cleaned_data['cedula']
            usuario.first_name = form.cleaned_data['nombre']
            usuario.last_name = form.cleaned_data['apellido']
            usuario.email = form.cleaned_data['correo']
            if (form.cleaned_data['tipo']=="administrador"):
                usuario.groups = [Group.objects.get(name='Administradores'),
                                  Group.objects.get(name='Almacenistas'),
                                  Group.objects.get(name='Técnicos')]
            elif(form.cleaned_data['tipo']=="almacenista"):
                usuario.groups = [Group.objects.get(name='Almacenistas'),
                                  Group.objects.get(name='Técnicos')]
            else:
                usuario.groups = [Group.objects.get(name='Técnicos')]
        
            usuario.is_active = int(form.cleaned_data['estado'])
            usuario.save()
            color = green
            msg = "El usuario '%s' fue editado exitosamente." % nombre

            if "Guardar" in request.POST:
                usuarios = User.objects.order_by('first_name')        
                return render(request,'adminUsuarios.html', {'usuarios': usuarios, 'mensaje': msg}) 

    else:
        if (usuario.groups.filter(name="Administradores")):
                cargo = "administrador"
        elif(usuario.groups.filter(name="Almacenistas")):
                cargo = "almacenista"
        else: 
            cargo = "tecnico"
        form = editarUsuarioForm(initial = {'cedula':usuario.username,'nombre':usuario.first_name,
                                            'apellido':usuario.last_name,'correo':usuario.email,
                                            'tipo':cargo,'estado':str(int(usuario.is_active))})

    return render(request,'editarUsuario.html',{'form':form,
                                                'usuario': usuario,
                                                'nombre':nombre,
                                                'color':color,
                                                'mensaje':msg})

def adminDptos(request):

    if not request.user.groups.filter(name = "Administradores").exists():
        raise PermissionDenied
    color = black
    msg = None

    if request.method == 'POST':
        form = departamentoForm(request.POST)
        if form.is_valid():
            dptonombre = form.cleaned_data['nombre']
            dptonombre = dptonombre.upper()
        
            try: 
                dpto = Departamento.objects.get(nombre = dptonombre)
                if Departamento.objects.filter(pk=dpto.pk).exists():
                    msg = "El departamento '%s' ya existe." % (dptonombre)
                    color = red
            except ObjectDoesNotExist:
                obj = Departamento(nombre = dptonombre,
                                estado = 1)
                obj.save()
                msg = "Departamento '%s' creado exitosamente." % (dptonombre)
                color = green
                form = departamentoForm()
        dptos = Departamento.objects.order_by('nombre')
    else:
        form = departamentoForm()
        dptos = Departamento.objects.order_by('nombre')

    return render(request,'adminDptos.html',{'dptos':dptos,'form':form,'color':color,'mensaje':msg})

def editarDpto(request,_id):
    if not request.user.groups.filter(name = "Administradores").exists():
        raise PermissionDenied
    dpto = Departamento.objects.get(id = _id)
    nombre = dpto.nombre
    color = black
    msg = None
    if request.method == "POST":
        form = editarDptoForm(request.POST)
        if form.is_valid():
            nombreMayus = form.cleaned_data['nombre'].upper()
            if (dpto.nombre != nombreMayus):
                try:
                    nombreNuevo = Departamento.objects.get(nombre=nombreMayus)
                    msg = "El Departamento ingresado ya existe. Intente de nuevo."
                    color = red
                    return render(request,'editarDpto.html',{'form':form,'mensaje':msg,'color':color,'nombre':nombre})
                except Departamento.DoesNotExist:
                    dpto.nombre = nombreMayus
        
            dpto.estado = int(form.cleaned_data['estado'])
            dpto.save()
            color = green
            msg = "El Departamento '%s' fue editado exitosamente." % dpto.nombre 

            if "Guardar" in request.POST:
                    form = departamentoForm()
                    dptos = Departamento.objects.order_by('nombre')

                    return render(request,'adminDptos.html',{'dptos':dptos,
                                                      'form':form,
                                                      'mensaje2':msg})


    else:
        form = editarDptoForm(initial = {'nombre':dpto.nombre,'estado':str(dpto.estado)})
        
    return render(request,'editarDpto.html',{'form':form,'color':color,'mensaje':msg,'nombre':nombre})
