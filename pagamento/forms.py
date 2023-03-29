from django import forms
from .models import Pagamento
from datetime import datetime
from usuario.models import Perfil
from utils.scripts import unmaskMoney

class PagamentoForm(forms.Form):
    _profiles = Perfil.objects.filter(imovel__isnull = False)
    _profileChoices = [(None, '-- Selecione o usuário --')] + [(i.id, i) for i in _profiles]
    profile = forms.ChoiceField(label='Usuário pagador', label_suffix=' *', choices=_profileChoices, required=True)
    _statusChoices = [('P', 'Pago'), ('A', 'Em análise')]
    status = forms.ChoiceField(label='Status', label_suffix=' *', choices=_statusChoices, required=True)
    value = forms.CharField(label='Valor pago', label_suffix=' *', required=True, widget=forms.TextInput(attrs={'placeholder': 'Valor pago'}), max_length=10)
    date = forms.DateTimeField(label='Data do pagamento', label_suffix=' *', required=True, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    def __init__(self, request=None, payment:Pagamento=None, *args, **kwargs) -> None:
        super(PagamentoForm, self).__init__(*args, **kwargs)

        if request:
            self['profile'].initial = request['profile']
            self['status'].initial = request['status']
            self['value'].initial = request['value']
            self['date'].initial = request['date']
        if payment:
            self['profile'].initial = (payment.perfil.id, payment.perfil.nome_completo)
            self['status'].initial = (payment.status, payment.status)
            self['value'].initial = payment.valor_pago
            self['date'].initial = payment.data.strftime("%Y-%m-%dT%H:%m")

        if not payment and not request:
            self.fields['date'].initial = datetime.now().strftime("%Y-%m-%dT%H:%M")

    def save(self):
        saved = False
        errors = []

        profileID = self['profile'].value()
        status = self['status'].value()
        value = unmaskMoney(self['value'].value())

        # convert date str to datetime
        date = self['date'].value()
        dateSplit = date.split('T')
        dateDate = dateSplit[0].split('-')
        dateTime = dateSplit[1].split(':')
        dateFinal = datetime(int(dateDate[0]), int(dateDate[1]), int(dateDate[2]), int(dateTime[0]), int(dateTime[1]))

        profile = Perfil.objects.get(id = profileID)
        payments = Pagamento.objects.filter(perfil=profile)
        
        thisMonthPaid = False
        for payment in payments:
            if payment.data.month == dateFinal.month:
                thisMonthPaid = True
                break
        
        if thisMonthPaid:
            errors.append('Ja existe um pagamento deste usuário para o mês selecionado.')

        if not errors:
            Pagamento.objects.create(perfil=profile, status=status, valor_pago=value, data=dateFinal)
            saved = True

        return saved, errors        

    def update(self, payment:Pagamento):
        saved = False
        errors = []

        profileID = self['profile'].value()
        status = self['status'].value()
        value = unmaskMoney(self['value'].value())

        # convert date str to datetime
        date = self['date'].value()
        dateSplit = date.split('T')
        dateDate = dateSplit[0].split('-')
        dateTime = dateSplit[1].split(':')
        dateFinal = datetime(int(dateDate[0]), int(dateDate[1]), int(dateDate[2]), int(dateTime[0]), int(dateTime[1]))

        profile = Perfil.objects.get(id = profileID)
        payments = Pagamento.objects.filter(perfil=profile).exclude(id=payment.id)
        
        thisMonthPaid = False
        for payment in payments:
            if payment.data.month == dateFinal.month:
                thisMonthPaid = True
                break
        
        if thisMonthPaid:
            errors.append('Ja existe um pagamento deste usuário para o mês selecionado.')

        if not errors:
            payment.perfil = profile
            payment.status = status
            payment.valor_pago = value
            payment.data = dateFinal
            payment.save()
            saved = True

        return saved, errors