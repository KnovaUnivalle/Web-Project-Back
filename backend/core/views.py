from .validations import verify_password
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from .models import Admin, User
from .serializers import AdminSerializer, UserSerializer
from .validations import encrypt_password


@api_view(["POST"])
def registerUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.password = encrypt_password(user.password)
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def registerAdmin(request):
    serializer = AdminSerializer(data=request.data)
    if serializer.is_valid():
        admin = serializer.save()
        admin.password = encrypt_password(admin.password)
        admin.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
        # user_type = User.objects.get()
    except User.DoesNotExist:
        try:
            user = Admin.objects.get(email=email)
            # user_type = 'admin'
        except Admin.DoesNotExist:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    if verify_password(password, user.password):
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'token': str(refresh.access_token),
        }
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logout(request):
    try:
        token = request.headers['Authorization'].split()[1]
        print(type(token))
        print(token)
        return Response({'message': 'Logout exitoso'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'detail': str(e), 'code': 'logout_error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
