from django.urls import path
from .views import (
    AdvisoryListAPIView,
    AdvisoryCreateAPIView,
    AdvisoryRetrieveAPIView,
    AdvisoryUpdateAPIView,
    AdvisoryDeleteAPIView,
)

urlpatterns = [
    path('advisories/list/', AdvisoryListAPIView.as_view(), name='advisory-list'),
    path('advisories/create/', AdvisoryCreateAPIView.as_view(), name='advisory-create'),
    path('advisories/<int:pk>/', AdvisoryRetrieveAPIView.as_view(), name='advisory-detail'),
    path('advisories/<int:pk>/update/', AdvisoryUpdateAPIView.as_view(), name='advisory-update'),
    path('advisories/<int:pk>/delete/', AdvisoryDeleteAPIView.as_view(), name='advisory-delete'),
]
