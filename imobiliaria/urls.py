from django.urls import path
from .views import *

urlpatterns = [    
    path('cadastrar/', cadastrarImovel, name="cadastrarimovel"),
    path('listar/', listarImoveis, name="listarimoveis"),
    path('read-property/<int:id>', readProperty, name='read-property'),
    path('list-available-properties/', listAvailableProperties, name='list-available-properties'),
    path('atualizar/<int:id>', atualizarDadosImovel, name="atualizardadosimovel"),
    path('deletar/<int:id>', deletarImovel, name="deletarimovel"),
]