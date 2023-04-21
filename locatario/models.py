from django.db import models
from django.contrib.auth.models import User
from locador.models import Locador
from imovel.models import Imovel


class Locatario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    locador = models.ForeignKey(Locador, null=True, blank=True, on_delete=models.SET_NULL)
    imovel = models.ForeignKey(Imovel, null=True, blank=True, on_delete=models.SET_NULL)
    data_entrada_imovel = models.DateField(null=True, blank=True, verbose_name="Data de entrada no imovel")
    data_nascimento = models.DateField()
    telefone = models.CharField(null=True, blank=True, max_length=20)

    def __str__(self) -> str:
        if self.usuario:
            return f'{self.usuario.username} - {self.usuario.first_name}'
        else:
            return f'SEM USUARIO'