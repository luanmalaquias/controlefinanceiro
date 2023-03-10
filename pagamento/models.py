from django.db import models
from usuario.models import Perfil

STATUS_CHOICES = (
    ("P", "Pago"),
    ("A", "Em Análise"),
    ("N", "Não pago"),
)

class Pagamento(models.Model):
    # TODO on apagar perfil apagar o pagamento, para não ficar registros desnecessários
    perfil = models.ForeignKey(Perfil, null=True, on_delete=models.SET_NULL, verbose_name="Usuario pagador")
    status = models.CharField(choices=STATUS_CHOICES, default="A", max_length=20,  verbose_name="Status do pagamento")
    valor_pago = models.CharField(null = True, max_length=10, verbose_name="Valor pago")
    data = models.DateField(null=True, blank=True, verbose_name="Data do pagamento")

    def __str__(self) -> str:
        return f'{self.perfil}, {self.status}, {self.data}'