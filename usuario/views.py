from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import PerfilForm
from django.contrib.auth.forms import UserCreationForm
from .models import Imovel
from utils.scripts import generatePassword, unmaskCpf, unmaskPhone
from usuario.models import Perfil
from django.contrib.auth.models import User

# Create your views here.

def criar_superusuario(request):
    # TODO criar super usuario
    # existe super usuario?
    #   sim : redirecionar imobiliaria
    #   nao : criar
    pass

@login_required
@staff_member_required
def criar_usuario(request):
    context = {}

    imoveis = Imovel.objects.all()
    tem_imoveis = True if len(imoveis) > 0 else False
    context['tem_imoveis'] = tem_imoveis

    senhaGerada = generatePassword(0)
    context['senhaGerada'] = senhaGerada

    if request.method == 'POST':
        formUsuario = UserCreationForm(request.POST)  
        formPerfil = PerfilForm(request.POST)

        if formUsuario.is_valid() and formPerfil.is_valid():
            usuario = formUsuario.save(commit=False)
            usuario.username = unmaskCpf(usuario.username)           
            
            perfil = formPerfil.save(commit=False)
            perfil.telefone = unmaskPhone(perfil.telefone)
            perfil.cpf = usuario.username
            perfil.usuario = usuario

            usuario.save()
            perfil.save()

            return redirect('listarusuarios')        

    else:
        formUsuario = UserCreationForm()
        formPerfil = PerfilForm()

    context['formUsuario'] = formUsuario
    context['formPerfil'] = formPerfil

    return render(request, 'registration/create.html', context)

@login_required
@staff_member_required
def listar_usuarios(request):
    context = {}
    
    perfis = Perfil.objects.all()
    context['perfis'] = perfis
    
    try:
        Imovel.objects.get()
        tem_imoveis = True
    except:
        tem_imoveis = False
    context['tem_imoveis'] = tem_imoveis

    return render(request, 'registration/list.html', context)

@login_required
@staff_member_required
def alterar_dados_usuarios(request):
    # TODO alterar dados usuario
    pass

def recuperar_senha(request):
    # TODO recuperar senha
    pass

@login_required
def alterar_senha(request):
    # TODO alterar senha
    pass
