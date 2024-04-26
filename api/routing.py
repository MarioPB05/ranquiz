from django.urls import path

from api.controllers.category_controller import validate_category, get_categories, add_category, \
    get_categories_filtered, follow_category
from api.controllers.list_controller import get_list_types, like_list, favorite_list, get_lists_filtered
from api.controllers.social_controller import get_comments, create_and_return_comment, add_award_to_comment_function, \
    get_awards
from api.controllers.shop_controller import highlight_calculator, get_avatars, buy_a_avatar, equip_a_avatar
from api.controllers.user_controller import get_user_data, get_users_filtered, follow_user

urlpatterns = [
    path('list/filter', get_lists_filtered, name='api_lists_filtered'),
    path('list/types', get_list_types, name='api_list_types'),
    path('category/', get_categories, name='api_categories'),
    path('category/filter', get_categories_filtered, name='api_categories_filtered'),
    path('category/create/', add_category, name='api_category_create'),
    path('category/validate/<str:category_name>', validate_category, name='api_category_validator'),
    path('list/<str:share_code>/comments', get_comments, name='api_list_comments'),
    path('list/<str:share_code>/comment/create', create_and_return_comment, name='api_new_comment'),
    path('list/<str:share_code>/comment/<int:comment_id>/awards', create_and_return_comment,
         name='get_awards_from_comment'),
    path('list/<str:share_code>/comment/<int:comment_id>/add_award', add_award_to_comment_function,
         name='add_award_to_comment'),
    path('social/awards', get_awards, name='get_all_awards'),
    path('category/validate/<str:category_name>', validate_category, name='api_category_validator'),
    path('category/<str:share_code>/follow', follow_category, name='api_follow_category'),
    path('shop/avatar/', get_avatars, name='api_shop_avatars'),
    path('shop/avatar/<int:avatar_id>/buy', buy_a_avatar, name='api_shop_avatar_buy'),
    path('shop/avatar/<int:avatar_id>/equip', equip_a_avatar, name='api_shop_avatar_equip'),
    path('shop/highlight/calculator', highlight_calculator, name='api_shop_highlight_calculator'),
    path('user/', get_user_data, name='api_user'),
    path('user/filter', get_users_filtered, name='api_users_filtered'),
    path('user/<str:share_code>/follow', follow_user, name='api_follow_user'),
    path('list/<str:share_code>/like', like_list, name='api_like_list'),
    path('list/<str:share_code>/favorite', favorite_list, name='api_favorite_list'),
]
