from django.shortcuts import render, redirect
from utils.scripts import unmask
from usuario.models import Perfil
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout



def loginPage(request):
    context = {}

    if request.method == 'POST':
        cpf = unmask(request.POST.get('cpf'), '.-')
        password = request.POST.get('password')

        errors = []
        
        user = authenticate(username=cpf, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('indeximobiliaria')
        else:
            errors.append('CPF ou senha inválidos.')

        context['errors'] = errors
        
    return render(request, 'login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('loginPage')