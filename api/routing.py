from django.urls import path

from api.controllers.shop_controller import highlight_calculator

urlpatterns = [
    path('shop/highlight/calculator', highlight_calculator, name='api_shop_highlight_calculator'),
]
