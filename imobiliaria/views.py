from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView

# Create your views here.

@login_required
def index_imobiliaria(request):
    return render(request, 'imobiliaria.html', {})