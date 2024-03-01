
from django.urls import path
from websocket import consumer

websocket_urlpatterns = [
    path('ws/data/', consumer.MyConsumer.as_asgi()),
    path('ws/test/',consumer.MySocketConsumer.as_asgi()),
]

