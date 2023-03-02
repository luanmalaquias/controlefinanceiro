from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from usuario.models import Perfil
from .models import Imovel
from .forms import ImovelForm
from django.shortcuts import get_object_or_404
# FIXME remover isso daqui quando for implantar
from utils.scripts import gerarDados, unmask

# Create your views here.

@login_required
def index_imobiliaria(request):
    context = {}

    # FIXME remover isso daqui quando for implantar
    # gerarDados(5)

    # TODO levar pra area de cadastro de superusuario se não existir

    # quando o usuario nao tiver perfil
    usuario_logado = request.user
    try:
        perfil = Perfil.objects.get(usuario = usuario_logado)
        context['perfil'] = perfil
    except:
        pass

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