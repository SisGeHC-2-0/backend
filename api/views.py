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

class ComplementaryActivitySerializerStudent(generics.ListCreateAPIView):
    serializer_class = ComplementaryActivitySerializer
    def get_queryset(self):
        return ComplementaryActivity.objects.filter(studentId=self.kwargs['studentId_id'])

class ComplementaryActivitySerializerStudentName(generics.ListCreateAPIView):
    serializer_class = ComplementaryActivitySerializer
    def get_queryset(self):
        name = self.kwargs['name']
        return ComplementaryActivity.objects.filter(studentId__name__icontains=name)


class ComplementaryActivitySerializerStudentType(generics.ListCreateAPIView):
    serializer_class = ComplementaryActivitySerializer
    def get_queryset(self):
        return ComplementaryActivity.objects.filter(studentId=self.kwargs['studentId_id'], ActivityTypeId=self.kwargs['ActivityTypeId_id'])

class ComplementaryActivitySerializerMajor(generics.ListCreateAPIView):
    serializer_class = ComplementaryActivitySerializer

    def get_queryset(self):
        course_id = self.kwargs['majorId_id']
        return ComplementaryActivity.objects.filter(
            studentId__majorId=course_id
        )

class ComplementaryActivitySerializerMajorType(generics.ListCreateAPIView):
    serializer_class = ComplementaryActivitySerializer

    def get_queryset(self):
        course_id = self.kwargs['majorId_id']
        return ComplementaryActivity.objects.filter(
            studentId__majorId=course_id, ActivityTypeId=self.kwargs['ActivityTypeId_id']
        )


class ActivityTypeListCreate(generics.ListCreateAPIView):
    queryset = ActivityType.objects.all()
    serializer_class = ActivityTypeSerializer

class ActivityTypeRetreiveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = ActivityType.objects.all()
    serializer_class = ActivityTypeSerializer
    lookup_field = "pk"


class SubmitComplementaryActivityCreate(generics.CreateAPIView):
    queryset = ComplementaryActivity.objects.all()
    serializer_class = SubmitComplementaryActivitySerializer