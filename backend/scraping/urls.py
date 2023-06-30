from django.urls import path
from .views import *

urlpatterns = [
    path('scraping/', searchProduct, name='searchProduct'),
    path('suggestion/', getRandomProducts, name='suggestion')
]
