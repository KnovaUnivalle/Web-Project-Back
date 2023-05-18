from django.contrib import admin
from django.urls import path, include
import django.urls as urls
from core.views import GoogleLogin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('accounts/', include('allauth.urls')),
    path('api-auth/google/', GoogleLogin.as_view(), name='google_login'),
]
