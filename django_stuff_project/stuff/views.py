from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Stuff
from .serializers import StuffSerializer

class StuffList(ListCreateAPIView):
    queryset = Stuff.objects.all()

   
    serializer_class = StuffSerializer

class StuffDetail(RetrieveUpdateDestroyAPIView):
    queryset = Stuff.objects.all()
    serializer_class = StuffSerializer