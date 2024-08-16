import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import chartauditor.pdf_wrapper.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HeathCare.settings')
django.setup()
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    # 'http': django_asgi_app,
    'http': get_asgi_application(),
    'websocket': URLRouter(
        chartauditor.pdf_wrapper.routing.websocket_urlpatterns

    )
})