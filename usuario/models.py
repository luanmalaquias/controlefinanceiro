from django.db import models
from django.contrib.auth.models import User
from imobiliaria.models import Imovel
import uuid

class Perfil(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    cpf = models.CharField(max_length=14, null=True)
    nome_completo = models.CharField(max_length=50, null=True)
    telefone = models.CharField(max_length=16, null=True)
    usuario = models.OneToOneField(User, blank=True, on_delete=models.CASCADE)
    imovel = models.OneToOneField(Imovel, null=True, blank=False, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return self.nome_completo

class HistoricoPagamento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    perfil = models.OneToOneField(Perfil, on_delete=models.PROTECT)
    pago = models.BooleanField(default=True, verbose_name="Pagamento efetuado?")
    valorPago = models.FloatField(default=0.0, verbose_name="Valor pago")
    dataReferencia = models.DateField(auto_now=True, verbose_name="Data de referencia do pagamento")

    def __str__(self) -> str:
        return f'{self.perfil} - {self.dataReferencia} - {self.valorPago}'
