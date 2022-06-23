from django.urls import path, include
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('', include('mega_market.urls')),
]
urlpatterns += doc_urls
