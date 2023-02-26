from django.urls import path
from .views import *

urlpatterns = [
    path('cadastrar/', criar_usuario, name="cadastrarusuario"),
    path('listar/', listar_usuarios, name="listarusuarios"),
    path('editarperfil/<int:id>', editar_perfil, name="editarperfil"),
    path('editarusuario/<int:id>', editar_usuario, name="editarusuario"),
    path('deletar/<int:id>', deletar_usuario, name="deletarusuario")
]