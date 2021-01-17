from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import exceptions
from .models import UserRole,Product,Order,OrderItem


from drf.models import User, CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('role')


class UserSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(required=True)

    """
    However UserSerializer is a bit more complicated. Because we need the UserCustom to be serialized/deserialized as 
    part of the User model we created a Writable Nested Serializer as defined in the DRF documentation. 
    That is, a serializer that uses another serializer for a particular field ( user in this case).
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password','is_active' 'user')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        us_data = validated_data.pop('user')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        CustomUser.objects.create(user=user, **us_data)
        return user

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        data = instance.user

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        data.role = user_data.get('role', data.role)
        data.save()

        return instance

# class RegisterSerializer(serializers.ModelSerializer):
#     def create(self, validated_data):
#         users = User.objects.create_user(**validated_data)
#         return users

#     class Meta:
#         model = User
#         fields = ('username', 'password', 'email', 'first_name','last_name','is_active')
#         extra_kwargs = {'password': {'write_only': True}}


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