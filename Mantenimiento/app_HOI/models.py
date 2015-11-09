# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.fields import TextField
from django.contrib.auth.models import User, Group, Permission
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_migrate
import datetime

@receiver(post_migrate)
def init_groups(sender, **kwargs):
    group, created = Group.objects.get_or_create(name='Técnicos')
    if not created:
        group.save()
    group, created = Group.objects.get_or_create(name='Almacenistas')
    if not created:
        group.save()
    group, created = Group.objects.get_or_create(name='Administradores')
    if not created:
        group.save()

class Categoria(models.Model):
    nombre = models.CharField(max_length = 100, unique=True)
    opciones_estado = ((0, "Inactivo"),
                        (1, "Activo"))
    estado = models.PositiveIntegerField(choices=opciones_estado, default = 1)

    def __str__(self):
        return self.nombre
    
class Item(models.Model):
    nombre = models.CharField(max_length = 100)
    cantidad = models.PositiveIntegerField()
    id_categoria = models.ForeignKey(Categoria)
    minimo = models.PositiveIntegerField() # Minimo cantidad de items para enviar alerta
    opciones_estado = ((0, "Inactivo"),
                        (1, "Activo"))
    estado = models.PositiveIntegerField(choices=opciones_estado, default = 1)
    
    def __str__(self):
        return self.nombre
    
class Departamento(models.Model):
    nombre = models.CharField(max_length = 500)
    opciones_estado = ((0, "Inactivo"),
                        (1, "Activo"))
    estado = models.PositiveIntegerField(choices=opciones_estado, default = 1)
    
    def __str__(self):
        return self.nombre

class Solicitud(models.Model):
    fecha = models.DateTimeField()
    dpto = models.ForeignKey(Departamento)
    cantidad = models.PositiveIntegerField()
    opciones_estado = (("A", "Aprobado"),
                       ("R", "Rechazado"),
                       ("E", "Esperando respuesta"))
    estado = models.CharField(max_length = 1,choices = opciones_estado, default = "E")

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