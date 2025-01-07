from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

from app.models import Category, Task


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer
    """

    class Meta:
        ref_name = "User"
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    """
    Register serializer
    """

    class Meta:
        ref_name = "Register User"
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        This method is used to create a new user
        """
        if 'email' not in validated_data:
            raise serializers.ValidationError({'email': 'This field is required'})
        if 'username' not in validated_data:
            raise serializers.ValidationError({'username': 'This field is required'})
        if 'password' not in validated_data:
            raise serializers.ValidationError({'password': 'This field is required'})
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user


class LoginSerializer(serializers.Serializer):
    class Meta:
        ref_name = "Login User"

    """
    Login serializer
    """
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        """
        This method is called when .is_valid() is called on the serializer class
        """
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect Credentials Passed.')


class CategorySerializer(serializers.ModelSerializer):
    """
    Category serializer
    """

    class Meta:
        ref_name = "Category"
        model = Category
        fields = ('id', 'name')

    def create(self, validated_data):
        """
        This method is used to create a new category
        """
        if 'name' not in validated_data:
            raise serializers.ValidationError({'name': 'This field is required'})
        category = Category.objects.create(name=validated_data['name'])
        return category

    def update(self, instance, validated_data):
        """
        This method is used to update a category
        """
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class TaskSerializer(serializers.ModelSerializer):
    """
    Task serializer
    """

    class Meta:
        ref_name = "Task"
        model = Task
        fields = ('id', 'name', 'description', 'category', 'user')

    def create(self, validated_data):
        """
        This method is used to create a new task
        """
        if 'name' not in validated_data:
            raise serializers.ValidationError({'name': 'This field is required'})
        if 'description' not in validated_data:
            raise serializers.ValidationError({'description': 'This field is required'})
        if 'category' not in validated_data:
            raise serializers.ValidationError({'category': 'This field is required'})
        if 'user' not in validated_data:
            raise serializers.ValidationError({'user': 'This field is required'})
        task = Category.objects.create(name=validated_data['name'], description=validated_data['description'], category=validated_data['category'], user=validated_data['user'])
        return task

    def update(self, instance, validated_data):
        """
        This method is used to update a task
        """
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.user = validated_data.get('user', instance.user)
        instance.save()
        return instance
