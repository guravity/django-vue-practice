from rest_framework import serializers
from .models import Category, Book
from django.contrib.auth import get_user_model

usermodel = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """ユーザーシリアライザー"""
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email')


class CategorySerializer(serializers.ModelSerializer):
    """カテゴリシリアライザ"""
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class BookSerializer(serializers.ModelSerializer):
    """本シリアライザ"""
    categories = CategorySerializer(many=True, read_only=True) # 読み込み(デシリアライズ)用
    category_ids = serializers.PrimaryKeyRelatedField( # 書き込み(シリアライズ)用
        queryset=Category.objects.all(),
        many=True,
        write_only=True
    )
    user = UserSerializer(read_only=True)
    class Meta:
        model = Book
        fields = ('id', 'user', 'title', 'content', 'created_at', 'updated_at', 'published_at', 'categories', 'category_ids')
    
    def create(self, validated_data):
        category_ids = validated_data.pop('category_ids', [])
        book = Book.objects.create(**validated_data)
        if len(category_ids) != 0:
            for id in category_ids:
                book.categories.add(id)
        book.save()
        return book
    
    def update(self, instance, validated_data):
        category_ids = validated_data.pop('category_ids', [])
        book = super().update(instance, validated_data)
        book.categories.set([]) # カテゴリのリセット
        if len(category_ids) != 0:
            for id in category_ids:
                instance.categories.add(id)
        book.save()
        return book