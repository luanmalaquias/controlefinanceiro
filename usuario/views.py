from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Imovel
from usuario.models import Perfil
from .forms import PerfilForm
from utils.scripts import generatePassword, unmaskCpf, unmaskPhone
from django.shortcuts import get_object_or_404

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
            
            # igualar login do usuario com o cpf do perfil
            perfil = formPerfil.save(commit=False)
            perfil.telefone = unmaskPhone(perfil.telefone)
            perfil.cpf = usuario.username
            perfil.usuario = usuario

            # alterar disponibilidade do imovel
            imovel = Imovel.objects.get(id = perfil.imovel.id)
            imovel.alterar_disponibilidade(False)

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

    if request.method == "GET":
        busca = request.GET.get('busca')
        if busca != None:
            perfis = Perfil.objects.all().filter(nome_completo__contains = busca)
            context['perfis'] = perfis
            return render(request, 'registration/list.html', context)
    
    try:
        Imovel.objects.get()
        tem_imoveis = True
    except:
        tem_imoveis = False
    context['tem_imoveis'] = tem_imoveis

    return render(request, 'registration/list.html', context)

@login_required
@staff_member_required
def editar_perfil(request, id):
    context = {}

    imoveis = Imovel.objects.all()
    tem_imoveis = True if len(imoveis) > 0 else False

    perfil = get_object_or_404(Perfil, pk=id,)
    formPerfil = PerfilForm(instance=perfil)

    if request.method == 'POST':
        formPerfil = PerfilForm(request.POST, instance=perfil)
        if formPerfil.is_valid():

            # alterar disponibilidade do imovel
            try:
                perfil_antes = Perfil.objects.get(id = id)
                imovel_antes = Imovel.objects.get(id = perfil_antes.imovel.id)
                imovel_antes.alterar_disponibilidade(True)
            except:
                # usuario sem imovel antes da atualização
                pass
            perfil.atualizar_data_entrada_imovel()
            imovel = Imovel.objects.get(id = perfil.imovel.id)
            imovel.alterar_disponibilidade(False)

            perfil = formPerfil.save()
            return redirect('listarusuarios')
        
    else:
        formPerfil = PerfilForm(instance = perfil)

    context['tem_imoveis'] = tem_imoveis
    context['perfil'] = perfil
    context['formPerfil'] = formPerfil
    
    return render(request, 'registration/editprofile.html', context)

@login_required
def editar_usuario(request, id):
    context = {}

    perfil = get_object_or_404(Perfil, pk=id)
    usuario = get_object_or_404(User, pk=perfil.usuario.id)

    if request.method == 'POST':
        formUsuario = UserCreationForm(request.POST, instance=usuario)
        if formUsuario.is_valid():
            usuario = formUsuario.save()
            return redirect('listarusuarios')
    
    else:
        formUsuario = UserCreationForm(instance = usuario)

    context['formUsuario'] = formUsuario
    context['usuario'] = usuario
    context['perfil'] = perfil
    
    return render(request, 'registration/edituser.html', context)

@login_required
@staff_member_required
def deletar_usuario(request, id):
    perfil = get_object_or_404(Perfil, pk=id)
    usuario = get_object_or_404(User, pk=perfil.usuario.id)
    perfil.imovel.alterar_disponibilidade(True)
    usuario.delete()
    return redirect('listarusuarios')

def recuperar_senha(request):
    # TODO recuperar senha da pagina de login
    pass
