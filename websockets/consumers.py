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

    async def disconnect(self, close_code):
        """Función que se ejecuta cuando se desconecta el cliente"""
        pass

    async def receive(self, text_data=None, bytes_data=None):
        """Función que se ejecuta cuando se recibe un mensaje del cliente"""
        await self.send(text_data=json.dumps({
            'status': 'mensaje recibido'
        }))
