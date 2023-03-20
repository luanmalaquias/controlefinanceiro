from django.urls import path
from .views import *

urlpatterns = [
    path('cadastrar/', criar_usuario, name="cadastrarusuario"),
    path('listar/', listar_usuarios, name="listarusuarios"),
    # TODO listar um usuario -> listar/<int:id>
    # TODO listar usuarios sem imovel
    path('listUsersWithoutProperty', listUsersWithoutProperty, name='listUsersWithoutProperty'),
    path('editarperfil/<int:id>', editar_perfil, name="editarperfil"),
    path('editarusuario/<int:id>', editar_usuario, name="editarusuario"),
    path('deletar/<int:id>', deletar_usuario, name="deletarusuario"),
    path('removerdoimovel/<int:id>', remover_do_imovel, name="removerdoimovel"),
    path('incluirnoimovel/<int:id>', incluir_no_imovel, name="incluirnoimovel"),
    # path('recuperarsenha/', recuperar_senha, name="recuperarsenha"), # FIXME o usuario vai poder recuperar senha?
]