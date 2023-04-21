from django.urls import path
from .views import *

urlpatterns = [
    path('', index_imobiliaria_view, name='index_imobiliaria'),
    path('csu/', create_super_user),
]