from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from advertisements.filters import AdvertisementFilter

from advertisements.models import Advertisement
from advertisements.permissions import IsOwnerOrAdmin, NotOwner
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action in ['add_favorite']:
            return Advertisement.objects.get(id=self.kwargs['pk'])
        elif self.action in ['list_favorite']:
            return Advertisement.objects.filter(in_favorite=self.request.user)
        elif not self.request.user.is_anonymous:
            return qs.filter(~Q(status='DRAFT') | Q(creator=self.request.user))
        return qs.exclude(Q(status='DRAFT'))

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update"]:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        elif self.action in ["destroy"]:
            return [IsOwnerOrAdmin()]
        elif self.action in ["add_favorite"]:
            return [IsAuthenticated(), NotOwner()]
        elif self.action in ["list_favorite"]:
            return [IsAuthenticated()]
        return []

    @action(methods=['patch'], detail=True)
    def add_favorite(self, request, pk=None):
        obj = Advertisement.objects.get(id=pk)
        self.check_object_permissions(request, obj)
        obj.in_favorite.add(request.user)
        return Response('Добавлено')

    @action(detail=False)
    def list_favorite(self, request):
        return super().list(self, request)
