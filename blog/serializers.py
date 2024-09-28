from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError

from .models import Post
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=15)

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'password', 'confirm_password')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image', 'category', 'created_at', 'user']
        read_only_fields = ['user', 'created_at']

    def validate_image(self, value):
        # Ensure image size is not more than 2MB
        if value and value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Image file too large ( > 2MB )")
        return value