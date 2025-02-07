from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from django.http import HttpRequest, FileResponse, HttpResponseNotFound, JsonResponse
from django.http import Http404 
# Create your views here.

class MajorListCreate(generics.ListCreateAPIView):
    queryset = Major.objects.all()
    serializer_class = MajorSerializer

class MajorRetreiveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Major.objects.all()
    serializer_class = MajorSerializer
    lookup_field = "pk"

class ComplementaryActivitySerializerStudent(generics.ListAPIView):
    serializer_class = ComplementaryActivitySerializer
    def get_queryset(self):
        return ComplementaryActivity.objects.filter(studentId=self.kwargs['studentId_id'])

class ComplementaryActivitySerializerStudentName(generics.ListAPIView):
    serializer_class = ComplementaryActivitySerializer
    def get_queryset(self):
        name = self.kwargs['name']
        return ComplementaryActivity.objects.filter(studentId__name__icontains=name)


class ComplementaryActivitySerializerStudentType(generics.ListAPIView):
    serializer_class = ComplementaryActivitySerializer
    def get_queryset(self):
        return ComplementaryActivity.objects.filter(studentId=self.kwargs['studentId_id'], ActivityTypeId=self.kwargs['ActivityTypeId_id'])

class ComplementaryActivitySerializerMajor(generics.ListAPIView):
    serializer_class = ComplementaryActivitySerializer

    def get_queryset(self):
        course_id = self.kwargs['majorId_id']
        return ComplementaryActivity.objects.filter(
            studentId__majorId=course_id
        )

class ComplementaryActivitySerializerMajorType(generics.ListAPIView):
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

class StudentListCreate(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentRetreiveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = "pk"

class EventListCreate(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventRetreiveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = "pk"

class CertificateRetrieve(generics.RetrieveAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer

class CertificateRetrieveByEventAndStudent(generics.RetrieveAPIView):
    serializer_class = CertificateSerializer
    def get_object(self):
        event_id = self.kwargs['event_id']  
        student_id = self.kwargs['student_id']

        try:
            return ComplementaryActivity.objects.get(
                                                    studentId_id = student_id, 
                                                    certificateId__eventId_id = event_id
                                                    ).certificateId
        except Exception as e:
            raise Http404("Couldnt find the certificate associeted with these values")



# File retrievers

def retrieve_img(request : HttpRequest,entitty_name , pic_name: str):
    path = os.sep.join(['files', 'images', entitty_name, pic_name])
    
    if not os.path.exists( path):
        return HttpResponseNotFound(f"File {entitty_name}, {pic_name} doesnt exist")

    return FileResponse(open(path, 'rb'))


def retrieve_certificate(request : HttpRequest, cer_name: str):
    path = os.sep.join(['files', 'certificates', cer_name])
    
    if not os.path.exists( path):
        return HttpResponseNotFound(f"certificate {cer_name} doesnt exist")

    return FileResponse(open(path, 'rb'))