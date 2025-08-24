# serializers.py
from rest_framework import serializers
from .models import Labour, Attendance
# , Payment





from rest_framework import serializers
from .models import Labour, Attendance

class LabourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labour
        fields = '__all__'
        read_only_fields = ['user']  # 👈 This line fixes the error


        

class AttendanceListSerializer(serializers.ModelSerializer):
    labour = LabourSerializer(read_only=True)

    class Meta:
        model = Attendance
        fields = '__all__'

class AttendanceCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
