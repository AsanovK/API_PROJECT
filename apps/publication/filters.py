from .models import Publication
from django_filters.rest_framework import  FilterSet, DateTimeFromToRangeFilter

class PublicationDateFilter(FilterSet):
    created_at = DateTimeFromToRangeFilter()

    class Meta:
        model = Publication
        fields = ('created_at', )

    
