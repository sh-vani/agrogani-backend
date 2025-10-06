# advisory/views.py
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from .models import Advisory, FertilizerShop
from .serializers import AdvisorySerializer, FertilizerShopSerializer
from adminauth.auth import AdminJWTAuthentication

# === USER APIS (Logged-in users can view only) ===
class UserAdvisoryListView(generics.ListAPIView):
    queryset = Advisory.objects.all()
    serializer_class = AdvisorySerializer
    authentication_classes = [AdminJWTAuthentication]  # ✅ User must be logged in
    permission_classes = [IsAuthenticated]  # ✅ Must be authenticated

class UserFertilizerShopListView(generics.ListAPIView):
    queryset = FertilizerShop.objects.all().order_by('name')
    serializer_class = FertilizerShopSerializer
    authentication_classes = [AdminJWTAuthentication]  # ✅ User must be logged in
    permission_classes = [IsAuthenticated]  # ✅ Must be authenticated

# === ADMIN APIS (JWT required for CRUD) ===
class AdminAdvisoryListCreateView(generics.ListCreateAPIView):
    queryset = Advisory.objects.all()
    serializer_class = AdvisorySerializer
    authentication_classes = [AdminJWTAuthentication]
    permission_classes = [IsAuthenticated]

class AdminAdvisoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Advisory.objects.all()
    serializer_class = AdvisorySerializer
    authentication_classes = [AdminJWTAuthentication]
    permission_classes = [IsAuthenticated]

class AdminFertilizerShopListCreateView(generics.ListCreateAPIView):
    queryset = FertilizerShop.objects.all().order_by('name')
    serializer_class = FertilizerShopSerializer
    authentication_classes = [AdminJWTAuthentication]
    permission_classes = [IsAuthenticated]

class AdminFertilizerShopDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FertilizerShop.objects.all()
    serializer_class = FertilizerShopSerializer
    authentication_classes = [AdminJWTAuthentication]
    permission_classes = [IsAuthenticated]

# === DASHBOARD COUNT VIEW ===
class AdvisoryShopCountView(APIView):
    authentication_classes = [AdminJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = now().date()
        data = [
            {
                "title": "Total Advisors",
                "count": Advisory.objects.count()
            },
            {
                "title": "Advisors Added Today",
                "count": Advisory.objects.filter(created_at__date=today).count()
            },
            {
                "title": "Total Fertilizer Shops",
                "count": FertilizerShop.objects.count()
            }
        ]
        return Response(data)