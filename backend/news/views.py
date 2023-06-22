from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import NewsSerializer
from .models import News


class NewsListView(APIView):
    def get(self, request):
        news = News.objects.order_by('-id')[:10]
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class NewsCreateView(APIView):
    def post(self, request):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            news = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class NewsUpdateView(APIView):
    def get(self, request, id):
        news = News.objects.get(id=id)
        serializer = NewsSerializer(news)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        news = News.objects.get(id=id)
        serializer = NewsSerializer(news, data=request.data)
        if serializer.is_valid():
            news = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)