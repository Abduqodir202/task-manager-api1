import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):

    # User ulanadi
    async def connect(self):
        await self.accept()

        await self.send(
            text_data=json.dumps({
                "message": "WebSocket ga xush kelibsiz!"
            })
        )

    # User uziladi
    async def disconnect(self, close_code):
        print("User chiqib ketdi")

    # Xabar qabul qilinadi
    async def receive(self, text_data):
        data = json.loads(text_data)

        message = data.get("message")

        # Xabarni userga qaytarish
        await self.send(
            text_data=json.dumps({
                "message": message
            })
        )