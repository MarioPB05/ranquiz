import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from api.services.social_service import get_following


class DefaultConsumer(AsyncWebsocketConsumer):
    """Consumidor de WebSockets por defecto"""

    async def connect(self):
        """Función que se ejecuta cuando se conecta el cliente"""
        await self.accept()
        await self.send_error_message("Ruta no encontrada")
        await self.close()

    async def send_error_message(self, message):
        """Función para enviar un mensaje de error al cliente"""
        await self.send(text_data=json.dumps({
            'type': 'error',
            'message': message
        }))


channels_for_followers = []


def append_channel(channel):
    """Añade un canal para los seguidores"""
    global channels_for_followers
    channels_for_followers.append(channel)


def remove_channel(share_code):
    """Elimina un canal para los seguidores"""
    global channels_for_followers
    channels_for_followers = list(filter(
        lambda channel: channel['share_code'] != share_code,
        channels_for_followers
    ))


def find_channel_for_followers(share_code):
    """Busca un canal para los seguidores"""
    for channel in channels_for_followers:
        if channel['share_code'] == share_code:
            return channel['channel_name']

    return None


def debug_show_channels():
    """Función para mostrar los canales de los seguidores"""
    print("+" + "-"*20 + "+" + "-"*30 + "+")
    print("| Canal               | Share code                        |")
    print("+" + "-"*20 + "+" + "-"*30 + "+")
    for channel in channels_for_followers:
        channel_name = channel["channel_name"]
        share_code = channel["share_code"]
        print(f"| {channel_name.ljust(20)} | {share_code.ljust(30)} |")
    print("+" + "-"*20 + "+" + "-"*30 + "+")


class NotificationsConsumer(AsyncWebsocketConsumer):
    """Consumidor de WebSockets para notificaciones"""

    async def create_channel_for_followers(self, user):
        """Crea un canal para los seguidores"""
        channel_name = f'followers_{user.share_code}'

        # Guardamos la instancia del consumidor junto al share_code del usuario
        await self.channel_layer.group_add(
            channel_name,
            self.channel_name
        )

        append_channel({
            'share_code': user.share_code,
            'channel_name': channel_name
        })

    async def remove_channel_for_followers(self, user):
        """Elimina un canal para los seguidores"""
        channel_name = f'followers_{user.share_code}'

        # Eliminamos la instancia del consumidor del grupo del share_code del usuario
        await self.channel_layer.group_discard(
            channel_name,
            self.channel_name
        )

        remove_channel(user.share_code)

    async def join_followers_channel(self, user):
        """Función para unirse al canal de los seguidores de los usuarios que sigue el usuario"""
        following_users = await sync_to_async(get_following)(user)

        async for following in following_users:
            if find_channel_for_followers(following.user_followed.share_code):
                await self.channel_layer.group_add(
                    f'followers_{following.user_followed.share_code}',
                    self.channel_name
                )

    async def leave_followers_channel(self, user):
        """Función para salir del canal de los seguidores de los usuarios que sigue el usuario"""
        following_users = await sync_to_async(get_following)(user)

        async for following_user in following_users:
            if find_channel_for_followers(following_user):
                await self.channel_layer.group_discard(
                    f'followers_{following_user.share_code}',
                    self.channel_name
                )

    async def connect(self):
        """Función que se ejecuta cuando se conecta el cliente"""
        await self.accept()

        user = self.scope['user']

        if user.is_authenticated:
            # Guardamos la instancia del consumidor junto al share_code del usuario
            await self.channel_layer.group_add(
                user.share_code,
                self.channel_name
            )

            await self.create_channel_for_followers(user)
            await self.join_followers_channel(user)
        else:
            await self.send(text_data=json.dumps({
                'status': 'Usuario no autenticado'
            }))
            await self.close()

        debug_show_channels()

    async def disconnect(self, close_code):  # skipcq: PYL-W0613
        """Función que se ejecuta cuando se desconecta el cliente"""
        user = self.scope['user']

        if user.is_authenticated:
            # Eliminamos la instancia del consumidor del grupo del share_code del usuario
            await self.channel_layer.group_discard(
                user.share_code,
                self.channel_name
            )

            await self.remove_channel_for_followers(user)
            await self.leave_followers_channel(user)

        debug_show_channels()

    async def receive(self, text_data=None, bytes_data=None):
        """Función que se ejecuta cuando se recibe un mensaje del cliente"""
        await self.send(text_data=json.dumps({
            'status': 'mensaje recibido'
        }))

    async def send_notification(self, event):
        """Función para enviar una notificación al cliente"""
        await self.send(text_data=json.dumps({
            'icon': event['icon'],
            'title': event['title'],
            'description': event['description'],
            'share_code': event['share_code']
        }))
