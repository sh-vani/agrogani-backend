from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.models import Plan, User
import razorpay
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .serializers import PlanSerializer,UserPlanSerializer
# Razorpay client init
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

class PlanListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        plans = Plan.objects.filter(is_active=True)
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data)

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        plan_id = request.data.get('plan_id')
        try:
            plan = Plan.objects.get(id=plan_id, is_active=True)
        except Plan.DoesNotExist:
            return Response({'error': 'Invalid plan selected.'}, status=400)

        if plan.price == 0:
            return Response({'message': 'This is a free plan. Please choose via registration or admin.'}, status=400)

        order = razorpay_client.order.create({
            "amount": int(plan.price * 100),
            "currency": "INR",
            "payment_capture": 1
        })

        return Response({
            "order_id": order['id'],
            "amount": order['amount'],
            "currency": order['currency']
        })

class PaymentSuccessView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_id = request.data.get('payment_id')
        plan_id = request.data.get('plan_id')

        try:
            plan = Plan.objects.get(id=plan_id, is_active=True)
        except Plan.DoesNotExist:
            return Response({'error': 'Invalid plan.'}, status=400)

        # Update user plan
        user = request.user
        user.plan = plan
        user.save()

        return Response({"message": "Plan activated successfully!"})

class ActivePlanView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.plan:
            serializer = UserPlanSerializer(request.user)
            return Response(serializer.data)
        return Response({"message": "No active plan."})
