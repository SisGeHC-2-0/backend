from urllib import request

from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from django.http import HttpRequest, FileResponse, HttpResponseNotFound, JsonResponse
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
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

class ComplementaryActivitySerializerCoordenadorMajor(generics.ListAPIView):
    serializer_class = ComplementaryActivitySerializerCoordenador

    def get_queryset(self):
        course_id = self.kwargs['majorId_id']
        return ComplementaryActivity.objects.filter(
            studentId__majorId=course_id, status=None
        )

class ComplementaryActivitySerializerMajorType(generics.ListAPIView):
    serializer_class = ComplementaryActivitySerializer

    def get_queryset(self):
        course_id = self.kwargs['majorId_id']
        return ComplementaryActivity.objects.filter(
            studentId__majorId=course_id, ActivityTypeId=self.kwargs['ActivityTypeId_id']
        )

class ComplementaryActivitySerializerEditApprovedRecuseFeedbak(generics.UpdateAPIView):
    serializer_class = EditApprovedRecuseFeedbackComplementaryActivitySerializer
    def get_object(self):
        try:
            pk = self.kwargs['ComplementaryActivity_id']
            return ComplementaryActivity.objects.get(pk=pk)
        except ComplementaryActivity.DoesNotExist:
            raise Http404("Couldn't find the complementary activity associated with these values")

    def update(self, request, *args, **kwargs):
        activity = self.get_object()

        serializer = self.get_serializer(activity, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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