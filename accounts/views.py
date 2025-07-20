from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, OTP, Plan
from .serializers import RegisterSerializer, VerifyOTPSerializer, SetPasswordSerializer
from django.core.mail import send_mail
from random import randint

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            mobile = serializer.validated_data.get('mobile')
            full_name = serializer.validated_data['full_name']

            if User.objects.filter(email=email).exists() or User.objects.filter(mobile=mobile).exists():
                return Response({'detail': 'User already exists with this email or mobile.'}, status=400)

            user = User.objects.create(
                email=email,
                mobile=mobile,
                full_name=full_name,
                plan=Plan.objects.get(name="Free")
            )

            email_otp = str(randint(100000, 999999))
            mobile_otp = str(randint(100000, 999999))
            OTP.objects.create(user=user, email_otp=email_otp, mobile_otp=mobile_otp)

            if email:
                send_mail(
                    'Your AgroGanit Email OTP',
                    f'Your OTP is {email_otp}',
                    'yourmail@example.com',
                    [email]
                )
            if mobile:
                # Yaha SMS service integrate karni hai
                print(f'Mobile OTP: {mobile_otp}')  # Abhi print kar rahe

            return Response({'detail': 'OTP sent on provided email and mobile.'})
        return Response(serializer.errors, status=400)

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            mobile = serializer.validated_data.get('mobile')
            otp = serializer.validated_data['otp']

            try:
                user = None
                if email:
                    user = User.objects.get(email=email)
                elif mobile:
                    user = User.objects.get(mobile=mobile)

                user_otp = OTP.objects.get(user=user)
                if user_otp.email_otp == otp or user_otp.mobile_otp == otp:
                    return Response({'detail': 'OTP verified successfully. Now set password.'})
                else:
                    return Response({'detail': 'Invalid OTP.'}, status=400)
            except User.DoesNotExist:
                return Response({'detail': 'User not found.'}, status=400)
        return Response(serializer.errors, status=400)

class SetPasswordView(APIView):
    def post(self, request):
        serializer = SetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            identifier = serializer.validated_data['email_or_mobile']
            password = serializer.validated_data['password']
            confirm_password = serializer.validated_data['confirm_password']

            if password != confirm_password:
                return Response({'detail': 'Passwords do not match.'}, status=400)

            try:
                user = User.objects.filter(email=identifier).first() or User.objects.filter(mobile=identifier).first()
                user.set_password(password)
                user.save()
                return Response({'detail': 'User registered successfully!'})
            except:
                return Response({'detail': 'User not found.'}, status=400)
        return Response(serializer.errors, status=400)


from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class LoginView(APIView):
    def post(self, request):
        email_or_mobile = request.data.get('email_or_mobile')
        password = request.data.get('password')

        # Try to get user by email or mobile
        user = User.objects.filter(email=email_or_mobile).first() or User.objects.filter(mobile=email_or_mobile).first()

        if user is None:
            return Response({"detail": "User not found."}, status=404)

        if not user.check_password(password):
            return Response({"detail": "Invalid password."}, status=400)

        # Generate JWT
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_id": user.id,
            "full_name": user.full_name,
            "plan": user.plan.name if user.plan else None
        })








# razorpay view

import razorpay
from django.conf import settings
from .models import RazorpayLog, Plan
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status

class CreatePlanOrderAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        plan_id = request.data.get('plan_id')
        plan = Plan.objects.get(id=plan_id)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        amount_paise = int(plan.price * 100)

        order_data = {
            "amount": amount_paise,
            "currency": "INR",
            "payment_capture": 1,
        }

        razorpay_order = client.order.create(data=order_data)

        RazorpayLog.objects.create(
            user=request.user,
            plan=plan,
            order_id=razorpay_order['id'],
            amount=plan.price,
            status='created'
        )

        return Response({
            "order_id": razorpay_order['id'],
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "amount": plan.price,
            "currency": "INR",
            "plan_name": plan.name
        })




class VerifyPaymentAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_id = request.data.get('payment_id')
        order_id = request.data.get('order_id')
        signature = request.data.get('signature')

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })
        except razorpay.errors.SignatureVerificationError:
            return Response({"error": "Payment verification failed."}, status=400)

        log = RazorpayLog.objects.filter(order_id=order_id).last()
        log.payment_id = payment_id
        log.status = 'success'
        log.save()

        request.user.plan = log.plan
        request.user.device_limit = log.plan.device_limit
        request.user.save()

        return Response({"message": "Payment verified. Plan upgraded successfully."})




from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .serializers import DashboardHeaderSerializer
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_header(request):
    now = timezone.now()
    user = request.user
    data = {
        "full_name": user.full_name or user.username,  # Fixed key name
        "date": now.strftime("%A, %B %d, %Y"),
        "time": now.strftime("%I:%M %p"),
    }
    serializer = DashboardHeaderSerializer(data)
    return Response(serializer.data)




from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import WeatherSerializer
from .services import fetch_weather_data

class WeatherAPIView(APIView):
    def get(self, request):
        lat = request.GET.get("lat")
        lon = request.GET.get("lon")

        if not lat or not lon:
            return Response({"error": "Missing location data"}, status=400)

        weather_info = fetch_weather_data(lat, lon)

        if "error" in weather_info:
            return Response({"error": weather_info["error"]}, status=500)

        serializer = WeatherSerializer(weather_info)
        return Response(serializer.data)
