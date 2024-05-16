import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from api.models import User, List
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


class ChannelManager:
    """Clase para gestionar los canales de los seguidores"""

    def __init__(self):
        self.channels_for_followers = []

    async def append_channel(self, channel):
        """Añade un canal para los seguidores"""
        self.channels_for_followers.append(channel)

    async def remove_channel(self, share_code):
        """Elimina un canal para los seguidores"""
        self.channels_for_followers = [
            channel for channel in self.channels_for_followers
            if channel['share_code'] != share_code
        ]

    async def find_channel_for_followers(self, share_code):
        """Busca un canal para los seguidores"""
        for channel in self.channels_for_followers:
            if channel['share_code'] == share_code:
                return channel['channel_name']
        return None

    async def debug_show_channels(self):
        """Función para mostrar los canales de los seguidores"""
        print(f"CANALES DE LOS SEGUIDORES ({len(self.channels_for_followers)})")

        for channel in self.channels_for_followers:
            print("+" + "-" * 40 + "+")
            channel_name = channel["channel_name"]
            share_code = channel["share_code"]
            print(f"Canal: {channel_name}")
            print(f"Share code: {share_code}")

        print("+" + "-" * 40 + "+")


channel_manager = ChannelManager()


async def get_share_code_async(following):
    """Función para obtener el share_code de un usuario de forma asíncrona"""
    share_code = await sync_to_async(lambda f: f.user_followed.share_code)(following)
    return share_code


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

        await channel_manager.append_channel({
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

        await channel_manager.remove_channel(user.share_code)

    async def join_followers_channel(self, user):
        """Función para unirse al canal de los seguidores de los usuarios que sigue el usuario"""
        following_users = await sync_to_async(get_following)(user)

        async for following in following_users:
            share_code = await get_share_code_async(following)

            if await channel_manager.find_channel_for_followers(share_code) is not None:
                await self.channel_layer.group_add(
                    f'followers_{following.user_followed.share_code}',
                    self.channel_name
                )

    async def leave_followers_channel(self, user):
        """Función para salir del canal de los seguidores de los usuarios que sigue el usuario"""
        following_users = await sync_to_async(get_following)(user)

        async for following_user in following_users:
            if await channel_manager.find_channel_for_followers(following_user):
                await self.channel_layer.group_discard(
                    f'followers_{following_user.share_code}',
                    self.channel_name
                )

    async def join_global_channel(self):
        """Función para unirse al canal global"""
        await self.channel_layer.group_add(
            'global',
            self.channel_name
        )

    async def leave_global_channel(self):
        """Función para salir del canal global"""
        await self.channel_layer.group_discard(
            'global',
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
            await self.join_global_channel()
        else:
            await self.send(text_data=json.dumps({
                'status': 'Usuario no autenticado'
            }))
            await self.close()

        await channel_manager.debug_show_channels()

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
            await self.leave_global_channel()

        await channel_manager.debug_show_channels()

    async def receive(self, text_data=None, bytes_data=None):
        """Función que se ejecuta cuando se recibe un mensaje del cliente"""
        await self.send(text_data=json.dumps({
            'status': 'mensaje recibido'
        }))

    async def send_notification(self, event):
        """Función para enviar una notificación al cliente"""
        if event['target'] == 2 and self.scope['user'].share_code == event['share_code']:
            # Es una notificación para los seguidores, el dueño también está en el grupo, pero no la debe recibir
            return

        if event['share_code'][0:2] == 'US':
            notification_user = await sync_to_async(User.get)(share_code=event['share_code'])
            title = event['title'].replace('[USUARIO]', notification_user.username)
            desc = event['description'].replace('[USUARIO]', notification_user.username)
        elif event['share_code'][0:2] == 'LS':
            list_obj = await sync_to_async(List.get)(share_code=event['share_code'])
            list_owner_username = await sync_to_async(lambda ls: ls.owner.username)(list_obj)
            list_owner_share_code = await sync_to_async(lambda ls: ls.owner.share_code)(list_obj)

            title = event['title'].replace('[USUARIO]', list_owner_username)
            desc = event['description'].replace('[USUARIO]', list_owner_username)

            if event['target'] == 2 and self.scope['user'].share_code == list_owner_share_code:
                # Es una notificación para los seguidores, el dueño también está en el grupo, pero no la debe recibir
                return
        else:
            title = event['title']
            desc = event['description']

        await self.send(text_data=json.dumps({
            'icon': event['icon'],
            'title': title,
            'description': desc,
            'share_code': event['share_code']
        }))
