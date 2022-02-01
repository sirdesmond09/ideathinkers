from django.urls import path, include
from . import views

urlpatterns = [
    path('users/', views.signup, name='signup'),
    path('users/profile', views.user_detail, name='profile'),
    path('auth/', views.user_login, name='auth'),
    path('weather/', views.weather, name='weather')
]