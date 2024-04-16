from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('list/create/', views.create_list_view, name='create_list'),
    path('user/', views.profile, name='user'),
    path('user/<str:share_code>/', views.profile, name='user'),
    path('shop/', views.shop, name='shop'),
    path('admin/', admin.site.urls),
]
