# Movie Review — Backend

Django + Django REST Framework API for managing movies, actors and reviews.

## Features

- Movies: paginated list (title, average review, actor count), detail view (description, actors, average review, review count), create, update (title/description), delete
- Actors: create (attached to a movie), retrieve, update, delete
- Reviews: create a 1–5 rating on a movie
- Django admin enabled
- OpenAPI schema with Swagger UI / ReDoc (drf-spectacular)
- CORS configured for the Vite frontend
- Unit tests (pytest-django)
- Code formatted with [black](https://black.readthedocs.io/)
- Middleware setup to log the API database query count to track performance issue
- AGENTS.md to help agentic keep track of their previous mistake. To be updated each time a developer correct its agent.

## Setup

The project was initialized with the following commands:

```bash
python -m venv ./.venv
pip install Django==6.1
django-admin startproject training
```

---

## Quick Start

### Prerequisites
- Python 3.13+
- pip

### Initial Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate
# On Windows:
.venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt

# Copy the example env file and adjust values if needed
cp .env.example .env

# Apply migrations
python manage.py migrate

# (optional) create an admin user
python manage.py createsuperuser

# Run the server
python manage.py runserver
```

### Environment Variables

Configuration that varies per environment (secrets, debug flag, allowed hosts, CORS origins, pagination size) is read from a `.env` file at the project root, loaded via `django-environ`. Copy `.env.example` to `.env` and adjust values for your local setup — `.env` is gitignored, `.env.example` is committed as the reference.

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Django cryptographic secret key | insecure dev key (change for any real deployment) |
| `DEBUG` | Django debug mode | `True` |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hostnames | empty (with `DEBUG=True`, Django auto-allows `localhost`/`127.0.0.1`) |
| `CORS_ALLOWED_ORIGINS` | Comma-separated list of origins allowed to call the API | `http://localhost:5173,http://127.0.0.1:5173` |
| `MOVIE_PAGE_SIZE` | Number of movies returned per page on the movie list endpoint | `5` |

---

## Running the Application

### Start the Development Server

```bash
python manage.py runserver
```

The server runs at `http://127.0.0.1:8000`

### Apply Database Migrations

```bash
python manage.py migrate
```

---

## Running Tests

Unit tests use [pytest-django](https://pytest-django.readthedocs.io/):

```bash
python -m pytest
```

---

## Code Formatting

This project is formatted with [black](https://black.readthedocs.io/). Prefer the "Black Formatter" VS Code extension (`ms-python.black-formatter`) with format-on-save enabled, or run it manually before committing:

```bash
pip install black
black .
```

---

## API Documentation

Once the server is running, access the API documentation at:

- **Swagger UI**: http://127.0.0.1:8000/api/schema/swagger-ui/
- **ReDoc**: http://127.0.0.1:8000/api/schema/redoc/

---
