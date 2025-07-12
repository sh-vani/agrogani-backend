from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
from .models import Device
from accounts.models import Plan  

class DeviceLoginView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        device_id = request.data.get("device_id")
        device_name = request.data.get("device_name", "")
        
        if not device_id:
            return Response({"error": "Device ID is required"}, status=400)

        user = request.user
        user_plan = getattr(user, 'plan', None)

        if not user_plan:
            return Response({"error": "No plan assigned to user."}, status=400)

        # Count active devices for this user
        active_devices = Device.objects.filter(user=user).count()

        # Check if device already exists
        existing_device = Device.objects.filter(user=user, device_id=device_id).first()

        if existing_device:
            existing_device.last_login = timezone.now()
            existing_device.save()
            return Response({"message": "Login successful on existing device."})

        if active_devices >= user_plan.device_limit:
            return Response({"error": f"Device limit reached ({user_plan.device_limit})."}, status=403)

        # Add new device
        Device.objects.create(
            user=user,
            device_id=device_id,
            device_name=device_name
        )
        return Response({"message": "Login successful and device registered."})
