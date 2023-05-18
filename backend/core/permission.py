import jwt
from backend.settings import SIMPLE_JWT
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.http import JsonResponse
from rest_framework import status


class IsCustomer(permissions.BasePermission):
    # Verify if the user is a customer
    def has_permission(self, request, view):
        jwt_authentication = JWTAuthentication()
        try:
            data = jwt.decode(request.headers['Authorization'], SIMPLE_JWT['SIGNING_KEY'], algorithms=[
                SIMPLE_JWT['ALGORITHM']])
            result = jwt_authentication.authenticate(request)
            if result is None and data['rol_id'] == 1:
                return True
            else:
                return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        except KeyError:
            raise AuthenticationFailed('Missing authorization header')


class IsManager(permissions.BasePermission):
    # Verify if the user is a customer
    def has_permission(self, request, view):
        jwt_authentication = JWTAuthentication()
        try:
            data = jwt.decode(request.headers['Authorization'], SIMPLE_JWT['SIGNING_KEY'], algorithms=[
                SIMPLE_JWT['ALGORITHM']])
            result = jwt_authentication.authenticate(request)
            if result is not None and data['rol_id'] == 2:
                return True
            else:
                return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_403_FORBIDDEN)
        except (KeyError, jwt.exceptions.DecodeError):
            return JsonResponse({'error': 'Token inválido.'}, status=status.HTTP_401_UNAUTHORIZED)
