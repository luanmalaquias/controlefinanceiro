from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Imovel
from usuario.models import Perfil
from .forms import PerfilForm, RecuperarSenhaForm, IncluirNoImovelForm
from utils.scripts import generatePassword, unmask
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
            usuario.username = unmask(usuario.username, '-.,')
            
            # igualar login do usuario com o cpf do perfil
            perfil = formPerfil.save(commit=False)
            perfil.telefone = unmask(perfil.telefone, ' ()-')
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
        formPerfil.ajustar_escolhas()

    context['formUsuario'] = formUsuario
    context['formPerfil'] = formPerfil

    return render(request, 'views/criar-usuario.html', context)

@login_required
@staff_member_required
def listar_usuarios(request):
    context = {}
    
    perfis = Perfil.objects.all().order_by('imovel','-data_entrada_imovel','nome_completo')
    context['perfis'] = perfis

    if request.method == "GET":
        busca = request.GET.get('busca')
        if busca != None:
            perfis = Perfil.objects.all().filter(nome_completo__contains = busca)
            context['perfis'] = perfis
            return render(request, 'views/listar-usuarios.html', context)
    
    try:
        Imovel.objects.get()
        tem_imoveis = True
    except:
        tem_imoveis = False
    context['tem_imoveis'] = tem_imoveis

    return render(request, 'views/listar-usuarios.html', context)

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
        formPerfil.ajustar_escolhas(perfil)

    context['tem_imoveis'] = tem_imoveis
    context['perfil'] = perfil
    context['formPerfil'] = formPerfil
    
    return render(request, 'views/editar-perfil.html', context)

@login_required
@staff_member_required
def editar_usuario(request, id):
    context = {}

    perfil = get_object_or_404(Perfil, pk=id)
    usuario = get_object_or_404(User, pk=perfil.usuario.id)
    senhaGerada = generatePassword(2)

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
    context['senhaGerada'] = senhaGerada
    return render(request, 'views/editar-usuario.html', context)

@login_required
@staff_member_required
def deletar_usuario(request, id):
    perfil = get_object_or_404(Perfil, pk=id)
    usuario = get_object_or_404(User, pk=perfil.usuario.id)
    try:
        perfil.imovel.alterar_disponibilidade(True)
    except: pass
    usuario.delete()
    return redirect('listarusuarios')

def recuperar_senha(request):
    context = {}

    formPerfil = RecuperarSenhaForm()

    if request.method == "POST":
        formPerfil = RecuperarSenhaForm(request.POST)

        if formPerfil.is_valid():
            # get perfil
            cpf = formPerfil.cleaned_data['cpf']
            cpf = unmask(cpf, '.-')
            data_nascimento = formPerfil.cleaned_data['data_de_nascimento']
            data_nascimento = unmask(data_nascimento, '/')

            usuario = None

            # get usuario
            try:
                perfil = Perfil.objects.get(cpf = cpf, data_nascimento = data_nascimento)
                usuario = User.objects.get(username = perfil.cpf)
                context['usuario'] = usuario
            except:
                context['erro'] = 'Usuario não encontrado!'

            # tentar salvar
            try:
                senha1 = request.POST['password1']
                senha2 = request.POST['password2']
                if senha1 == senha2:
                    usuario.set_password(senha1)
                    usuario.save()
                    return redirect('login')
            except:
                pass

    context['formPerfil'] = formPerfil
    return render(request, 'registration/recoverpassword.html', context)

def remover_do_imovel(request, id):
    perfil = get_object_or_404(Perfil, pk=id)
    perfil.imovel.alterar_disponibilidade(True)
    perfil.imovel = None
    perfil.save()
    return redirect('listarusuarios')

def incluir_no_imovel(request, id):
    context = {}

    perfil = get_object_or_404(Perfil,pk=id)

    if request.method == 'POST':
        form = IncluirNoImovelForm(request.POST, instance=perfil)
        form.ajustar_escolhas()
        if form.is_valid():
            perfil.imovel.alterar_disponibilidade(False)
            form.save()
            return redirect('listarusuarios')
    else:
        form = IncluirNoImovelForm(instance=perfil)
        form.ajustar_escolhas()

    context['perfil'] = perfil
    context['form'] = form

    return render(request, 'views/adicionar-imovel-usuario.html', context)
