from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User
from utils.scripts import validar_cpf_cnpj



class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='CPF/CNPJ', label_suffix=' *', max_length=14, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF/CNPJ'}))
    password1 = forms.CharField(label='Senha', label_suffix=' *', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}))
    password2 = forms.CharField(label='Confirmação de senha', label_suffix=' *', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmação de senha'}))
    first_name = forms.CharField(label='Nome', label_suffix=' *', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}))
    last_name = forms.CharField(label='Sobrenome', label_suffix='', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'}))
    # email = forms.EmailField(label='Email', label_suffix='', required=False, widget=forms.EmailInput(attrs={'class': 'form-control', 'type': 'email', 'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name',)

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            if self[field].errors:
                self.fields[field].widget.attrs['class'] = 'form-control is-invalid'
    
    def clean(self):
        cleaned_data = super().clean()
        cpf_cnpj = cleaned_data.get('username')
        if not validar_cpf_cnpj(cpf_cnpj):
            raise forms.ValidationError('Cpf ou Cnpj inválido.')
        return super().clean()


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'CPF'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = self[field].label

class UpdatePasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='Senha', label_suffix=' *', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}))
    new_password2 = forms.CharField(label='Confirmação de senha', label_suffix=' *', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmação de senha'}))


class CustomUpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(label='Nome', label_suffix=' *', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}))
    last_name = forms.CharField(label='Sobrenome', label_suffix='', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'}))
    email = forms.EmailField(label='Email', label_suffix='', required=False, widget=forms.EmailInput(attrs={'class': 'form-control', 'type': 'email', 'placeholder': 'Email'}))
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)