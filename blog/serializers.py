from rest_framework import serializers
from .models import User, Blog, Comment
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'email', 'phone', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # هش کردن رمز عبور
        return super().create(validated_data)

class BlogSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.id')

    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'created_at', 'author']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
