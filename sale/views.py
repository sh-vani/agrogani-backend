# from rest_framework import permissions, status, generics
# from rest_framework.response import Response
# from .models import QuickSale, DetailedSale
# from .serializers import QuickSaleSerializer, DetailedSaleSerializer
# from .permissions import IsPaidMember

# # QUICK SALE ADD
# class QuickSaleAddView(generics.CreateAPIView):
#     queryset = QuickSale.objects.all()
#     serializer_class = QuickSaleSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

#     def create(self, request, *args, **kwargs):
#         response = super().create(request, *args, **kwargs)
#         return Response({
#             'message': 'Quick sale successfully added',
#             'data': response.data
#         }, status=status.HTTP_201_CREATED)

# # QUICK SALE VIEW
# class QuickSaleListView(generics.ListAPIView):
#     serializer_class = QuickSaleSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return QuickSale.objects.filter(user=self.request.user)

# # DETAILED SALE ADD (PAID MEMBERS ONLY)
# class DetailedSaleAddView(generics.CreateAPIView):
#     queryset = DetailedSale.objects.all()
#     serializer_class = DetailedSaleSerializer
#     permission_classes = [permissions.IsAuthenticated, IsPaidMember]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

#     def create(self, request, *args, **kwargs):
#         response = super().create(request, *args, **kwargs)
#         return Response({
#             'message': 'Detailed sale successfully added',
#             'data': response.data
#         }, status=status.HTTP_201_CREATED)

# # DETAILED SALE VIEW
# class DetailedSaleListView(generics.ListAPIView):
#     serializer_class = DetailedSaleSerializer
#     permission_classes = [permissions.IsAuthenticated, IsPaidMember]

#     def get_queryset(self):
#         return DetailedSale.objects.filter(user=self.request.user)




from rest_framework import permissions, status, generics
from rest_framework.response import Response
from .models import QuickSale, DetailedSale
from .serializers import QuickSaleSerializer, DetailedSaleSerializer
from .permissions import IsPaidMember  # Assuming ye bana hai







# ✅ Quick Sale Add (sirf add)
class QuickSaleAddView(generics.CreateAPIView):
    serializer_class = QuickSaleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({
            "message": "Quick sale successfully added"
        }, status=status.HTTP_201_CREATED)

# ✅ Detailed Sale Add (sirf add, paid member)
class DetailedSaleAddView(generics.CreateAPIView):
    serializer_class = DetailedSaleSerializer
    permission_classes = [permissions.IsAuthenticated, IsPaidMember]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({
            "message": "Detailed sale successfully added"
        }, status=status.HTTP_201_CREATED)

# QUICK SALE VIEW
class QuickSaleListView(generics.ListAPIView):
    serializer_class = QuickSaleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return QuickSale.objects.filter(user=self.request.user)



# DETAILED SALE VIEW
class DetailedSaleListView(generics.ListAPIView):
    serializer_class = DetailedSaleSerializer
    permission_classes = [permissions.IsAuthenticated, IsPaidMember]

    def get_queryset(self):
        return DetailedSale.objects.filter(user=self.request.user)
