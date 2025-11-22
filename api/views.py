from rest_framework.views import APIView 
from rest_framework.response import Response
from .models import Experimento
from django.shortcuts import get_object_or_404
from .serializers import ExperimentoSerializer

class ExperimentoCreate(APIView):
    def get(self, request):
        experiementos = Experimento.objects.all()
        serializer = ExperimentoSerializer(experiementos, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ExperimentoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
class ExperimentoDetalhe(APIView):
    def get(self, request, pk):
        experimento = get_object_or_404(Experimento, pk=pk)
        serializer = ExperimentoSerializer(experimento)
        return Response(serializer.data)