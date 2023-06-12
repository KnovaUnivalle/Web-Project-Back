from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers
from .views import *
from .crud import *

router = routers.DefaultRouter()

router.register(r'rol', RoleViewSet)
router.register(r'product', ProductViewSet)
router.register(r'store', StoreViewSet)
router.register(r'search_history', SearchHistoryViewSet)
router.register(r'suggestion', SuggestionViewSet)

urlpatterns = [
    path('admin/register/', registerAdmin, name='registerAdmin'),
    path('user/register/', RegisterUser.as_view(), name='resgisterUser'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('customer/', CustomerView.as_view(), name='customer'),
    path('manager/', ManagerView.as_view(), name='manager'),
    path('administrator/', AdminView.as_view(), name='administrator'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('google/', GoogleSocialAuthView.as_view()),
    # Creates the urls for POST, DELETE, PUT and GET
    path('users/', list_user, name='list-users'),
    path('users/latest/', list_latest_users, name='latest-users'),
    path('users/<int:id>/', list_user_by_id, name='user-by-type'),
    path('users/update/<int:id>/', update_user, name='update-user'),
    path('admins/', list_user, name='list-admins'),
    path('admin/latest/', list_latest_users, name='latest-users'),
    path('admin/update/<int:id>/', update_user, name='update-user'),
    path('crud/', include(router.urls)),
]
