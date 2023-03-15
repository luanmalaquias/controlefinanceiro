from django.db import models
import uuid

# Create your models here.

class Imovel(models.Model):
    nome = models.CharField(max_length=50, blank=True, verbose_name='Nome do imóvel / vila / condominio')
    cep = models.CharField(max_length=9, blank=True, verbose_name= 'CEP')
    endereco = models.CharField(max_length=100, blank=True, verbose_name= 'Endereço')
    numero = models.CharField(max_length=100, blank=True, verbose_name= 'Numero')
    bairro = models.CharField(max_length=100, blank=True, verbose_name= 'Bairro')
    cidade = models.CharField(max_length=100, blank=True, verbose_name= 'Cidade')
    uf = models.CharField(max_length=2, blank=True, verbose_name= 'UF')

    # TODO tipo inteiro
    mensalidade = models.CharField(max_length=10, blank=True, verbose_name='Mensalidade R$')
    vencimento = models.IntegerField(default=10, verbose_name="Dia do vencimento da mensalidade")

    disponibilidade = models.BooleanField(default=True, verbose_name="Disponibilidade")

    # TODO Colocar características do imovel tais como tamanho e quantidade de quartos e imoveis?

    def alterarDisponibilidade(self, disponibilidade: bool) -> None:
        self.disponibilidade = disponibilidade
        self.save()

    def __str__(self) -> str:
        nome = ''
        if self.nome:
            nome = self.nome
        else:
            nome = self.endereco
        return f'{nome}, {self.numero} - {self.bairro}'
