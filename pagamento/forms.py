from django import forms
from .models import Pagamento
from datetime import datetime

class PagamentoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super(PagamentoForm, self).__init__(*args, **kwargs)
        initial = datetime.now().strftime("%Y-%m-%dT%H:%M")
        self.fields['data'] = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), initial=initial)
        
    class Meta:
        model = Pagamento
        fields = '__all__'