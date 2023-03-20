from django.urls import path
from .views import *

urlpatterns = [
    path('adicionar/', criar_pagamento, name="adicionarpagamento"),
    # FIXME devedores
    path('listar-pagamentos-por-usuarios/', listarPagamentosPorUsuarios, name="listar-pagamentos-por-usuarios"),
    path('listar-pagamentos-por-usuarios/<str:dataParam>', listarPagamentosPorUsuarios, name="listar-pagamentos-por-usuarios-com-data"),
    # FIXME read-payments or list-payments
    path('listar-todos-os-pagamentos/', listar_pagamentos, name='listar-todos-os-pagamentos'),
    path('adicionarpagamentorapido/<int:id>/<str:data>', criar_pagamento_rapido, name='adicionarpagamentorapido'),
    path('deletarpagamentorapido/<int:id>/<str:data>', deletar_pagamento_rapido, name='deletarpagamentorapido'),
    path('deletar-pagamento/<int:id>', deletar_pagamento, name='deletar-pagamento'),
    path('editar-pagamento/<int:id>/<str:pagina>/<str:data>', editar_pagamento, name="editar-pagamento"),
]