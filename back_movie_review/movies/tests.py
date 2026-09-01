import pytest
from rest_framework import status
from rest_framework.test import APIClient

from movies.models import Actor, Movie, Review


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def actor():
    return Actor.objects.create(first_name="aaaaa", last_name="bbbbb")


@pytest.fixture
def movie(actor):
    movie = Movie.objects.create(title="aaaaa", description="bbbbb")
    movie.actors.add(actor)
    return movie


@pytest.mark.django_db
def test_list_movies(client, movie):
    response = client.get("/api/movies/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data[0] == {
        "id": movie.id,
        "title": movie.title,
        "average_review": None,
        "actor_count": 1,
    }


@pytest.mark.django_db
def test_list_movies_average_review(client, movie):
    Review.objects.create(grade=2, movie=movie)
    Review.objects.create(grade=4, movie=movie)

    response = client.get("/api/movies/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]["average_review"] == 3
    assert response.data[0]["actor_count"] == 1


@pytest.mark.django_db
def test_retrieve_movie(client, movie, actor):
    response = client.get(f"/api/movies/{movie.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == movie.title
    assert response.data["description"] == movie.description
    assert response.data["actors"] == [
        {"id": actor.id, "first_name": actor.first_name, "last_name": actor.last_name}
    ]
    assert response.data["average_review"] is None
    assert response.data["review_count"] == 0


@pytest.mark.django_db
def test_retrieve_movie_average_review(client, movie):
    Review.objects.create(grade=1, movie=movie)
    Review.objects.create(grade=5, movie=movie)

    response = client.get(f"/api/movies/{movie.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["average_review"] == 3
    assert response.data["review_count"] == 2


@pytest.mark.django_db
def test_create_movie(client):
    response = client.post(
        "/api/movies/",
        {"title": "ccccc", "description": "ddddd"},
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert Movie.objects.count() == 1
    created = Movie.objects.get()
    assert created.title == "ccccc"
    assert created.description == "ddddd"


@pytest.mark.django_db
def test_create_movie_ignores_actors(client, actor):
    response = client.post(
        "/api/movies/",
        {"title": "ccccc", "description": "ddddd", "actors": [actor.id]},
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    created = Movie.objects.get()
    assert list(created.actors.all()) == []


@pytest.mark.django_db
def test_update_movie(client, movie):
    response = client.put(
        f"/api/movies/{movie.id}/",
        {"title": "eeeee", "description": "fffff"},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    movie.refresh_from_db()
    assert movie.title == "eeeee"
    assert movie.description == "fffff"


@pytest.mark.django_db
def test_update_movie_does_not_change_actors(client, movie, actor):
    other_actor = Actor.objects.create(first_name="ccccc", last_name="ddddd")

    response = client.put(
        f"/api/movies/{movie.id}/",
        {"title": "eeeee", "description": "fffff", "actors": [other_actor.id]},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    movie.refresh_from_db()
    assert list(movie.actors.all()) == [actor]


@pytest.mark.django_db
def test_delete_movie(client, movie):
    response = client.delete(f"/api/movies/{movie.id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Movie.objects.count() == 0


@pytest.mark.django_db
def test_retrieve_movie_not_found(client):
    response = client.get("/api/movies/999/")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_create_movie_duplicate_title_rejected(client, movie):
    response = client.post(
        "/api/movies/",
        {"title": movie.title, "description": "ddddd"},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Movie.objects.count() == 1


@pytest.mark.django_db
def test_update_movie_duplicate_title_rejected(client, movie):
    other_movie = Movie.objects.create(title="ccccc", description="ddddd")

    response = client.put(
        f"/api/movies/{other_movie.id}/",
        {"title": movie.title, "description": "ddddd"},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_movie_keeps_own_title(client, movie):
    response = client.put(
        f"/api/movies/{movie.id}/",
        {"title": movie.title, "description": "updated"},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_actor(client, movie):
    response = client.post(
        "/api/actors/",
        {"first_name": "ccccc", "last_name": "ddddd", "movie_id": movie.id},
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert Actor.objects.count() == 2
    created = Actor.objects.get(first_name="ccccc")
    assert created.last_name == "ddddd"
    assert created in movie.actors.all()


@pytest.mark.django_db
def test_create_actor_requires_movie_id(client):
    response = client.post(
        "/api/actors/",
        {"first_name": "ccccc", "last_name": "ddddd"},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Actor.objects.count() == 0


@pytest.mark.django_db
def test_create_actor_movie_not_found(client):
    response = client.post(
        "/api/actors/",
        {"first_name": "ccccc", "last_name": "ddddd", "movie_id": 999},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Actor.objects.count() == 0


@pytest.mark.django_db
def test_retrieve_actor(client, actor):
    response = client.get(f"/api/actors/{actor.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "id": actor.id,
        "first_name": actor.first_name,
        "last_name": actor.last_name,
    }


@pytest.mark.django_db
def test_retrieve_actor_not_found(client):
    response = client.get("/api/actors/999/")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_actor(client, actor):
    response = client.put(
        f"/api/actors/{actor.id}/",
        {"first_name": "eeeee", "last_name": "fffff"},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    actor.refresh_from_db()
    assert actor.first_name == "eeeee"
    assert actor.last_name == "fffff"


@pytest.mark.django_db
def test_update_actor_ignores_movie_id(client, actor, movie):
    other_movie = Movie.objects.create(title="ccccc", description="ddddd")

    response = client.put(
        f"/api/actors/{actor.id}/",
        {"first_name": "eeeee", "last_name": "fffff", "movie_id": other_movie.id},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert list(other_movie.actors.all()) == []
    assert actor in movie.actors.all()


@pytest.mark.django_db
def test_delete_actor(client, actor):
    response = client.delete(f"/api/actors/{actor.id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Actor.objects.count() == 0


@pytest.mark.django_db
def test_delete_actor_removes_it_from_movie(client, actor, movie):
    client.delete(f"/api/actors/{actor.id}/")

    assert list(movie.actors.all()) == []


@pytest.mark.django_db
def test_create_review(client, movie):
    response = client.post(
        "/api/reviews/",
        {"grade": 4, "movie": movie.id},
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert Review.objects.count() == 1
    created = Review.objects.get()
    assert created.grade == 4
    assert created.movie == movie


@pytest.mark.django_db
def test_create_review_requires_movie(client):
    response = client.post(
        "/api/reviews/",
        {"grade": 4},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Review.objects.count() == 0


@pytest.mark.django_db
def test_create_review_movie_not_found(client):
    response = client.post(
        "/api/reviews/",
        {"grade": 4, "movie": 999},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Review.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize("grade", [0, 6])
def test_create_review_grade_out_of_range_rejected(client, movie, grade):
    response = client.post(
        "/api/reviews/",
        {"grade": grade, "movie": movie.id},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Review.objects.count() == 0
