from django.shortcuts import render
from rest_framework import generics
from .models import Major, HourType
from .serializers import MajorSerializer, HourTypeSerializer


# Create your views here.


class MajorListCreate(generics.ListCreateAPIView):
    queryset = Major.objects.all()
    serializer_class = MajorSerializer

class MajorRetreiveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Major.objects.all()
    serializer_class = HourTypeSerializer
    lookup_field = "pk"


class HourTypeListCreate(generics.ListCreateAPIView):
    queryset = HourType.objects.all()
    serializer_class = MajorSerializer

class HourTypeRetreiveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = HourType.objects.all()
    serializer_class = HourTypeSerializer
    lookup_field = "pk"

