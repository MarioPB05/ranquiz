from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

from api.forms.shop_service import get_avatar
from api.forms.user_form import LoginUserForm, CreateUserForm
from api.services.client_service import create_client, get_client_form


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


def get_user_form(request):
    """Obtiene el formulario para crear un usuario"""
    return CreateUserForm(request.POST) if request.method == 'POST' else CreateUserForm()


def create_user(user_form, avatar, client):
    """Función que crea un usuario en la aplicación"""
    if user_form.is_valid():
        # Establecemos las propiedades del usuario
        user = user_form.save(commit=False)
        user.client = client
        user.avatar = avatar

        # Guardamos el usuario
        user.save(commit=False)

        return user
    else:
        return None


def user_register(request):
    """"Función que permite a un usuario crear una cuenta en la aplicación"""
    client_form = get_client_form(request)
    user_form = get_user_form(request)

    if request.method == 'POST':
        client = create_client(client_form)

        if client is not None:
            # Obtenemos el avatar
            avatar = get_avatar(request.POST['avatar_id'])

            # Creamos el usuario
            user = create_user(request, avatar, client)

            if user is not None:
                # Guardamos el cliente
                client.save()

                # Guardamos el usuario
                user.save()

                # Redirigimos al usuario a la página de inicio de sesión
                redirect('login')
            else:
                user_form.add_error(None, 'Error al crear el usuario')
        else:
            user_form.add_error(None, 'Error al crear el cliente')

    return {
        'client_form': client_form,
        'user_form': user_form
    }
