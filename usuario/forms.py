from django import forms
from imobiliaria.models import Imovel
from .models import Perfil
from utils.scripts import unmask, cpfIsValid
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth import authenticate, login, logout

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


class LoginForm(forms.Form):
    cpf = forms.CharField(label_suffix='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Cpf'}))
    password = forms.CharField(label_suffix='', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}))

    def login(self):
        result = False
        errors = []

        cpf = unmask(self.cleaned_data['cpf'], '.-')
        password = self.cleaned_data['password']

        user = authenticate(username=cpf, password=password)
        if not user:
            errors.append("CPF ou senha incorreto.")
        if user:
            if user.is_active:
                result = True

        return result, user, errors


class AutoCadastroForm(forms.Form):
    cpf = forms.CharField(label_suffix='', required=True, max_length=14, min_length=14, widget=forms.TextInput(attrs={'placeholder': 'Cpf'}))
    password1 = forms.CharField(label='Senha', label_suffix='',required=True, min_length=8, max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Senha'}))
    password2 = forms.CharField(label='Confirmar senha', label_suffix='', required=True, min_length=8, max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Repita a senha'}))
    fullName = forms.CharField(label='Nome completo', label_suffix='', required=True, min_length=4, max_length=80, widget=forms.TextInput(attrs={'placeholder': 'Nome completo'}))
    phone = forms.CharField(label='Telefone', label_suffix='', required=True, min_length=16, max_length=16, widget=forms.TextInput(attrs={'placeholder': 'Telefone para contato'}))
    birth = forms.DateField(label='Data de nascimento', label_suffix='', widget=forms.DateInput(attrs={'type': 'date'}))

    def save(self):
        saved = False
        errors = []

        cpf = unmask(self.cleaned_data['cpf'], '.-')
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        fullname = self.cleaned_data['fullName']
        phone = unmask(self.cleaned_data['phone'], '() -')
        birth = self.cleaned_data['birth']

        if User.objects.filter(username = cpf).exists():
            errors.append("CPF já cadastrado no sistema, tente fazer login.")
        if not cpfIsValid(cpf):
            errors.append("CPF informado não é valido.")
        if password1 != password2:
            errors.append("Senhas não conferem.")

        if not errors:
            # salvar um administrador se não existir usuarios cadastrados
            if User.objects.count() == 0:
                User.objects.create_superuser(username=cpf, password=password1)                
            else:
                user = User.objects.create_user(username=cpf, password=password1)
                Perfil.objects.create(usuario=user, cpf=cpf, nome_completo=fullname, data_nascimento=birth, telefone=phone)
            saved = True
        else:
            saved = False

        return saved, errors


class ChangePasswordForm(forms.Form):
    cpf = forms.CharField(label_suffix='', required=True, min_length=11, max_length=11, widget=forms.TextInput(attrs={'placeholder': 'Cpf'}))
    birth = forms.DateField(label='Data de nascimento', label_suffix='', widget=forms.DateInput(attrs={'type': 'date'}))
    password1 = forms.CharField(label='Nova senha', label_suffix='',required=True, min_length=8, max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Nova senha'}))
    password2 = forms.CharField(label='Confirmar nova senha', label_suffix='', required=True, min_length=8, max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Confirmar nova senha'}))

    def save(self):
        saved = False
        errors = []

        cpf = unmask(self.cleaned_data['cpf'], '.-')
        birth = self.cleaned_data['birth']
        birthFinal = birth.split('-')
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        try:
            birthFinal = datetime(int(birthFinal[0]), int(birthFinal[1]), int(birthFinal[2]))
        except:
            birthFinal = None

        profile = Perfil.objects.filter(cpf = cpf, data_nascimento = birthFinal).first()
        if not profile:
            errors.append("CPF ou data de nascimento inválido.")
        if password1 != password2:
            errors.append("Senhas não conferem.")

        if not errors:
            profile.usuario.set_password(str(password1))
            profile.usuario.save()
            saved = True
        else:
            saved = False
        
        return saved, errors


class IncluirNoImovelForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ('imovel',)

    def ajustar_escolhas(self):
        _imoveis_filtrados = Imovel.objects.filter(disponibilidade = True)
        _imovel_initial = None
        self.fields['imovel'] = forms.ModelChoiceField(queryset=_imoveis_filtrados, initial=_imovel_initial)