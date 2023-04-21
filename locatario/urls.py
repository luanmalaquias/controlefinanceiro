from django.urls import path
from .views import *

urlpatterns = [
    path('auto_cadastro/', cadastro_view, name='auto_cadastro_locatario_view'),
    path('home/', home_view, name='home_locatario')
]