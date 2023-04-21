from django import forms
from .models import *
from locatario.models import Locatario
from django.utils import timezone

class ImovelCreationForm(forms.ModelForm):
    nome = forms.CharField(label='Nome/Identificação do imóvel', label_suffix=' *', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do imóvel'}))
    cep = forms.CharField(label='CEP', max_length=9, label_suffix=' *', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP'}))
    numero = forms.CharField(label='Número', label_suffix=' *', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número'}))
    endereco = forms.CharField(label='Endereço', label_suffix=' *', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço'}))
    bairro = forms.CharField(label='Bairro', label_suffix=' *', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro'}))
    cidade = forms.CharField(label='Cidade', label_suffix=' *', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}))
    uf = forms.CharField(label='UF', label_suffix=' *', max_length=2, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'UF'}))
    mensalidade = forms.CharField(label='Mensalidade', max_length=13, label_suffix=' *', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mensalidade'}))
    class Meta:
        model = Imovel
        fields = ('nome', 'cep', 'numero', 'endereco', 'bairro', 'cidade', 'uf', 'mensalidade')

class ImovelUpdateForm(forms.ModelForm):
    nome = forms.CharField(label='Nome/Identificação do imóvel', label_suffix=' *', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do imóvel'}))
    cep = forms.CharField(label='CEP', max_length=9, label_suffix=' *', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP'}))
    numero = forms.CharField(label='Número', label_suffix=' *', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número'}))
    endereco = forms.CharField(label='Endereço', label_suffix=' *', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço'}))
    bairro = forms.CharField(label='Bairro', label_suffix=' *', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro'}))
    cidade = forms.CharField(label='Cidade', label_suffix=' *', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}))
    uf = forms.CharField(label='UF', label_suffix=' *', max_length=2, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'UF'}))
    mensalidade = forms.CharField(label='Mensalidade', max_length=13, label_suffix=' *', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mensalidade'}))
    DISPONIVEL_CHOICES = [(True, 'Disponível'), (False, 'Indisponível')]
    disponivel = forms.ChoiceField(choices=DISPONIVEL_CHOICES, label='Disponível', label_suffix='', widget=forms.Select(attrs={'class':'form-control', 'placeholder': 'Disponível'}))
    class Meta:
        model = Imovel
        fields = '__all__'
        exclude = ('locador',)

class LocatarioAoImovelForm(forms.Form):
    imovel = forms.ModelChoiceField(queryset=Imovel.objects.filter(disponivel=True), label='Imóvel', widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Imóvel'}))
    locatario = forms.ModelChoiceField(queryset=Locatario.objects.filter(imovel__isnull = True), label='Inquilino', widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Inquilino'}))

    def save(self):
        imovel = self.cleaned_data['imovel']
        locatario = self.cleaned_data['locatario']
        imovel.disponivel = False
        locatario.imovel = imovel
        locatario.data_entrada_imovel = timezone.now()
        imovel.save()
        locatario.save()