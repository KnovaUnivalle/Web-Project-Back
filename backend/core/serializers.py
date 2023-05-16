from rest_framework import serializers
<<<<<<< HEAD
from .models import Admin, Rol, User, Product, Store, SearchHistory
=======
from .models import admin, rol, user, product, store, searchHistory, suggestion
>>>>>>> origin/adminCrud


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
<<<<<<< HEAD
        model = Admin
        fields = '__all__'


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'
=======
        model = admin
        fields = ('id', 'email', 'password')


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = rol
        fields = ('id', 'name')
>>>>>>> origin/adminCrud


class UserSerializer(serializers.ModelSerializer):
    class Meta:
<<<<<<< HEAD
        model = User
        fields = '__all__'
=======
        model = user
        fields = ('id', 'id_rol', 'name', 'last_name',
                  'email', 'password', 'birth_date')
>>>>>>> origin/adminCrud


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
<<<<<<< HEAD
        model = Product
        fields = '__all__'
=======
        model = product
        fields = ('id', 'name', 'description', 'price')
>>>>>>> origin/adminCrud


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
<<<<<<< HEAD
        model = Store
        fields = '__all__'
=======
        model = store
        fields = ('id', 'name', 'address')
>>>>>>> origin/adminCrud


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
<<<<<<< HEAD
        model = SearchHistory
        fields = '__all__'
=======
        model = searchHistory
        fields = ('id', 'id_user', 'id_product', 'id_store', 'date')


class SuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = suggestion
        fields = ('id', 'id_product', 'product_option', 'store_option')
        read_only_fields = ('date', )
>>>>>>> origin/adminCrud
