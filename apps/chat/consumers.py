import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        print("CONNECT CALLED")
        print("Connected user:", self.scope["user"])
        
        print("USER:", self.scope["user"])
        print("IS AUTHENTICATED:", self.scope["user"].is_authenticated)

        self.receiver_username = self.scope['url_route']['kwargs']['username']
        self.sender = self.scope["user"]

        users = sorted([self.sender.username, self.receiver_username])
        self.room_name = f"chat_{users[0]}_{users[1]}"

        print("Room name:", self.room_name)

        await self.channel_layer.group_add(
        self.room_name,
        self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )


    async def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data["message"]

        print("RECEIVE CALLED")
        print("Message received:", message_text)

        receiver = await sync_to_async(User.objects.get)(
        username=self.receiver_username
        )

        await sync_to_async(Message.objects.create)(
        sender=self.sender,
        receiver=receiver,
        content=message_text
        )

        await self.channel_layer.group_send(
        self.room_name,
            {
            "type": "chat_message",
            "message": message_text,
            "sender": self.sender.username,
            }
            )


    async def chat_message(self, event):

        print("BROADCASTING MESSAGE")

        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
        }))