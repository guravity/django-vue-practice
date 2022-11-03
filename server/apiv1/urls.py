from django.urls import path
from . import views
from django.conf.urls import url, include
from rest_framework import routers

app_name = 'apiv1'

router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet)

urlpatterns = [
    path('categories-list/', views.CategoryListAPIView.as_view()),
    path('books-list/', views.BookListAPIView.as_view()),
    url(r'', include(router.urls))
]