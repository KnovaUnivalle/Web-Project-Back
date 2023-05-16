from rest_framework import viewsets, permissions
from .serializers import AdminSerializer, RolSerializer, UserSerializer, ProductSerializer, StoreSerializer, SearchHistorySerializer, SuggestionSerializer
from .models import Admin, Rol, User, Product, Store, SearchHistory, Suggestion


# Indicates which queries could be made
class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = AdminSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RolSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ProductSerializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = StoreSerializer


class SearchHistoryViewSet(viewsets.ModelViewSet):
    queryset = SearchHistory.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = SearchHistorySerializer


class SuggestionViewSet(viewsets.ModelViewSet):
    queryset = Suggestion.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = SuggestionSerializer
