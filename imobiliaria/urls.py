from django.urls import path
from .views import *

urlpatterns = [
    path('', index_imobiliaria, name="indeximobiliaria"),
    path('cadastrar/', cadastrar_imovel, name="cadastrarimovel"),
    path('listar/', listar_imoveis, name="listarimoveis"),
    path('atualizar/<int:id>', atualizar_dados_imovel, name="atualizardadosimovel"),
    path('deletar/<int:id>', deletar_imovel, name="deletarimovel"),
]