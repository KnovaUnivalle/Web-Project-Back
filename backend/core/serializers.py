from rest_framework import serializers
from .models import admin, rol, user, product, store, searchHistory, suggestion


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = admin
        fields = ('id', 'email', 'password')


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = rol
        fields = ('id', 'name')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ('id', 'id_rol', 'name', 'last_name',
                  'email', 'password', 'birth_date')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = ('id', 'name', 'description', 'price')


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = store
        fields = ('id', 'name', 'address')


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = searchHistory
        fields = ('id', 'id_user', 'id_product', 'id_store', 'date')
        read_only_fields = ('date', )


class SuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = suggestion
        fields = ('id', 'id_product', 'product_option', 'store_option')
        read_only_fields = ('date', )
