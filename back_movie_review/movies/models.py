from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Actor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    actors = models.ManyToManyField(Actor, related_name="movies", blank=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    grade = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    movie = models.ForeignKey(Movie, related_name="reviews", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.movie.title} - {self.grade}/5"
