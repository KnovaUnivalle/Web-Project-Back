from rest_framework import serializers
from .models import Admin, Rol, User, Product, Store, SearchHistory, Suggestion
from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from library.sociallib import google
from rest_framework.exceptions import AuthenticationFailed
import json

UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
	birth_date = serializers.DateField()

	class Meta:
		model = UserModel
		fields = ('id', 'rol', 'name', 'last_name', 'email', 'birth_date', 'is_active', 'password')

class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField()
	##
	def check_user(self, clean_data):
		user = authenticate(username=clean_data['email'], password=clean_data['password'])
		if not user:
			raise ValidationError('user not found')
		return user


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'


class AdminSerializerReduce(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ('id', 'email', 'is_active')


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserSerializerReduce(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'rol', 'name', 'last_name', 'email', 'birth_date', 'is_active')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = '__all__'


class SuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggestion
        fields = '__all__'
        read_only_fields = ('date', )
        

class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )
        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed('oops, who are you?')
            
        return user_data
