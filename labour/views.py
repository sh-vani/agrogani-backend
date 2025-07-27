# views.py
from rest_framework import generics, permissions
from .models import Labour, Attendance
# Payment
from .serializers import LabourSerializer
# , PaymentSerializer
from rest_framework.response import Response
from rest_framework import status


# LABOUR VIEW



class LabourListView(generics.ListAPIView):
    serializer_class = LabourSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Labour.objects.filter(user=self.request.user)
    

class LabourCreateView(generics.CreateAPIView):
    serializer_class = LabourSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)

        return Response({
            "message": "Labour added successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

# class LabourCreateView(generics.CreateAPIView):
#     serializer_class = LabourSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

class LabourRetrieveView(generics.RetrieveAPIView):
    serializer_class = LabourSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Labour.objects.filter(user=self.request.user)

class LabourUpdateView(generics.UpdateAPIView):
    serializer_class = LabourSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Labour.objects.filter(user=self.request.user)

class LabourDeleteView(generics.DestroyAPIView):
    serializer_class = LabourSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Labour.objects.filter(user=self.request.user)


# labout Attendence 

from rest_framework import generics
from .models import Attendance
from .serializers import (
    AttendanceListSerializer, AttendanceCreateUpdateSerializer
)

# 📥 Create
class AttendanceCreateView(generics.CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceCreateUpdateSerializer
 
# 📃 List
class AttendanceListView(generics.ListAPIView):
    queryset = Attendance.objects.select_related('labour').all()
    serializer_class = AttendanceListSerializer

# 🔄 Update
class AttendanceUpdateView(generics.UpdateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceCreateUpdateSerializer

# ❌ Delete
class AttendanceDeleteView(generics.DestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceCreateUpdateSerializer

# 🔍 Retrieve (Optional)
class AttendanceRetrieveView(generics.RetrieveAPIView):
    queryset = Attendance.objects.select_related('labour').all()
    serializer_class = AttendanceListSerializer







from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from .models import Labour, Attendance

class DailyAttendanceOverview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_str = request.query_params.get('date')
        if not date_str:
            return Response({"error": "Date parameter is required"}, status=400)

        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

        labours = Labour.objects.filter(user=request.user)
        response_data = []

        for labour in labours:
            attendance = Attendance.objects.filter(labour=labour, date=target_date).first()
            response_data.append({
                "labour_id": labour.id,
                "name": labour.name,
                "mobile": labour.mobile,
                "daily_wage": str(labour.daily_wage),
                "gender": labour.gender,
                "status": attendance.status if attendance else None,
                "date": date_str
            })

        return Response(response_data)





# payment 


# from rest_framework import generics, permissions
# from core.models import Payment
# from core.serializers.payment_serializers import PaymentSerializer

# class PaymentListView(generics.ListAPIView):
#     serializer_class = PaymentSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Payment.objects.filter(labour__user=self.request.user)

# class PaymentCreateView(generics.CreateAPIView):
#     serializer_class = PaymentSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class PaymentRetrieveView(generics.RetrieveAPIView):
#     serializer_class = PaymentSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Payment.objects.filter(labour__user=self.request.user)

# class PaymentUpdateView(generics.UpdateAPIView):
#     serializer_class = PaymentSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Payment.objects.filter(labour__user=self.request.user)

# class PaymentDeleteView(generics.DestroyAPIView):
#     serializer_class = PaymentSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Payment.objects.filter(labour__user=self.request.user)



