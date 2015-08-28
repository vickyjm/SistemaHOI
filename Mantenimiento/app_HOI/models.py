# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.fields import TextField
from django.contrib.auth.models import User, Group, Permission
from django.dispatch.dispatcher import receiver
from django.core.signals import request_finished
from django.db.models.signals import post_migrate
# Permisos de usuario
#p_aprobar_solicitud = Permission.objects.create(name='Puede aprobar solicitud')

# Grupos con los 3 tipos de actores del sistema
@receiver(post_migrate)
def init_groups(sender, **kwargs):
    g_tecnicos, created = Group.objects.get_or_create(name='tecnicos')
    g_almacenistas, created = Group.objects.get_or_create(name='almacenistas')
    g_administrador, created = Group.objects.get_or_create(name='administrador')

# Faltan los permisos

class Registro(models.Model):
    cedula = models.PositiveIntegerField(primary_key=True,unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    cargoEmpleado = (("tecnico","Técnico"), ("almacenista", "Almacenista"), ("admin", "Administrador"))
    cargo = models.CharField(max_length=32,choices = cargoEmpleado) # Creo que es redundante poner los choices aqui si ya estan en el form

@receiver(request_finished,sender=Registro)
def crearUsuario(sender, **kwargs):
    if instance.cargo == "Técnico":
        grupo = g_tecnicos
    elif instance.cargo == "Almacenista":
        grupo = g_almacenistas
    else:
        grupo = g_administrador

    nuevo_usuario = User.objects.create_user(username = instance.cedula,
                                             first_name = instance.nombre,
                                             last_name = instance.apellido,
                                             password = 'provisional',
                                             groups = grupo
                                            )
    nuevo_usuario.save()

class Categoria(models.Model):
    nombre = models.CharField(max_length = 100, unique=True)

    def __str__(self):
        return self.nombre
    
class Item(models.Model):
    # id = models.CharField(max_length = 50) Esto sería en caso que tengan algo tipo n° de bien
    nombre = models.CharField(max_length = 100)
    cantidad = models.PositiveIntegerField()
    id_categoria = models.ForeignKey(Categoria)
    opciones_prioridad = ((0, "Baja"),
                          (1, "Media"),
                          (2, "Alta"))
    prioridad = models.PositiveIntegerField(choices=opciones_prioridad)
    minimo = models.PositiveIntegerField() # Minimo cantidad de items para enviar alerta
    
class Solicitud(models.Model):
    dpto = models.CharField(max_length = 100) # Preguntar si ponerlo como opciones
    fecha = models.DateTimeField()
    cantidad = models.PositiveIntegerField()
    opciones_estado = (("A", "Aprobado"),
                       ("R", "Rechazado"),
                       ("E", "Esperando respuesta"))
    estado = models.CharField(max_length = 1,choices = opciones_estado)

class Crea(models.Model):
    id_usuario = models.ForeignKey(User)
    id_item = models.ForeignKey(Item)
    id_solicitud = models.ForeignKey(Solicitud)
    fecha = models.DateTimeField()
    
class Aprueba(models.Model):
    id_usuario = models.ForeignKey(User)
    id_solicitud = models.ForeignKey(Solicitud)
    fecha = models.DateTimeField()
    
class Ingresa(models.Model):
    id_usuario = models.ForeignKey(User)
    id_item = models.ForeignKey(Item)
    fecha = models.DateTimeField()
    cantidad = models.PositiveIntegerField()
    
class Reporte(models.Model):
    fecha_ini = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    contenido = TextField(max_length = 100) # Tentativo. Depende de cómo queramos el reporte.
    ciUsuario = models.ForeignKey(User)
