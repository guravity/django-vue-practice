from rest_framework import serializers
from .models import Category, Book

# class UserSerializer(serializers.ModelSerializer):
#     """ユーザーシリアライザー"""
#     class Meta:
#         model = get_user_model()
#         fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """カテゴリシリアライザ"""
    class Meta:
        model = Category
        fields = ('name', 'slug')


class BookSerializer(serializers.ModelSerializer):
    """本シリアライザ"""
    categories = CategorySerializer(many=True, read_only=True)
    class Meta:
        model = Book
        fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'published_at', 'categories')