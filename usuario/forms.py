from django import forms
from imobiliaria.models import Imovel
from .models import Perfil
from django.db.models import Q

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ('nome_completo', 'telefone', 'imovel')