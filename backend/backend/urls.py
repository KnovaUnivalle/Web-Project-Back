from django.contrib import admin
from django.urls import path, include
import django.urls as urls
from core.views import GoogleLogin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
]
