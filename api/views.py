from rest_framework.views import APIView 
from rest_framework.response import Response
from .models import PontosColeta
from django.shortcuts import get_object_or_404
from .serializers import PontosColetaSerializer
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework import permissions, status
from .models import User, UserProfile
from django.contrib.auth import authenticate    
class RegistroUsuarioView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response( data= {
                'mensagem': 'Usuário criado com sucesso!',
                'token': token.key,
                'usuario': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email, 
                    'profile': {
                        'cep': user.userprofile.cep,
                        'cpf_cnpj': user.userprofile.cpf_cnpj,
                        'telefone': user.userprofile.telefone
                    }
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        email = request.data.get('email')  
        password = request.data.get('password')
        
        if not email or not password:
            return Response({'erro': 'Email e senha são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response({'erro': 'Credenciais inválidas (E-mail não encontrado).'}, status=status.HTTP_401_UNAUTHORIZED)
        auth_user = authenticate(username=user.username, password=password)
        
        if auth_user is not None:
            token, _ = Token.objects.get_or_create(user=auth_user)
            
            profile_data = {}
            try:
                profile_data = {
                    'cep': auth_user.userprofile.cep,
                    'cpf_cnpj': auth_user.userprofile.cpf_cnpj,
                    'telefone': auth_user.userprofile.telefone
                }
            except UserProfile.DoesNotExist:
                pass 

            return Response( data= {
                'token': token.key,
                'usuario_id': auth_user.id,
                'username': auth_user.username,
                'email': auth_user.email, 
                'profile': profile_data
            }, status=status.HTTP_200_OK)
        
        return Response({'erro': 'Credenciais inválidas (E-mail ou senha incorretos).'}, status=status.HTTP_401_UNAUTHORIZED)
class PontosColetaCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        pontosColeta = PontosColeta.objects.filter(usuario=request.user)
        serializer = PontosColetaSerializer(pontosColeta, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PontosColetaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PontosColetaDetalhe(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, pk):
        pontosColeta = get_object_or_404(PontosColeta, pk=pk, usuario = request.user)
        serializer = PontosColetaSerializer(pontosColeta)
        return Response(serializer.data)
    
    def put(self, request, pk):
        pontoColeta = get_object_or_404(PontosColeta, pk=pk, usuario=request.user)
        serializer = PontosColetaSerializer(pontoColeta, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        pontoColeta = get_object_or_404(PontosColeta, pk=pk, usuario=request.user)
        pontoColeta.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)