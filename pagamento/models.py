from django.db import models
from usuario.models import Perfil
from django.core.validators import MaxValueValidator, MinValueValidator

STATUS_CHOICES = (
    ("P", "Pago"),
    ("A", "Em Análise"),
    ("N", "Não pago"),
)

class Pagamento(models.Model):
    perfil = models.ForeignKey(Perfil, null=True, on_delete=models.CASCADE, verbose_name="Usuario pagador")
    status = models.CharField(choices=STATUS_CHOICES, default="A", max_length=20,  verbose_name="Status do pagamento")
    valor_pago = models.IntegerField(null = True, verbose_name="Valor pago", validators=[MaxValueValidator(999999), MinValueValidator(0)])
    data = models.DateTimeField(null=True, blank=True, verbose_name="Data do pagamento")

    def __str__(self) -> str:
        return f'{self.perfil}, {self.status}, {self.data}'