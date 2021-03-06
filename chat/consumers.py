from .models import Message
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from channels.generic.websocket import WebsocketConsumer

import json

class Consumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        receiver = text_data_json['receiver']
        message_type = text_data_json['message_type']
        room_id = text_data_json['room_id']
        username = text_data_json['username']

        if(room_id):            
            newMessage = Message(sender=sender, receiver=receiver, text=message, message_type=message_type, room_id=room_id)
        else:
            newMessage = Message(sender=sender, receiver=receiver, text=message, message_type=message_type)
        newMessage.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender' : sender,
                'message_type': message_type,
                'username': username
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        message_type = event['message_type']
        username = event['username']

        print(message)

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'type': message_type,
            'username': username
        }))
        