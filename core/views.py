from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Tribunal
from .serializers import TribunalSerializer

class TribunalViewSet(viewsets.ModelViewSet):
    queryset = Tribunal.objects.all()
    serializer_class = TribunalSerializer

    @action(detail=True, methods=['post'])
    def create_a_tribunal(self, request, pk=None):
        tribunal = self.get_object()
        tribunal.save()
        serializer = self.get_serializer(tribunal)
        return Response(serializer.data)
    
