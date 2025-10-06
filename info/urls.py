


# pages/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminPageViewSet, UserPageViewSet

# Admin router (JWT required)
admin_router = DefaultRouter()
admin_router.register(r'admin/pages', AdminPageViewSet, basename='admin-pages')

# User router (no auth required)
user_router = DefaultRouter()
user_router.register(r'pages', UserPageViewSet, basename='user-pages')

urlpatterns = [
    path('', include(admin_router.urls)),  # Admin APIs
    path('', include(user_router.urls)),   # User APIs
]