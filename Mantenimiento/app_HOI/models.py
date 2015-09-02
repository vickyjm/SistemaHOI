from django.db import models
from django.db.models.fields import TextField
from django.contrib.auth.models import User
    
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
