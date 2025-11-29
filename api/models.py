from django.db import models
from django.contrib.auth.models import User

TIPO_USUARIO_CHOICES = [
    ('Doador', 'Doador'),
    ('Empresa', 'Empresa'),
]
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cep = models.CharField(max_length=9, null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)
    cnpj = models.CharField(max_length=14, unique=True, null=True, blank=True)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    tipo_usuario = models.CharField(max_length=7, choices=TIPO_USUARIO_CHOICES)
    
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

condicao_eletronico = [
    ('Novo', 'Novo'),
    ('Usado', 'Usado'),
    ('Para peças', 'Para peças'),
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