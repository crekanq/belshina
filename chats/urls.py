from django.urls import path

from .views import ChatView, CreateChatView

urlpatterns = [
    path('create_chat/', CreateChatView.as_view(), name='create_chat'),
    path('', ChatView.as_view(), name='chat'),
]
