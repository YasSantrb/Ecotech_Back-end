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