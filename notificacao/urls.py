from django.urls import path
from .views import *

urlpatterns = [
    path('list/', listNotifications, name='list-notifications'),
    path('create/', createNotification, name='create-notification'),
    path('read/<int:id>', readNotification, name='read-notification'),
    path('delete/<int:id>', deleteNotification, name='delete-notification'),
]