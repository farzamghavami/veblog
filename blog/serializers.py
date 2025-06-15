from rest_framework import serializers
from .models import User, Blog, Comment
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions



class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:

        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone",
            "password1",
            "password2",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def validate(self, attrs):
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")

        if password1 or password2:
            if password1 != password2:
                raise serializers.ValidationError("Passwords must match")

            try:
                validate_password(password1)
            except exceptions.ValidationError as e:
                raise serializers.ValidationError({"password1": list(e.messages)})

        return attrs

    """for hashing password"""

    def create(self, validated_data):
        password = validated_data.pop("password1")
        validated_data.pop("password2")

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class BlogSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'created_at','updated_at', 'author']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
