from django.urls import path

from .views import *




urlpatterns = [
    # LABOUR
    path('labour/', LabourListView.as_view(), name='labour-list'),
    path('add/', LabourCreateView.as_view(), name='labour-add'),
    path('<int:pk>/', LabourRetrieveView.as_view(), name='labour-detail'),
    path('<int:pk>/update/', LabourUpdateView.as_view(), name='labour-update'),
    path('<int:pk>/delete/', LabourDeleteView.as_view(), name='labour-delete'),

    # ATTENDANCE
    path('attendance/', AttendanceListView.as_view(), name='attendance-list'),
    path('attendance/add/', AttendanceCreateView.as_view(), name='attendance-add'),
    path('attendance/<int:pk>/', AttendanceRetrieveView.as_view(), name='attendance-detail'),
    path('attendance/<int:pk>/update/', AttendanceUpdateView.as_view(), name='attendance-update'),
    path('attendance/<int:pk>/delete/', AttendanceDeleteView.as_view(), name='attendance-delete'),

path('attendance/daily-overview/', DailyAttendanceOverview.as_view(), name='attendance-daily-overview'),




    # PAYMENT
#     path('payment/', PaymentListView.as_view(), name='payment-list'),
#     path('payment/add/', PaymentCreateView.as_view(), name='payment-add'),
#     path('payment/<int:pk>/', PaymentRetrieveView.as_view(), name='payment-detail'),
#     path('payment/<int:pk>/update/', PaymentUpdateView.as_view(), name='payment-update'),
#     path('payment/<int:pk>/delete/', PaymentDeleteView.as_view(), name='payment-delete'),
#
 ]
