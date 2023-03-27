from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Imovel
from usuario.models import Perfil
from pagamento.models import Pagamento
from .forms import PerfilForm, ChangePasswordForm, IncluirNoImovelForm, AutoCadastroForm
from utils.scripts import generatePassword, unmask, cpfIsValid
from django.shortcuts import get_object_or_404
from notificacao.models import Notificacao
from django.db.models import Q
from datetime import datetime, date
from utils.scripts import unmask, porcentagem
from utils import pixcodegen
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


# FIXME refatorar para ingles

def register(request):
    context = {}

    generatedPass = generatePassword(0)
    form = AutoCadastroForm(initial={'password1': generatedPass, 'password2': generatedPass})
    context['form'] = form

    if request.method == 'POST':
        form = AutoCadastroForm(request.POST)

        context['form'] = form    

        if form.is_valid():            
            saved, errors = form.save()
            context['saved'] = saved
            context['errors'] = errors

    return render(request, 'views/auto-cadastro-usuario.html', context)


def recoverPassword(request):
    context = {}

    form = ChangePasswordForm()

    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            saved, errors = form.save()
            context['saved'] = saved
            context['errors'] = errors

    context['form'] = form
    return render(request, 'views/recover-password.html', context)


@login_required
@staff_member_required
def createUser(request):
    context = {}

    generatedPassword = generatePassword(0)
    form = PerfilForm(initial={'password1':generatedPassword, 'password2':generatedPassword})

    if request.method == 'POST':
        form = PerfilForm(request.POST)

        if form.is_valid():
            saved, errors = form.save()
            context['errors'] = errors
            if saved:
                return redirect('listarusuarios')

    context['form'] = form

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
    form = IncluirNoImovelForm()

    if request.method == 'POST':
        form = IncluirNoImovelForm(request.POST)

        if form.is_valid():
            form.save(profile)
            return redirect('listarusuarios')

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

        for _ in range(passedMonths+1):
            thisMonthPaid = False
            for p in payments:
                if (p.status == "P" or p.status == "A") and (p.data.month == referrenceMonth.month and p.data.year == referrenceMonth.year):
                    thisMonthPaid = True
                    break

            if thisMonthPaid:
                invoices.append({"pagamento": p})
            else:
                payments = Pagamento(perfil=profile, status="N")
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
    return render(request, 'views/home-usuario.html', context)


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
                        'valor_pago': p.valor_pago, 
                        'data_pagamento': p.data})
                    paid = True
                    continue
            if not paid:
                paymentsArray.insert(0,
                    {'mes_referencia': dateEntryProperty, 
                    'status': 'N', 
                    'valor_pago': '', 
                    'data_pagamento': ''})
            dateEntryProperty += relativedelta(months=1)

        context['pagamentos'] = paymentsArray
    
    return render(request, 'views/historico-usuario.html', context)
