from django.shortcuts import render, redirect
from .forms import *
from imobiliaria.forms import *
from imovel.models import Imovel
from locador.models import Locador
from django.contrib.auth.decorators import login_required
from imovel.forms import *
from django.shortcuts import get_object_or_404
from locatario.models import Locatario
from django.db.models import Q
from django.contrib import messages
from pagamento.models import PagamentoImovel, PagamentoAssinatura


def cadastro_view(request):
    context = {}
    if request.method == 'GET':
        form1 = CustomUserCreationForm()
        form2 = LocadorCreationForm()
    elif request.method == 'POST':
        form1 = CustomUserCreationForm(request.POST)
        form2 = LocadorCreationForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save(commit=False)
            form2.save(user)
            print('redirecionar locador para a pagina de pagamento')
            # return redirect('locador_pagamento_view')
    context['form1'] = form1
    context['form2'] = form2
    return render(request, 'views/cadastro_locador.html', context)


@login_required
def home_view(request):
    context = {}
    locador = Locador.objects.get(usuario=request.user)

    context['locador'] = locador
    return render(request, 'views/home_locador.html', context)


@login_required
def meus_imoveis_view(request):
    context = {}

    order_by = request.GET.get('order_by', 'id')
    direction = request.GET.get('direction', 'id')

    locador = Locador.objects.get(usuario=request.user)
    imoveis = Imovel.objects.filter(locador=locador).order_by(order_by)
    if request.method == 'GET':
        if request.GET.get('busca'):
            busca = request.GET.get('busca')
            imoveis = Imovel.objects.filter(locador=locador).order_by('disponivel')
            imoveis = imoveis.filter(Q(nome__icontains=busca) | Q(endereco__icontains=busca))

    context['order_by'] = order_by
    context['direction'] = direction
    context['imoveis'] = imoveis
    return render(request, 'views/imoveis_locador.html', context)


@login_required
def cadastro_imovel_view(request):
    form = ImovelCreationForm()

    if request.method == 'POST':
        form = ImovelCreationForm(request.POST)
        if form.is_valid():
            imovel = form.save(commit=False)
            locador = Locador.objects.get(usuario=request.user)
            imovel.locador = locador
            imovel.save()
            return redirect('imoveis_locador_view')

    return render(request, 'views/cadastro_imovel.html', {'form': form})


@login_required
def atualizar_imovel_view(request, id):
    context = {}

    locador = Locador.objects.get(usuario=request.user)
    imovel = get_object_or_404(Imovel, pk=id)

    if imovel.locador != locador:
        redirect('imoveis_locador_view')

    form = ImovelUpdateForm(instance=imovel)
    if request.method == 'POST':
        form = ImovelUpdateForm(request.POST, instance=imovel)
        if form.is_valid():
            form.save()
            return redirect('imoveis_locador_view')

    context['form'] = form
    context['imovel'] = True
    return render(request, 'views/cadastro_imovel.html', context)


@login_required
def remover_inquilino_do_imovel_view(request, tipo, id):
    if tipo == 'imovel':
        imovel = get_object_or_404(Imovel, pk=id)
        inquilino = get_object_or_404(Locatario, imovel=imovel)
    else:
        inquilino = get_object_or_404(Locatario, pk=id)
        imovel = inquilino.imovel

    imovel.disponivel = True
    inquilino.imovel = None
    inquilino.data_entrada_imovel = None
    imovel.save()
    inquilino.save()
    return redirect('imoveis_locador_view')


@login_required
def deletar_imovel_view(request, id):
    locador = Locador.objects.get(usuario=request.user)
    imovel = get_object_or_404(Imovel, pk=id)
    if imovel.locador != locador:
        redirect('imoveis_locador_view')
    imovel.delete()
    return redirect('imoveis_locador_view')


@login_required
def meus_inquilinos_view(request):
    context = {}

    order_by = request.GET.get('order_by', 'id')

    locador = Locador.objects.get(usuario=request.user)
    locatarios = Locatario.objects.filter(locador=locador).order_by(order_by)

    if request.method == 'GET':
        if request.GET.get('busca'):
            busca = request.GET.get('busca')
            locatarios = locatarios.filter(Q(usuario__first_name__icontains=busca) | Q(usuario__last_name__icontains=busca) | Q(imovel_nome__icontains=busca))

    context['inquilinos'] = locatarios
    context['order_by'] = order_by
    context['meu_id'] = locador.id
    return render(request, 'views/inquilinos_locador.html', context)


@login_required
def inquilino_ao_imovel_view(request, tipo, id):
    if tipo == 'imovel':
        form = LocatarioAoImovelForm(
            initial={'imovel': Imovel.objects.get(pk=id)})
    else:
        form = LocatarioAoImovelForm(
            initial={'locatario': Locatario.objects.get(pk=id)})

    if request.method == 'POST':
        form = LocatarioAoImovelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('imoveis_locador_view')

    return render(request, 'views/inquilino_ao_imovel.html', {'form': form})


@login_required
def ler_inquilino_view(request, id):
    locador = Locador.objects.get(usuario=request.user)
    inquilino = get_object_or_404(Locatario, pk=id)

    if inquilino.locador != locador:
        return redirect('inquilinos_locador_view')
    
    return render(request, 'views/ler_inquilino.html', {'inquilino': inquilino})


@login_required
def ler_imovel_view(request, id):
    locador = Locador.objects.get(usuario=request.user)
    imovel = get_object_or_404(Imovel, pk=id)

    if imovel.locador != locador:
        return redirect('imoveis_locador_view')
    
    return render(request, 'views/ler_imovel.html', {'imovel': imovel})


@login_required
def configuracoes_view(request):
    return render(request, 'views/configuracoes.html')


@login_required
def alterar_senha_view(request):
    context = {}
    form = UpdatePasswordForm(user=request.user)
    if request.method == 'POST':
        form = UpdatePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('logout_view')
    context['form'] = form
    return render(request, 'views/configuracoes/senha.html', context)


@login_required
def alterar_informacoes_da_conta_view(request):
    context = {}

    user = request.user
    locador = Locador.objects.get(usuario=user)
    locador.data_nascimento_criacao = locador.data_nascimento_criacao.strftime("%Y-%m-%d")
    
    form1 = CustomUpdateUserForm(instance=user)
    form2 = LocadorUpdateForm(instance=locador)

    if request.method == 'POST':
        form1 = CustomUpdateUserForm(instance=user, data=request.POST)
        form2 = LocadorUpdateForm(instance=locador, data=request.POST)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            messages.success(request, 'Dados atualizados com sucesso!')

    context['form1'] = form1
    context['form2'] = form2
    return render(request, 'views/configuracoes/conta.html', context)


@login_required
def devedores_view(request):
    context = {}
    locador = Locador.objects.get(usuario=request.user)
    
    mes_referencia = request.GET.get('mes_referencia')
    pagamentos = locador.get_devedores(mes_referencia)
    
    context['pagamentos'] = pagamentos
    context['mes_referencia'] = mes_referencia
    return render(request, 'views/devedores.html', context)


def pagamentos_locador_view(request):
    context = {}
    locador = Locador.objects.get(usuario=request.user)
    pagamentos_locador = PagamentoAssinatura.objects.filter(locador=locador)
    pagamentos_inquilinos = PagamentoImovel.objects.filter(locatario__locador=locador)

    context['pagamentos_locador'] = pagamentos_locador
    context['pagamentos_inquilinos'] = pagamentos_inquilinos
    return render(request, 'views/pagamentos_locador.html', context)