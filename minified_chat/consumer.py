import json
from channels.generic.websocket import WebsocketConsumer
from .models import Group, Message
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()
    
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
    
    def chat_message(self, event):
        message = event['message']
        Message.objects.create(
            from_=User.objects.get(username=self.scope['user']),
            group_=Group.objects.get(group_name=self.group_name),
            content=message
        )
        self.send(json.dumps({
            'message': message
        }))

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                "type": 'chat_message',
                "message": text_data_json.message
            }
        )