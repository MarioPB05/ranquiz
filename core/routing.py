from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('list/<str:share_code>/play', views.play_list, name='play_list'),
    path('list/create/', views.create_list_view, name='create_list'),
    path('admin/', admin.site.urls),
]
