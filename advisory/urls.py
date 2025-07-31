from django.urls import path
from .views import (
    AdvisoryListAPIView,
    AdvisoryCreateAPIView,
    AdvisoryRetrieveAPIView,
    AdvisoryUpdateAPIView,
    AdvisoryDeleteAPIView,
        AddFertilizerShopView,
    ListFertilizerShopsView,
    UpdateFertilizerShopView,
    DeleteFertilizerShopView,
    AdvisoryShopCountView
)

urlpatterns = [
    path('advisories/list/', AdvisoryListAPIView.as_view(), name='advisory-list'),
    path('advisories/create/', AdvisoryCreateAPIView.as_view(), name='advisory-create'),
    path('advisories/<int:pk>/', AdvisoryRetrieveAPIView.as_view(), name='advisory-detail'),
    path('advisories/<int:pk>/update/', AdvisoryUpdateAPIView.as_view(), name='advisory-update'),
    path('advisories/<int:pk>/delete/', AdvisoryDeleteAPIView.as_view(), name='advisory-delete'),

     path('shops/add/', AddFertilizerShopView.as_view(), name='add-shop'),
    path('shops/list/', ListFertilizerShopsView.as_view(), name='list-shops'),
    path('shops/<int:shop_id>/update/', UpdateFertilizerShopView.as_view(), name='update-shop'),
    path('shops/<int:shop_id>/delete/', DeleteFertilizerShopView.as_view(), name='delete-shop'),


    path('advisory-count/', AdvisoryShopCountView.as_view(), name='advisory-shop-count'),


]




# from django.urls import path
# from .views import (
#     RegionCreateAPIView,
#     AdvisoryCreateAPIView,
#     ServiceProviderCreateAPIView,
#     AdvisoryDashboardAPIView
# )

# urlpatterns = [
#     path('region/', RegionCreateAPIView.as_view(), name='create-region'),
#     path('advisory/', AdvisoryCreateAPIView.as_view(), name='create-advisory'),
#     path('service-provider/', ServiceProviderCreateAPIView.as_view(), name='create-service-provider'),
#     path('dashboard/', AdvisoryDashboardAPIView.as_view(), name='advisory-dashboard'),
# ]




