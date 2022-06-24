from rest_framework.routers import DefaultRouter
from .views import PublicationViewSet

router = DefaultRouter()
router.register('publication', PublicationViewSet)\

urlpatterns = []
urlpatterns += router.urls
