from django.urls import path
from . import views
from django.conf.urls import url, include
from rest_framework import routers

app_name = 'apiv1'

router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'categories', views.CategoryViewSet)


urlpatterns = [
    url(r'', include(router.urls))
]