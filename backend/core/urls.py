from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from .views import registerAdmin, registerUser, login, logout, test_Authorization_cutomer, test_Authorization_manager, test_user
from .api import AdminViewSet, RoleViewSet, UserViewSet, ProductViewSet, StoreViewSet, SearchHistoryViewSet, SuggestionViewSet

urlpatterns = [
    path('admin/register/', registerAdmin, name='registerAdmin'),
    path('user/register/', registerUser, name='resgisterUser'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('customer/', test_Authorization_cutomer, name='customer'),
    path('manager/', test_Authorization_manager, name='customer'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
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
