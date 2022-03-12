from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from src.common.mixins import UpdateModelMixin
from src.shops.models import Shop
from src.shops.serializers import ShopSerializer


class ShopViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin,
                  GenericViewSet):
    serializer_class = ShopSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'slug'
    queryset = Shop.objects.prefetch_related('address')
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']
