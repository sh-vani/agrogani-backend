from rest_framework import generics, permissions
from .models import Advisory  # Updated model import
from .serializers import AdvisorySerializer  # Updated serializer import

# List all advisories
class AdvisoryListAPIView(generics.ListAPIView):
    queryset = Advisory.objects.all()
    serializer_class = AdvisorySerializer
    permission_classes = [permissions.IsAuthenticated]

# Create new advisory
class AdvisoryCreateAPIView(generics.CreateAPIView):
    queryset = Advisory.objects.all()
    serializer_class = AdvisorySerializer
    permission_classes = [permissions.IsAuthenticated]

# Retrieve single advisory
class AdvisoryRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Advisory.objects.all()
    serializer_class = AdvisorySerializer
    permission_classes = [permissions.IsAuthenticated]

# Update single advisory
class AdvisoryUpdateAPIView(generics.UpdateAPIView):
    queryset = Advisory.objects.all()
    serializer_class = AdvisorySerializer
    permission_classes = [permissions.IsAuthenticated]

# Delete single advisory
class AdvisoryDeleteAPIView(generics.DestroyAPIView):
    queryset = Advisory.objects.all()
    serializer_class = AdvisorySerializer
    permission_classes = [permissions.IsAuthenticated]
