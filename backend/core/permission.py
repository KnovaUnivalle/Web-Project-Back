from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from .validations import decode_token

class IsAdmin(BasePermission):
    # Verify if the user is a manager
    def has_permission(self, request, view):
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            data = decode_token(token)
            return data['rol_id'] == 0
        except KeyError:
            return False


class IsCustomer(BasePermission):
    # Verify if the user is a customer
    def has_permission(self, request, view):
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            data = decode_token(token)
            return data['rol_id'] == 1
        except KeyError:
            return False


class IsManager(BasePermission):
    # Verify if the user is a manager
    def has_permission(self, request, view):
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            data = decode_token(token)
            print(data["rol_id"])
            return data['rol_id'] == 2
        except KeyError:
            return False
        

class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            data = decode_token(token)
            rol_id = data.get('rol_id')
            return rol_id in [0, 2] 
        except (KeyError, IndexError):
            return False