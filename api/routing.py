from django.urls import path

from api.controllers.item_controller import get_current_items, get_all_items
from api.controllers.category_controller import validate_category, get_categories, add_category, \
    get_categories_filtered, follow_category
from api.controllers.list_controller import get_list_types, like_list, favorite_list, get_lists_filtered, \
    visibility_list, delete_or_recover_list, recover_list_eliminated, add_result_to_list
from api.controllers.goal_controller import claim_quest_reward
from api.controllers.social_controller import get_comments, create_and_return_comment, add_award_to_comment_function, \
    get_awards
from api.controllers.shop_controller import highlight_calculator, get_avatars, buy_a_avatar, equip_a_avatar, \
    highlight_list, list_is_highlighted
from api.controllers.user_controller import (get_user_data, get_users_filtered, follow_user, user_lists,
                                             user_categories, user_following)

urlpatterns = [
    path('list/filter', get_lists_filtered, name='api_lists_filtered'),
    path('list/types', get_list_types, name='api_list_types'),
    path('category/', get_categories, name='api_categories'),
    path('category/filter', get_categories_filtered, name='api_categories_filtered'),
    path('category/create/', add_category, name='api_category_create'),
    path('category/<str:share_code>/follow', follow_category, name='api_category_follow'),
    path('category/validate/<str:category_name>', validate_category, name='api_category_validator'),
    path('list/<str:share_code>/comments', get_comments, name='api_list_comments'),
    path('list/<str:share_code>/comment/create', create_and_return_comment, name='api_new_comment'),
    path('list/<str:share_code>/item/', get_current_items, name='get_list_items'),
    path('list/<str:share_code>/item/all', get_all_items, name='get_all_items'),
    path('list/<str:share_code>/play/result/add', add_result_to_list, name='add_result_to_list'),
    path('list/<str:share_code>/comment/<int:comment_id>/add_award', add_award_to_comment_function,
         name='add_award_to_comment'),
    path('social/awards', get_awards, name='get_all_awards'),
    path('category/validate/<str:category_name>', validate_category, name='api_category_validator'),
    path('category/<str:share_code>/follow', follow_category, name='api_follow_category'),
    path('shop/avatar/', get_avatars, name='api_shop_avatars'),
    path('shop/avatar/<int:avatar_id>/buy', buy_a_avatar, name='api_shop_avatar_buy'),
    path('shop/avatar/<int:avatar_id>/equip', equip_a_avatar, name='api_shop_avatar_equip'),
    path('shop/highlight/<str:share_code>/check', list_is_highlighted, name='api_shop_highlight_check'),
    path('shop/highlight/calculator', highlight_calculator, name='api_shop_highlight_calculator'),
    path('shop/highlight/<str:share_code>', highlight_list, name='api_shop_highlight_list'),
    path('user/', get_user_data, name='api_user'),
    path('user/filter', get_users_filtered, name='api_users_filtered'),
    path('user/<str:share_code>/lists', user_lists, name='api_user_lists'),
    path('user/<str:share_code>/categories', user_categories, name='api_user_categories'),
    path('user/<str:share_code>/following', user_following, name='api_following_user'),
    path('user/<str:share_code>/follow', follow_user, name='api_follow_user'),
    path('list/<str:share_code>/like', like_list, name='api_like_list'),
    path('list/<str:share_code>/favorite', favorite_list, name='api_favorite_list'),
    path('list/<str:share_code>/visibility', visibility_list, name='api_visibility_list'),
    path('list/<str:share_code>/delete', delete_or_recover_list, name='api_delete_list'),
    path('list/<str:share_code>/recover', recover_list_eliminated, name='api_recover_list'),
    path('quest/claim', claim_quest_reward, name='api_claim_quest_reward'),
]
