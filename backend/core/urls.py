from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *
from .api import *

urlpatterns = [
    path('admin/register/', registerAdmin, name='registerAdmin'),
    path('user/register/', registerUser, name='resgisterUser'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('customer/', CustomerView.as_view(), name='customer'),
    path('manager/', ManagerView.as_view(), name='manager'),
    path('administrator/', AdminView.as_view(), name='administrator'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('google/', GoogleSocialAuthView.as_view()),
    # Creates the urls for POST, DELETE, PUT and GET
    path('admin/', AdminViewSet.as_view({'get': 'list'}), name='admin'),
    path('role/', RoleViewSet.as_view({'get': 'list'}), name='role'),
    path('user/', UserViewSet.as_view({'get': 'list'}), name='user'),
    path('product/', ProductViewSet.as_view({'get': 'list'}), name='product'),
    path('store/', StoreViewSet.as_view({'get': 'list'}), name='store'),
    path('searchHistory/',
         SearchHistoryViewSet.as_view({'get': 'list'}), name='searchHistory'),
    path('suggestion/',
         SuggestionViewSet.as_view({'get': 'list'}), name='suggestion')
]
