from rest_framework.viewsets import ModelViewSet

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer

from rest_framework.filters import SearchFilter


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.prefetch_related('positions')
    serializer_class = StockSerializer
    filter_backends = [SearchFilter]
    search_fields = ['products__title', 'products__description']

