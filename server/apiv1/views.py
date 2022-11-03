from rest_framework import generics
from .models import Book, Category
from .serializers import CategorySerializer, BookSerializer

class CategoryListAPIView(generics.ListAPIView):
    """カテゴリモデルの取得（一覧）APIクラス"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BookListAPIView(generics.ListAPIView):
    """本モデルの取得（一覧）APIクラス"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer