from django import forms
from imobiliaria.models import Imovel
from .models import Perfil
from utils.scripts import unmask, cpfIsValid
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth import authenticate, login, logout



class PerfilForm(forms.Form):
    cpf = forms.CharField(label_suffix=' *', required=True, max_length=14, min_length=14, widget=forms.TextInput(attrs={'placeholder': 'Cpf'}))
    password1 = forms.CharField(label='Senha', label_suffix=' *',required=True, min_length=8, max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Senha'}))
    password2 = forms.CharField(label='Confirmar senha', label_suffix=' *', required=True, min_length=8, max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Repita a senha'}))
    fullName = forms.CharField(label='Nome completo', label_suffix=' *', required=True, min_length=4, max_length=80, widget=forms.TextInput(attrs={'placeholder': 'Nome completo'}))
    phone = forms.CharField(label='Telefone', label_suffix=' *', required=True, min_length=16, max_length=16, widget=forms.TextInput(attrs={'placeholder': 'Telefone para contato'}))
    birth = forms.DateField(label='Data de nascimento', label_suffix=' *', required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    _availableProperties = Imovel.objects.filter(disponibilidade = True)
    _choices = [(None, 'Sem imóvel')] + [(i.id, i) for i in _availableProperties]
    property = forms.ChoiceField(choices=_choices, label='Imóvel', label_suffix='', required=False)
    dateEntryProperty = forms.DateField(label='Data de entrada no imovel', required=False, label_suffix='', widget=forms.DateInput(attrs={'type': 'date'}))

    

    def save(self):
        saved = False
        errors = []

        cpf = unmask(self.cleaned_data['cpf'], '.-')
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        fullname = self.cleaned_data['fullName']
        phone = unmask(self.cleaned_data['phone'], '() -')
        birth = self.cleaned_data['birth']
        property = self.cleaned_data['property']
        dateEntryProperty = self.cleaned_data['dateEntryProperty']

        if User.objects.filter(username = cpf).exists():
            errors.append("CPF já cadastrado no sistema.")
        if not cpfIsValid(cpf):
            errors.append("CPF informado não é valido.")
        if password1 != password2:
            errors.append("Senhas não conferem.")

        if not errors:
            user = User.objects.create_user(username=cpf, password=password1)
            if property:
                propertyDB = property.objects.get(id = property)
            else:
                propertyDB = None
            Perfil.objects.create(usuario=user, cpf=cpf, nome_completo=fullname, data_nascimento=birth, telefone=phone, imovel=propertyDB, data_entrada_imovel=dateEntryProperty)
            saved = True
        else:
            saved = False

        return saved, errors



class UpdateProfileForm(forms.Form):
    fullName = forms.CharField(label='Nome completo', label_suffix=' *', required=True, min_length=4, max_length=80, widget=forms.TextInput(attrs={'placeholder': 'Nome completo'}))
    phone = forms.CharField(label='Telefone', label_suffix=' *', required=True, min_length=16, max_length=16, widget=forms.TextInput(attrs={'placeholder': 'Telefone para contato'}))
    birth = forms.DateField(label='Data de nascimento', label_suffix=' *', required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    dateEntryProperty = forms.DateField(label='Data de entrada no imovel', required=False, label_suffix='', widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, request=None, profile:Perfil=None, *args, **kwargs):
        super(UpdateProfileForm, self).__init__()
        if request:
            self.fields['fullName'].initial = request['fullName']
            self.fields['phone'].initial = request['phone']
            self.fields['birth'].initial = request['birth']
            self.fields['dateEntryProperty'].initial = request['dateEntryProperty']

        if profile:
            self.fields['fullName'].initial = profile.nome_completo
            self.fields['phone'].initial = profile.telefone
            if profile.data_nascimento:
                self.fields['birth'].initial = profile.data_nascimento.strftime("%Y-%m-%d")
            if profile.data_entrada_imovel:
                self.fields['dateEntryProperty'].initial = profile.data_entrada_imovel.strftime("%Y-%m-%d")

    def save(self, profile:Perfil):
        saved = False

        profileDB = Perfil.objects.get(id = profile.id)
        profileDB.nome_completo = self['fullName'].value()
        profileDB.telefone = self['phone'].value()
        profileDB.data_nascimento = self['birth'].value()

        try:
            profileDB.save()
            saved = True
        except:
            saved = False
        return saved



class UpdatePasswordForm(forms.Form):
    cpf = forms.CharField(label_suffix=' *', required=True, max_length=14, min_length=14, widget=forms.TextInput(attrs={'readonly':True, 'placeholder': 'Cpf'}))
    password1 = forms.CharField(label='Senha', label_suffix=' *',required=True, min_length=8, max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'Senha'}))
    password2 = forms.CharField(label='Confirmar senha', label_suffix=' *', required=True, min_length=8, max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'Repita a senha'}))

    def __init__(self, request=None, user:User=None, *args, **kwargs):
        super(UpdatePasswordForm, self).__init__()
        if request:
            print(request)
            self.fields['cpf'].initial = request['cpf']
            self.fields['password1'].initial = request['password1']
            self.fields['password2'].initial = request['password2']
        if user:
            self.fields['cpf'].initial = user.username

    def save(self, user:User):
        saved = False
        errors = []

        password1 = self['password1'].value()
        password2 = self['password2'].value()

        if password1 != password2:
            errors.append("Senhas não conferem")

        if not errors:
            user.set_password(password1)
            user.save()
            saved = True
        else:
            saved = False

        return saved, errors



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
    birth = forms.DateField(label='Data de nascimento', required=True, label_suffix='', widget=forms.DateInput(attrs={'type': 'date'}))

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



class IncluirNoImovelForm(forms.Form):
    _availableProperties = Imovel.objects.filter(disponibilidade = True)
    _choices = ((i.id, i) for i in _availableProperties)
    property = forms.ChoiceField(choices=_choices, label='Imóveis', label_suffix='', required=True)

    def save(self, profile: Perfil):        
        property = Imovel.objects.get(id = self.cleaned_data['property'])
        property.disponibilidade = False
        profile.imovel = property
        profile.data_entrada_imovel = datetime.now()

        property.save()
        profile.save()
