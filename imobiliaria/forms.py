from django import forms
from .models import Imovel
from .models import Imovel


class ImovelForm(forms.ModelForm):
    class Meta:
        model = Imovel
        fields = ('nome','cep','endereco','numero','bairro','cidade','uf','mensalidade','vencimento',)