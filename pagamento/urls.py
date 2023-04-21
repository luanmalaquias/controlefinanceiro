from django.urls import path
from .views import *

urlpatterns = [
    path('criar_pagamento_rapido/<int:id_locatario>/<str:mes_referencia>/', criar_pagamento_rapido_view, name='criar_pagamento_rapido_view'),    
    path('deletar_pagamento_rapido/<int:id_locatario>/<str:mes_referencia>/', deletar_pagamento_rapido_view, name='deletar_pagamento_rapido_view'),    
]