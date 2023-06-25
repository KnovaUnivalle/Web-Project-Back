from django.urls import path
from .views import *

urlpatterns = [
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/update/<int:id>/', NewsUpdateView.as_view(), name='news_update'),
    path('news/<int:id>/', NewsGetView.as_view(), name='news_get'),
]