from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from usuario.models import Perfil
from pagamento.models import Pagamento
from .models import Imovel
from .forms import ImovelForm
from django.shortcuts import get_object_or_404
# FIXME remover gerar dadosisso daqui quando for implantar
from utils.scripts import gerarDados, unmask, porcentagem
from utils import pixcodegen
from datetime import datetime, timedelta, time, date
from dateutil.relativedelta import relativedelta
from django.db.models import Q



@login_required
def homeRealEstate(request):
    if not request.user.is_staff:
        return redirect('home-usuario')

    context = {}

    properties = Imovel.objects.all()
    profiles = Perfil.objects.all()
    payments = Pagamento.objects.all()

    availableProperties = Imovel.objects.filter(disponibilidade=True)
    profilesWithoutProperty = Perfil.objects.filter(imovel=None)
    
    thisMonthDebtors = []
    today = datetime.now()
    for profile in profiles:
        paid = False
        if profile.imovel != None:
            for payment in payments:
                if payment.perfil == profile and payment.data.month == today.month and payment.data.year == today.year:
                    paid = True
                    break
        else: continue
        if paid == False:
            thisMonthDebtors.append(profile)

    totalIncome = 0
    for payment in payments:
        totalIncome += int(unmask(payment.valor_pago, '.'))
    
    monthlyIncome = 0
    for property in properties:
        if property.disponibilidade == False:
            monthlyIncome += int(property.mensalidade)

    # FIXME remover gerar dados isso daqui quando for implantar
    # gerarDados(2)

    # quando o usuario nao tiver perfil
    loggedInUser = request.user
    if request.user.is_staff == False:
        profile = Perfil.objects.get(usuario = loggedInUser)
        context['perfil'] = profile

    context['imoveis'] = properties
    context['perfis'] = profiles
    context['pagamentos'] = payments
    context['imoveisDisponiveis'] = availableProperties
    context['perfisSemImovel'] = profilesWithoutProperty
    context['devedoresDesteMes'] = thisMonthDebtors
    context['rendimentoTotal'] = totalIncome
    context['rendimentoMensal'] = monthlyIncome
    context['hoje'] = today

    return render(request, 'index-imobiliaria.html', context)


@login_required
@staff_member_required
def createProperty(request):
    context = {}
    if request.method == 'POST':
        formProperty = ImovelForm(request.POST)
        if formProperty.is_valid():
            property = formProperty.save(commit=False)
            property.mensalidade = unmask(property.mensalidade, '.,')
            property.save()
            return redirect('listarimoveis')
    else:
        formProperty = ImovelForm()
    context['formImovel'] = formProperty
    return render(request, 'views/criar-imovel.html', context)


@login_required
@staff_member_required
def listProperties(request):
    context = {}
    properties = Imovel.objects.all().order_by('-disponibilidade','nome')
    context['imoveis'] = properties

    if request.method == "GET":
        search = request.GET.get('busca')
        if search != None:
            properties = Imovel.objects.all().filter(Q(nome__contains=search) | Q(cep__contains=search) | Q(endereco__contains=search) | Q(bairro__contains=search) | Q(cidade__contains=search) | Q(uf__contains=search)).order_by('-disponibilidade','nome')
            context['imoveis'] = properties
            return render(request, 'views/listar-imoveis.html', context)

    return render(request, 'views/listar-imoveis.html', context)


@login_required
def readProperty(request, id):
    context = {}

    # o imovel tem que ser do usuario
    if request.user.is_staff == False:
        profile = Perfil.objects.get(cpf = request.user.username)
        if id != profile.imovel.id:
            return redirect('read-property', profile.imovel.id)

    property = get_object_or_404(Imovel, pk=id)
    tenant = Perfil.objects.filter(imovel = property)
    tenant = tenant[0] if len(tenant) > 0 else None
    payments = []
    if tenant:
        payments = Pagamento.objects.filter(perfil = tenant)

    context['imovel'] = property
    context['inquilino'] = tenant
    context['pagamentos'] = payments if payments else []
    return render(request, 'views/read-property.html', context)


@login_required
@staff_member_required
def listAvailableProperties(request):
    context = {}
    availableProperties = Imovel.objects.filter(disponibilidade = True).order_by('nome')
    context['imoveis'] = availableProperties
    return render(request, 'views/listar-imoveis.html', context)


@login_required
@staff_member_required
def updateProperty(request, id):
    context = {}

    property = get_object_or_404(Imovel, pk=id)
    formProperty = ImovelForm(instance=property)

    if request.method == 'POST':
        formProperty = ImovelForm(request.POST, instance=property)
        if formProperty.is_valid():
            property = formProperty.save(commit=False)
            property.mensalidade = unmask(property.mensalidade, '.,')
            property.save()
            return redirect('listarimoveis')
        
    context['formImovel'] = formProperty
    context['imovel'] = property
        
    return render(request, 'views/criar-imovel.html', context)


@login_required
@staff_member_required
def deleteProperty(request, id):
    property = get_object_or_404(Imovel, pk=id)
    property.delete()
    return redirect('listarimoveis')
