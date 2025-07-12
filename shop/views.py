from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Shop
from .serializers import ShopSerializer

class ShopCreateView(generics.CreateAPIView):
    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ShopListView(generics.ListAPIView):
    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Shop.objects.filter(user=self.request.user).order_by('-created_at')
