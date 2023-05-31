from django_filters import rest_framework as filters, DateFromToRangeFilter

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    # TODO: задайте требуемые фильтры

    created_at = DateFromToRangeFilter()
    creator = filters.NumberFilter()

    class Meta:
        model = Advertisement
        fields = ['creator', 'status', 'created_at',]