from django.shortcuts import render, redirect
from django.urls import reverse
from locatario.models import Locatario
from django.utils import timezone
from datetime import datetime, date
import calendar
from pagamento.models import PagamentoImovel
from django.db.models import Q

def criar_pagamento_rapido_view(request, id_locatario, mes_referencia=None):
    if not mes_referencia or mes_referencia == 'None':
        mes_referencia = timezone.now()
    else:
        mes_referencia = datetime.strptime(mes_referencia, '%Y-%m').date()

    locatario = Locatario.objects.get(pk=id_locatario)
    inicio_mes = date(timezone.now().year, timezone.now().month, 1)
    fim_mes = date(timezone.now().year, timezone.now().month, calendar.monthrange(timezone.now().year, timezone.now().month)[1])
    pagamento_deste_mes = PagamentoImovel.objects.filter(locatario=locatario).filter(Q(data__gte=inicio_mes, data__lte=fim_mes)).first()
    if pagamento_deste_mes:
        if pagamento_deste_mes.status == 'N' or pagamento_deste_mes.status == 'A':
            pagamento_deste_mes.status = 'P' 
            pagamento_deste_mes.save()
            return redirect(f'/locador/devedores/?mes_referencia={mes_referencia.strftime("%Y-%m")}')
    mes_referencia_new = date(mes_referencia.year, mes_referencia.month, timezone.now().day)
    PagamentoImovel.objects.create(locatario=locatario, imovel=locatario.imovel, valor=float(locatario.imovel.mensalidade.replace(',','.')), data=mes_referencia_new, status='P')
    
    return redirect(f'/locador/devedores/?mes_referencia={mes_referencia.strftime("%Y-%m")}')


def deletar_pagamento_rapido_view(request, id_locatario, mes_referencia=None):
    if not mes_referencia or mes_referencia == 'None':
        mes_referencia = timezone.now()
    else:
        mes_referencia = datetime.strptime(mes_referencia, '%Y-%m').date()

    PagamentoImovel.objects.get(pk=id_locatario).delete()
    return redirect(f'/locador/devedores/?mes_referencia={mes_referencia.strftime("%Y-%m")}')
