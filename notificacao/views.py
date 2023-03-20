from django.shortcuts import render, redirect
from .models import Notificacao
from usuario.models import Perfil
from django.shortcuts import get_object_or_404
from .forms import NotificacaoForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


@login_required
def listNotifications(request):
    context = {}

    if request.user.is_staff:
        notificacoes = Notificacao.objects.all().order_by('lido', 'datahora')
    else:
        perfil = Perfil.objects.get(cpf = request.user.username)
        notificacoes = Notificacao.objects.filter(perfil = perfil).order_by('lido', 'datahora')

    context['notificacoes'] = notificacoes
    return render(request, 'list-notifications.html', context)


@login_required
def readNotification(request, id):
    context = {}

    notification = get_object_or_404(Notificacao, pk=id)
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
        mensagem:Notificacao = form.save(commit=False)
        perfil = Perfil.objects.get(cpf = request.user.username)
        mensagem.perfil = perfil
        mensagem.save()
        return redirect('list-notifications')

    context['form'] = form
    return render(request, 'create-notification.html', context)
