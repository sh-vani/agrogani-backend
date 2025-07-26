
from django.urls import path
from .views import UserProfileView, UserProfileUpdateView, UserProfileDeleteView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('profile/delete/', UserProfileDeleteView.as_view(), name='user-profile-delete'),
]
