from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('apiv1.urls')),
    path('kanri/', admin.site.urls),
]
