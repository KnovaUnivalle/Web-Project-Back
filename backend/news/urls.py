from django.urls import path
from .views import NewsListView, NewsCreateView, NewsUpdateView

urlpatterns = [
    path('news/', NewsListView.as_view(), name='news_list'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/update/<int:pk>/', NewsUpdateView.as_view(), name='news_update'),
]