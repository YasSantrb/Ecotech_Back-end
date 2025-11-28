from .views import PontosColetaCreate, PontosColetaDetalhe
from django.urls import path
from .views import LoginView
from .views import RegistroUsuarioView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registro/', RegistroUsuarioView.as_view(), name='registrar'),
    path('pontos_coleta/', PontosColetaCreate.as_view(), name='pontos_coleta-criar'),
    path('pontos_coleta/<int:pk>/', PontosColetaDetalhe.as_view(), name='pontos_coleta-detalhe'),
]
