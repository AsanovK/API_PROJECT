from rest_framework.viewsets import ModelViewSet
from .models import Publication
from .serializers import PublicationSerializer
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PublicationDateFilter


class PublicationViewSet(ModelViewSet):
    queryset = Publication.objects.filter(published=True)
    serializer_class = PublicationSerializer
    # filterset_class = PublicationDateFilter
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['category', 'author']
    search_fields = ['title', 'content']

    def retrieve(self, request, *args, **kwargs):
        publication = self.get_object()
        publication.views_count += 1
        publication.save()
        return super(PublicationViewSet, self).retrieve(request, *args, **kwargs)


    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        elif self.action in ['create']:
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in self.permission_classes]