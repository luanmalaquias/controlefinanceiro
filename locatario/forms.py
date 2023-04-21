from django import forms
from locatario.models import Locatario
from locador.models import Locador



class LocatarioCreationForm(forms.ModelForm):
    id_locador = forms.CharField(label='Código do proprietário', label_suffix=' *', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código do proprietário'}))
    data_nascimento = forms.DateField(label='Sua data de nascimento', label_suffix=' *', widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = Locatario
        exclude = ('usuario', 'imovel', 'data_entrada_imovel', 'telefone', 'locador')

    def clean_locador(self, locador):
        self.cleaned_data['locador'] = Locador.objects.get(id=locador)

    def save(self, user, commit: bool = ...):
        user.save()
        locador = Locador.objects.get(pk=self['id_locador'].value())
        locatario = Locatario.objects.create(usuario=user, locador=locador, data_nascimento=self['data_nascimento'].value())
        return locatario
