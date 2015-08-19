from django.shortcuts import render
from django.contrib.auth import authenticate, login
from app_HOI.forms import * 
from app_HOI.models import *

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
                    print("Te loggeaste") # Aqui iria al siguiente html?
                else:
                    print("No estas activo") # Aqui envia un mensaje en el html de que no esta activo
            else:
                print("Usuario o contraseña mala") # Aqui envia un mensaje en el html de que puso las cosas mal
    else:
        form = iniciarSesionForm()
    return render(request, 'prueba.html', {'form': form}) # Cambiar el nombre del html