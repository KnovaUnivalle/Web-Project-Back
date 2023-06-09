from rest_framework import status, generics, permissions, status, serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .validations import *
from .models import Admin, User
from .serializers import *
from .permission import IsCustomer, IsManager, IsAdmin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView


class RegisterUser(generics.CreateAPIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.password = encrypt_password(user.password)
            user.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def registerAdmin(request):
    serializer = AdminSerializer(data=request.data)
    if serializer.is_valid():
        admin = serializer.save()
        admin.password = encrypt_password(admin.password)
        admin.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
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
        refresh = RefreshToken.for_user(user)
        refresh['rol_id'] = rol_id
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'rol_id': rol_id
        }

        response = JsonResponse(data, status=status.HTTP_200_OK)
        response.set_cookie('refresh_token', str(refresh), httponly=True)
        return response
    else:
        return JsonResponse({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
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


class CustomerView(APIView):
	permission_classes = [permissions.IsAuthenticated, IsCustomer]
	def get(self, request):
            token = request.headers.get('Authorization').split(' ')[1]
            data = decode_token(token)
            user = User.objects.get(id=data["user_id"])
            serializers = UserSerializer(user)
            return JsonResponse(serializers.data, status=status.HTTP_200_OK)
        
class ManagerView(APIView):
	permission_classes = [permissions.IsAuthenticated, IsManager]
	def get(self, request):
            token = request.headers.get('Authorization').split(' ')[1]
            data = decode_token(token)
            user = User.objects.get(id=data["user_id"])
            serializers = UserSerializer(user)
            return JsonResponse(serializers.data, status=status.HTTP_200_OK)
        
class AdminView(APIView):
	permission_classes = [permissions.IsAuthenticated, IsAdmin]
	def get(self, request):
            token = request.headers.get('Authorization').split(' ')[1]
            data = decode_token(token)
            user = Admin.objects.get(id=data["user_id"])
            serializers = AdminSerializer(user)
            return JsonResponse(serializers.data, status=status.HTTP_200_OK)
            

class MyProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Lógica de la vista protegida
        return JsonResponse("Acceso permitido para usuarios autenticados")


class GoogleLoginSerializer(serializers.Serializer):
    # Define los campos de serialización necesarios para el inicio de sesión con Google

    def validate(self, attrs):
        # Realiza la validación necesaria para el inicio de sesión con Google
        return attrs


class GoogleLogin(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = GoogleLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        User = get_user_model()

        # Comprueba si ya existe un usuario con el correo electrónico proporcionado
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create(email=email)

        refresh = RefreshToken.for_user(user)

        return JsonResponse({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

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
            'name': data['given_name'],
            'last_name': data['family_name'],
            'password': settings.SOCIAL_SECRET_KEY,
            'rol_id': 1,
            "birth_date": "1990-01-01"
        }
        
        if tempUser.exists():
                tempUser = User.objects.get(email=user['email'])
                refresh = RefreshToken.for_user(tempUser)
                refresh['rol_id'] = tempUser.rol_id 
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'rol_id': tempUser.rol_id
                }
                print(data)
                response = JsonResponse(data, status=status.HTTP_200_OK)
                response.set_cookie('refresh_token', str(refresh), httponly=True)
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
            refresh = RefreshToken.for_user(user)
            refresh['rol_id'] = user.rol_id
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'rol_id': user.rol_id
            }
            response = JsonResponse(data, status=status.HTTP_200_OK)
            response.set_cookie('refresh_token', str(refresh), httponly=True)
            return response