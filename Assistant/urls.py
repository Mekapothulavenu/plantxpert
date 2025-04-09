from django.urls import path
from .views import assistant, send_message

urlpatterns = [
    path('', assistant, name='assistant'),
    path('send-message/', send_message, name='send_message'),

]