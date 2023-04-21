from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import date, datetime
import calendar
from django.db.models import Q


class Locador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    data_nascimento_criacao = models.DateField()
    ultimo_pagamento = models.DateField(null=True, blank=True)
    telefone = models.CharField(null=True, blank=True, max_length=20)

    def __str__(self) -> str:
        if self.usuario:
            return f'{self.id} - {self.usuario.username} - {self.usuario.first_name}'
        else:
            return f'SEM USUARIO'
        
    def get_devedores(self, mes_referencia=None):
        from locatario.models import Locatario
        from pagamento.models import PagamentoImovel

        if not mes_referencia:
            mes_referencia = timezone.now().date()
        else:
            mes_referencia = datetime.strptime(mes_referencia, '%Y-%m').date()
        
        devedores = []
        inquilinos = Locatario.objects.filter(locador=self, imovel__isnull=False)
        
        for inquilino in inquilinos:
            inicio_mes = date(mes_referencia.year, mes_referencia.month, 1)
            fim_mes = date(mes_referencia.year, mes_referencia.month, calendar.monthrange(mes_referencia.year, mes_referencia.month)[1])
            pagamento_deste_mes = PagamentoImovel.objects.filter(locatario=inquilino).filter(Q(data__gte=inicio_mes, data__lte=fim_mes)).first()
            if pagamento_deste_mes:
                devedores.append(pagamento_deste_mes)
            else:
                devedores.append(PagamentoImovel(locatario=inquilino, imovel=inquilino.imovel, valor=0.0, status='N'))
            mes_referencia = mes_referencia + relativedelta(months=1)
        
        return devedores
