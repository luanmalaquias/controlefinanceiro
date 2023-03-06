from django import forms
from imobiliaria.models import Imovel
from .models import Perfil

class PerfilForm(forms.ModelForm):

    class Meta:
        model = Perfil
        fields = ('nome_completo', 'data_nascimento', 'telefone', 'imovel')

    def ajustar_escolhas(self, perfil: Perfil = None):
        if perfil and perfil.imovel:
            _imoveis_filtrados = Imovel.objects.filter(id=perfil.imovel.id) | Imovel.objects.filter(disponibilidade = True)
            _imovel_initial = Imovel.objects.filter(id=perfil.imovel.id)
        else:
            _imoveis_filtrados = Imovel.objects.filter(disponibilidade = True)
            _imovel_initial = None
        self.fields['imovel'] = forms.ModelChoiceField(queryset=_imoveis_filtrados, initial=_imovel_initial, required=False)


class RecuperarSenhaForm(forms.Form):
    cpf = forms.CharField()
    data_de_nascimento = forms.DateField()


class IncluirNoImovelForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ('imovel',)

    def ajustar_escolhas(self):
        _imoveis_filtrados = Imovel.objects.filter(disponibilidade = True)
        _imovel_initial = None
        self.fields['imovel'] = forms.ModelChoiceField(queryset=_imoveis_filtrados, initial=_imovel_initial)