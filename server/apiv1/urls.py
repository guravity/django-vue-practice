from django.urls import path
from . import views
from django.conf.urls import include
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'apiv1'

router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'categories', views.CategoryViewSet)


urlpatterns = [
    path(r'', include(router.urls)),
    path(r'^api-token-auth/', auth_views.obtain_auth_token),
    path('jwt-token/', TokenObtainPairView.as_view()),
    path('jwt-token/refresh/', TokenRefreshView.as_view()),
]