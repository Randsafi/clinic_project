import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import Question.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinic_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            Question.routing.websocket_urlpatterns
        )
    ),
})
