from django.urls import path
from .views import mercadoLibre

urlpatterns = [
    path('mercadolibre/', mercadoLibre, name='mercadolibre'),
]