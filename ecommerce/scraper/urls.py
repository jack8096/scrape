from django.urls import path
from .views import ProductSearchAPIView

urlpatterns = [
    path("search/", ProductSearchAPIView.as_view(), name="product-search"),
]
