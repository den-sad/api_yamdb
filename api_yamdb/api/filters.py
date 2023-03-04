from django_filters import rest_framework as filters

from .views import Title


class TitleSlugFilter(filters.FilterSet):
    genre = filters.CharFilter(field_name='name',
                               lookup_expr='icontains')
    genre = filters.NumberFilter(field_name='year',
                                 lookup_expr='contains')
    genre = filters.CharFilter(field_name='genre__slug',
                               lookup_expr='icontains')
    category = filters.CharFilter(field_name='category__slug',
                                  lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ['name', 'year', 'category', 'genre']
