from django.shortcuts import render, redirect
from .forms import *
from imobiliaria.forms import *


def cadastro_view(request):
    context = {}    
    if request.method == 'GET':
        form1 = CustomUserCreationForm()
        form2 = LocatarioCreationForm()
    elif request.method == 'POST':
        form1 = CustomUserCreationForm(request.POST)
        form2 = LocatarioCreationForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save(commit=False)
            form2.save(user)
            return redirect('login_view')

    context['form1'] = form1
    context['form2'] = form2
    return render(request, 'cadastro_locatario.html', context)


def home_view(request):
    return render(request, 'home_locatario.html')