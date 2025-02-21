from django.urls import path
from .views import index, get_signed_url

urlpatterns = [
    path('', index, name='index'),  # Rota para a página inicial
    path('api/get-signed-url/', get_signed_url, name='get_signed_url'),
]