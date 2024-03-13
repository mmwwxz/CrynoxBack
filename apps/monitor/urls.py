from rest_framework import routers
from .views import UserFormViewSet, PortfolioListView

router = routers.DefaultRouter()
router.register(r'', UserFormViewSet, PortfolioListView)

urlpatterns = []
urlpatterns += router.urls
