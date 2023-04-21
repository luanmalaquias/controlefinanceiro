from django.db import models
from imovel.models import Imovel
from djmoney.models.fields import MoneyField
from locatario.models import Locatario
from locador.models import Locador
from datetime import date
from django.utils import timezone
from datetime import datetime
import calendar
from django.db.models import Q

STATUS_CHOICES = (
    ("P", "Pago"),
    ("A", "Em Análise"),
    ("N", "Não pago"),
)

class PagamentoImovel(models.Model):
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE)
    locatario = models.ForeignKey(Locatario, on_delete=models.CASCADE)
    valor = MoneyField(max_digits=10, decimal_places=2, default_currency='BRL')
    data = models.DateField()
    status = models.CharField(choices=STATUS_CHOICES, default="A", max_length=20,  verbose_name="Status do pagamento")

    def __str__(self) -> str:
        return f'{self.data} | {self.locatario}'
    
class PagamentoAssinatura(models.Model):
    locador = models.ForeignKey(Locador, on_delete=models.CASCADE)
    valor = MoneyField(max_digits=10, decimal_places=2, default_currency='BRL')
    data = models.DateField()
    status = models.CharField(choices=STATUS_CHOICES, default="A", max_length=20,  verbose_name="Status do pagamento")
