from django.shortcuts import render, redirect
from utils.scripts import unmask
from django.contrib.auth import login, logout
from usuario.forms import LoginForm



def loginPage(request):
    context = {}

    form = LoginForm()

    if request.method == 'POST':        
        form = LoginForm(request.POST)
        if form.is_valid():
            result, user, errors = form.login()
            context['errors'] = errors
            if result:
                login(request, user)
                return redirect('indeximobiliaria')
        
    context['form'] = form
    return render(request, 'login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('loginPage')