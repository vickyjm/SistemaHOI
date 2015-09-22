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

@login_required
def verperfil(request):
    grupo = request.user.groups.values('name')
    if (not grupo) and request.user.is_superuser:
        request.user.groups.add(Group.objects.get(name='Administradores'))
        request.user.groups.add(Group.objects.get(name='Almacenistas'))
        request.user.groups.add(Group.objects.get(name='Técnicos'))

    aprobar = Aprueba.objects.filter(id_usuario = request.user)
    crear = Crea.objects.all()

    return render(request, 'verperfil.html',{'user': request.user, 'aprobar': aprobar, 'crear':crear})

def perfil_editar(request, _id):
    if request.method == "POST":
        form = perfilForm(request.POST)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['nombre']
            request.user.last_name = form.cleaned_data['apellido']
            request.user.email = form.cleaned_data['correo']
            request.user.save()
            return HttpResponseRedirect('/verperfil')
    else:

        form = perfilForm(initial = {'nombre':request.user.first_name,
                                     'apellido':request.user.last_name,
                                     'correo':request.user.email})

    return render(request, 'perfil_editar.html', {'form':form,
                                                  'user':request.user})

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
        if form.is_valid():
            ci = form.cleaned_data['cedula']
            if User.objects.filter(username=ci).exists():
                msg = "Esta cédula ya se encuentra registrada"
                return render(request,'registro.html',{'form' : form, 'msg' : msg})
            if (form.cleaned_data['contraseña1']!= form.cleaned_data['contraseña2']):
                msg = "Las contraseñas no coinciden. Intente de nuevo"
                return render(request,'registro.html',{'form' : form, 'msg' : msg})
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
            user.is_active = True
            user.save()
            msg = "Su usuario fue registrado exitosamente"
            return render(request,'registro.html',{'form': form, 'msg': msg})
    else:
        form = registroForm()
    return render(request,'registro.html', {'form': form})
   
def recuperarContraseña(request):
    if request.method == "POST":
        form = recuperarContraseñaForm(request.POST)
        if form.is_valid():
            ci = form.cleaned_data['cedula']
            if User.objects.filter(username=ci).exists():
                if (form.cleaned_data['contraseña1']!= form.cleaned_data['contraseña2']):
                    msg = "Las contraseñas no coinciden. Intente de nuevo"
                    return render(request,'recuperarContrasenia.html',{'form' : form, 'msg' : msg})
                user = User.objects.get(username=ci)
                user.set_password(form.cleaned_data['contraseña1'])
                user.save()
                msg = "Su contraseña fue cambiada"
                return render(request,'recuperarContrasenia.html',{'form' : form, 'msg' : msg})  
            else:
                msg = "La cédula ingresada no se encuentra registrada"
                return render(request,'recuperarContrasenia.html',{'form' : form, 'msg' : msg})
    else:
        form = recuperarContraseñaForm()
    return render(request,'recuperarContrasenia.html',{'form': form})
   
def cerrarSesion(request):
    logout(request)
    return HttpResponseRedirect('/')

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
                            minimo = form.cleaned_data['minimo']
                            )
                obj.save()
                mensaje = "Item %s creado exitosamente" % (inombre) 
                form = itemForm(initial={'cantidad': '0', 'minimo': '5'})   
    else:
        form = itemForm(initial={'cantidad': '0', 'minimo': '5'})
    return render(request,'crearItem.html', {'form': form})

def categoria(request):
    if request.method == "POST":
        form = categoriaForm(request.POST)
        mensaje = None
        if form.is_valid():
            catnombre = form.cleaned_data['nombre']

            try: 
                cat = Categoria.objects.get(nombre = catnombre)
                # Verifica si el nombre de la categoria ya existe
                if Categoria.objects.filter(pk=cat.pk).exists():
                    mensaje = "Categoría '%s' ya existe" % (catnombre)
            # Si no existe, crea el objeto y lo guarda
            except ObjectDoesNotExist:
                obj = Categoria(nombre = catnombre,
                                estado = 1)
                obj.save()
                mensaje = "Categoría '%s' creada exitosamente" % (catnombre)
                form = categoriaForm()
        categorias = Categoria.objects.order_by('nombre')

    else:
        form = categoriaForm()
        mensaje = None  
        categorias = Categoria.objects.order_by('nombre')

    return render(request,'categoria.html', {'form': form, 
                                             'categorias': categorias, 
                                             'mensaje': mensaje})

# Vista creada para editar una categoria en el sistema
def categoria_editar(request, _id):

    categoria = Categoria.objects.get(id = _id)
    # Lista de items dentro de la categoria
    #items = Item.objects.filter(id_categoria = _id)
    # Cantidad de items dentro de la categoria
    #cantidad = items.count()

    if request.method == "POST":
        
        form = categoria_editarForm(request.POST)
        
        if form.is_valid():
            #Obtiene datos del formulario
            cnombre = form.cleaned_data['nombre']
            cestado = form.cleaned_data['estado']
            try:
                # Obtiene la categoria con el nombre del formulario
                cat = Categoria.objects.get(nombre = cnombre)
                # Si la categoria es la misma a editar
                if int(cat.pk) == int(_id):
                    # Verifica si hay cambio en la categoria
                    if int(cestado) != int(categoria.estado):
                        categoria.estado = cestado
                        categoria.save()
                        mensaje = "Categoría editada exitosamente"
                    # No hubo cambios en la categoria
                    else: 
                        mensaje = None
                # Si la categoria no es la misma a editar
                else:
                    mensaje = "La categoría '%s' ya existe" % cnombre
            # Si no existe una categoria con el nombre introducido
            except:
                categoria.nombre = cnombre
                categoria.estado = cestado
                categoria.save()
                mensaje = "Categoría editada exitosamente"

    else:
        # Formulario con los datos a editar
        form = categoria_editarForm(initial={'nombre': categoria.nombre, 
                                             'estado': categoria.estado})
        mensaje = None
    return render(request,'categoria_editar.html', {'categoria': categoria, 
                                                    'form': form,
                                                    'mensaje': mensaje})

# Vista utilizada para editar un item en el sistema
def item_editar(request, _id):
    # Obtiene el objeto de item a editar
    item = Item.objects.get(id = _id)
    nombre = item.nombre
    if request.method == "POST":
        form = item_editarForm(request.POST)

        if form.is_valid():
            # Obtiene los datos del formulario
            inombre = form.cleaned_data['nombre']
            icategoria = form.cleaned_data['categoria']
            idcat = Categoria.objects.get(nombre = icategoria)
            print (idcat)
            try:
                itemexiste = Item.objects.get(nombre = inombre, 
                                              id_categoria = idcat.id)
                if int(itemexiste.id) == int(_id): 
                    item.cantidad = form.cleaned_data['cantidad']
                    item.minimo = form.cleaned_data['minimo']
                    item.estado = form.cleaned_data['estado']
                    item.save()
                    mensaje = "Item '%s' editado exitosamente" %nombre
                else:
                    mensaje = "Nombre '%s' ya existe en la categoría '%s'" %(inombre, idcat)
                    
            except ObjectDoesNotExist:

                item.nombre = inombre
                item.cantidad = form.cleaned_data['cantidad']
                item.id_categoria = idcat
                item.minimo = form.cleaned_data['minimo']
                item.estado = form.cleaned_data['estado']
                item.save()
                mensaje = "Item '%s' editado exitosamente" %nombre
                nombre = inombre
    else: 
        # Formulario con los datos del item a editar
        form = item_editarForm(initial = {'nombre': item.nombre, 
                                          'cantidad': item.cantidad,
                                          'categoria': item.id_categoria,
                                          'minimo': item.minimo})
        mensaje = None
    return render(request, 'item_editar.html', {'form' : form, 
                                                'nombre' : nombre,
                                                'mensaje': mensaje})
           
           
# Vista utilizada para mostrar los items del inventario
def inventario(request):
    items = Item.objects.order_by('nombre')
    if request.method == "POST":
        pass  
    else:
        pass
    return render(request,'inventario.html', {'items': items})


def solicitud(request):
    solic_creadas = Crea.objects.order_by('-fecha')

    # Si es un técnico, solo puede ver sus solicitudes
    if not request.user.groups.filter(name = "Almacenistas").exists():
        solicitudes = solic_creadas.filter(id_usuario = request.user)
    # Si es almacenista o administrador, solo ve las solicitudes de los técnicos
    else:
        solicitudes = solic_creadas.exclude(id_usuario = request.user)  ########### QUITAR
    if request.method == "POST":
        pass  
    else:
        pass
    return render(request,'solicitud.html', {'user' : request.user,
                                             'solicitudes': solicitudes})

@login_required
def crearSolicitud(request):
    categorias = Categoria.objects.values_list('nombre', flat = True)
    items = Item.objects.order_by('nombre') 
    error_obligatorio = None
    if request.method == "POST":
        mensaje = None
        form = solicitudForm(request.POST)

        if form.is_valid():

            fecha = datetime.datetime.now()
            scategoria = request.POST.get("role")
            sitem = request.POST.get("item")
            sdpto = form.cleaned_data['dpto']
            scantidad = form.cleaned_data['cantidad']

            if scategoria == "":
                form = solicitudForm(initial={'dpto': sdpto,
                                              'cantidad': scantidad})
                error_obligatorio = "Este campo es obligatorio."
                return render(request,'crearSolicitud.html', {'form': form,
                                                      'mensaje': mensaje,
                                                      'error_obligatorio': error_obligatorio,
                                                      'categorias': categorias,
                                                      'items': items})

    
            nueva_solicitud = Solicitud(fecha = fecha,
                                        dpto = sdpto,
                                        cantidad = scantidad)
            nueva_solicitud.save()

            id_cat = Categoria.objects.get(nombre = scategoria)
            iditem = Item.objects.filter(id_categoria = id_cat).get(nombre = sitem)
            obj = Crea(id_usuario = request.user,
                       id_item = iditem,
                       id_solicitud = nueva_solicitud,
                       fecha = fecha)
            obj.save()

            mensaje = "Solicitud creada exitosamente" 
            form = solicitudForm(initial={'cantidad': '1'})
    else:
        mensaje = None
        form = solicitudForm(initial={'cantidad': '1'})
    
    return render(request,'crearSolicitud.html', {'form': form,
                                                  'mensaje':mensaje,
                                                  'error_obligatorio': error_obligatorio,
                                                  'categorias': categorias,
                                                  'items':items})

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

# def solicitud_editar(request, _id):
#     obj = Crea.objects.get(pk = _id)
#     solicitud = Solicitud.objects.get(pk = obj.id_solicitud.pk)
#     if request.method == "POST":
#         form = solicitudForm(request.POST)

#         if form.is_valid():
#             #sdpto = form.cleaned_data['dpto']
#             #sitem = form.cleaned_data['item']
#             #scantidad = form.cleaned_data['cantidad']
            
#             mensaje = "Solicitud editada exitosamente"
#     else:
#         mensaje = None
#         form = solicitudForm(initial = {'dpto': item.nombre, 
#                                           #'item': ,
#                                           'cantidad': item.cantidad})
#     return render(request, 'solicitud_seditar.html', {'form' : form,
#                                                 'mensaje': mensaje})

# Actualiza el estado de las solicitudes de un técnico
def solicitud_estado(request, _id, _nuevo_estado):
    solic_creadas = Crea.objects.order_by('fecha')

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

        if _nuevo_estado == "A":
            aprobado = Aprueba(id_usuario = request.user,
                               id_solicitud = solicitud,
                               fecha = datetime.datetime.now())
            aprobado.save()

            # Si la solicitud se aprobó, se reduce la cantidad de ese item del inventario
            for s in solic_creadas: 
                if s.id_solicitud == solicitud:
                    item = Item.objects.get(pk = s.id_item.pk)
                    item.cantidad = item.cantidad - solicitud.cantidad
                    item.save()
    else:
        pass
    return render(request,'solicitud_estado.html', {'solicitudes':solicitudes})

def item_ingresar(request, _id):
    item = Item.objects.get(pk = _id)
    
    if request.method == "POST":
        form = item_ingresarForm(request.POST)
        
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
            
            mensaje = "Cantidad ingresada exitosamente"
            color = "#009900"
    else:
        mensaje = None
        color = "#000000"
        form = item_ingresarForm(initial={'cantidad': '1'})

    accion = "Ingresar"
    return render(request,'item_ingresar_retirar.html', {'form': form, 
                                                         'accion': accion,
                                                         'item': item,
                                                         'mensaje': mensaje,
                                                         'color': color})

def item_retirar(request, _id):
    item = Item.objects.get(pk = _id)

    if request.method == "POST":
        form = item_retirarForm(request.POST)
        
        if form.is_valid():
            fecha = datetime.datetime.now()
            icantidad = form.cleaned_data['cantidad']
            idpto = form.cleaned_data['dpto']

            if icantidad > item.cantidad:
                if item.cantidad == 0:
                    mensaje = "No quedan unidades de este item."
                else:
                    mensaje = "Solo quedan '%d' unidades de este item" % (item.cantidad)
                color = "#CC0000"
            else:
                item.cantidad = item.cantidad - icantidad
                item.save()            

                nueva_solicitud = Solicitud(fecha = fecha,
                                            dpto = idpto,
                                            cantidad = icantidad,
                                            estado = "A")
                nueva_solicitud.save()

                obj = Crea(id_usuario = request.user,
                           id_item = item,
                           id_solicitud = nueva_solicitud,
                           fecha = fecha)
                obj.save()

                aprobar = Aprueba(id_usuario = request.user,
                                  id_solicitud = nueva_solicitud,
                                  fecha = fecha)
                aprobar.save()

                mensaje = "Cantidad retirada exitosamente"
                color = "#009900"
    else:
        mensaje = None
        color = "#000000"
        form = item_retirarForm(initial={'cantidad': '1'})

    accion = "Retirar"
    return render(request,'item_ingresar_retirar.html', {'form': form, 
                                                         'accion': accion,
                                                         'item': item,
                                                         'mensaje': mensaje,
                                                         'color': color})
def imprimirReporte(request):
    msg = None
    if request.method == 'POST':
        form = reportesForm(request.POST)
        
        if form.is_valid():
            fechaIni = form.cleaned_data['fechaInicio']
            fechaFin = form.cleaned_data['fechaFin']
            
            if (fechaFin < fechaIni):
                msg = "Fechas inválidas. Intente de nuevo"
                
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