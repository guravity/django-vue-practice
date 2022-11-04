from django.urls import path
from . import views
from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken import views as auth_views

app_name = 'apiv1'

router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'categories', views.CategoryViewSet)


urlpatterns = [
    url(r'', include(router.urls)),
    url(r'^api-token-auth/', auth_views.obtain_auth_token),
]