from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('list/<str:share_code>/view', views.list_details, name='list_details'),
    path('admin/', admin.site.urls),
]
