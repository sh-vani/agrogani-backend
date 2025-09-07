from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PageViewSet

router = DefaultRouter()
router.register(r'pages', PageViewSet, basename='pages')


urlpatterns = router.urls