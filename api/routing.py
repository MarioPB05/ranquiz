from django.urls import path

from api.controllers.category_controller import validate_category
from api.controllers.list_controller import get_list_types
from api.controllers.shop_controller import highlight_calculator

urlpatterns = [
    path('shop/highlight/calculator', highlight_calculator, name='api_shop_highlight_calculator'),
    path('list/types', get_list_types, name='api_list_types'),
    path('category/validate/<str:category_name>', validate_category, name='api_category_validator')
]
