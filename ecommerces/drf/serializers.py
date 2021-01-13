from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import exceptions
from .models import UserRole,Product,Order,OrderItem


class RegisterSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        users = User.objects.create_user(**validated_data)
        return users

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name','last_name','is_active')
        extra_kwargs = {'password': {'write_only': True}}


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "User is deactivated."
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Unable to login with given credentials."
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide username and password both."
            raise exceptions.ValidationError(msg)
        return data
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

class UserRoleCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user_role = UserRole()
        user_role.title = validated_data['title']
        user_role.save()
        return user_role
    class Meta:
        model = UserRole
        fields = '__all__'

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'

class OrderCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user_role = UserRole()
        user_role.title = validated_data['title']
        user_role.save()
        return user_role
    class Meta:
        model = UserRole
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'