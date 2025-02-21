from django.contrib import admin
from django.urls import path, include
from django.urls import path
from s3_api.views import get_signed_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/get-signed-url/', get_signed_url, name='get_signed_url'),
    path('', include('s3_api.urls')),
]