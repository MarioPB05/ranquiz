from django.urls import path

from api.controllers.category_controller import validate_category, get_categories, add_category
from api.controllers.list_controller import get_list_types
from api.controllers.shop_controller import highlight_calculator, get_avatars, buy_a_avatar, equip_a_avatar
from api.controllers.user_controller import get_user_data

urlpatterns = [
    path('list/types', get_list_types, name='api_list_types'),
    path('category/', get_categories, name='api_categories'),
    path('category/create/', add_category, name='api_category_create'),
    path('category/validate/<str:category_name>', validate_category, name='api_category_validator'),
    path('shop/avatar/', get_avatars, name='api_shop_avatars'),
    path('shop/avatar/<int:avatar_id>/buy', buy_a_avatar, name='api_shop_avatar_buy'),
    path('shop/avatar/<int:avatar_id>/equip', equip_a_avatar, name='api_shop_avatar_equip'),
    path('shop/highlight/calculator', highlight_calculator, name='api_shop_highlight_calculator'),
    path('user/', get_user_data, name='api_user'),
]
