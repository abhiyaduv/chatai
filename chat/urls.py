from django.urls import path
from .views import home, chat_api, load_chat, delete_chat, clear_chat

urlpatterns = [
    path('', home),
    path('chat/', chat_api),
    path('load/<int:session_id>/', load_chat),
    path('delete/<int:session_id>/', delete_chat),
    path('clear/<int:session_id>/', clear_chat),
]