from django.urls import path
from .views import *

urlpatterns = [
    path('cadastrar/', criar_usuario, name="cadastrarusuario"),
    path('listar/', listar_usuarios, name="listarusuarios")
]