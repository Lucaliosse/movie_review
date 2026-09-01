from rest_framework import serializers

from .models import Actor, Movie, Review


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["id", "first_name", "last_name"]


class ActorCreateSerializer(serializers.ModelSerializer):
    movie_id = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(), write_only=True
    )

    class Meta:
        model = Actor
        fields = ["id", "first_name", "last_name", "movie_id"]

    def create(self, validated_data):
        movie = validated_data.pop("movie_id")
        actor = Actor.objects.create(**validated_data)
        movie.actors.add(actor)
        return actor


class MovieSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ["id", "title", "description", "actors"]


class MovieListSerializer(serializers.ModelSerializer):
    average_review = serializers.FloatField(read_only=True, allow_null=True)
    actor_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Movie
        fields = ["id", "title", "average_review", "actor_count"]


class MovieDetailSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True, read_only=True)
    average_review = serializers.FloatField(read_only=True, allow_null=True)
    review_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "description",
            "actors",
            "average_review",
            "review_count",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "grade", "movie"]
