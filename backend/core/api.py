from rest_framework import viewsets, permissions
from .serializers import AdminSerializer, RoleSerializer, UserSerializer, ProductSerializer, StoreSerializer, SearchHistorySerializer, SuggestionSerializer
from .models import admin, rol, user, product, store, searchHistory, suggestion


# Indicates which queries could be made
class AdminViewSet(viewsets.ModelViewSet):
    queryset = admin.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = AdminSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = rol.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RoleSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = user.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = product.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductSerializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = store.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = StoreSerializer


class SearchHistoryViewSet(viewsets.ModelViewSet):
    queryset = searchHistory.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = SearchHistorySerializer


class SuggestionViewSet(viewsets.ModelViewSet):
    queryset = suggestion.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = SuggestionSerializer
