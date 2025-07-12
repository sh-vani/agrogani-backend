from django.urls import path
from .views import AddCropAPIView ,CropListAPIView,CropRecentListAPIView,CropDeleteAPIView ,UserCropListView

urlpatterns = [
    path('add-crop/', AddCropAPIView.as_view(), name='add-crop'),
        path('my-crops/', CropListAPIView.as_view(), name='my-crops'),
     path('crop/recent/', CropRecentListAPIView.as_view(), name='crop-recent'),
    path('crop/delete/<int:pk>/', CropDeleteAPIView.as_view(), name='crop-delete'),
   path('user-crops/', UserCropListView.as_view(), name='user-crop-list'),

]



