from .views import PontosColetaCreate, PontosColetaDetalhe, TodosPontosColetaGet
from django.urls import path
from .views import LoginView
from .views import RegistroUsuarioView
from .views import CriarDoacaoCreate, CriarDoacaoDetalhe, TodasDoacoesGet

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registro/', RegistroUsuarioView.as_view(), name='registrar'),
    path('todos_pontos_coleta/', TodosPontosColetaGet.as_view(), name='todos_pontos_coleta'),
    path('meus_pontos_coleta/', PontosColetaCreate.as_view(), name='meus_pontos_coleta'),
    path('meus_pontos_coleta/<int:pk>/', PontosColetaDetalhe.as_view(), name='meus_pontos_coleta-detalhe'),
    path('todas_doacoes/', TodasDoacoesGet.as_view(), name='todas_doacoes'),
    path('minhas_doacoes/', CriarDoacaoCreate.as_view(), name='minhas_doacoes'),
    path('minhas_doacoes/<int:pk>/', CriarDoacaoDetalhe.as_view(), name='minhas_doacoes-detalhe'),
]
