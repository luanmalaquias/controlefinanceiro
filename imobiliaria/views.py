from django.shortcuts import render

# Create your views here.

def index_imobiliaria(request):
    return render(request, 'teste.html', {})