from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from usuario.models import Perfil
from .models import Imovel
from .forms import ImovelForm

# Create your views here.

@login_required
def index_imobiliaria(request):
    # TODO levar pra area de cadastro de superusuario se não existir

    # FIXME isso é para quando o usuario tem perfil, e se o usuario não tiver perfil?
    usuario_logado = request.user
    context = {}
    try:
        perfil = Perfil.objects.get(usuario = usuario_logado)
        context['perfil'] = perfil
    except:
        pass

    # permitir que só possa criar usuario se existir pelo menos 1 imóvel
    imoveis = Imovel.objects.all()
    tem_imoveis = True if len(imoveis) > 0 else False
    context['tem_imoveis'] = tem_imoveis

    return render(request, 'index.html', context)

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
    return render(request, 'create.html', context)

@login_required
@staff_member_required
def listar_imoveis(request):
    context = {}
    imoveis = Imovel.objects.all()
    context['imoveis'] = imoveis
    return render(request, 'list.html', context)

@login_required
@staff_member_required
def alterar_dados_imoveis(request):
    # TODO alterar_dados_imoveis
    pass
