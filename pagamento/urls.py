from django.urls import path
from .views import *

urlpatterns = [
    path('create/', createPayment, name="adicionarpagamento"),
    path('quickcreate/<int:id>/<str:data>', quickCreatePayment, name='adicionarpagamentorapido'),
    path('listdebtors/', monthlyDebtors, name="listar-pagamentos-por-usuarios"),
    path('listdebtors/<str:dataParam>', monthlyDebtors, name="listar-pagamentos-por-usuarios-com-data"),
    path('list/', listPayments, name='listar-todos-os-pagamentos'),
    path('update/<int:id>/<str:pagina>/<str:data>', updatePayment, name="editar-pagamento"),
    path('quickdelete/<int:id>/<str:data>', quickDeletePayment, name='deletarpagamentorapido'),
    path('delete/<int:id>', deletePayment, name='deletar-pagamento'),
]