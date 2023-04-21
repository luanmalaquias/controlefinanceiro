from django.shortcuts import render, redirect
from locatario.forms import *
from django.contrib.auth import authenticate, login, logout
from imobiliaria.forms import *
from locador.models import Locador
from locatario.models import Locatario

def index_view(request):
    context = {}
    return render(request, 'index2.html', context)


def login_view(request):
    context = {}    
    if request.method == 'GET':
        form = CustomAuthenticationForm()
    elif request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                try:
                    Locador.objects.get(usuario=user)
                    return redirect('home_locador_view')
                except:
                    Locatario.objects.get(usuario=user)
                    return redirect('home_locatario_view')
    context['form'] = form    
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect('login_view')