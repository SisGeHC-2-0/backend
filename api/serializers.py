from django.db.models import Sum
from rest_framework import serializers, status
from rest_framework.response import Response

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
    event_dates = EventDateSerializer(many=True, read_only=True)  # Para receber a lista de datas
    
    class Meta:
        model = Event
        fields = ["id", "name", "desc_short", "desc_detailed", "enroll_date_begin", "enroll_date_end", "picture", "workload", "minimum_attendances", "maximum_enrollments", "address", "is_online", "ended", "ActivityTypeId", "professorId", "event_dates"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
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

        event = Event.objects.create(**validated_data)

        return event

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from .models import EventEnrollment, Event, EventDate, Attendance


class SubmitEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventEnrollment
        fields = ["id", "studentId", "eventId"]

    def create(self, validated_data):
        event = validated_data.get("eventId")
        student = validated_data.get("studentId")

        # Check max Enrollment
        current_enrollments = EventEnrollment.objects.filter(eventId=event).count()
        if current_enrollments >= event.maximum_enrollments:
            raise serializers.ValidationError({"error": "The Event is full."})

        # Check if Student is enrollment
        if EventEnrollment.objects.filter(eventId=event, studentId=student).exists():
            raise serializers.ValidationError({"error": "Student is already enrolled in this event."})

        # Create enrollment
        enrollment = EventEnrollment.objects.create(**validated_data)

        # Create Attendances
        event_dates = EventDate.objects.filter(eventId=event)
        for event_date in event_dates:
            Attendance.objects.create(
                enrollmentId=enrollment,
                eventDateId=event_date
            )

        return enrollment



class EventDateCreateSerializer(serializers.ModelSerializer):
    eventId = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())

    class Meta:
        model = EventDate
        fields = ["id", "eventId", "time_begin", "time_end", "date"]

    def create(self, validated_data):
        dates_data = validated_data.pop('dates', None)

        # Caso tenha 'dates', significa que o usuário passou uma lista
        if dates_data:
            event_dates = []
            for date_data in dates_data:
                date_data['eventId'] = validated_data['eventId']  # Herdando o evento
                event_date = EventDate.objects.create(**date_data)
                event_dates.append(event_date)
            return event_dates

        # Caso contrário, é a criação de apenas uma data
        return EventDate.objects.create(**validated_data)
