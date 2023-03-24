from django.urls import path
from .views import *

urlpatterns = [
    path('home/', homeRealEstate, name="indeximobiliaria"),
    path('create/', createProperty, name="cadastrarimovel"),
    path('list/', listProperties, name="listarimoveis"),
    path('read/<int:id>', readProperty, name='read-property'),
    path('listavailableproperties/', listAvailableProperties, name='list-available-properties'),
    path('update/<int:id>', updateProperty, name="atualizardadosimovel"),
    path('delete/<int:id>', deleteProperty, name="deletarimovel"),
]