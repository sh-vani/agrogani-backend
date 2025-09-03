from django.shortcuts import render

# Create your views here.
# adminauth/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AdminSignupSerializer

class AdminSignupView(APIView):
    def post(self, request):
        serializer = AdminSignupSerializer(data=request.data)
        if serializer.is_valid():
            admin = serializer.save()
            return Response({
                'message': 'Admin account created successfully',
                'admin': {
                    'id': admin.id,
                    'email': admin.email,
                    'full_name': admin.full_name
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
