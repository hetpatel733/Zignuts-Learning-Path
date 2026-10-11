# TaskPro Django Project

## Overview
TaskPro is a Django 5.x based task manager API with a simple frontend built with Bootstrap 5 and vanilla JavaScript. It provides:
- JWT authentication (access & refresh tokens) via `djangorestframework-simplejwt`.
- User‑isolated task CRUD using the Django REST Framework.
- Filtering, searching and ordering of tasks (`django‑filters`).
- PostgreSQL as the production database.

## Project Structure
```
TaskPro/
├── config/                # Django settings, urls, wsgi/asgi
├── tasks/                 # Core app: models, serializers, views, tests
├── templates/            # HTML templates (base, login, register, dashboard)
├── static/               # CSS & JS assets
├── requirements.txt      # Python dependencies
└── manage.py
```

## Database Configuration (PostgreSQL)
The `config/settings.py` file contains the following `DATABASES` configuration:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'blog_app'),
        'USER': os.environ.get('DB_USER', 'hetpatel'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'hetpatel'),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```
You can override any value with environment variables. Ensure PostgreSQL is running and a database named **blog_app** exists, or adjust the defaults accordingly.

### Install PostgreSQL driver
```bash
pip install psycopg2-binary>=2.9
```
(Already added to `requirements.txt`.)

## Authentication Flow
1. **Register** – `POST /api/register/` with `username`, `email`, `password`.
2. **Obtain Tokens** – `POST /api/token/` with `username` and `password` returns `access` and `refresh` tokens.
3. **Refresh** – `POST /api/token/refresh/` with `refresh` token returns a new `access` token.
4. Include the `Authorization: Bearer <access_token>` header in every subsequent API request.

## API Endpoints
| Method | URL | Description |
|--------|-----|-------------|
| `POST` | `/api/register/` | Create a new user |
| `POST` | `/api/token/` | Obtain JWT tokens |
| `POST` | `/api/token/refresh/` | Refresh access token |
| `GET` | `/api/tasks/` | List tasks for the authenticated user |
| `POST` | `/api/tasks/` | Create a task |
| `GET` | `/api/tasks/<id>/` | Retrieve a single task |
| `PUT`/`PATCH` | `/api/tasks/<id>/` | Update a task |
| `DELETE` | `/api/tasks/<id>/` | Delete a task |

### Filtering, Searching & Ordering
You can add query parameters to `/api/tasks/`:
- **Filtering**: `?status=Pending&priority=High`
- **Search**: `?search=meeting`
- **Ordering**: `?ordering=-due_date` (prefix `-` for descending)

## Running the Project
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Apply migrations
python manage.py migrate

# 3. Create a superuser (optional, for admin site)
python manage.py createsuperuser

# 4. Run the development server
python manage.py runserver
```
Open `http://127.0.0.1:8000/` in a browser. The frontend will allow you to register, log in, and manage tasks without page reloads.

## Tests
Run the test suite with:
```bash
python manage.py test tasks
```
All tests cover registration, JWT authentication, CRUD operations, permissions, and filtering.

## Environment Variables
You may set the following variables to customise the setup:
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG` (`True`/`False`)
- `DJANGO_ALLOWED_HOSTS` (space‑separated list)
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
- `JWT_ACCESS_LIFETIME_MINUTES`
- `JWT_REFRESH_LIFETIME_DAYS`

## License
MIT License – feel free to modify and extend.
