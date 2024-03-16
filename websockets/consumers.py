import json
from channels.generic.websocket import AsyncWebsocketConsumer


class DefaultConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send_error_message("Ruta no encontrada")
        await self.close()

    async def send_error_message(self, message):
        await self.send(text_data=json.dumps({
            'type': 'error',
            'message': message
        }))


class NotificationsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        # if text_data:
        #     text_data_json = json.loads(text_data)
        #     message = text_data_json['message']
        #     print(message)
        #     if message == 'ping':
        #         self.send(text_data=json.dumps({
        #             'message': 'pong'
        #         }))

        await self.send(text_data=json.dumps({
            'status': 'mensaje recibido'
        }))
