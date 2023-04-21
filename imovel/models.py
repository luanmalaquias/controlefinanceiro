from django.db import models
from locador.models import Locador


class Imovel(models.Model):
    nome = models.CharField(max_length=50)
    numero = models.CharField(max_length=100)
    cep = models.CharField(max_length=9)
    endereco = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    mensalidade = models.CharField(max_length=10)
    disponivel = models.BooleanField(default=True)
    locador = models.ForeignKey(Locador, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.nome}, {self.numero}'