from django import forms
from .models import Locador
from django.contrib.auth.models import User

class LocadorCreationForm(forms.ModelForm):
    data_nascimento_criacao = forms.DateField(label='Data de nascimento ou criação da empresa', label_suffix=' *', widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Data de nascimento ou criação da empresa'}))

    class Meta:
        model = Locador
        fields = '__all__'
        exclude = ('usuario', 'ultimo_pagamento', 'telefone')

    def save(self, user:User, commit: bool = ...):
        user.save()
        locador = Locador.objects.create(usuario=user, data_nascimento_criacao=self['data_nascimento_criacao'].value())
        return locador
    
class LocadorUpdateForm(forms.ModelForm):
    telefone = forms.CharField(label='Telefone para contato', label_suffix='', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone para contato'}))
    data_nascimento_criacao = forms.DateField(label='Data de nascimento ou criação da empresa', label_suffix=' *', required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Data de nascimento ou criação da empresa'}))
    
    class Meta:
        model = Locador
        fields = '__all__'
        exclude = ('usuario', 'ultimo_pagamento',)

    def save(self, commit: bool = ...):
        return super().save(commit)
