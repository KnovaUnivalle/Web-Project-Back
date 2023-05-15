from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import registerAdmin, registerUser, login, logout, test_Authorization_cutomer, test_Authorization_manager

urlpatterns = [
    path('admin/register/', registerAdmin, name='registerAdmin'),
    path('user/register/', registerUser, name='resgisterUser'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('customer/', test_Authorization_cutomer, name='customer'),
    path('manager/', test_Authorization_manager, name='customer'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
