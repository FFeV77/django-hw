from rest_framework.filters import SearchFilter

from logistic.models import Product, Stock, StockProduct


class PositionStockFilter(SearchFilter):
    def filter_queryset(self, request, queryset, view):
        self.queryset = Product.objects.prefetch_related('positions').filter(title='Виски')
        return