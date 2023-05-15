from .validations import verify_password
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from .models import Admin, User
from .serializers import AdminSerializer, UserSerializer
from .validations import encrypt_password
from .permission import IsCustomer, IsManager


@api_view(["POST"])
def registerUser(request):
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
        except Admin.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    if verify_password(password, user.password):
        refresh = RefreshToken.for_user(user)
        refresh['rol_id'] = rol_id
        data = {
            'refresh': str(refresh),
            'token': str(refresh.access_token),
        }
        response = JsonResponse(data, status=status.HTTP_200_OK)
        response.set_cookie('token', data['token'], httponly=True)
        return response
    else:
        return JsonResponse({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logout(request):
    try:
        token = request.headers['Authorization'].split()[1]
        print(type(token))
        print(token)
        return JsonResponse({'message': 'Logout exitoso'}, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'detail': str(e), 'code': 'logout_error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsCustomer])
def test_Authorization_cutomer(request):
    return JsonResponse({'message': 'Eres un customer, tienes accesso '}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsManager])
def test_Authorization_manager(request):
    return JsonResponse({'message': 'Eres un manager, tienes acceso'}, status=status.HTTP_200_OK)
