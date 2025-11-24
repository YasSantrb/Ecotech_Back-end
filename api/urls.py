from .views import ExperimentoCreate, ExperimentoDetalhe
from django.urls import path
from .views import LoginView
from .views import RegistroUsuarioView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registro/', RegistroUsuarioView.as_view(), name='registrar'),
    path('experimentos/', ExperimentoCreate.as_view(), name='experimento-criar'),
    path('experimentos/<int:pk>/', ExperimentoDetalhe.as_view(), name='experimento-detalhe'),
]

# {
#     "username": "yasmim",
#     "password": "senha123",
# }

# {
#     "username": "yasmim",
#     "password": "senha123",
#     "email": "yas@gmail.com",
#     "profile": {
#         "cidade": "São Paulo",
#         "estado": "SP"
#     }
# }