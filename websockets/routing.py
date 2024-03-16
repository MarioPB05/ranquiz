from django.urls import path, re_path
from .consumers import DefaultConsumer, NotificationsConsumer

websockets_urlpatterns = [
    path('ws/notifications/', NotificationsConsumer.as_asgi()),

    # Este es el consumidor por defecto, que se encarga de manejar las rutas no encontradas
    re_path(r'^', DefaultConsumer.as_asgi()),
]
