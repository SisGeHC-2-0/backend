from rest_framework import serializers


from .models import Major, ActivityType

class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ["id", "name"]


class ActivityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityType
        fields = ["id", "name", "total_max", "per_submission_max"]
