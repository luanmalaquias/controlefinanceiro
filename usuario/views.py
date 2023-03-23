from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Imovel
from usuario.models import Perfil
from pagamento.models import Pagamento
from .forms import PerfilForm, RecuperarSenhaForm, IncluirNoImovelForm, AutoCadastroForm
from utils.scripts import generatePassword, unmask, cpfIsValid
from django.shortcuts import get_object_or_404
from notificacao.models import Notificacao
from django.db.models import Q
from datetime import datetime, date
from utils.scripts import unmask, porcentagem
from utils import pixcodegen
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


# TODO usuario pode se auto-cadastrar

def criar_superusuario(request):
    # TODO criar super usuario
    # existe super usuario?
    #   sim : redirecionar imobiliaria
    #   nao : criar
    pass


@login_required
@staff_member_required
# FIXME refatorar com padrão CRUD
# FIXME refatorar para ingles
# FIXME criar view e form de login 
def criar_usuario(request):
    context = {}

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
            if perfil.imovel:
                imovel = Imovel.objects.get(id = perfil.imovel.id)
                imovel.alterarDisponibilidade(False)

            try:
                usuario.save()
                perfil.save()
            except:
                raise Exception

            return redirect('listarusuarios')        

    else:
        formUsuario = UserCreationForm()
        formPerfil = PerfilForm()
        formPerfil.ajustar_escolhas()

    context['formUsuario'] = formUsuario
    context['formPerfil'] = formPerfil

    return render(request, 'views/criar-usuario.html', context)


def autoCadastro(request):
    context = {}
    usuarioForm = UserCreationForm()
    perfilForm = AutoCadastroForm()
    context['usuarioForm'] = usuarioForm
    context['perfilForm'] = perfilForm
    context['senhaGerada'] = generatePassword(0)

    if request.method == 'POST':
        usuarioForm = UserCreationForm(request.POST)
        perfilForm = AutoCadastroForm(request.POST)

        context['usuarioForm'] = usuarioForm
        context['perfilForm'] = perfilForm

        # validação de erros
        errorsp = []
        cpf = unmask(request.POST.get('username'), '.-')
        telefone = unmask(request.POST.get('telefone'), ' ()-')
        if User.objects.filter(username = cpf):
            errorsp.append("CPF já cadastrado no sistema, tente fazer login")
        if not cpfIsValid(cpf):
            errorsp.append("CPF informado não é valido")
        if len(telefone) != 11:
            errorsp.append("Telefone invalido")

        if len(errorsp) == 0:
            if usuarioForm.is_valid() and perfilForm.is_valid():
                usuario = usuarioForm.save(commit=False)
                usuario.username = unmask(usuario.username, '.-')

                perfil = perfilForm.save(commit=False)
                perfil.usuario = usuario
                perfil.cpf = usuario.username
                perfil.telefone = unmask(perfil.telefone, ' ()-')

                try:
                    usuario.save()
                    perfil.save()
                    context['contaCriada'] = True
                except:
                    pass

        
        context['errorsp'] = errorsp

    # TODO desmascarar os dados
    # TODO verificar se o cpf é valido e possui 16 letras, caso contrario enviar erro

    return render(request, 'views/auto-cadastro-usuario.html', context)


@login_required
@staff_member_required
def listar_usuarios(request):
    context = {}
    
    perfis = Perfil.objects.all().order_by('imovel','-data_entrada_imovel','nome_completo')
    context['perfis'] = perfis

    if request.method == "GET":
        busca = request.GET.get('busca')
        if busca != None:
            perfis = Perfil.objects.all().filter(Q(nome_completo__contains=busca) | Q(cpf__contains=busca))
            context['perfis'] = perfis
            return render(request, 'views/listar-usuarios.html', context)

    return render(request, 'views/listar-usuarios.html', context)


@login_required
def readUser(request, id):
    context = {}

    # o usuário tem que ser o logado
    if request.user.is_staff == False:
        perfil = Perfil.objects.get(cpf = request.user.username)
        if id != perfil.id:
            return redirect('home-usuario')

    perfil = get_object_or_404(Perfil, pk=id)
    pagamentos = Pagamento.objects.filter(perfil = perfil).order_by('-data')
    mensagens = Notificacao.objects.filter(perfil = perfil).order_by('lido', 'datahora')
    msgsNaoLidas = len(Notificacao.objects.filter(perfil = perfil, lido = False))

    context['perfil'] = perfil
    context['pagamentos'] = pagamentos
    context['mensagens'] = mensagens
    context['msgsNaoLidas'] = msgsNaoLidas
    return render(request, 'views/read-user.html', context)


@login_required
@staff_member_required
def listUsersWithoutProperty(request):
    context = {}
    perfis = Perfil.objects.filter(imovel = None).order_by('nome_completo')
    context['perfis'] = perfis
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
                imovel_antes.alterarDisponibilidade(True)
            except:
                # usuario sem imovel antes da atualização
                pass

            if perfil.imovel:
                perfil.atualizar_data_entrada_imovel()
                imovel = Imovel.objects.get(id = perfil.imovel.id)
                imovel.alterarDisponibilidade(False)

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
        perfil.imovel.alterarDisponibilidade(True)
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


@login_required
@staff_member_required
def remover_do_imovel(request, id):
    perfil = get_object_or_404(Perfil, pk=id)
    perfil.imovel.alterarDisponibilidade(True)
    perfil.imovel = None
    perfil.save()

    Pagamento.objects.filter(perfil = perfil).delete()
    return redirect('listarusuarios')


@login_required
@staff_member_required
def incluir_no_imovel(request, id):
    context = {}

    perfil = get_object_or_404(Perfil,pk=id)

    if request.method == 'POST':
        form = IncluirNoImovelForm(request.POST, instance=perfil)
        form.ajustar_escolhas()
        if form.is_valid():
            perfil.imovel.alterarDisponibilidade(False)
            form.save()
            return redirect('listarusuarios')
    else:
        form = IncluirNoImovelForm(instance=perfil)
        form.ajustar_escolhas()

    context['perfil'] = perfil
    context['form'] = form

    return render(request, 'views/adicionar-imovel-usuario.html', context)


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
