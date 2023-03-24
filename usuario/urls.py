from django.urls import path
from .views import *

urlpatterns = [
    path('home/', homeUser, name="home-usuario"),
    path('paymenthistory', userPaymentHistory, name="historico-usuario"),
    path('registry/', register, name="auto-cadastro"),
    path('recoverpassword/', recoverPassword, name="recuperarsenha"),
    path('create/', createUser, name="cadastrarusuario"),
    path('list/', listUsers, name="listarusuarios"),
    path('read/<int:id>', readUser, name='read-user'),
    path('listuserswithoutproperty', listUsersWithoutProperty, name='list-users-without-property'),
    path('editprofile/<int:id>', updateProfile, name="editarperfil"),
    path('changepassword/<int:id>', updateUser, name="editarusuario"),
    path('delete/<int:id>', deleteUserAndProfile, name="deletarusuario"),
    path('removefromproperty/<int:id>', removeFromProperty, name="removerdoimovel"),
    path('includeinproperty/<int:id>', includeInProperty, name="incluirnoimovel"),
]