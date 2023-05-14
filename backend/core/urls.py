from rest_framework import routers
from .api import AdminViewSet

router = routers.DefaultRouter()

# Creates the urls for POST, DELETE, PUT and GET 
router.register('api/admin', AdminViewSet, 'admin')

urlpatterns = router.urls
