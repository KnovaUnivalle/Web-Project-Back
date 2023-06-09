from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status, permissions, generics, filters
from .serializers import NewsSerializer
from .models import News
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from core.permission import *


@permission_classes((IsAuthenticated, IsManager ))
class NewsListView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title','id']

    def get_queryset(self):
        queryset = super().get_queryset()
        query_param = self.request.query_params.get('last')
        
        if query_param:
            return News.objects.order_by('-id')[:10]
        return queryset

    def filter_queryset(self, queryset):
        query_param = self.request.query_params.get('title')

        if query_param:
            queryset = queryset.filter(title__icontains=query_param)
        return queryset
    

class NewsListViewCustomer(APIView):
    def get(self, request):
        news = News.objects.filter(is_active=True).order_by('-id')[:10]
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)    


@permission_classes((IsAuthenticated, IsManager ))
class NewsCreateView(APIView):
    def post(self, request):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            news = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated, IsManager ))
class NewsUpdateView(APIView):
    def put(self, request, id):
        news = News.objects.get(id=id)
        serializer = NewsSerializer(news, data=request.data, partial=True)
        if serializer.is_valid():
            news = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@permission_classes((IsAuthenticated, IsManager ))
class NewsGetView(APIView):
    def get(self, request, id):
        news = News.objects.get(id=id)
        serializer = NewsSerializer(news)
        return Response(serializer.data, status=status.HTTP_200_OK)