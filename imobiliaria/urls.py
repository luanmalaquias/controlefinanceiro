from django.urls import path
from .views import *

urlpatterns = [
    path('home/', homeRealEstate, name="indeximobiliaria"),
    path('cadastrar/', createProperty, name="cadastrarimovel"),
    path('listar/', listProperties, name="listarimoveis"),
    path('read-property/<int:id>', readProperty, name='read-property'),
    path('list-available-properties/', listAvailableProperties, name='list-available-properties'),
    path('atualizar/<int:id>', updateProperty, name="atualizardadosimovel"),
    path('deletar/<int:id>', deleteProperty, name="deletarimovel"),
]