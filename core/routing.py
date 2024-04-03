from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login, name='login'),
    path('admin/', admin.site.urls),
]