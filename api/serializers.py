from django.db.models import Sum
from rest_framework import serializers
from .validators import non_negative_int

from .models import *

class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ["id", "name"]

class ComplementaryActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = ComplementaryActivity
        fields = ["id", "workload", "status", "description", "feedback", "ActivityTypeId_id", "certificateId_id", "studentId_id"]

class ComplementaryActivitySerializerStudent(serializers.ModelSerializer):
    activity_name = serializers.CharField(source='ActivityTypeId.name', read_only=True)
    certificate_date = serializers.DateTimeField(source='certificateId.emission_date', read_only=True)
    class Meta:
        model = ComplementaryActivity
        fields = ["id", "workload", "status", "description", "feedback", "activity_name", "certificate_date", "studentId_id"]

class ComplementaryActivitySerializerCoordenador(serializers.ModelSerializer):
    # Campos personalizados
    activity_name = serializers.CharField(source='ActivityTypeId.name', read_only=True)
    student_name = serializers.CharField(source='studentId.name', read_only=True)
    certificate_file = serializers.FileField(source='certificateId.file', read_only=True)

    class Meta:
        model = ComplementaryActivity
        fields = ['id', 'workload', 'description', 'activity_name', 'student_name', 'certificate_file']

    def to_representation(self, instance):
        # Retorna os dados personalizados
        representation = super().to_representation(instance)

        return representation

class EditApprovedRecuseFeedbackComplementaryActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplementaryActivity
        fields = ["id", "status", "feedback"]

class ActivityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityType
        fields = ["id", "name", "total_max", "per_submission_max"]

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "email", "enrollment_number", "status", "name", "majorId_id"]
        
        
class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = [ 'file', 'studentId', 'eventId', 'emission_date' ]

class SubmitComplementaryActivitySerializer(serializers.ModelSerializer):
    certificateId = CertificateSerializer(required=True, many=False)
    workload = serializers.IntegerField(validators=[non_negative_int])


    class Meta:
        model = ComplementaryActivity
        fields = ['workload', 'description', 'ActivityTypeId', 'certificateId']


    def create(self, validated_data):

        # ComplementaryActivity.objects.all().delete()

        certificate_data = validated_data.pop('certificateId')

        cerr = Certificate.objects.create(**certificate_data)

        activity = ComplementaryActivity(**validated_data, status=None, feedback='',certificateId=cerr, studentId=cerr.studentId)
        activity_type = activity.ActivityTypeId

        activity.workload = min(activity.workload, activity_type.per_submission_max)
               
        activity.save()

        return activity                                     
                                                    
