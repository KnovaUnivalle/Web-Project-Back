from rest_framework import status, viewsets, permissions, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
from .permission import *
from .models import *
from django.db.models import Q

from rest_framework.response import Response

@permission_classes((IsAuthenticated, IsAdmin, ))
class AdminListView(generics.ListAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializerReduce
    filterset_fields = ['id', 'email', 'is_active']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        if 'last' in self.request.GET:
            return Admin.objects.order_by('-id')[:10]
        return queryset
    
    def filter_queryset(self, queryset):
        search_param = self.request.query_params.get('q')
        if search_param:
            queryset = queryset.filter(
                Q(email__icontains=search_param)
            )
        return queryset


@permission_classes((IsAuthenticated, IsAdminOrManager,  ))
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerReduce
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id', 'rol', 'name', 'last_name', 'email', 'is_active']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        if 'last' in self.request.GET:
            return User.objects.order_by('-id')[:10]
        return queryset

    def filter_queryset(self, queryset):
        search_param = self.request.query_params.get('q')
        if search_param:
            queryset = queryset.filter(
                Q(name__icontains=search_param) |
                Q(last_name__icontains=search_param) |
                Q(email__icontains=search_param)
            )
        return queryset
    

@api_view(['GET'])
def user_id(request, id):
    try:
        user = User.objects.get(id=id)
        serializer = UserSerializerReduce(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['PUT'])
@permission_classes((IsAuthenticated, IsAdmin, ))
def update_admin(request, id):
    try:
        admin = Admin.objects.get(id=id)
    except Admin.DoesNotExist:
        return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = AdminSerializerReduce(admin, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes((IsAuthenticated, IsAdmin, ))
def disable_admin(request, id):
    try:
        admin = Admin.objects.get(id=id)
        admin.is_active = False
        admin.save()
        serializer = AdminSerializerReduce(admin)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Admin.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes((IsAuthenticated, IsAdmin, ))
def update_user(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializerReduce(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes((IsAuthenticated, IsAdmin, ))
def disable_user(request, id):
    try:
        user = User.objects.get(id=id)
        user.is_active = False
        user.save()
        serializer = UserSerializerReduce(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)


@permission_classes((IsAuthenticated, IsAdmin, ))
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer


@permission_classes((IsAuthenticated, IsAdmin, ))
class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@permission_classes((IsAuthenticated, IsAdmin, ))
class StoreViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


@permission_classes((IsAuthenticated, IsAdmin, ))
class SearchHistoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer


@permission_classes((IsAuthenticated, IsAdmin, ))
class SuggestionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionSerializer