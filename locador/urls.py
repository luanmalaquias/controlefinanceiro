from django.urls import path
from .views import *

urlpatterns = [
    path('auto_cadastro/', cadastro_view, name='auto_cadastro_locador_view'),
    path('home/', home_view, name='home_locador_view'),
    path('meus_imoveis/', meus_imoveis_view, name='imoveis_locador_view'),
    path('meus_imoveis/novo/', cadastro_imovel_view, name='cadastro_imovel_view'),
    path('meus_imoveis/<int:id>/', ler_imovel_view, name='ler_imovel_view'),
    path('meus_imoveis/atualizar/<int:id>/', atualizar_imovel_view, name='atualizar_imovel_view'),
    path('meus_imoveis/deletar/<int:id>/', deletar_imovel_view, name='deletar_imovel_view'),
    path('meus_inquilinos/', meus_inquilinos_view, name='inquilinos_locador_view'),
    path('meus_inquilinos/<int:id>/', ler_inquilino_view, name='ler_inquilino_view'),
    path('meus_inquilinos/adicionar_ao_imovel/<str:tipo><int:id>', inquilino_ao_imovel_view, name='inquilino_ao_imovel_view'),
    path('meus_inquilinos/remover_do_imovel/<str:tipo><int:id>', remover_inquilino_do_imovel_view, name='remover_inquilino_do_imovel_view'),
    path('configuracoes/', configuracoes_view, name='configuracoes_locador_view'),
    path('configuracoes/alterar_senha/', alterar_senha_view, name='alterar_senha_view'),
    path('configuracoes/informacoes_da_conta/', alterar_informacoes_da_conta_view, name='alterar_informacoes_da_conta_view'),
    path('devedores/', devedores_view, name='devedores_view'),
    path('pagamentos_locador/', pagamentos_locador_view, name='pagamentos_locador_view')
]