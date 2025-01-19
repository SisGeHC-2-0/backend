from rest_framework import serializers


from .models import Major, HourType

class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ["id", "name"]


class HourTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HourType
        fields = ["id", "name", "total_max", "per_submission_max"]
