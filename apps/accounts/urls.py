
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home_page"),
    path('accounts/login/', views.user_login, name="user_login"),
    path('accounts/register/', views.register, name="register"),
    path('accounts/logout/', views.user_logout, name="user_logout"),
    path("searched/", views.searched, name="search")
]
