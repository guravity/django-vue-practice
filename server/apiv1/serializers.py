from cProfile import label
from rest_framework import serializers
from .models import Category, Book

# class UserSerializer(serializers.ModelSerializer):
#     """ユーザーシリアライザー"""
#     class Meta:
#         model = get_user_model()
#         fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """カテゴリシリアライザ"""
    id = serializers.IntegerField(label="id") # デフォルトだとread_onlyなのでPOSTで追加できない。
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class BookSerializer(serializers.ModelSerializer):
    """本シリアライザ"""
    categories = CategorySerializer(many=True)
    class Meta:
        model = Book
        fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'published_at', 'categories')
    
    def create(self, validated_data):
        categories = validated_data.pop('categories', [])
        print(categories, validated_data)
        book = Book.objects.create(**validated_data)
        
        if len(categories) != 0:
            for category_dict in categories:
                if not 'id' in category_dict:
                    print("category_dict has no key named 'id'.")
                    continue
                category = Category.objects.get(id=category_dict['id'])
                book.categories.add(category)
        book.save()
        return book