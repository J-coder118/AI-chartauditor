from django.urls import path
from chartauditor.pdf_wrapper import consumers

websocket_urlpatterns = [
    path('ws/progress/<int:user_id>/', consumers.ProgressBarConsumer.as_asgi()),
]