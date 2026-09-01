from django.db.models import Avg, Count
from rest_framework import mixins, viewsets

from .models import Actor, Movie, Review
from .serializers import (
    ActorCreateSerializer,
    ActorSerializer,
    MovieDetailSerializer,
    MovieListSerializer,
    MovieSerializer,
    ReviewSerializer,
)


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return MovieListSerializer
        if self.action == "retrieve":
            return MovieDetailSerializer
        return MovieSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list":
            return queryset.annotate(
                average_review=Avg("reviews__grade"),
                actor_count=Count("actors", distinct=True),
            )
        if self.action == "retrieve":
            return queryset.annotate(
                average_review=Avg("reviews__grade"),
                review_count=Count("reviews", distinct=True),
            ).prefetch_related("actors")
        return queryset


class ActorViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return ActorCreateSerializer
        return ActorSerializer


class ReviewViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
