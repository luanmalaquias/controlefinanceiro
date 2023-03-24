from django.urls import path
from .views import *

urlpatterns = [
    path('adicionar/', createPayment, name="adicionarpagamento"),
    path('adicionarpagamentorapido/<int:id>/<str:data>', createQuickPayment, name='adicionarpagamentorapido'),
    path('listar-pagamentos-por-usuarios/', monthlyDebtors, name="listar-pagamentos-por-usuarios"),
    path('listar-pagamentos-por-usuarios/<str:dataParam>', monthlyDebtors, name="listar-pagamentos-por-usuarios-com-data"),
    path('listar-todos-os-pagamentos/', listPayments, name='listar-todos-os-pagamentos'),
    path('editar-pagamento/<int:id>/<str:pagina>/<str:data>', updatePayment, name="editar-pagamento"),
    path('deletarpagamentorapido/<int:id>/<str:data>', deleteQuickPayment, name='deletarpagamentorapido'),
    path('deletar-pagamento/<int:id>', deletePayment, name='deletar-pagamento'),
]