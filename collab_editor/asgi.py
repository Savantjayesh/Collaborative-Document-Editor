import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import editor.routing  # 👈 Import your routing module

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collab_editor.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            editor.routing.websocket_urlpatterns
        )
    ),
})
