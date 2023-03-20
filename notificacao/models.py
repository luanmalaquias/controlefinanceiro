from django.db import models
from usuario.models import Perfil

class Notificacao(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, verbose_name="Usuario")
    datahora = models.DateTimeField(auto_now_add=True, verbose_name="Data/hora da notificacao")
    mensagem = models.TextField(verbose_name="Mensagem")
    lido = models.BooleanField(default=False, verbose_name="Notificação lida?")
    resolvido = models.BooleanField(default=False, verbose_name="Problema resolvido?")

    def __str__(self) -> str:
        nome = str(self.perfil.nome_completo.split(' ')[0])
        data = str(self.datahora.strftime("%H:%M %d/%m/%y"))
        return f'{nome} {data}'