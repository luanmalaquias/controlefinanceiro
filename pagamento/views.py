from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Pagamento
from usuario.models import Perfil
from datetime import datetime
from .forms import PagamentoForm
from .models import Pagamento

# Create your views here.

@login_required
@staff_member_required
def monthlyDebtors(request, dataParam=None):
    context = {}

    # get objects
    pagamentos = Pagamento.objects.all().order_by('-status', '-data')
    perfis = Perfil.objects.all().order_by('imovel')

    # para referencia no calendario
    data_atual = datetime.now()
    
    # mudar a data
    if request.method == 'GET' or dataParam:
        data = None
        if request.GET.get('data'):
            data = (request.GET.get('data')).split('-')
        elif dataParam:
            data = dataParam.split('-')
        if data:
            mes_vigente = datetime(year=int(data[0]), month=int(data[1]), day=1)
            data_atual = mes_vigente

    # criar novos itens com os valores juntos
    pagamentosDesteMes = []
    for perfil in perfis:
        encontrado = False
        if not perfil.imovel:
            continue
        for pagamento in pagamentos:
            if pagamento.perfil == perfil and pagamento.data.month == data_atual.month and pagamento.data.year == data_atual.year:
                pagamentosDesteMes.append({'perfil':perfil, 'pagamento':pagamento})
                encontrado = True
                break
        if not encontrado:
            pagamentosDesteMes.append({'perfil':perfil, 'pagamento':Pagamento(perfil=perfil, status="N")})
    
    # ordenação
    pagamentosDesteMes.sort(key=_orderList)

    context['data_atual'] = data_atual
    context['pagamentosDesteMes'] = pagamentosDesteMes

    return render(request, 'views/listar-pagamentos.html', context)


@login_required
@staff_member_required
def listPayments(request):
    context = {}

    pagamentos = Pagamento.objects.all().order_by('-data').order_by('-status', '-data')

    if request.method == "GET":
        busca = request.GET.get('busca')
        if busca != None and busca != '':
            perfis = Perfil.objects.filter(nome_completo__contains = busca)
            if len(perfis)>0:
                pagamentos = Pagamento.objects.filter(perfil=perfis[0])
            else:
                pagamentos = []


    context['pagamentos'] = pagamentos

    return render(request, 'views/listar-todos-pagamentos.html', context)


@login_required
@staff_member_required
def createPayment(request):
    context = {}

    form = PagamentoForm()
    context['form'] = form

    profiles = Perfil.objects.all()

    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            
            # Não permitir mais de um pagamento para o mesmo mês
            userPayments = Pagamento.objects.filter(perfil=payment.perfil)
            thisMonthPayment = False
            for p in userPayments:
                if p.data.month == payment.data.month :
                    thisMonthPayment = True
                    if p.status == "A":
                        p.status = "P"
                        p.save()
                    break
            
            if thisMonthPayment:
                context['errop'] = True
                context['form'] = form
            else:
                payment.save()
                return redirect('listar-pagamentos-por-usuarios')

    context['temPerfis'] = True if len(profiles) > 0 else False
    return render(request, 'views/criar-pagamento.html', context)


@login_required
@staff_member_required
def quickCreatePayment(request, id, data):
    context = {}

    today = datetime.now()
    newDate = data.split('-')
    newDate = datetime(day=today.day, month=int(newDate[1]), year=int(newDate[0]), hour=today.hour, minute=today.minute)

    profile = get_object_or_404(Perfil, pk=id)

    userPayments = Pagamento.objects.filter(perfil=profile)

    # Verificar se existe pagamento para este mês, se tiver ele troca o status de "A (Em analise)" para "P (pago)"
    # se não, ele criar um pagamento para este mês
    thisMonthPayment = False
    for p in userPayments:
        if p.data.month == newDate.month and p.data.year == newDate.year:
            thisMonthPayment = True
            if p.status == "A":
                p.status = "P"
                p.save()
    if not thisMonthPayment:
        Pagamento.objects.create(
            perfil = profile, 
            status = "P", 
            valor_pago = profile.imovel.mensalidade, 
            data = newDate
        ).save()
    
    return redirect('listar-pagamentos-por-usuarios-com-data', dataParam=data)


@login_required
@staff_member_required
def updatePayment(request, id, pagina:str, data:str = 'None'):
    context = {}

    payment = get_object_or_404(Pagamento, pk=id)
    # hora com timezone local
    dateTime = datetime(payment.data.year, payment.data.month, payment.data.day, payment.data.hour-3, payment.data.minute)
    payment.data = dateTime.strftime("%Y-%m-%dT%H:%M")

    form = PagamentoForm(instance = payment)
    profiles = Perfil.objects.all()

    if request.method == 'POST':
        form = PagamentoForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            if data=='None':
                return redirect(pagina)
            else:
                return redirect('listar-pagamentos-por-usuarios-com-data', dataParam=data)
        else:
            print(form.errors)

    context['pagamento'] = payment
    context['form'] = form
    context['temPerfis'] = True if len(profiles) > 0 else False
    return render(request, 'views/criar-pagamento.html', context)


@login_required
@staff_member_required
def deletePayment(request, id):
    get_object_or_404(Pagamento, pk=id).delete()
    return redirect('listar-todos-os-pagamentos')        


@login_required
@staff_member_required
def quickDeletePayment(request, id, data):
    context = {}
    get_object_or_404(Pagamento, pk=id).delete()
    return redirect('listar-pagamentos-por-usuarios-com-data', dataParam=data)


def _orderList(list):
    return list["perfil"].imovel.vencimento