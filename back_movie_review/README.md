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

# Run the server
python manage.py runserver
```

### Environment Variables

Configuration that varies per environment (secrets, debug flag, allowed hosts, CORS origins) is read from a `.env` file at the project root, loaded via `django-environ`. Copy `.env.example` to `.env` and adjust values for your local setup — `.env` is gitignored, `.env.example` is committed as the reference.


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

## API Documentation

Once the server is running, access the API documentation at:

- **Swagger UI**: http://127.0.0.1:8000/api/schema/swagger-ui/
- **ReDoc**: http://127.0.0.1:8000/api/schema/redoc/

---