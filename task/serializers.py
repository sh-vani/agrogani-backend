from rest_framework import serializers
from .models import Task



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'is_completed']
