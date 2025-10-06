
# pages/serializers.py
from rest_framework import serializers
from .models import Page

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'page_type', 'title', 'description', 'created_at', 'updated_at']

class PageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['title', 'description']  # Don't allow changing page_type