from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index_view'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('imobiliaria/', include('imobiliaria.urls')),
    path('locador/', include('locador.urls')),
    path('locatario/', include('locatario.urls')),
    path('pagamento/', include('pagamento.urls')),
]