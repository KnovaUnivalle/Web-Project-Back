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
    path('user/register/', UserRegisterView.as_view(), name='registerUser'),
    path('customer/register/', CustomerRegisterView.as_view(), name='registerCustomer'),
    path('customer/search/', RegisterSearch.as_view(), name='addSearch'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('customer/', CustomerView.as_view(), name='customer'),
    path('manager/', ManagerView.as_view(), name='manager'),
    path('administrator/', AdminView.as_view(), name='administrator'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('google/', GoogleSocialAuthView.as_view()),
    # Creates the urls for POST, DELETE, PUT and GET
    path('users/', UserListView.as_view(), name='list-users'),
    path('users/<int:id>/', user_id, name='user-id'),
    path('users/update/<int:id>/', update_user, name='update-user'),
    path('users/disable/<int:id>/', disable_user, name='delete-user'),
    path('admins/', AdminListView.as_view(), name='list-admins'),
    path('admin/update/<int:id>/', update_admin, name='update-user'),
    path('admin/disable/<int:id>/', disable_admin, name='delete-user'),
    path('reports/', ReportListView.as_view(), name='list-reports'),
    path('crud/', include(router.urls)),
]
