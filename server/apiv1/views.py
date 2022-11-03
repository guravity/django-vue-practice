from rest_framework import generics, viewsets, filters
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

class BookViewSet(viewsets.ModelViewSet):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  filter_backends = [
    filters.SearchFilter,
    filters.OrderingFilter,
    #CategoryFilter,
  ]
  search_fields = ('title', 'content')
  ordering_fields = ('created_at', 'updated_at')

#   def perform_create(self, serializer):
#     serializer.save(user=self.request.user)