from django.urls import re_path, path

from .consumers import ChatConsumer,ActivityConsumer

websocket_urlpatterns = [
    re_path(r'chat/projects/(?P<project_pk>\w+)/$', ChatConsumer.as_asgi()),
    path(r'activities/', ActivityConsumer.as_asgi())
]