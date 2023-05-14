from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import registerAdmin, registerUser, login, logout

urlpatterns = [
    path('admin/register/', registerAdmin, name='registerAdmin'),
    path('user/register/', registerUser, name='resgisterUser'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
