from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

from api.forms.user_form import LoginUserForm


def user_login(request):
    """Función que permite a un usuario iniciar sesión en la aplicación"""
    if request.method == 'POST':
        form = LoginUserForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)

                redirect('homepage')
            else:
                form.add_error(None, 'Email o contraseña incorrectos')
    else:
        form = LoginUserForm()

    return form
