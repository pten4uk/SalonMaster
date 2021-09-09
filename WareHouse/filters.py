import django_filters
from django_filters import FilterSet

from .models import Material


class MaterialFilter(FilterSet):
    number = django_filters.CharFilter(field_name='number__name', lookup_expr='icontains', label='Название')

    class Meta:
        model = Material
        fields = ['category', 'number']
