from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cep = models.CharField(max_length=9, null=True, blank=True)
    cpf_cnpj = models.CharField(max_length=14, unique=True, null=True, blank=True)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    
    def __str__(self):
        return self.user.username

class Experimento(models.Model): 
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experimentos', null=
                                True, blank=True)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    criado_em = models.DateTimeField(auto_now_add = True)
    
    def __srt__(self):
        return self.titulo