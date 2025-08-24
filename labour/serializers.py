# serializers.py
from rest_framework import serializers
from .models import Labour, Attendance
# , Payment




   # serializers.py
class LabourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labour
        fields = '__all__'
        read_only_fields = ['user']  # ✅ Prevent user spoofing
     

class AttendanceListSerializer(serializers.ModelSerializer):
    labour = LabourSerializer(read_only=True)

    class Meta:
        model = Attendance
        fields = '__all__'




class AttendanceCreateUpdateSerializer(serializers.ModelSerializer):
    def validate_labour(self, value):
        request = self.context.get('request')
        if value.user != request.user:
            raise serializers.ValidationError("You can only mark attendance for your own labour.")
        return value

    class Meta:
        model = Attendance
        fields = '__all__'

