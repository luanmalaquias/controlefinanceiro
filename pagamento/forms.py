from django import forms
from .models import Pagamento
from datetime import datetime
from usuario.models import Perfil

class PagamentoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super(PagamentoForm, self).__init__(*args, **kwargs)

        # setar a data e hora atual ao inicializar
        initial = datetime.now().strftime("%Y-%m-%dT%H:%M")
        self.fields['data'] = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), initial=initial)

        # permitir apenas perfis com imovel na escolha de perfis
        perfisComImovel = Perfil.objects.filter(imovel__isnull = False)
        self.fields['perfil'] = forms.ModelChoiceField(queryset=perfisComImovel)
        
    class Meta:
        model = Pagamento
        fields = '__all__'