from django.urls import path
from .views import *

urlpatterns = [
    path('home-usuario', homeUser, name="home-usuario"),
    path('historico-usuario', userPaymentHistory, name="historico-usuario"),
    path('auto-cadastro/', register, name="auto-cadastro"),
    path('recuperarsenha/', recoverPassword, name="recuperarsenha"),
    path('cadastrar/', createUser, name="cadastrarusuario"),
    path('listar/', listUsers, name="listarusuarios"),
    path('read-user/<int:id>', readUser, name='read-user'),
    path('list-users-without-property', listUsersWithoutProperty, name='list-users-without-property'),
    path('editarperfil/<int:id>', updateProfile, name="editarperfil"),
    path('editarusuario/<int:id>', updateUser, name="editarusuario"),
    path('deletar/<int:id>', deleteUserAndProfile, name="deletarusuario"),
    path('removerdoimovel/<int:id>', removeFromProperty, name="removerdoimovel"),
    path('incluirnoimovel/<int:id>', includeInTheProperty, name="incluirnoimovel"),
]