import json
from channels.generic.websocket import AsyncWebsocketConsumer


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


class NotificationsConsumer(AsyncWebsocketConsumer):
    """Consumidor de WebSockets para notificaciones"""

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
        else:
            await self.send(text_data=json.dumps({
                'status': 'Usuario no autenticado'
            }))
            await self.close()

    async def disconnect(self, close_code):
        """Función que se ejecuta cuando se desconecta el cliente"""
        user = self.scope['user']

        if user.is_authenticated:
            # Eliminamos la instancia del consumidor del grupo del share_code del usuario
            await self.channel_layer.group_discard(
                user.share_code,
                self.channel_name
            )

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
