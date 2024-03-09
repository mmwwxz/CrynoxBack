from rest_framework import routers
from .views import UserFormViewSet

router = routers.DefaultRouter()
router.register(r'', UserFormViewSet)

urlpatterns = []
urlpatterns += router.urls
