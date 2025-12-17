from rest_framework import serializers
from .models import PontosColeta
from .models import UserProfile
from .models import User
from .models import Doacao
from django.db import IntegrityError

class PontosColetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PontosColeta
        fields = '__all__'
        
class DoacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doacao
        fields = ['id', 'usuario', 'nome_doacao', 'especificacao', 'endereco',
            'descricao_geral', 'observacao', 'condicao', 'fotos_eletronico', 
            'criado_em']

def validar_cpf(value):
    if len(value) == 11:
        return value
    
def validar_cnpj(value):
    if len(value) == 14:
        return value
class UserProfileSerializer(serializers.ModelSerializer):
    cpf_cnpj = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = UserProfile
        fields = ['cpf', 'cnpj', 'telefone', 'cep', 'cpf_cnpj', 'tipo_usuario', 'criado_em']
        read_only_fields = ['cpf', 'cnpj', 'tipo_usuario', 'criado_em']
        
    def validate(self, data):
        identificador = data.pop('cpf_cnpj', None)
        if not identificador:
            raise serializers.ValidationError("O campo 'cpf_cnpj' é obrigatório.")
        if identificador:
            identificador_limpo = identificador.replace('.', '').replace('-', '').replace('/', '')
            if validar_cpf(identificador_limpo):
                data['cpf'] = identificador_limpo       
                data['tipo_usuario'] = 'DOADOR'
            elif validar_cnpj(identificador_limpo):
                data['cnpj'] = identificador_limpo      
                data['tipo_usuario'] = 'EMPRESA'
            else:
                raise serializers.ValidationError("O valor inserido não é um CPF ou CNPJ válido.")
        if 'tipo_usuario' not in data:
            pass

        return data
        
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
                user.is_active = True
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
        
        data.pop('confirmar_senha')
        return data
        
        
        
