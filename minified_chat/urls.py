from django.urls import path
from .views import *
urlpatterns = [
    path('', index, name='HomePage'),
    path('<str:process>/', login_register, name='Authentication'),
    path('chat/<str:group_name>/', group_page, name='GroupPage'),
    path('logout/', logout_page, name='Logout')
]
