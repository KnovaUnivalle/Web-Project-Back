from rest_framework import viewsets, permissions
from .serializers import AdminSerializer
from .models import admin

# Indicates which queries could be made
class AdminViewSet(viewsets.ModelViewSet):
    queryset = admin.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = AdminSerializer