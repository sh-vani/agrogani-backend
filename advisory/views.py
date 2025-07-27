from rest_framework import generics, permissions
from .models import Advisory,FertilizerShop  # Updated model import
from .serializers import AdvisorySerializer,FertilizerShopSerializer  # Updated serializer import
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404



# your other imports...


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



# add
class AddFertilizerShopView(APIView):
    def post(self, request):
        serializer = FertilizerShopSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Shop added."}, status=201)
        return Response(serializer.errors, status=400)



# 
class ListFertilizerShopsView(APIView):
    def get(self, request):
        shops = FertilizerShop.objects.all().order_by('name')
        serializer = FertilizerShopSerializer(shops, many=True)
        return Response(serializer.data)


# 

class UpdateFertilizerShopView(APIView):
    def put(self, request, shop_id):
        shop = get_object_or_404(FertilizerShop, id=shop_id)
        serializer = FertilizerShopSerializer(shop, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Shop updated."})
        return Response(serializer.errors, status=400)




# 
class DeleteFertilizerShopView(APIView):
    def delete(self, request, shop_id):
        shop = get_object_or_404(FertilizerShop, id=shop_id)
        shop.delete()
        return Response({"success": True, "message": "Shop deleted."})






# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import generics
# from datetime import date
# from django.contrib.gis.measure import D
# from .models import Region, Advisory, ServiceProvider
# from .serializers import RegionSerializer, AdvisorySerializer, ServiceProviderSerializer

# # 🔹 POST APIs
# class RegionCreateAPIView(generics.CreateAPIView):
#     queryset = Region.objects.all()
#     serializer_class = RegionSerializer

# class AdvisoryCreateAPIView(generics.CreateAPIView):
#     queryset = Advisory.objects.all()
#     serializer_class = AdvisorySerializer

# class ServiceProviderCreateAPIView(generics.CreateAPIView):
#     queryset = ServiceProvider.objects.all()
#     serializer_class = ServiceProviderSerializer

# # 🔹 Dashboard GET API
# class AdvisoryDashboardAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         crop = request.query_params.get("crop", "wheat")
#         radius = int(request.query_params.get("radius", 50))
#         region = request.user.profile.region  # Assuming user profile has region
#         location_point = region.point

#         advisories = Advisory.objects.filter(crop=crop, region=region)
#         summary = {
#             "active": advisories.count(),
#             "critical": advisories.filter(urgency="critical").count(),
#             "new_today": advisories.filter(date=date.today()).count()
#         }

#         highlight = advisories.order_by('-urgency', '-date').first()

#         services = ServiceProvider.objects.filter(
#             location__distance_lte=(location_point, D(km=radius))
#         )

#         return Response({
#             "summary": summary,
#             "highlight": AdvisorySerializer(highlight).data if highlight else {},
#             "agri_services": {
#                 "radius_km": radius,
#                 "center": {
#                     "lat": region.lat,
#                     "lng": region.lng
#                 },
#                 "providers": ServiceProviderSerializer(services, many=True).data
#             }
#         })
