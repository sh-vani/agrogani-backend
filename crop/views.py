from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Crop
from .serializers import CropSerializer
# add
class AddCropAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        plan = user.plan

        if not plan:
            return Response({"error": "No plan assigned. Please subscribe to a plan."}, status=status.HTTP_403_FORBIDDEN)

        crop_type = request.data.get("crop_type")

        # Block Type 3 permanently
        if crop_type == "type3":
            return Response({"error": "Crop type 3 is not allowed."}, status=status.HTTP_403_FORBIDDEN)

        # Plan-based crop type validation
        if plan.price == 0:  # Free plan
            if crop_type != "type1":
                return Response({"error": "Your plan only allows adding crop type 1."}, status=status.HTTP_403_FORBIDDEN)
        elif plan.price in [699, 1199]:
            if crop_type not in ["type1", "type2"]:
                return Response({"error": "Invalid crop type for your plan."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error": "Your plan does not allow adding crops."}, status=status.HTTP_403_FORBIDDEN)

        serializer = CropSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({"success": "Crop added successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#  list 


class CropListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        crops = Crop.objects.filter(user=user).order_by('-created_at')
        serializer = CropSerializer(crops, many=True)
        return Response({
            "success": True,
            "count": crops.count(),
            "data": serializer.data
        })


# recent  list 

class CropRecentListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        crops = Crop.objects.filter(user=user).order_by('-created_at')[:3]
        serializer = CropSerializer(crops, many=True)
        return Response({
            "success": True,
            "count": crops.count(),
            "data": serializer.data
        })



# delete
class CropDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        user = request.user
        try:
            crop = Crop.objects.get(pk=pk, user=user)
        except Crop.DoesNotExist:
            return Response({"error": "Crop not found or you don't have permission to delete it."}, status=status.HTTP_404_NOT_FOUND)

        crop.delete()
        return Response({"success": "Crop deleted successfully."}, status=status.HTTP_200_OK)
    



# crop list
from rest_framework import generics, permissions
from .models import Crop
from .serializers import CropSerializer  # banaya hua serializer

class UserCropListView(generics.ListAPIView):
    serializer_class = CropSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Crop.objects.filter(user=self.request.user)
