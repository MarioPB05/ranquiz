from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from api.models import User
from api.services.email_service import send_register_email
from api.services.shop_service import get_avatar
from api.forms.user_form import LoginUserForm, CreateUserForm
from api.services.client_service import create_client, get_client_form


def user_login(request):
    """Función que permite a un usuario iniciar sesión en la aplicación"""
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        next_url = request.POST.get('next', None)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                if next_url and next_url != 'None':
                    return redirect(next_url)

                return redirect('homepage')

            form.add_error(None, 'Email o contraseña incorrectos')
    else:
        form = LoginUserForm()
        next_url = request.GET.get('next', None)

    return render(request, 'pages/login.html', {'form': form, 'next': next_url})


def get_user_form(request):
    """Obtiene el formulario para crear un usuario"""
    return CreateUserForm(request.POST) if request.method == 'POST' else CreateUserForm()


def create_user(user_form, avatar, client):
    """Función que crea un usuario en la aplicación"""
    if user_form.is_valid() and avatar is not None and client is not None:
        # Establecemos las propiedades del usuario
        user = user_form.save(commit=False)
        user.client = client
        user.avatar = avatar

        return user

    return None


def user_register(request):
    """Función que permite a un usuario crear una cuenta en la aplicación"""
    client_form = get_client_form(request)
    user_form = get_user_form(request)

    if request.method == 'POST':
        client = create_client(client_form)

        if client is not None:
            # Obtenemos el avatar
            avatar = get_avatar(1)

            # Creamos el usuario
            user = create_user(user_form, avatar, client)

            if user is not None:
                # Guardamos el cliente
                client.save()

                # Guardamos el usuario
                user.save()

                # Enviar correo de registro exitoso
                send_register_email(client)

                messages.success(request, 'Inicia sesión con tus credenciales para comenzar a explorar, '
                                          'crear listas y jugar en Ranquiz.', extra_tags='register')

                # Redirigimos al usuario a la página de inicio de sesión
                return redirect('login')

            user_form.add_error(None, 'Error al crear el usuario')

        user_form.add_error(None, 'Error al crear el cliente')

    return render(request, 'pages/register.html', {'forms': {
        'client_form': client_form,
        'user_form': user_form
    }})


def get_user(user_id=None, share_code=None):
    """Función que obtiene un usuario por su id o su share_code"""
    try:
        if user_id is not None:
            return User.objects.get(id=user_id)

        if share_code is not None:
            return User.objects.get(share_code=share_code)

        return None
    except User.DoesNotExist:
        return None
