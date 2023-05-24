from rest_framework import serializers
from .models import Admin, Rol, User, Product, Store, SearchHistory, Suggestion
from django.contrib.auth import get_user_model, authenticate

UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
	birth_date = serializers.DateField()

	class Meta:
		model = UserModel
		fields = '__all__'

	def create(self, clean_data):
		email = clean_data['email']
		password = clean_data['password']
		rol_data = clean_data['rol']
		name = clean_data['name']
		last_name = clean_data['last_name']
		birth_date = clean_data['birth_date']
		rol = Rol.objects.get(id=rol_data)  # Obtener el objeto Rol existente por su nombre
		user_obj = UserModel.objects.create_user(email=email, password=password)
		user_obj.rol = rol  # Asignar el objeto Rol al campo rol
		user_obj.name = name
		user_obj.last_name = last_name
		user_obj.birth_date = birth_date
		user_obj.save()
		return user_obj

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


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


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
