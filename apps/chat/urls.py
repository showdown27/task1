
from django.urls import path
from . import views

urlpatterns = [
    path("<str:username>/", views.chatRoom, name="chat_page")
]
