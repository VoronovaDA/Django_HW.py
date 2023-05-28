from django_filters import rest_framework as filters
from advertisements.models import Advertisement, FavoriteAdvertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    # TODO: задайте требуемые фильтры
    created_at = filters.DateFromToRangeFilter()
    creator = filters.NumberFilter()

    class Meta:
        model = Advertisement
        fields = ['status', 'created_at', 'creator']


class FavoriteAdvertisementFilter(filters.Filter):

    class Meta:
        model = Advertisement
        fields = ['status']
