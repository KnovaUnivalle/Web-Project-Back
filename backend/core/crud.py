from rest_framework import status, viewsets, permissions, generics, filters
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Count
from django.views import View
from .serializers import *
from .permission import *
from .models import *
import datetime
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



class ReportListView(View):
    def get(self, request):
        query_param = request.GET.get('q')

        if query_param == 'top_products':
            top_products = SearchHistory.objects.values('product_id').annotate(total_searches=Count('product_id')).order_by('-total_searches')[:5]
            product_ids = [item['product_id'] for item in top_products]
            top_products_list = Product.objects.filter(id__in=product_ids)

            response_data = []
            for product in top_products_list:
                search_count = SearchHistory.objects.filter(product=product).count()
                response_data.append({
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'search_count': search_count
                })

            return JsonResponse(response_data, safe=False ,status=200)
        
        if query_param == 'top_store':
            top_store = SearchHistory.objects.values('store').annotate(total_searches=Count('store')).order_by('-total_searches')[:5]
            store_ids = [item['store'] for item in top_store]
            top_stores_list = Store.objects.filter(id__in=store_ids)

            response_data = []
            for store in top_stores_list:
                search_count = SearchHistory.objects.filter(store=store).count()
                response_data.append({
                    'id': store.id,
                    'name': store.name,
                    'price': store.address,
                    'search_count': search_count
                })

            return JsonResponse(response_data, safe=False ,status=200)

        elif query_param == 'top_users':
            top_users = SearchHistory.objects.values('user_id').annotate(total_searches=Count('user')).order_by('-total_searches')[:5]
            user_ids = [item['user_id'] for item in top_users]
            top_users_list = User.objects.filter(id__in=user_ids)

            response_data = []
            for user in top_users_list:
                search_count = SearchHistory.objects.filter(user=user).count()
                response_data.append({
                    'id': user.id,
                    'name': user.name,
                    'last_name': user.last_name,
                    'search_count': search_count
                })

            return JsonResponse(response_data,  safe=False, status=200)
        
        elif query_param == 'lower_products':
            top_products = Product.objects.order_by('price')[:5]

            response_data = []
            for product in top_products:
                response_data.append({
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                })

            return JsonResponse(response_data, safe=False, status=200)
    
        else:
            return JsonResponse({'error': 'Invalid query parameter'}, status=400)
        

class RegisterSearch(APIView):
    def post(self, request):
        data = request.data
        name = data.get('name')
        price = data.get('price')
        description = data.get('description')

        product = Product.objects.create(name=name, price=price, description=description)

        product_id = product.id

        store_name = data.get('store')
        store = Store.objects.get(name=store_name)

        serializer = SearchHistorySerializer(data={
            'date': datetime.datetime.now(),
            'product_id': product_id,
            'store_id': store.id,
            'user_id': data.get('user_id')
        })
        if serializer.is_valid():
            search = serializer.save()
            search.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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