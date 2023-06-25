from django.urls import path
from .views import searchProduct

urlpatterns = [
    path('scraping/', searchProduct, name='searchProduct'),
]
