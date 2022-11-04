from rest_framework import viewsets, filters
from .models import Book, Category
from .serializers import CategorySerializer, BookSerializer

class CategoryFilter(filters.BaseFilterBackend):
    """カテゴリによるフィルタ"""
    def filter_queryset(self, request, queryset, view): # クエリパラメタ
        if request.query_params.get('category'):
            return queryset.filter(categories__slug=request.query_params.get('category'))
        return queryset

class CategoryViewSet(viewsets.ModelViewSet):
    """カテゴリのModelViewSet"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BookViewSet(viewsets.ModelViewSet):
    """本のModelViewSet"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        CategoryFilter,
    ]
    search_fields = ('title', 'content')
    ordering_fields = ('created_at', 'updated_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
