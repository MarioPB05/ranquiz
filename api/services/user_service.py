from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from api.models import Notification, UserFollow, List
from api.models.notification_type import NotificationTypes
from api.services import PAGINATION_ITEMS_PER_PAGE
from api.services.email_service import send_register_email
from api.services.query_service import execute_query
from api.services.shop_service import get_avatar
from api.forms.user_form import LoginUserForm, CreateUserForm
from api.services.client_service import create_client, get_client_form
from api.services.transaction_service import do_transaction


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
        user.money = 0

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

                # Creamos la transacción
                do_transaction(user, 50, 'Registro en Ranquiz')

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


def get_user_stats(user):
    """Función que obtiene las estadísticas de un usuario"""
    return {
        'money': user.money,
        'followers': UserFollow.objects.filter(user_followed=user).count(),
        'following': UserFollow.objects.filter(follower=user).count(),
        'lists': List.objects.filter(owner=user, public=True).count()
    }


def get_users(limit=None, page=1, search='', order='default', user=None):
    """Servicio que devuelve los usuarios con filtros"""
    order_by = "lists DESC"

    if order == 'popular':
        order_by = "followers DESC"
    elif order == 'newest':
        order_by = "max(l.creation_date) DESC"

    query = f"""SELECT u.id, u.username, u.share_code, a.image as avatar,
                    (SELECT COUNT(uf.user_followed_id)
                     FROM api_userfollow uf
                     WHERE uf.user_followed_id = u.id) AS followers,
                    (SELECT IF(COUNT(uf.user_followed_id) > 0, TRUE, FALSE)
                     FROM api_userfollow uf
                     WHERE uf.user_followed_id = u.id AND uf.follower_id = %s) AS followed,
                    COUNT(l.id) AS lists
                FROM api_user u
                JOIN ranquiz.api_avatar a on u.avatar_id = a.id
                LEFT JOIN api_list l on u.id = l.owner_id and l.public = TRUE
                WHERE u.username LIKE %s AND u.id != %s
                GROUP BY u.id
                ORDER BY {order_by}
                LIMIT %s OFFSET %s;"""

    params = [user.id if user.id is not None else 0, f"%{search}%", user.id if user.id is not None else 0, limit,
              (page - 1) * limit]

    return execute_query(query, params)


def get_users_following(user, selected_user, page=1):
    """Servicio que devuelve los usuarios que sigue un usuario"""
    query = """SELECT u.username, u.share_code, a.image as avatar,
                    (SELECT COUNT(uf.user_followed_id)
                     FROM api_userfollow uf
                     WHERE uf.user_followed_id = u.id) AS followers,
                    (SELECT IF(COUNT(uf.user_followed_id) > 0, TRUE, FALSE)
                     FROM api_userfollow uf
                     WHERE uf.user_followed_id = u.id AND uf.follower_id = %s) AS followed,
                    COUNT(l.id) AS lists
                FROM api_user u
                JOIN ranquiz.api_avatar a on u.avatar_id = a.id
                LEFT JOIN api_list l on u.id = l.owner_id and l.public = TRUE
                JOIN api_userfollow uf on u.id = uf.user_followed_id and uf.follower_id = %s
                WHERE(SELECT IF(COUNT(uf.user_followed_id) > 0, TRUE, FALSE)
                     FROM api_userfollow uf
                     WHERE uf.user_followed_id = u.id AND uf.follower_id = %s) = TRUE
                GROUP BY u.id
                LIMIT %s OFFSET %s;"""

    params = [selected_user.id, user.id, user.id, PAGINATION_ITEMS_PER_PAGE, (page - 1) * PAGINATION_ITEMS_PER_PAGE]

    return execute_query(query, params)


def get_users_followers(user, selected_user, page=1):
    """Servicio que devuelve los usuarios que siguen a un usuario"""
    query = """SELECT u.username, u.share_code, a.image as avatar,
                    (SELECT COUNT(uf1.user_followed_id)
                     FROM api_userfollow uf1
                     WHERE uf1.follower_id = u.id) AS followers,
                    (SELECT IF(COUNT(uf2.user_followed_id) > 0, TRUE, FALSE)
                     FROM api_userfollow uf2
                     WHERE uf2.user_followed_id = u.id AND uf2.follower_id = %s) AS followed,
                    COUNT(l.id) AS lists
                FROM api_user u
                JOIN ranquiz.api_avatar a ON u.avatar_id = a.id
                LEFT JOIN api_list l ON u.id = l.owner_id AND l.public = TRUE
                JOIN api_userfollow uf ON u.id = uf.follower_id
                WHERE uf.user_followed_id = %s
                GROUP BY u.id, u.username, u.share_code, a.image
                LIMIT %s OFFSET %s;"""

    params = [selected_user.id, user.id, PAGINATION_ITEMS_PER_PAGE, (page - 1) * PAGINATION_ITEMS_PER_PAGE]

    return execute_query(query, params)


def toggle_user_follow(user, followed_user):
    """Servicio que permite seguir o dejar de seguir a un usuario"""
    if followed_user is None or user is None or followed_user == user:
        return False

    is_following = user.following_set.filter(user_followed=followed_user).exists()

    if is_following:
        user.following_set.filter(user_followed=followed_user).delete()
    else:
        user.following_set.create(user_followed=followed_user)
        Notification.create(1, NotificationTypes.NEW_FOLLOWER.object, followed_user, user.share_code)

    return True
