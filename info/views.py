# from rest_framework import viewsets
# from .models import Page
# from .serializers import PageSerializer

# class PageViewSet(viewsets.ModelViewSet):   # <-- Important (not ReadOnly)
#     queryset = Page.objects.all()
#     serializer_class = PageSerializer



from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Page
from .serializers import PageSerializer

class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    # 🔹 Custom endpoints for each page
    @action(detail=False, methods=['get'], url_path='terms')
    def terms(self, request):
        page = Page.objects.filter(page_type='terms').first()
        if page:
            return Response(PageSerializer(page).data)
        return Response({"detail": "Terms not found"}, status=404)

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
