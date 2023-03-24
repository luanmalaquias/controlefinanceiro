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


# FIXME refatorar com padrão CRUD
# FIXME refatorar para ingles

def register(request):
    context = {}

    userForm = UserCreationForm()
    profileForm = AutoCadastroForm()
    context['usuarioForm'] = userForm
    context['perfilForm'] = profileForm
    context['senhaGerada'] = generatePassword(0)

    if request.method == 'POST':
        userForm = UserCreationForm(request.POST)
        profileForm = AutoCadastroForm(request.POST)

        context['usuarioForm'] = userForm
        context['perfilForm'] = profileForm

        cpf = unmask(request.POST.get('username'), '.-')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        phone = unmask(request.POST.get('telefone'), ' ()-')
        birth = request.POST.get('data_nascimento')

        errors = []
        if User.objects.filter(username = cpf):
            errors.append("CPF já cadastrado no sistema, tente fazer login.")
        if not cpfIsValid(cpf) or len(cpf) != 11:
            errors.append("CPF informado não é valido.")
        if len(phone) != 11:
            errors.append("Telefone invalido.")
        if pass1 != pass2:
            errors.append("Senhas não conferem.")
        if len(pass1) < 8:
            errors.append("Senha fraca.")
        if len(birth) != 10 and len(birth) != 0:
            errors.append("Data de nascimento inválida.")

        if len(errors) == 0:
            if userForm.is_valid() and profileForm.is_valid():
                user = userForm.save(commit=False)
                user.username = unmask(user.username, '.-')                

                profile = profileForm.save(commit=False)
                profile.usuario = user
                profile.cpf = user.username
                profile.telefone = unmask(profile.telefone, ' ()-')

                try:
                    if User.objects.count() == 0:
                        User.objects.create_superuser(username=unmask(request.POST.get('username'), '.-'), password=request.POST.get('password1'))
                    else:
                        user.save()
                        profile.save()
                except: pass
                context['contaCriada'] = True
        
        context['errors'] = errors

    return render(request, 'views/auto-cadastro-usuario.html', context)


def recoverPassword(request):
    context = {}

    if request.method == "POST":
        cpf = unmask(request.POST.get('cpf'), '.-')
        birth = request.POST.get('dataNascimento')
        birthFinal = birth.split('-')
        try:
            birthFinal = datetime(int(birthFinal[0]), int(birthFinal[1]), int(birthFinal[2]))
        except:
            birthFinal = None
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        errors = []
        profile = Perfil.objects.filter(cpf = cpf, data_nascimento = birthFinal).first()
        if not profile:
            errors.append("CPF ou data de nascimento inválido.")
        if password1 != password2:
            errors.append("Senhas não conferem.")
        if len(birth) != 10:
            errors.append("Data de nascimento inválida.")

        if len(errors) == 0:
            profile.usuario.set_password(str(password1))
            profile.usuario.save()
            return redirect('loginPage')

        context['errors'] = errors
    return render(request, 'views/recover-password.html', context)


@login_required
@staff_member_required
def createUser(request):
    context = {}

    context['senhaGerada'] = generatePassword(0)

    if request.method == 'POST':
        userForm = UserCreationForm(request.POST)  
        profileForm = PerfilForm(request.POST)

        if userForm.is_valid() and profileForm.is_valid():
            user = userForm.save(commit=False)
            user.username = unmask(user.username, '-.,')
            
            # igualar login do usuario com o cpf do perfil
            profile = profileForm.save(commit=False)
            profile.telefone = unmask(profile.telefone, ' ()-')
            profile.cpf = user.username
            profile.usuario = user

            # alterar disponibilidade do imovel
            if profile.imovel:
                property = Imovel.objects.get(id = profile.imovel.id)
                property.alterarDisponibilidade(False)

            try:
                user.save()
                profile.save()
            except:
                raise Exception

            return redirect('listarusuarios')        

    else:
        userForm = UserCreationForm()
        profileForm = PerfilForm()
        profileForm.ajustar_escolhas()

    context['formUsuario'] = userForm
    context['formPerfil'] = profileForm

    return render(request, 'views/criar-usuario.html', context)


@login_required
@staff_member_required
def listUsers(request):
    context = {}
    
    profiles = Perfil.objects.all().order_by('imovel','-data_entrada_imovel','nome_completo')
    context['perfis'] = profiles

    if request.method == "GET":
        search = request.GET.get('busca')
        if search != None:
            profiles = Perfil.objects.all().filter(Q(nome_completo__contains=search) | Q(cpf__contains=search))
            context['perfis'] = profiles
            return render(request, 'views/listar-usuarios.html', context)

    return render(request, 'views/listar-usuarios.html', context)


@login_required
def readUser(request, id):
    context = {}

    # o usuário tem que ser o logado
    if request.user.is_staff == False:
        profile = Perfil.objects.get(cpf = request.user.username)
        if id != profile.id:
            return redirect('read-user', profile.id)

    profile = get_object_or_404(Perfil, pk=id)
    payments = Pagamento.objects.filter(perfil = profile).order_by('-data')
    messages = Notificacao.objects.filter(perfil = profile).order_by('lido', 'datahora')
    unreadMessages = len(Notificacao.objects.filter(perfil = profile, lido = False))

    context['perfil'] = profile
    context['pagamentos'] = payments
    context['mensagens'] = messages
    context['msgsNaoLidas'] = unreadMessages    
    return render(request, 'views/read-user.html', context)


@login_required
@staff_member_required
def listUsersWithoutProperty(request):
    context = {}
    profiles = Perfil.objects.filter(imovel = None).order_by('nome_completo')
    context['perfis'] = profiles
    return render(request, 'views/listar-usuarios.html', context)


@login_required
@staff_member_required
def updateProfile(request, id):
    context = {}

    properties = Imovel.objects.all()
    hasProperty = True if len(properties) > 0 else False

    profile = get_object_or_404(Perfil, pk=id,)
    profileForm = PerfilForm(instance=profile)

    if request.method == 'POST':
        profileForm = PerfilForm(request.POST, instance=profile)
        if profileForm.is_valid():

            # check this
            # alterar disponibilidade do imovel
            try:
                profileBefore = Perfil.objects.get(id = id)
                propertyBefore = Imovel.objects.get(id = profileBefore.imovel.id)
                propertyBefore.alterarDisponibilidade(True)
            except:
                # usuario sem imovel antes da atualização
                pass

            if profile.imovel:
                profile.atualizar_data_entrada_imovel()
                property = Imovel.objects.get(id = profile.imovel.id)
                property.alterarDisponibilidade(False)

            profile = profileForm.save()
            return redirect('listarusuarios')
        
    else:
        profileForm = PerfilForm(instance = profile)
        profileForm.ajustar_escolhas(profile)

    context['tem_imoveis'] = hasProperty
    context['perfil'] = profile
    context['formPerfil'] = profileForm
    
    return render(request, 'views/editar-perfil.html', context)


@login_required
@staff_member_required
def updateUser(request, id):
    context = {}

    profile = get_object_or_404(Perfil, pk=id)
    user = get_object_or_404(User, pk=profile.usuario.id)

    if request.method == 'POST':
        userForm = UserCreationForm(request.POST, instance=user)
        if userForm.is_valid():
            user = userForm.save()
            return redirect('listarusuarios')
    
    else:
        userForm = UserCreationForm(instance = user)

    context['formUsuario'] = userForm
    context['usuario'] = user
    context['perfil'] = profile
    context['senhaGerada'] = generatePassword(2)
    return render(request, 'views/editar-usuario.html', context)


@login_required
@staff_member_required
def deleteUserAndProfile(request, id):
    profile = get_object_or_404(Perfil, pk=id)
    user = get_object_or_404(User, pk=profile.usuario.id)

    if profile.imovel:
        profile.imovel.alterarDisponibilidade(True)
    
    user.delete()
    return redirect('listarusuarios')


@login_required
@staff_member_required
def removeFromProperty(request, id):
    profile = get_object_or_404(Perfil, pk=id)

    profile.imovel.alterarDisponibilidade(True)
    profile.imovel = None
    profile.save()

    Pagamento.objects.filter(perfil = profile).delete()
    return redirect('listarusuarios')


@login_required
@staff_member_required
def includeInProperty(request, id):
    context = {}

    profile = get_object_or_404(Perfil,pk=id)

    if request.method == 'POST':
        form = IncluirNoImovelForm(request.POST, instance=profile)
        form.ajustar_escolhas()
        if form.is_valid():
            profile.imovel.alterarDisponibilidade(False)
            form.save()
            return redirect('listarusuarios')
    else:
        form = IncluirNoImovelForm(instance=profile)
        form.ajustar_escolhas()

    context['perfil'] = profile
    context['form'] = form

    return render(request, 'views/adicionar-imovel-usuario.html', context)


# USUARIO
@login_required
def homeUser(request):
    context = {}

    profile = Perfil.objects.get(usuario=request.user)
    payments = Pagamento.objects.filter(perfil=profile)
    todayDateTime = datetime.now()
    dotayDate = date(todayDateTime.year, todayDateTime.month, todayDateTime.day)

    # Faturas
    invoices = []
    if profile.imovel:
        dateEntryProperty = date(profile.data_entrada_imovel.year, profile.data_entrada_imovel.month, profile.imovel.vencimento)
        passedMonths = relativedelta(date.today(), dateEntryProperty).months
        referrenceMonth = dateEntryProperty

        # FIXME ajeitar isso daqui
        for _ in range(passedMonths+1):
            thisMonthPaid = False
            for p in payments:
                if (p.status == "P" or p.status == "A") and (p.data.month == referrenceMonth.month and p.data.year == referrenceMonth.year):
                    thisMonthPaid = True
                    break

            if thisMonthPaid:
                invoices.append({"pagamento": p})
            else:
                payments = Pagamento(perfil=profile)
                payments.status = "N"
                # aplicar juros
                lateDays = (dotayDate-referrenceMonth).days
                if lateDays > 0:
                    amountWithInterest = int(porcentagem(1, valor=profile.imovel.mensalidade, porcentagem=lateDays))
                    payments.valor_pago = amountWithInterest
                else:
                    payments.valor_pago = profile.imovel.mensalidade
                payments.data = referrenceMonth
                payload = pixcodegen.Payload('Luan dos Santos Sousa', '10421063475', str(payments.valor_pago), 'Joao Pessoa', 'IMOBILIARIA')
                invoices.append({"pagamento": payments, "diasAtrasados": lateDays, 'brcode': payload.crc16, 'b64qrcode': payload.base64})
            referrenceMonth = date(referrenceMonth.year, referrenceMonth.month + 1, referrenceMonth.day)
    invoices = invoices[::-1]

    if request.method == 'POST':
        dataPayment = request.POST.get('dadosPagamento')

        payments = Pagamento(perfil = profile)
        payments.valor_pago = dataPayment
        payments.data = todayDateTime

        try:
            payments = Pagamento.objects.get(perfil=profile, data=payments.data)
            payments.status = "A"
            payments.save()
        except:
            payments.save()

        return redirect('home-usuario')

    context['hojeDateTime'] = todayDateTime
    context['hojeDate'] = dotayDate
    context['perfil'] = profile
    context['faturas'] = invoices
    return render(request, 'views/usuario/home-usuario.html', context)


@login_required
def userPaymentHistory(request):
    context = {}

    profile = Perfil.objects.get(usuario=request.user)
    payments = Pagamento.objects.filter(perfil=profile)

    if profile.imovel:
        dateEntryProperty = profile.data_entrada_imovel
        today = date(datetime.now().year, datetime.now().month, datetime.now().day)
        passedMonths = relativedelta(today, dateEntryProperty).months

        # FIXME ajeitar isso daqui
        paymentsArray = []        
        for _ in range(passedMonths+1):
            paid = False
            for p in payments:
                if p.data.month == dateEntryProperty.month and p.data.year == dateEntryProperty.year:
                    paymentsArray.insert(0,
                        {'mes_referencia': dateEntryProperty, 
                        'status': p.status, 
                        'vencimento': p.perfil.imovel.vencimento, 
                        'mensalidade': p.perfil.imovel.mensalidade, 
                        'valor_pago': p.valor_pago, 
                        'data_pagamento': p.data})
                    paid = True
                    continue
            if not paid:
                paymentsArray.insert(0,
                    {'mes_referencia': dateEntryProperty, 
                    'status': 'Aguardando', 
                    'vencimento': profile.imovel.vencimento, 
                    'mensalidade': profile.imovel.mensalidade, 
                    'valor_pago': '--', 
                    'data_pagamento': ''})
            dateEntryProperty += relativedelta(months=1)

        context['pagamentos'] = paymentsArray
    
    return render(request, 'views/usuario/historico-usuario.html', context)
