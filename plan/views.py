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
from rest_framework import status
from django.shortcuts import get_object_or_404


class PlanListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        plans = Plan.objects.filter(is_active=True)
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlanDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Plan, pk=pk)

    def get(self, request, pk):
        plan = self.get_object(pk)
        serializer = PlanSerializer(plan)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        plan = self.get_object(pk)
        serializer = PlanSerializer(plan, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        plan = self.get_object(pk)
        plan.is_active = False  # Soft delete
        plan.save()
        return Response(
            {"message": "Plan deactivated successfully."}, 
            status=status.HTTP_200_OK


        )












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
