from rest_framework import status, generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from django.utils.translation import gettext_lazy as _
from .utils import *
from .validations import *
from .models import Admin, User
from .serializers import *
from .permission import IsCustomer, IsManager, IsAdmin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

@permission_classes((AllowAny, ))
class UserRegisterView(generics.CreateAPIView):
    def post(self, request):
        request.data['rol'] = 1 or request.data
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.password = encrypt_password(user.password)
            user.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(["POST"])
@permission_classes((AllowAny, ))
def registerAdmin(request):
    serializer = AdminSerializer(data=request.data)
    if serializer.is_valid():
        admin = serializer.save()
        admin.password = encrypt_password(admin.password)
        admin.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = User.objects.get(email=email)
        rol_id = user.rol_id
    except User.DoesNotExist:
        try:
            user = Admin.objects.get(email=email)
            rol_id = 0
        except Admin.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    if verify_password(password, user.password):
        data = generateToken(user, rol_id)
    
        response = JsonResponse(data, status=status.HTTP_200_OK)
        response.set_cookie('refresh_token', data['refresh'], httponly=True)
        return response
    else:
        return JsonResponse({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def logout(request):
    token = request.COOKIES.get('refresh_token')
    try:
            refresh_token = RefreshToken(token)
            # refresh_token.blacklist()
            response = JsonResponse({'detail': 'Logout exitoso.'}, status=status.HTTP_200_OK)
            response.delete_cookie('refresh_token')
            return response
    except Exception as e:
            return JsonResponse({'error': 'No se pudo invalidar el token de acceso.'}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated, IsCustomer))
class CustomerView(APIView):
	def get(self, request):
            token = request.headers.get('Authorization').split(' ')[1]
            data = decode_token(token)
            user = User.objects.get(id=data["user_id"])
            serializers = UserSerializer(user)
            return JsonResponse(serializers.data, status=status.HTTP_200_OK)
        
        
@permission_classes((IsAuthenticated, IsManager))
class ManagerView(APIView):
	def get(self, request):
            token = request.headers.get('Authorization').split(' ')[1]
            data = decode_token(token)
            user = User.objects.get(id=data["user_id"])
            serializers = UserSerializer(user)
            return JsonResponse(serializers.data, status=status.HTTP_200_OK)
        

@permission_classes((IsAuthenticated, IsAdmin))
class AdminView(APIView):
	def get(self, request):
            token = request.headers.get('Authorization').split(' ')[1]
            data = decode_token(token)
            user = Admin.objects.get(id=data["user_id"])
            serializers = AdminSerializer(user)
            return JsonResponse(serializers.data, status=status.HTTP_200_OK)
        
      
@permission_classes((AllowAny, ))
class GoogleSocialAuthView(generics.GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
    
        tempUser = User.objects.filter(email=data['email'])
        user = {
            'email': data['email'],
            'password': generate_random_password(),
            'name': data['given_name'],
            'last_name': data['family_name'],
            'birth_date': "1990-01-01",
            'rol': 1
        }
        
        if tempUser.exists():
                tempUser = User.objects.get(email=user['email'])
                data = generateToken(tempUser, user['rol'])
                response = JsonResponse(data, status=status.HTTP_200_OK)
                response.set_cookie('refresh_token', data['refresh'], httponly=True)
                return response
        else:
            ## Register user
            serializer = UserSerializer(data=user)
            if serializer.is_valid():
                user = serializer.save()
                user.password = encrypt_password(user.password)
                user.save()
            else:
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Login
            tempUser = User.objects.get(email=data['email'])
            data = generateToken(tempUser, tempUser.rol_id)
    
            response = JsonResponse(data, status=status.HTTP_200_OK)
            response.set_cookie('refresh_token', data['refresh'], httponly=True)
            return response