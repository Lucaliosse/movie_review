from rest_framework import mixins, viewsets

from .models import Actor, Movie
from .serializers import ActorCreateSerializer, ActorSerializer, MovieSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


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
