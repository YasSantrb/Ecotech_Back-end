from rest_framework import serializers
from .models import Experimento
from .models import UserProfile
from .models import User
from django.db import IntegrityError

class ExperimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experimento
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['cidade', 'estado']
        
class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'profile']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password', None)
        
        try:
            # 1. Cria o objeto User no banco de dados
            user = User.objects.create(**validated_data)
            
            # 2. Define e salva a senha (melhor prática: usa set_password)
            if password:
                user.set_password(password)
                user.save()
            
            # 3. Cria o UserProfile, associando-o ao novo usuário
            UserProfile.objects.create(user=user, **profile_data)
            
            return user
            
        except IntegrityError as e:
            # Captura erros do DB, como username/email duplicados
            # O DRF precisa de ValidationError, não IntegrityError diretamente
            
            # Se o usuário foi criado, mas o perfil falhou, delete o usuário para evitar órfãos
            if 'user' in locals():
                 user.delete()
                 
            # Mensagem de erro amigável
            raise serializers.ValidationError({"detail": "Já existe um usuário com este nome de usuário ou e-mail."}) 
            
        except Exception as e:
            # Captura outros erros inesperados
            if 'user' in locals():
                 user.delete()
                 
            # Re-lança o erro para o DRF/Django tratar
            raise serializers.ValidationError({"error": "Erro desconhecido ao criar usuário: " + str(e)})