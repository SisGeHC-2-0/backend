from django.db.models import Sum
from rest_framework import serializers
from .validators import non_negative_int
from rest_framework.validators import ValidationError

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

class ComplementaryActivitySerializerStudentName(serializers.ModelSerializer):
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

    def validate(self, data):
        if self.instance.status is not None:
            raise ValidationError("Can only edit Complementary Activities with status null")
        if data['status'] is None:
            raise ValidationError("Cant change Complementary Activities status to null")

        return data

    def update(self, instance :ComplementaryActivity, validated_data):
        if validated_data['status']:

            all_valid_activities_of_type = ComplementaryActivity.objects.filter(
                                                                                status=True, 
                                                                                ActivityTypeId=instance.ActivityTypeId, 
                                                                                studentId=instance.studentId
                                                                               )
            
            accumulated_workload = all_valid_activities_of_type.aggregate(Sum('workload'))["workload__sum"] or 0

            validated_data['workload'] = min(
                                             instance.ActivityTypeId.total_max - accumulated_workload, 
                                             instance.workload, 
                                             instance.ActivityTypeId.per_submission_max
                                            )

        return super().update(instance, validated_data)

class ActivityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityType
        fields = ["id", "name", "total_max", "per_submission_max"]

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "name", "password", "email", "enrollment_number", "majorId_id"]
        
        
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

        certificate_data = validated_data.pop('certificateId')

        cerr = Certificate.objects.create(**certificate_data)

        activity = ComplementaryActivity(**validated_data, status=None, feedback='',certificateId=cerr, studentId=cerr.studentId)               
        activity.save()

        return activity                                     

class ProfessorSerializer(serializers.ModelSerializer):
    major = MajorSerializer(source="majorId")

    class Meta:
        model = Professor
        fields = ["id", "name", "email", "enrollment_number", "major"]

class EventDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventDate
        fields = ["date", "time_begin", "time_end"]

class EventSerializer(serializers.ModelSerializer):
    # professor = ProfessorSerializer(source="professorId", read_only=True)
    professorId = serializers.PrimaryKeyRelatedField(queryset=Professor.objects.all(), write_only=True)
    event_dates = EventDateSerializer(many=True)  # Para receber a lista de datas
    
    class Meta:
        model = Event
        fields = ["id", "name", "desc_short", "desc_detailed", "enroll_date_begin", "enroll_date_end", "picture", "workload", "minimum_attendances", "maximum_enrollments", "address", "is_online", "ended", "ActivityTypeId", "professorId", "event_dates"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        path_begin = str(instance._meta.get_field('picture').upload_to) 
        path_end = instance.picture.url

        full_path = '/' + path_begin.replace(os.sep, '/') + path_end[1:]

        req = self.context["request"]

        representation['picture'] = req.build_absolute_uri(full_path)

        # Adicionando detalhes do professor ao campo professorId
        professor = instance.professorId
        representation['professorId'] = {
            "id": professor.id,
            "name": professor.name,
            "email": professor.email,
            "enrollment_number": professor.enrollment_number,
            "major": {
                "id": professor.majorId.id,
                "name": professor.majorId.name
            }
        }
        return representation

    def create(self, validated_data):
        event_dates_data = validated_data.pop("event_dates")

        event = Event.objects.create(**validated_data)

        for date in event_dates_data:
            EventDate.objects.create(eventId=event, **date) 

        return event
