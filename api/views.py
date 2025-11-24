from rest_framework.views import APIView 
from rest_framework.response import Response
from .models import Experimento
from django.shortcuts import get_object_or_404
from .serializers import ExperimentoSerializer
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework import permissions, status
from .models import UserProfile
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
                    'email': user.email
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        from django.contrib.auth import authenticate
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response( data= {
                'token': token.key,
                'usuario_id': user.id,
                'username': user.username,
            })
        return Response({'erro': 'Credenciais inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def get(self, request):
        return Response({'mensagem': 'Envie username e password via post para obter o TOKEN.'})