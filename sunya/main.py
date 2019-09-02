from django.shortcuts import render
from django.views import View
from rest_framework import generics

# Create your views here.
from sunya.models import Health
from sunya.serializers import HealthSerializer


class MainPage(View):
    def get(self, request):
        return render(request, 'health/index.html')


class HealthList(generics.ListCreateAPIView):
    queryset = Health.objects.all()
    serializer_class = HealthSerializer


class HealthDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Health.objects.all()
    serializer_class = HealthSerializer

