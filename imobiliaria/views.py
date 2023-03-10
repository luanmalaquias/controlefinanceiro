from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from usuario.models import Perfil
from pagamento.models import Pagamento
from .models import Imovel
from .forms import ImovelForm
from django.shortcuts import get_object_or_404
# FIXME remover gerar dadosisso daqui quando for implantar
from utils.scripts import gerarDados, unmask, porcentagem
from utils import pixcodegen
from datetime import datetime, timedelta, time, date
from dateutil.relativedelta import relativedelta

# Create your views here.

@login_required
def index_imobiliaria(request):
    if not request.user.is_staff:
        return redirect('home-usuario')

    context = {}

    imoveis = Imovel.objects.all()
    perfis = Perfil.objects.all()
    pagamentos = Pagamento.objects.all()

    imoveis_disponiveis = Imovel.objects.filter(disponibilidade=True)
    perfis_sem_imovel = Perfil.objects.filter(imovel=None)
    
    devedores_deste_mes = []
    hoje = datetime.now()
    for perfil in perfis:
        pagou = False
        if perfil.imovel != None:
            for pagamento in pagamentos:
                if pagamento.perfil == perfil and pagamento.data.month == hoje.month and pagamento.data.year == hoje.year:
                    pagou = True
                    break
        else: continue
        if pagou == False:
            devedores_deste_mes.append(perfil)

    rendimento_total = 0
    for pagamento in pagamentos:
        rendimento_total += int(unmask(pagamento.valor_pago, '.'))
    
    rendimentoMensal = 0
    for imovel in imoveis:
        if imovel.disponibilidade == False:
            rendimentoMensal += int(imovel.mensalidade)

    # FIXME remover gerar dados isso daqui quando for implantar
    # gerarDados(5)

    # TODO levar pra area de cadastro de superusuario se não existir

    # quando o usuario nao tiver perfil
    usuario_logado = request.user
    if request.user.is_staff == False:
        perfil = Perfil.objects.get(usuario = usuario_logado)
        context['perfil'] = perfil

    context['imoveis'] = imoveis
    context['perfis'] = perfis
    context['pagamentos'] = pagamentos
    context['imoveis_disponiveis'] = imoveis_disponiveis
    context['perfis_sem_imovel'] = perfis_sem_imovel
    context['devedores_deste_mes'] = devedores_deste_mes
    context['rendimento_total'] = rendimento_total
    context['rendimentoMensal'] = rendimentoMensal
    context['hoje'] = hoje

    return render(request, 'index-imobiliaria.html', context)

@login_required
@staff_member_required
def cadastrar_imovel(request):
    context = {}
    if request.method == 'POST':
        formImovel = ImovelForm(request.POST)
        if formImovel.is_valid():
            formImovel.save()
            return redirect('listarimoveis')
    else:
        formImovel = ImovelForm()
    context['formImovel'] = formImovel
    return render(request, 'views/criar-imovel.html', context)

@login_required
@staff_member_required
def listar_imoveis(request):
    context = {}
    imoveis = Imovel.objects.all().order_by('-disponibilidade','nome')
    context['imoveis'] = imoveis

    if request.method == "GET":
        busca = request.GET.get('busca')
        if busca != None:
            imoveis = Imovel.objects.all().filter(nome__contains = busca).order_by('-disponibilidade','nome')
            context['imoveis'] = imoveis
            return render(request, 'views/listar-imoveis.html', context)

    return render(request, 'views/listar-imoveis.html', context)

@login_required
@staff_member_required
def atualizar_dados_imovel(request, id):
    context = {}

    imovel = get_object_or_404(Imovel, pk=id)
    formImovel = ImovelForm(instance=imovel)

    if request.method == 'POST':
        formImovel = ImovelForm(request.POST, instance=imovel)
        if formImovel.is_valid():
            formImovel.save()
            return redirect('listarimoveis')
        
    context['formImovel'] = formImovel
    context['imovel'] = imovel
        
    return render(request, 'views/criar-imovel.html', context)

@login_required
@staff_member_required
def deletar_imovel(request, id):
    imovel = get_object_or_404(Imovel, pk=id)
    imovel.delete()
    return redirect('listarimoveis')


# USUARIO
@login_required
def home_usuario(request):
    context = {}

    perfil = Perfil.objects.get(usuario=request.user)
    # Pagamento.objects.filter(perfil = perfil).delete()
    # p = Pagamento.objects.create()
    # p.perfil = perfil; p.status = "P"; p.valor_pago = perfil.imovel.mensalidade; p.data = date.today(); p.save()
    pagamentos = Pagamento.objects.filter(perfil=perfil)
    hoje = date(datetime.now().year, datetime.now().month, datetime.now().day)

    faturas = []
    if perfil.imovel:
        dataEntradaImovel = date(perfil.data_entrada_imovel.year, perfil.data_entrada_imovel.month, perfil.imovel.vencimento)
        mesesPassados = relativedelta(date.today(), dataEntradaImovel).months
        mesReferencia = dataEntradaImovel

        for _ in range(mesesPassados+1):
            pagoMesAtual = False
            for p in pagamentos:
                if (p.status == "P" or p.status == "A") and (p.data.month == mesReferencia.month and p.data.year == mesReferencia.year):
                    pagoMesAtual = True
                    break

            if pagoMesAtual:
                faturas.append({"pagamento": p})
            else:
                pagamento = Pagamento(perfil=perfil)
                pagamento.status = "N"
                # aplicar juros
                diasAtrasados = (hoje-mesReferencia).days
                valorComJuros = int(porcentagem(1, valor=perfil.imovel.mensalidade, porcentagem=diasAtrasados))
                pagamento.valor_pago = valorComJuros
                pagamento.data = mesReferencia
                payload = pixcodegen.Payload('Luan dos Santos Sousa', '10421063475', str(valorComJuros), 'Joao Pessoa', 'IMOBILIARIA')
                faturas.append({"pagamento": pagamento, "diasAtrasados": diasAtrasados, 'brcode': payload.crc16, 'b64qrcode': payload.base64})
            mesReferencia = date(mesReferencia.year, mesReferencia.month + 1, mesReferencia.day)
    faturas = faturas[::-1]

    if request.method == 'POST':
        dadosPagamento = request.POST.get('dadosPagamento')
        dadosPagamento = dadosPagamento.split(':')
        dataRefPagamentoYMD = dadosPagamento[0].split('-')
        valorPagamento = dadosPagamento[1]

        pagamento = Pagamento(perfil = perfil)
        pagamento.valor_pago = valorPagamento
        pagamento.data = datetime(year=int(dataRefPagamentoYMD[0]), month=int(dataRefPagamentoYMD[1]), day=int(dataRefPagamentoYMD[2]))

        try:
            pagamento = Pagamento.objects.get(perfil=perfil, data=pagamento.data)
            pagamento.status = "A"
            pagamento.save()
        except:
            pagamento.save()

        return redirect('home-usuario')

    context['hoje'] = hoje
    context['perfil'] = perfil
    context['faturas'] = faturas
    return render(request, 'views/usuario/home-usuario.html', context)


@login_required
def historico_usuario(request):
    context = {}

    perfil = Perfil.objects.get(usuario=request.user)
    pagamentos = Pagamento.objects.filter(perfil=perfil)

    if perfil.imovel:
        data_entrada_imovel = perfil.data_entrada_imovel
        hoje = date(datetime.now().year, datetime.now().month, datetime.now().day)
        meses_passados = relativedelta(hoje, data_entrada_imovel).months

        pagamentos_array = []
        
        for _ in range(meses_passados+1):
            pago = False
            for p in pagamentos:
                if p.data.month == data_entrada_imovel.month and p.data.year == data_entrada_imovel.year:
                    pagamentos_array.insert(0,
                        {'mes_referencia': data_entrada_imovel, 
                        'status': p.status, 
                        'vencimento': p.perfil.imovel.vencimento, 
                        'mensalidade': p.perfil.imovel.mensalidade, 
                        'valor_pago': p.valor_pago, 
                        'data_pagamento': p.data})
                    pago = True
                    continue
            if not pago:
                pagamentos_array.insert(0,
                    {'mes_referencia': data_entrada_imovel, 
                    'status': 'Aguardando', 
                    'vencimento': perfil.imovel.vencimento, 
                    'mensalidade': perfil.imovel.mensalidade, 
                    'valor_pago': '--', 
                    'data_pagamento': ''})
            data_entrada_imovel += relativedelta(months=1)

        context['pagamentos'] = pagamentos_array
    
    return render(request, 'views/usuario/historico-usuario.html', context)