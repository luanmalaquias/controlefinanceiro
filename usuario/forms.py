from django import forms
from imobiliaria.models import Imovel
from .models import Perfil
from django.db.models import Q

class PerfilForm(forms.ModelForm):

    def __init__(self, perfil: Perfil = None,*args,**kwargs):
        super(PerfilForm,self).__init__(*args,**kwargs)
        if perfil:
            imovel = forms.ModelChoiceField(queryset=Imovel.objects.filter(Q(id=perfil.imovel.id) | Q(disponibilidade = True)), initial=Imovel.objects.filter(Q(id=perfil.imovel.id)))
        else:
            imovel = forms.ModelChoiceField(queryset=Imovel.objects.filter(Q(disponibilidade = True)))
        self.fields['imovel'] = imovel

    class Meta:
        model = Perfil
        fields = ('nome_completo', 'telefone')