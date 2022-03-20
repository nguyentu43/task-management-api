"""
ASGI taskmanagement for taskmanagement project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanagement.settings')
django.setup()


from websocket.middlewares import QueryAuthMiddleware
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from websocket import urls


application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': QueryAuthMiddleware(
        URLRouter(
            urls.websocket_urlpatterns
        )
    ),
})
