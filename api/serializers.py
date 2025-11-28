from rest_framework import serializers
from .models import PontosColeta
from .models import UserProfile
from .models import User
from django.db import IntegrityError

class PontosColetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PontosColeta
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['cpf_cnpj', 'telefone', 'cep']
        
class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    
    confirmar_senha = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'confirmar_senha', 'email', 'profile']
        extra_kwargs = {'password': {'write_only': True}, 
                        'email': {'required': True}}
        
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password', None)
        
        try:
            user = User.objects.create(**validated_data)
            if password:
                user.set_password(password)
                user.save()
            UserProfile.objects.create(user=user, **profile_data)
            return user
            
        except IntegrityError as e:
            if 'user' in locals():
                 user.delete()
            raise serializers.ValidationError({"detail": "Já existe um usuário com este nome de usuário ou e-mail."}) 
            
        except Exception as e:
            if 'user' in locals():
                 user.delete()
            raise serializers.ValidationError({"error": "Erro desconhecido ao criar usuário: " + str(e)})
        
    def validate(self, data):
        if data['password'] != data['confirmar_senha']:
            raise serializers.ValidationError("As senhas não coincidem.")
        
        if 'profile' in data and 'cpf_cnpj' not in data['profile']:
            raise serializers.ValidationError("O campo CPF/CNPJ é obrigatório no perfil.")
        
        data.pop('confirmar_senha')
        return data
        