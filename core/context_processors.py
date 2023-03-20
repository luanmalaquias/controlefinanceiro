from notificacao.models import Notificacao

def qtdNotificacoes(request):
    notificacoes = Notificacao.objects.filter(lido = False)
    return {'qtdNotificacoesAdmin' : len(notificacoes)}