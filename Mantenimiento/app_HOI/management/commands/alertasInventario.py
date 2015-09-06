from django.core.management.base import NoArgsCommand
from app_HOI.models import Item
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail

class Command(NoArgsCommand):
	help = "Comando para enviar alertas de inventario"

	def handle_noargs(self,**options):
		activos = Item.objects.filter(estado=1).order_by('id_categoria')
		aux = ""
		for item in activos:
			if (item.cantidad <= item.minimo):
				aux += item.id_categoria.nombre + "\t" + item.nombre + "\t\t" + str(item.cantidad) + "\t\t   " + "\n"
		if (aux != ""):
			msg = "Los siguientes ítems han alcanzado el mínimo programado en el inventario."
			msg += " Si no se repondrá alguno de ellos, puede acceder al sistema y cambiarle su estado a inactivo." 
			msg += " Además, puede ajustar la cantidad mínima de cada elemento según sus necesidades.\n"
			msg += "Categoría \t Ítem \t\t Cantidad Actual\n" + aux
			admins = User.objects.filter(groups__name='Administradores')
			for usuario in admins:
				send_mail('Inventario',msg,'sistemahoi@gmail.com',[usuario.email])