from rest_framework.views import APIView 
from rest_framework.response import Response
from .models import Experimento
from django.shortcuts import get_object_or_404
from .serializers import ExperimentoSerializer
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework import permissions, status
from .models import User, UserProfile
from django.contrib.auth import authenticate
class ExperimentoCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        experimentos = Experimento.objects.filter(usuario=request.user)
        serializer = ExperimentoSerializer(experimentos, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ExperimentoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ExperimentoDetalhe(APIView):
    def get(self, request, pk):
        experimento = get_object_or_404(Experimento, pk=pk)
        serializer = ExperimentoSerializer(experimento)
        return Response(serializer.data)
    
    
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
        
        user = None
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            pass
        if user is not None:
            auth_user = authenticate(username=user.username, password = password)
            if auth_user:
                token, _ = Token.objects.get_or_create(user=user)
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
                    'usuario_id': user.id,
                    'username': user.username,
                    'email': user.email, 
                    'profile': profile_data
                    })
            return Response({'erro': 'Credenciais inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def get(self, request):
        return Response({'mensagem': 'Envie username e password via post para obter o TOKEN.'})