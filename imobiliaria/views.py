from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def create_super_user(request):
    User.objects.all().delete()
    User.objects.create_superuser(username='luan', telefone='(11) 1234-5678', password='luan')
    return HttpResponse(f'Criado')


@login_required
def index_imobiliaria_view(request):
    return render(request, 'index_imobiliaria.html')