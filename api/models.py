from django.db import models
from django.contrib.auth.models import User

TIPO_USUARIO_CHOICES = [
    ('DOADOR', 'Doador'),
    ('EMPRESA', 'Empresa'),
]
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cep = models.CharField(max_length=9, null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)
    cnpj = models.CharField(max_length=14, unique=True, null=True, blank=True)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    tipo_usuario = models.CharField(max_length=8, choices=TIPO_USUARIO_CHOICES)
    
    def __str__(self):
        return self.user.username

class PontosColeta(models.Model): 
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pontos_coletas', null=
                                True, blank=True)
    rua = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    cep = models.CharField(max_length=9)
    telefone = models.CharField(max_length=15)
    horario_funcionamento = models.CharField(max_length=100)
    criado_em = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.rua
    
# {
#     "rua": "Rua João Dantas",
#     "bairro": "Centro",
#     "telefone": "(89)99929-2129",
#     "cep": "64800-086",
#     "horario_funcionamento": "Segunda a Sexta: 8h às 17:00"
# }

condicao_eletronico = [
    ('NOVO', 'Novo'),
    ('USADO', 'Usado'),
    ('PARA PEÇAS', 'Para peças'),
]    
class CriarDoacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doacoes', null=True, blank=True)
    nome_doacao = models.CharField(max_length=100)
    especificacao = models.TextField()
    endereco = models.CharField(max_length=200)
    descricao_geral = models.TextField()
    observacao = models.TextField(null=True, blank=True)
    condicao = models.CharField(max_length=100, choices=condicao_eletronico, default='Usado')
    fotos_eletronico = models.ImageField(upload_to='fotos_eletronicos/', null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nome_doacao
    
# {
#     "nome_doacao": "Notebook Dell",
#     "especificacao": "Modelo XPS 13, 16GB RAM, 512GB SSD",
#     "endereco": "Rua das Flores, 123, Apt 45",
#     "descricao_geral": "Notebook em bom estado, usado por 1 ano.",
#     "observacao": "Pequenos arranhões na tampa.",
#     "condicao": "Usado"
# }