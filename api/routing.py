from django.urls import path

from api.controllers.category_controller import validate_category, get_categories, add_category
from api.controllers.list_controller import get_list_types
from api.controllers.shop_controller import highlight_calculator
from api.controllers.social_controller import get_comments, create_and_return_comment

urlpatterns = [
    path('shop/highlight/calculator', highlight_calculator, name='api_shop_highlight_calculator'),
    path('list/types', get_list_types, name='api_list_types'),
    path('category/', get_categories, name='api_categories'),
    path('category/create/', add_category, name='api_category_create'),
    path('category/validate/<str:category_name>', validate_category, name='api_category_validator'),
    path('list/<str:share_code>/comments', get_comments, name='api_list_comments'),
    path('list/<str:share_code>/comment/create', create_and_return_comment, name='api_new_comment'),
    path('list/<str:share_code>/comment/<int:comment_id>/awards', create_and_return_comment, name='get_awards_from_comment'),
]
