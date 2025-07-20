from django.urls import path
from .views import AddServiceProviderAPIView, AdvisoryServiceProvidersAPIView

urlpatterns = [
    path('api/service-providers/add/', AddServiceProviderAPIView.as_view(), name='add-service-provider'),
    path('api/advisory/service-providers/', AdvisoryServiceProvidersAPIView.as_view(), name='advisory-service-providers'),
]
