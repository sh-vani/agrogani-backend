# pages/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Page
from .serializers import PageSerializer, PageUpdateSerializer
from adminauth.auth import AdminJWTAuthentication

class AdminPageViewSet(viewsets.ModelViewSet):
    """
    Admin API for managing all pages (Terms, Privacy, About, Contact)
    JWT authentication required for all operations
    """
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    authentication_classes = [AdminJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return PageUpdateSerializer
        return PageSerializer

    # 🔹 Custom endpoints for each page type
    @action(detail=False, methods=['get'], url_path='terms')
    def terms(self, request):
        page = Page.objects.filter(page_type='terms').first()
        if page:
            return Response(PageSerializer(page).data)
        return Response({"detail": "Terms & Conditions not found"}, status=404)

    @action(detail=False, methods=['get'], url_path='privacy')
    def privacy(self, request):
        page = Page.objects.filter(page_type='privacy').first()
        if page:
            return Response(PageSerializer(page).data)
        return Response({"detail": "Privacy Policy not found"}, status=404)

    @action(detail=False, methods=['get'], url_path='about')
    def about(self, request):
        page = Page.objects.filter(page_type='about').first()
        if page:
            return Response(PageSerializer(page).data)
        return Response({"detail": "About Us not found"}, status=404)

    @action(detail=False, methods=['get'], url_path='contact')
    def contact(self, request):
        page = Page.objects.filter(page_type='contact').first()
        if page:
            return Response(PageSerializer(page).data)
        return Response({"detail": "Contact Us not found"}, status=404)

class UserPageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    User API for viewing pages (no authentication required)
    Only GET operations allowed
    """
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = [AllowAny]  # ✅ No authentication required

    @action(detail=False, methods=['get'], url_path='terms')
    def terms(self, request):
        page = Page.objects.filter(page_type='terms').first()
        if page:
            return Response(PageSerializer(page).data)
        return Response({"detail": "Terms & Conditions not found"}, status=404)

    @action(detail=False, methods=['get'], url_path='privacy')
    def privacy(self, request):
        page = Page.objects.filter(page_type='privacy').first()
        if page:
            return Response(PageSerializer(page).data)
        return Response({"detail": "Privacy Policy not found"}, status=404)

    @action(detail=False, methods=['get'], url_path='about')
    def about(self, request):
        page = Page.objects.filter(page_type='about').first()
        if page:
            return Response(PageSerializer(page).data)
        return Response({"detail": "About Us not found"}, status=404)

    @action(detail=False, methods=['get'], url_path='contact')
    def contact(self, request):
        page = Page.objects.filter(page_type='contact').first()
        if page:
            return Response(PageSerializer(page).data)
        return Response({"detail": "Contact Us not found"}, status=404)