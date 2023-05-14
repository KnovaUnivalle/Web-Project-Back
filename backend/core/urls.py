from rest_framework import routers
from .api import AdminViewSet, RoleViewSet, UserViewSet, ProductViewSet, StoreViewSet, SearchHistoryViewSet, SuggestionViewSet

router = routers.DefaultRouter()

# Creates the urls for POST, DELETE, PUT and GET 
router.register('api/admin', AdminViewSet, 'admin')
router.register('api/role', RoleViewSet, 'role')
router.register('api/user', UserViewSet, 'user')
router.register('api/product', ProductViewSet, 'product')
router.register('api/store', StoreViewSet, 'store')
router.register('api/searchHistory', SearchHistoryViewSet, 'searchHistory')
router.register('api/suggestion', SuggestionViewSet, 'suggestion')

urlpatterns = router.urls
