from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from apps.monitor.views import PortfolioListView

from .drf_swagger import urlpatterns as doc_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('form/', include('apps.monitor.urls')),
    path('portfolio/', PortfolioListView.as_view(), name='portfolio-list'),
]

urlpatterns += doc_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
