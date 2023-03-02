from django.db import models
from django.contrib.auth.models import User
from imobiliaria.models import Imovel
from datetime import datetime

class Perfil(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    cpf = models.CharField(max_length=14, null=True)
    nome_completo = models.CharField(max_length=50, null=True, verbose_name="Nome completo")
    data_nascimento = models.DateField(max_length=10, null=True, verbose_name="Data de nascimento")
    telefone = models.CharField(max_length=16, null=True, verbose_name="Telefone para contato")
    data_entrada_imovel = models.DateField(auto_now_add=True, editable=True, verbose_name="Data de entrada no imovel")
    usuario = models.OneToOneField(User, blank=True, on_delete=models.CASCADE)
    imovel = models.OneToOneField(Imovel, null=True, blank=False, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return self.nome_completo
    
    def atualizar_data_entrada_imovel(self):
        self.data_entrada_imovel = datetime.now()
        self.save()
