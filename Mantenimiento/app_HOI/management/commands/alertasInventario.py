from django.core.management.base import NoArgsCommand
from app_HOI.models import Item
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from app_HOI.generarPdf import *
from io import BytesIO
import datetime

class Command(NoArgsCommand):
	help = "Comando para enviar alertas de inventario"

	def handle_noargs(self,**options):
		activos = Item.objects.filter(estado=1).order_by('id_categoria')
		aux = [["Categoría","Ítem","Cantidad mínima","Cantidad actual"]]
		for item in activos:
			if (item.cantidad <= item.minimo):
				aux.append([item.id_categoria.nombre,item.nombre,str(item.minimo),str(item.cantidad)])
		if (len(aux)!=1):
			admins = User.objects.filter(groups__name='Administradores')
			destinatarios = []
			for usuario in admins:
				destinatarios.append(usuario.email)
			msg = "Los ítems que se encuentran en el archivo PDF adjunto han alcanzado el mínimo programado en el inventario."
			msg += " Si no se repondrá alguno de ellos, puede acceder al sistema y cambiarle su estado a inactivo." 
			msg += " Además, puede ajustar la cantidad mínima de cada elemento según sus necesidades."
			email = EmailMessage('Alertas inventario Departamento de Mantenimiento HOI',msg,'sistemahoi@gmail.com',destinatarios)
			buffer = BytesIO()
			report = MiPDF(buffer,'Letter')
			pdf = report.imprimir_alertas(aux)
			email.attach('alertasInventario_'+str(datetime.datetime.now().date())+'.pdf', pdf, 'application/pdf')
			email.send()