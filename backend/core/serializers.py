from rest_framework import serializers
from .models import admin

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = admin
        fields = ('id', 'email', 'password')
        