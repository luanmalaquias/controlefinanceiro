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
def listar_pagamentos_por_usuarios(request, dataParam=None):
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
    perfil_com_pagamento = []
    for perfil in perfis:
        encontrado = False
        if not perfil.imovel:
            continue
        for pagamento in pagamentos:
            encontrado = False
            if pagamento.perfil == perfil and pagamento.data.month == data_atual.month and pagamento.data.year == data_atual.year:
                perfil_com_pagamento.append(
                    {"id":perfil.id,
                    "nomeperfil":perfil.nome_completo, 
                    "nomeimovel":perfil.imovel.nome, 
                    "pagamento":pagamento.status,
                    "pagamentoid":pagamento.id, 
                    "vencimento":perfil.imovel.vencimento, 
                    "mensalidade": f'R$ {perfil.imovel.mensalidade}', 
                    "pagamentoefetuado": f'R$ {pagamento.valor_pago}', 
                    "data":pagamento.data})
                encontrado = True
                break
        if not encontrado:
            perfil_com_pagamento.append(
                {"id":perfil.id,
                "nomeperfil":perfil.nome_completo, 
                "nomeimovel":perfil.imovel.nome, 
                "pagamento":"N??o efetuado",
                "vencimento":perfil.imovel.vencimento, 
                "mensalidade": f'R$ {perfil.imovel.mensalidade}', 
                "pagamentoefetuado":"", 
                "data":"--/--/--"})
    
    # ordena????o
    perfil_com_pagamento.sort(key=_ordenar_lista)

    context['data_atual'] = data_atual
    context['perfilComPagamento'] = perfil_com_pagamento

    return render(request, 'views/listar-pagamentos.html', context)

@login_required
@staff_member_required
def listar_pagamentos(request):
    context = {}

    pagamentos = Pagamento.objects.all().order_by('-data')
    context['pagamentos'] = pagamentos

    return render(request, 'views/listar-todos-pagamentos.html', context)

@login_required
@staff_member_required
def criar_pagamento(request):
    context = {}
    form = PagamentoForm()

    hoje = datetime.now()

    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            pagamento = form.save(commit=False)
            
            # N??o permitir mais de um pagamento para o mesmo m??s
            pagamentos_do_usuario = Pagamento.objects.filter(perfil=pagamento.perfil)
            existe_pagamento_para_este_mes = False
            for p in pagamentos_do_usuario:
                if p.data.month == pagamento.data.month :
                    existe_pagamento_para_este_mes = True
                    if p.status == "A":
                        p.status = "P"
                        p.save()
                    break
            
            if existe_pagamento_para_este_mes:
                context['errop'] = True
                context['form'] = form
                return render(request, 'views/criar-pagamento.html', context)
            else:
                pagamento.save()
            return redirect('listar-pagamentos-por-usuarios')

    context['form'] = form
    return render(request, 'views/criar-pagamento.html', context)


@login_required
@staff_member_required
def criar_pagamento_rapido(request, id, data):
    context = {}
    newdata = data.split('-')
    newdata = datetime(day=datetime.now().day, month=int(newdata[1]), year=int(newdata[0]))

    perfil = get_object_or_404(Perfil, pk=id)

    pagamentos_do_usuario = Pagamento.objects.filter(perfil=perfil)

    # Verificar se existe pagamento para este m??s, se tiver ele troca o status de "A (Em analise)" para "P (pago)"
    # se n??o, ele criar um pagamento para este m??s
    existe_pagamentos_deste_mes = False
    for p in pagamentos_do_usuario:
        if p.data.month == newdata.month and p.data.year == newdata.year:
            existe_pagamentos_deste_mes = True
            if p.status == "A":
                p.status = "P"
                p.save()
    if not existe_pagamentos_deste_mes:
        Pagamento.objects.create(
            perfil = perfil, 
            status = "P", 
            valor_pago = perfil.imovel.mensalidade, 
            data = newdata
        ).save()
    
    return redirect('listar-pagamentos-por-usuarios-com-data', dataParam=data)


@login_required
@staff_member_required
def editar_pagamento(request, id, pagina:str, data:str = 'None'):
    context = {}
    pagamento = get_object_or_404(Pagamento, pk=id)
    form = PagamentoForm(instance = pagamento)

    if request.method == 'POST':
        form = PagamentoForm(request.POST, instance=pagamento)
        if form.is_valid():
            form.save()
            if data=='None':
                return redirect(pagina)
            else:
                return redirect('listar-pagamentos-por-usuarios-com-data', dataParam=data)
        else:
            print(form.errors)

    context['pagamento'] = pagamento
    context['form'] = form
    return render(request, 'views/criar-pagamento.html', context)


@login_required
@staff_member_required
def deletar_pagamento(request, id):
    get_object_or_404(Pagamento, pk=id).delete()
    return redirect('listar-todos-os-pagamentos')        


@login_required
@staff_member_required
def deletar_pagamento_rapido(request, id, data):
    context = {}
    newdata = data.split('-')
    newdata = datetime(day=datetime.now().day, month=int(newdata[1]), year=int(newdata[0]))

    get_object_or_404(Pagamento, pk=id).delete()

    return redirect('listar-pagamentos-por-usuarios-com-data', dataParam=data)

def _ordenar_lista(lista):
    return lista["vencimento"]