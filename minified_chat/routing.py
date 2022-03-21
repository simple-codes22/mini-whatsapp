from django.urls import re_path
from .consumer import ChatConsumer

websocket_urlpattern = [
    re_path(r'chat/(?P<group_name>\w+)/$', ChatConsumer.as_asgi())
]