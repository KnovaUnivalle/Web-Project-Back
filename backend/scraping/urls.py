from django.urls import path
from .views import searchProduct

urlpatterns = [
    path('', searchProduct, name='searchProduct'),
]