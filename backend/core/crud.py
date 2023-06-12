from rest_framework import status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
from .permission import *
from .models import *

from rest_framework.response import Response

@api_view(['GET'])
#  @permission_classes([IsAdmin])
def list_admin_users(request):
    admins = Admin.objects.all()
    serializer = AdminSerializer(admins, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
# @permission_classes([IsAdmin]) 
def list_latest_admins(request):
    admins = Admin.objects.order_by('-id')[:10]
    serializer = AdminSerializer(admins, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
# @permission_classes([IsAdmin])  # Reemplaza IsAdmin con tu clase de permiso personalizada para los administradores
def update_admin(request, id):
    try:
        admin = Admin.objects.get(id=id)
    except Admin.DoesNotExist:
        return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = AdminSerializer(admin, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_user(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def list_user_by_id(request, id):
    users = User.objects.filter(id=id)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def list_latest_users(request):
    users = User.objects.order_by('-id')[:10]
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
# @permission_classes([IsAdmin])  # Reemplaza IsAdmin con tu clase de permiso personalizada para los administradores
def update_user(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
#  @permission_classes([IsAdmin])
def list_rol(request):
    rol = Rol.objects.all()
    serializer = AdminSerializer(rol, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
# @permission_classes([IsAdmin])
def list_product(request):
    product = Product.objects.all()
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
# @permission_classes([IsAdmin])
def list_store(request):
    store = Store.objects.all()
    serializer = StoreSerializer(store, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
# @permission_classes([IsAdmin])
def list_search_history(request):
    search_history = SearchHistory.objects.all()
    serializer = SearchHistorySerializer(search_history, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
# @permission_classes([IsAdmin])
def list_suggestion(request):
    suggestion = Suggestion.objects.all()
    serializer = SuggestionSerializer(suggestion, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RolSerializer

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