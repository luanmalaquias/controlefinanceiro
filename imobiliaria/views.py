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
from django.db.models import Q



@login_required
def indexImobiliaria(request):
    if not request.user.is_staff:
        return redirect('home-usuario')

    context = {}

    imoveis = Imovel.objects.all()
    perfis = Perfil.objects.all()
    pagamentos = Pagamento.objects.all()

    imoveisDisponiveis = Imovel.objects.filter(disponibilidade=True)
    perfisSemImovel = Perfil.objects.filter(imovel=None)
    
    devedoresDesteMes = []
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
            devedoresDesteMes.append(perfil)

    rendimentoTotal = 0
    for pagamento in pagamentos:
        rendimentoTotal += int(unmask(pagamento.valor_pago, '.'))
    
    rendimentoMensal = 0
    for imovel in imoveis:
        if imovel.disponibilidade == False:
            rendimentoMensal += int(imovel.mensalidade)

    # FIXME remover gerar dados isso daqui quando for implantar
    # gerarDados(2)

    # TODO levar pra area de cadastro de superusuario se não existir

    # quando o usuario nao tiver perfil
    usuarioLogado = request.user
    if request.user.is_staff == False:
        perfil = Perfil.objects.get(usuario = usuarioLogado)
        context['perfil'] = perfil

    context['imoveis'] = imoveis
    context['perfis'] = perfis
    context['pagamentos'] = pagamentos
    context['imoveisDisponiveis'] = imoveisDisponiveis
    context['perfisSemImovel'] = perfisSemImovel
    context['devedoresDesteMes'] = devedoresDesteMes
    context['rendimentoTotal'] = rendimentoTotal
    context['rendimentoMensal'] = rendimentoMensal
    context['hoje'] = hoje

    return render(request, 'index-imobiliaria.html', context)


@login_required
@staff_member_required
def cadastrarImovel(request):
    context = {}
    if request.method == 'POST':
        formImovel = ImovelForm(request.POST)
        if formImovel.is_valid():
            imovel = formImovel.save(commit=False)
            imovel.mensalidade = unmask(imovel.mensalidade, '.,')
            imovel.save()
            return redirect('listarimoveis')
    else:
        formImovel = ImovelForm()
    context['formImovel'] = formImovel
    return render(request, 'views/criar-imovel.html', context)


@login_required
@staff_member_required
def listarImoveis(request):
    context = {}
    imoveis = Imovel.objects.all().order_by('-disponibilidade','nome')
    context['imoveis'] = imoveis

    if request.method == "GET":
        busca = request.GET.get('busca')
        if busca != None:
            imoveis = Imovel.objects.all().filter(Q(nome__contains=busca) | Q(cep__contains=busca) | Q(endereco__contains=busca) | Q(bairro__contains=busca) | Q(cidade__contains=busca) | Q(uf__contains=busca)).order_by('-disponibilidade','nome')
            context['imoveis'] = imoveis
            return render(request, 'views/listar-imoveis.html', context)

    return render(request, 'views/listar-imoveis.html', context)


@login_required
def readProperty(request, id):
    context = {}

    # o imovel tem que ser do usuario
    if request.user.is_staff == False:
        perfil = Perfil.objects.get(cpf = request.user.username)
        if id != perfil.imovel.id:
            return redirect('home-usuario')

    imovel = get_object_or_404(Imovel, pk=id)
    inquilino = Perfil.objects.filter(imovel = imovel)
    inquilino = inquilino[0] if len(inquilino) > 0 else None
    pagamentos = []
    if inquilino:
        pagamentos = Pagamento.objects.filter(perfil = inquilino)

    context['imovel'] = imovel
    context['inquilino'] = inquilino
    context['pagamentos'] = pagamentos if pagamentos else []
    return render(request, 'views/read-property.html', context)


@login_required
@staff_member_required
def listAvailableProperties(request):
    context = {}
    availableProperties = Imovel.objects.filter(disponibilidade = True).order_by('nome')
    context['imoveis'] = availableProperties
    return render(request, 'views/listar-imoveis.html', context)



@login_required
@staff_member_required
def atualizarDadosImovel(request, id):
    context = {}

    imovel = get_object_or_404(Imovel, pk=id)
    formImovel = ImovelForm(instance=imovel)

    if request.method == 'POST':
        formImovel = ImovelForm(request.POST, instance=imovel)
        if formImovel.is_valid():
            imovel = formImovel.save(commit=False)
            imovel.mensalidade = unmask(imovel.mensalidade, '.,')
            imovel.save()
            return redirect('listarimoveis')
        
    context['formImovel'] = formImovel
    context['imovel'] = imovel
        
    return render(request, 'views/criar-imovel.html', context)


@login_required
@staff_member_required
def deletarImovel(request, id):
    imovel = get_object_or_404(Imovel, pk=id)
    imovel.delete()
    return redirect('listarimoveis')


# USUARIO
@login_required
def homeUsuario(request):
    context = {}

    perfil = Perfil.objects.get(usuario=request.user)
    pagamentos = Pagamento.objects.filter(perfil=perfil)
    hojeDateTime = datetime.now()
    hojeDate = date(hojeDateTime.year, hojeDateTime.month, hojeDateTime.day)

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
                diasAtrasados = (hojeDate-mesReferencia).days
                if diasAtrasados > 0:
                    valorComJuros = int(porcentagem(1, valor=perfil.imovel.mensalidade, porcentagem=diasAtrasados))
                    pagamento.valor_pago = valorComJuros
                else:
                    pagamento.valor_pago = perfil.imovel.mensalidade
                pagamento.data = mesReferencia
                payload = pixcodegen.Payload('Luan dos Santos Sousa', '10421063475', str(pagamento.valor_pago), 'Joao Pessoa', 'IMOBILIARIA')
                faturas.append({"pagamento": pagamento, "diasAtrasados": diasAtrasados, 'brcode': payload.crc16, 'b64qrcode': payload.base64})
            mesReferencia = date(mesReferencia.year, mesReferencia.month + 1, mesReferencia.day)
    faturas = faturas[::-1]

    if request.method == 'POST':
        dadosPagamento = request.POST.get('dadosPagamento')

        pagamento = Pagamento(perfil = perfil)
        pagamento.valor_pago = dadosPagamento
        pagamento.data = hojeDateTime

        try:
            pagamento = Pagamento.objects.get(perfil=perfil, data=pagamento.data)
            pagamento.status = "A"
            pagamento.save()
        except:
            pagamento.save()

        return redirect('home-usuario')

    context['hojeDateTime'] = hojeDateTime
    context['hojeDate'] = hojeDate
    context['perfil'] = perfil
    context['faturas'] = faturas
    return render(request, 'views/usuario/home-usuario.html', context)


@login_required
def historicoUsuario(request):
    context = {}

    perfil = Perfil.objects.get(usuario=request.user)
    pagamentos = Pagamento.objects.filter(perfil=perfil)

    if perfil.imovel:
        dataEntradaImovel = perfil.data_entrada_imovel
        hoje = date(datetime.now().year, datetime.now().month, datetime.now().day)
        mesesPassados = relativedelta(hoje, dataEntradaImovel).months

        pagamentosArray = []
        
        for _ in range(mesesPassados+1):
            pago = False
            for p in pagamentos:
                if p.data.month == dataEntradaImovel.month and p.data.year == dataEntradaImovel.year:
                    pagamentosArray.insert(0,
                        {'mes_referencia': dataEntradaImovel, 
                        'status': p.status, 
                        'vencimento': p.perfil.imovel.vencimento, 
                        'mensalidade': p.perfil.imovel.mensalidade, 
                        'valor_pago': p.valor_pago, 
                        'data_pagamento': p.data})
                    pago = True
                    continue
            if not pago:
                pagamentosArray.insert(0,
                    {'mes_referencia': dataEntradaImovel, 
                    'status': 'Aguardando', 
                    'vencimento': perfil.imovel.vencimento, 
                    'mensalidade': perfil.imovel.mensalidade, 
                    'valor_pago': '--', 
                    'data_pagamento': ''})
            dataEntradaImovel += relativedelta(months=1)

        context['pagamentos'] = pagamentosArray
    
    return render(request, 'views/usuario/historico-usuario.html', context)