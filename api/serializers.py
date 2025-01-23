from django.db.models import Sum
from rest_framework import serializers
from .validators import non_negative_int


from .models import Major, ActivityType, ComplementaryActivity, Certificate, Student

class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ["id", "name"]


class ActivityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityType
        fields = ["id", "name", "total_max", "per_submission_max"]

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

        ComplementaryActivity.objects.all().delete()

        certificate_data = validated_data.pop('certificateId')

        cerr = Certificate.objects.create(**certificate_data)

        activity = ComplementaryActivity(**validated_data, status=None, feedback='',certificateId=cerr, studentId=cerr.studentId)
        activity_type = activity.ActivityTypeId

        activity.workload = min(activity.workload, activity_type.per_submission_max)
               
        activity.save()

        return activity                                     
                                                    
    # workload = models.IntegerField()
    # status = models.BooleanField(null=True, default=None)
    # description = models.CharField(max_length=500)
    # feedback = models.TextField(max_length=500)
    # ActivityTypeId = models.ForeignKey('ActivityType', on_delete=models.CASCADE)
    # studentId = models.ForeignKey('Student', on_delete=models.CASCADE)
    # certificateId = models.ForeignKey('Certificate', on_delete=models.CASCADE, unique=True))
