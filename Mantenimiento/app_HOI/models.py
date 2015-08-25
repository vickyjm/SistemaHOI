from django.db import models
from django.db.models.fields import TextField
from django.contrib.auth.models import User
    
class Categoria(models.Model):
    nombre = models.CharField(max_length = 100)
    
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
