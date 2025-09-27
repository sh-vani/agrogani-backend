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


from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from django.utils import timezone
from random import randint
from .models import User, OTP
from .serializers import (
    ForgotPasswordRequestSerializer,
    ForgotPasswordVerifyOTPSerializer,
    ResetPasswordSerializer
)

class ForgotPasswordRequestView(APIView):
    def post(self, request):
        serializer = ForgotPasswordRequestSerializer(data=request.data)
        if serializer.is_valid():
            identifier = serializer.validated_data.get('email_or_mobile')
            user = User.objects.filter(email=identifier).first() or User.objects.filter(mobile=identifier).first()

            if not user:
                return Response({'detail': 'User not found.'}, status=404)

            email_otp = str(randint(100000, 999999))
            mobile_otp = str(randint(100000, 999999))

            OTP.objects.update_or_create(
                user=user,
                defaults={'email_otp': email_otp, 'mobile_otp': mobile_otp, 'created_at': timezone.now()}
            )

            if user.email:
                send_mail(
                    'AgroGanit Password Reset OTP',
                    f'Your OTP is {email_otp}',
                    'yourmail@example.com',
                    [user.email]
                )
            if user.mobile:
                print(f'Mobile OTP: {mobile_otp}')  # Integrate SMS here

            return Response({'detail': 'OTP sent successfully.'})
        return Response(serializer.errors, status=400)

class ForgotPasswordVerifyOTPView(APIView):
    def post(self, request):
        serializer = ForgotPasswordVerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            otp = serializer.validated_data.get('otp')

            if not email:
                return Response({'detail': 'Email is required for verification.'}, status=400)

            try:
                user = User.objects.get(email=email)
                user_otp = OTP.objects.get(user=user)

                if user_otp.email_otp == otp:
                    user.is_otp_verified = True
                    user.save()
                    return Response({'detail': 'Email OTP verified successfully. You can now reset your password.'})
                else:
                    return Response({'detail': 'Invalid Email OTP.'}, status=400)
            except User.DoesNotExist:
                return Response({'detail': 'User not found.'}, status=404)
            except OTP.DoesNotExist:
                return Response({'detail': 'OTP not found.'}, status=404)
        return Response(serializer.errors, status=400)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import traceback

class ResetPasswordView(APIView):
    def post(self, request):
        try:
            serializer = ResetPasswordSerializer(data=request.data)
            if serializer.is_valid():
                identifier = serializer.validated_data.get('email_or_mobile')
                password = serializer.validated_data.get('password')
                confirm_password = serializer.validated_data.get('confirm_password')

                user = User.objects.filter(email=identifier).first()  # Only email allowed
                if not user:
                    return Response({'detail': 'User not found or mobile used instead of email.'}, status=404)

                if not user.is_otp_verified:
                    return Response({'detail': 'Email OTP not verified.'}, status=403)

                if password != confirm_password:
                    return Response({'detail': 'Passwords do not match.'}, status=400)

                user.set_password(password)
                user.is_otp_verified = False
                user.save()

                return Response({'detail': 'Password reset successful!'})
            return Response(serializer.errors, status=400)

        except Exception as e:
            traceback.print_exc()  # Will print full error in terminal
            return Response({'error': 'Internal Server Error: ' + str(e)}, status=500)

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChangePasswordSerializer

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            confirm_password = serializer.validated_data['confirm_password']

            user = request.user

            if not user.check_password(old_password):
                return Response({"detail": "Old password is incorrect."}, status=400)

            if new_password != confirm_password:
                return Response({"detail": "Passwords do not match."}, status=400)

            user.set_password(new_password)
            user.save()

            return Response({"detail": "Password changed successfully!"}, status=200)

        return Response(serializer.errors, status=400)



from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .serializers import DashboardHeaderSerializer

from django.utils import timezone
import pytz

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_header(request):
    ist = pytz.timezone('Asia/Kolkata')  # IST timezone
    now = timezone.now().astimezone(ist)
    user = request.user
    data = {
        "full_name": user.full_name or user.username,
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







# actuve log



# # active
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from .models import ActivityLog
# from .serializers import ActivityLogSerializer





# class RecentActivityAPI(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         logs = ActivityLog.objects.filter(
#             user=request.user
#         ).exclude(
#             event_type__icontains="/recent-activities/"
#         ).order_by("-timestamp")[:5]

#         serializer = ActivityLogSerializer(logs, many=True)
#         return Response(serializer.data)



# accounts/views.py

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import ActivityLog
from .serializers import ActivityLogSerializer

class RecentActivityAPI(APIView):
    """
    API endpoint to retrieve the 5 most recent activities for the logged-in user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the 5 most recent log entries for the current user
        logs = ActivityLog.objects.filter(user=request.user).order_by('-timestamp')[:5]
        
        # Serialize the data
        serializer = ActivityLogSerializer(logs, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # admin side api
    







from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # 🔑 Permission
from rest_framework_simplejwt.authentication import JWTAuthentication  # 🔑 JWT Auth
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from .models import RazorpayLog, User, Plan
from advisory.models import Advisory


class DashboardSummaryAPIView(APIView):
    authentication_classes = [JWTAuthentication]   # ✅ JWT token required
    permission_classes = [IsAuthenticated]         # ✅ Only logged-in users allowed

    def get(self, request):
        # 1. Basic Stats
        total_transactions = RazorpayLog.objects.filter(status='success').count()
        active_users = User.objects.filter(is_active=True).count()
        total_revenue = RazorpayLog.objects.filter(status='success').aggregate(Sum('amount'))['amount__sum'] or 0
        advisor_count = Advisory.objects.count()

        # 2. User Activity Data (Last 6 Weeks)
        user_activity = self.get_user_activity_data()

        # 3. User Distribution by Plan
        user_distribution = self.get_user_distribution()

        return Response({
            "total_transactions": total_transactions,
            "active_users": active_users,
            "total_revenue": total_revenue,
            "advisor_count": advisor_count,
            "user_activity": user_activity,
            "user_distribution": user_distribution
        })

    def get_user_activity_data(self):
        today = timezone.now().date()
        current = today
        weeks = []

        for i in range(6):
            week_start = current - timedelta(days=current.weekday())
            week_end = week_start + timedelta(days=6)
            weeks.append({
                "start": week_start,
                "end": week_end,
                "label": f"Week {i+1}"
            })
            current -= timedelta(weeks=1)

        weeks.reverse()

        result = []
        for week in weeks:
            new_registrations = User.objects.filter(
                date_joined__gte=week['start'],
                date_joined__lte=week['end']
            ).count()

            active_users_in_week = User.objects.filter(is_active=True).count()

            result.append({
                "week": week['label'],
                "active_users": active_users_in_week,
                "new_registrations": new_registrations
            })

        return result

    def get_user_distribution(self):
        distribution = User.objects.filter(plan__isnull=False).values('plan__name').annotate(count=Count('id'))
        return [
            {"plan": item['plan__name'], "count": item['count']}
            for item in distribution
        ]







from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import FarmerSerializer

class FarmersListView(APIView):
    """
    List all farmers or search by query
    GET /api/farmers/?search=John
    """
    def get(self, request):
        search = request.GET.get('search', '').strip()

        farmers = User.objects.all().select_related('plan')

        if search:
            farmers = farmers.filter(
                models.Q(full_name__icontains=search) |
                models.Q(email__icontains=search) |
                models.Q(mobile__icontains=search) |
                models.Q(id__icontains=search) |
                models.Q(plan__name__icontains=search) |
                models.Q(is_active__icontains=search.lower() in ['active', 'true'])
            )

        serializer = FarmerSerializer(farmers, many=True)
        return Response(serializer.data)

class FarmerDetailView(APIView):
    """
    Retrieve, Update or Delete a farmer
    """
    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    def get(self, request, pk):
        farmer = self.get_object(pk)
        serializer = FarmerSerializer(farmer)
        return Response(serializer.data)

    def put(self, request, pk):
        farmer = self.get_object(pk)
        serializer = FarmerSerializer(farmer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        farmer = self.get_object(pk)
        farmer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






















    
