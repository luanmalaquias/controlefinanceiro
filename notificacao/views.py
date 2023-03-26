from django.shortcuts import render, redirect
from .models import Notificacao
from usuario.models import Perfil
from django.shortcuts import get_object_or_404
from .forms import NotificacaoForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q


@login_required
def listNotifications(request):
    context = {}

    if request.user.is_staff:
        notifications = Notificacao.objects.all().order_by('lido', 'datahora')
        if request.method == 'GET':
            if request.GET.get('busca') != None:
                search = request.GET.get('busca')
                profiles = Perfil.objects.filter(Q(nome_completo__contains=search))
                notifications = []
                for p in profiles:
                    notificationsDB = Notificacao.objects.filter(perfil=p).order_by('datahora', 'lido')
                    for nDB in notificationsDB:
                        notifications.append(nDB)
                notifications.sort(key=_orderList)
                context['notificacoes'] = notifications
                return render(request, 'list-notifications.html', context)
    else:
        perfil = Perfil.objects.get(cpf = request.user.username)
        notifications = Notificacao.objects.filter(perfil = perfil).order_by('lido', 'datahora')

    context['notificacoes'] = notifications
    return render(request, 'list-notifications.html', context)


@login_required
def readNotification(request, id):
    context = {}

    notification = get_object_or_404(Notificacao, pk=id)

    # a notificação tem que ser do usuario
    if request.user.is_staff == False:
        profile = Perfil.objects.get(cpf = request.user.username)
        if notification.perfil != profile:
            return redirect('home-usuario')

    # só o adm setará como lido
    if request.user.is_staff and notification.lido == False:
        notification.lido = True
        notification.save()

    context['notification'] = notification
    return render(request, 'read-notification.html', context)


@login_required
def deleteNotification(request, id):
    notification = get_object_or_404(Notificacao, pk=id)
    notification.delete()
    return redirect('list-notifications')


@login_required
def createNotification(request):
    context = {}

    form = NotificacaoForm() 

    if request.method == 'POST':
        form = NotificacaoForm(request.POST)
        message:Notificacao = form.save(commit=False)
        profile = Perfil.objects.get(cpf = request.user.username)
        message.perfil = profile
        message.save()
        return redirect('list-notifications')

    context['form'] = form
    return render(request, 'create-notification.html', context)


def _orderList(lista):
    return lista.lido
