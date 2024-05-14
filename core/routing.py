from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('list/<str:share_code>/play', views.play_list, name='play_list'),
    path('list/<str:share_code>/view', views.list_details, name='list_details'),
    path('logout/', views.logout, name='logout'),
    path('list/create/', views.create_list_view, name='create_list'),
    path('list/<str:share_code>/edit', views.edit_list_view, name='edit_list'),
    path('user/', views.profile, name='user'),
    path('user/<str:share_code>/', views.profile, name='user'),
    path('shop/', views.shop, name='shop'),
    path('search/', views.search, name='search'),
    path('category/<str:share_code>/view', views.category_lists, name='category_lists'),
    path('admin/', admin.site.urls),
    path('list/<str:share_code>/result/<int:id>', views.result, name='list_result'),
]
