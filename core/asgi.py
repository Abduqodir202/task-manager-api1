import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_group_name = "chat_group"

        # Groupga qo'shish
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Groupdan chiqarish
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Clientdan xabar keladi
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]

        # Barcha userlarga yuborish
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
            }
        )

    # Groupdan kelgan xabarni clientga yuborish
    async def chat_message(self, event):
        message = event["message"]

        await self.send(
            text_data=json.dumps({
                "message": message
            })
        )