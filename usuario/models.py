from django.db import models
from django.contrib.auth.models import User
from imobiliaria.models import Imovel
from datetime import datetime
from django.core.validators import MinLengthValidator
from utils.scripts import unmask

class Perfil(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    cpf = models.CharField(max_length=14, null=True)
    nome_completo = models.CharField(max_length=50, null=True, blank=False, verbose_name="Nome completo")
    data_nascimento = models.DateField(max_length=10, null=True, blank=False, verbose_name="Data de nascimento")
    telefone = models.CharField(max_length=16, null=True, blank=False, verbose_name="Telefone para contato")
    data_entrada_imovel = models.DateField(null=True, blank=True, verbose_name="Data de entrada no imovel")
    usuario = models.OneToOneField(User, blank=False, on_delete=models.CASCADE)
    imovel = models.OneToOneField(Imovel, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return self.nome_completo
    
    def atualizar_data_entrada_imovel(self):
        self.data_entrada_imovel = datetime.now()
        self.save()
        context = {}
        context['errors'] = []

        user = data['user']
        cpf = data['cpf']
        password1 = unmask(data['password1'], '.-')
        password2 = data['password2']

        self.usuario = user
        self.cpf = cpf
        self.telefone = unmask(self.telefone, '() -')
        self.data_nascimento = data['birth']

        if User.objects.filter(username = cpf).exists():
            context['errors'].append("CPF já cadastrado no sistema, tente fazer login.")
        if not cpfIsValid(cpf) or len(cpf) != 11:
            context['errors'].append("CPF informado não é valido.")
        if len(self.telefone) != 11:
            context['errors'].append("Telefone invalido.")
        if password1 != password2:
            context['errors'].append("Senhas não conferem.")
        if len(password1) < 8:
            context['errors'].append("Senha fraca.")
        if len(self.data_nascimento) != 10:
            context['errors'].append("Data de nascimento inválida.")

        try:
            # salvar um administrador se não existir usuarios cadastrados
            if User.objects.count() == 0:
                User.objects.create_superuser(username=cpf, password=password1)                
            else:
                # User.objects.create(username=cpf, password=password1).save()
                # profile.save()
                pass
            context['saved'] = True
        except:
            context['saved'] = False
        return context
