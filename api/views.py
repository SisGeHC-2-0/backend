from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *


# Create your views here.


class MajorListCreate(generics.ListCreateAPIView):
    queryset = Major.objects.all()
    serializer_class = MajorSerializer

class MajorRetreiveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Major.objects.all()
    serializer_class = MajorSerializer
    lookup_field = "pk"

class ComplementaryActivitySerializer(generics.ListCreateAPIView):
    queryset = ComplementaryActivity.objects.all()
    serializer_class = ComplementaryActivitySerializer

class ActivityTypeListCreate(generics.ListCreateAPIView):
    queryset = ActivityType.objects.all()
    serializer_class = ActivityTypeSerializer

class ActivityTypeRetreiveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = ActivityType.objects.all()
    serializer_class = ActivityTypeSerializer
    lookup_field = "pk"

