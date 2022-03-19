from dash.models import PlannedAbsence, SkyUser, Attendance
from rest_framework import serializers

### Model Serialzers ###
class SkyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkyUser
        fields = ['id', 'preferred_name', 'last_name', 'roles', 'first_name']

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class PlannedAbsenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlannedAbsence
        fields = '__all__'

    def create(self, validated_data):
        record = PlannedAbsence(**validated_data)
        record.save()
        return record
        
### Custom Serialzers ###
class StudentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)

class AttendanceCodeSerializer(serializers.Serializer):
    codes = serializers.ListField()

class StudentRequestSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100) or ''
    last_name = serializers.CharField(max_length=100) or ''
    grade_level = serializers.CharField() or ''

