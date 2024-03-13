from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from apps.monitor.views import PortfolioViewSet, LanguageViewSet, UserFormViewSet

from .drf_swagger import urlpatterns as doc_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('form/', UserFormViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-form'),
    path('form/<int:pk>/', UserFormViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user'),
    path('portfolio/', PortfolioViewSet.as_view({'get': 'list', 'post': 'create'}), name='portfolio-list'),
    path('portfolio/<int:pk>/', PortfolioViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='portfolio-detail'),
    path('languages/', LanguageViewSet.as_view({'get': 'list'}), name='language-list'),
]

urlpatterns += doc_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
