from django.urls import path
from .views import *

urlpatterns = [
    path('adicionar/', criar_pagamento, name="adicionarpagamento"),
    path('listar-pagamentos-por-usuarios/', listar_pagamentos_por_usuarios, name="listar-pagamentos-por-usuarios"),
    path('listar-todos-os-pagamentos/', listar_pagamentos, name='listar-todos-os-pagamentos'),
    path('listar-pagamentos-por-usuarios/<str:dataParam>', listar_pagamentos_por_usuarios, name="listar-pagamentos-por-usuarios-com-data"),
    path('adicionarpagamentorapido/<int:id>/<str:data>', criar_pagamento_rapido, name='adicionarpagamentorapido'),
    path('deletarpagamentorapido/<int:id>/<str:data>', deletar_pagamento_rapido, name='deletarpagamentorapido'),
    path('deletar-pagamento/<int:id>', deletar_pagamento, name='deletar-pagamento'),
    path('editar-pagamento/<int:id>/<str:pagina>/<str:data>', editar_pagamento, name="editar-pagamento"),
]