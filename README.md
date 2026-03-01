# Task Manager REST API

A production-ready RESTful API for task management built with Django and Django REST Framework. Features include JWT authentication, role-based access control, filtering, searching, ordering, and pagination.

## Features

- 🔐 **JWT Authentication** - Secure token-based authentication with refresh tokens
- 👥 **Role-Based Access Control** - Admin and User roles with different permissions
- 📋 **Task Management** - Full CRUD operations for tasks
- 🔍 **Advanced Filtering** - Filter, search, and order tasks
- 📄 **Pagination** - Configurable page size with validation
- 🛡️ **Standardized Error Handling** - Consistent JSON error responses
- ✅ **Data Validation** - Comprehensive input validation
- 🔒 **Token Blacklisting** - Secure logout with token revocation
- 🧪 **Comprehensive Test Suite** - 66 test cases with full coverage
- 📚 **Interactive API Documentation** - Swagger UI and ReDoc

## Tech Stack

- **Python 3.12**
- **Django 6.0.2**
- **Django REST Framework 3.16.1**
- **djangorestframework-simplejwt 5.5.1** - JWT authentication with token blacklisting
- **django-filter 25.2** - Advanced filtering capabilities
- **drf-spectacular 0.29.0** - OpenAPI 3.0 schema generation and documentation
- **SQLite** - Default database (production-ready PostgreSQL support)

## Project Structure

```
task-manager-rest-apis/
├── core/                      # Project settings and configuration
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL configuration
│   ├── middleware.py         # Custom middleware for response standardization
│   └── exceptions.py         # Custom exception handlers
├── users/                     # User authentication app
│   ├── models.py             # Custom User model
│   ├── serializers.py        # User serializers
│   ├── views.py              # Authentication views
│   ├── tests.py              # User app test cases (24 tests)
│   └── urls.py               # Auth endpoints
├── task/                      # Task management app
│   ├── models.py             # Task model
│   ├── serializers.py        # Task serializers
│   ├── views.py              # Task views
│   ├── permissions.py        # Custom permissions
│   ├── tests.py              # Task app test cases (42 tests)
│   └── urls.py               # Task endpoints
├── env/                       # Virtual environment
├── db.sqlite3                # SQLite database
├── manage.py                 # Django management script
└── requirements.txt          # Python dependencies
```

## Database Models

### User Model
```python
{
    "id": "uuid",
    "username": "string (unique)",
    "email": "string (unique)",
    "password": "string (hashed)",
    "role": "admin | user"
}
```

### Task Model
```python
{
    "id": "uuid",
    "title": "string (max 255)",
    "description": "text",
    "completed": "boolean",
    "username": "string (read-only)",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

## Setup Instructions

### Prerequisites
- Python 3.12 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd task-manager-rest-apis
   ```

2. **Create and activate virtual environment**

   **Windows (PowerShell):**
   ```powershell
   python -m venv env
   .\env\Scripts\Activate.ps1
   ```

   **Windows (Command Prompt):**
   ```cmd
   python -m venv env
   env\Scripts\activate.bat
   ```

   **Linux/Mac:**
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`

### Interactive API Documentation

Once the server is running, you can access interactive API documentation:

- **Swagger UI:** http://127.0.0.1:8000/api/docs/swagger/
- **ReDoc:** http://127.0.0.1:8000/api/docs/redoc/
- **OpenAPI Schema (JSON):** http://127.0.0.1:8000/api/schema/

These provide a visual interface to explore and test all API endpoints.

## API Documentation

### Base URL
```
http://127.0.0.1:8000
```

### Response Format

All API responses follow a standardized format:

**Success Response (2xx):**
```json
{
    "success": true,
    "status_code": 200,
    "message": "Request successful",
    "data": { ... }
}
```

**Error Response (4xx/5xx):**
```json
{
    "success": false,
    "status_code": 400,
    "message": "Error message",
    "errors": { ... }
}
```

**Note:** API documentation endpoints (`/api/schema/`, `/api/docs/swagger/`, `/api/docs/redoc/`) return native format and are excluded from the standardized response wrapper.

---

## API Endpoints

The API provides 9 endpoints across authentication and task management:

### Authentication Endpoints (4)
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login (get JWT tokens)
- `POST /api/auth/token/refresh/` - Refresh access token
- `POST /api/auth/logout/` - Logout and blacklist token

### Task Endpoints (5)
- `GET /api/tasks/` - List tasks (with filtering, search, ordering)
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/<id>/` - Get task details
- `PUT/PATCH /api/tasks/<id>/` - Update a task
- `DELETE /api/tasks/<id>/` - Delete a task

---

## Authentication Endpoints

### 1. Register User

**Endpoint:** `POST /api/auth/register/`

**Description:** Create a new user account

**Request Body:**
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePassword123",
    "role": "user"  // Optional: "admin" or "user" (default: "user")
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePassword123",
    "role": "user"
  }'
```

**Success Response (201):**
```json
{
    "success": true,
    "status_code": 201,
    "message": "Request successful",
    "data": {
        "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
        "username": "john_doe",
        "email": "john@example.com"
    }
}
```

---

### 2. Login

**Endpoint:** `POST /api/auth/login/`

**Description:** Authenticate user and get JWT tokens

**Request Body:**
```json
{
    "username": "john_doe",
    "password": "SecurePassword123"
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "SecurePassword123"
  }'
```

**Success Response (200):**
```json
{
    "success": true,
    "status_code": 200,
    "message": "Request successful",
    "data": {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "user": {
            "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
            "username": "john_doe",
            "email": "john@example.com",
            "role": "user"
        }
    }
}
```

---

### 3. Refresh Token

**Endpoint:** `POST /api/auth/token/refresh/`

**Description:** Get a new access token using refresh token

**Request Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }'
```

**Success Response (200):**
```json
{
    "success": true,
    "status_code": 200,
    "message": "Request successful",
    "data": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
```

---

### 4. Logout

**Endpoint:** `POST /api/auth/logout/`

**Description:** Logout user and blacklist refresh token

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/logout/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }'
```

**Success Response (200):**
```json
{
    "success": true,
    "status_code": 200,
    "message": "Request successful",
    "data": {
        "message": "Logged out successfully"
    }
}
```

---

## Task Endpoints

**Note:** All task endpoints require authentication. Include the access token in the Authorization header.

### 5. List/Search/Filter Tasks

**Endpoint:** `GET /api/tasks/`

**Description:** Get all tasks (filtered by user role)
- **Regular users:** See only their own tasks
- **Admin users:** See all tasks

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page` - Page number (default: 1)
- `page_size` - Items per page (max: 100, default: 10)
- `completed` - Filter by completion status (true/false)
- `search` - Search in title and description
- `ordering` - Order by field (prefix with `-` for descending)
  - Options: `created_at`, `updated_at`, `completed`
  - Example: `-created_at` (newest first)

**cURL Examples:**

**Basic list:**
```bash
curl -X GET http://127.0.0.1:8000/api/tasks/ \
  -H "Authorization: Bearer <access_token>"
```

**With pagination:**
```bash
curl -X GET "http://127.0.0.1:8000/api/tasks/?page=1&page_size=20" \
  -H "Authorization: Bearer <access_token>"
```

**Filter completed tasks:**
```bash
curl -X GET "http://127.0.0.1:8000/api/tasks/?completed=true" \
  -H "Authorization: Bearer <access_token>"
```

**Search tasks:**
```bash
curl -X GET "http://127.0.0.1:8000/api/tasks/?search=groceries" \
  -H "Authorization: Bearer <access_token>"
```

**Order by newest first:**
```bash
curl -X GET "http://127.0.0.1:8000/api/tasks/?ordering=-created_at" \
  -H "Authorization: Bearer <access_token>"
```

**Combine filters, search, and ordering:**
```bash
curl -X GET "http://127.0.0.1:8000/api/tasks/?completed=false&search=buy&ordering=-created_at&page=1&page_size=20" \
  -H "Authorization: Bearer <access_token>"
```

**Success Response (200):**
```json
{
    "success": true,
    "status_code": 200,
    "message": "Request successful",
    "data": {
        "count": 25,
        "next": "http://127.0.0.1:8000/api/tasks/?page=2",
        "previous": null,
        "results": [
            {
                "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": false,
                "username": "john_doe",
                "created_at": "2026-03-01T10:30:00Z",
                "updated_at": "2026-03-01T10:30:00Z"
            }
        ]
    }
}
```

---

### 6. Create Task

**Endpoint:** `POST /api/tasks/`

**Description:** Create a new task

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false
}
```

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false
  }'
```

**Success Response (201):**
```json
{
    "success": true,
    "status_code": 201,
    "message": "Request successful",
    "data": {
        "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
        "completed": false,
        "username": "john_doe",
        "created_at": "2026-03-01T10:30:00Z",
        "updated_at": "2026-03-01T10:30:00Z"
    }
}
```

---

### 7. Get Task Details

**Endpoint:** `GET /api/tasks/<task_id>/`

**Description:** Retrieve a specific task by ID

**Headers:**
```
Authorization: Bearer <access_token>
```

**cURL Example:**
```bash
curl -X GET http://127.0.0.1:8000/api/tasks/a1b2c3d4-e5f6-7890-abcd-ef1234567890/ \
  -H "Authorization: Bearer <access_token>"
```

**Success Response (200):**
```json
{
    "success": true,
    "status_code": 200,
    "message": "Request successful",
    "data": {
        "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
        "completed": false,
        "username": "john_doe",
        "created_at": "2026-03-01T10:30:00Z",
        "updated_at": "2026-03-01T10:30:00Z"
    }
}
```

---

### 8. Update Task

**Endpoint:** `PUT /api/tasks/<task_id>/` or `PATCH /api/tasks/<task_id>/`

**Description:** Update a task (full or partial update)
- **PUT:** Requires all fields
- **PATCH:** Update specific fields only

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body (PATCH):**
```json
{
    "completed": true
}
```

**cURL Example (PATCH):**
```bash
curl -X PATCH http://127.0.0.1:8000/api/tasks/a1b2c3d4-e5f6-7890-abcd-ef1234567890/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "completed": true
  }'
```

**cURL Example (PUT):**
```bash
curl -X PUT http://127.0.0.1:8000/api/tasks/a1b2c3d4-e5f6-7890-abcd-ef1234567890/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "title": "Buy groceries - Updated",
    "description": "Milk, eggs, bread, cheese",
    "completed": true
  }'
```

**Success Response (200):**
```json
{
    "success": true,
    "status_code": 200,
    "message": "Request successful",
    "data": {
        "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "title": "Buy groceries - Updated",
        "description": "Milk, eggs, bread, cheese",
        "completed": true,
        "username": "john_doe",
        "created_at": "2026-03-01T10:30:00Z",
        "updated_at": "2026-03-01T15:45:00Z"
    }
}
```

---

### 9. Delete Task

**Endpoint:** `DELETE /api/tasks/<task_id>/`

**Description:** Delete a specific task

**Headers:**
```
Authorization: Bearer <access_token>
```

**cURL Example:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/tasks/a1b2c3d4-e5f6-7890-abcd-ef1234567890/ \
  -H "Authorization: Bearer <access_token>"
```

**Success Response (204):**
```
No content (successful deletion)
```

---

## Error Responses

### 400 Bad Request
```json
{
    "success": false,
    "status_code": 400,
    "message": "Validation failed",
    "errors": {
        "username": ["A user with that username already exists."],
        "email": ["This field is required."]
    }
}
```

### 401 Unauthorized
```json
{
    "success": false,
    "status_code": 401,
    "message": "Unauthorized",
    "errors": {
        "detail": "Authentication credentials were not provided."
    }
}
```

### 403 Forbidden
```json
{
    "success": false,
    "status_code": 403,
    "message": "Permission denied",
    "errors": {
        "detail": "You do not have permission to perform this action."
    }
}
```

### 404 Not Found
```json
{
    "success": false,
    "status_code": 404,
    "message": "Resource not found",
    "errors": {
        "detail": "Not found."
    }
}
```

### 500 Internal Server Error
```json
{
    "success": false,
    "status_code": 500,
    "message": "Internal server error",
    "errors": {
        "detail": "An error occurred processing your request."
    }
}
```

---

## Permissions

### User Roles

**Regular User (`role: "user"`):**
- Can create tasks
- Can view only their own tasks
- Can update only their own tasks
- Can delete only their own tasks

**Admin (`role: "admin"`):**
- Can create tasks
- Can view all users' tasks
- Can update any task
- Can delete any task

### Permission Rules

The API uses custom permission class `IsAdminOrOwner`:
- Admins have full access to all tasks
- Regular users can only access their own tasks
- Unauthenticated users cannot access task endpoints

---

## Testing Examples

### Complete Workflow Example

1. **Register a new user**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "TestPass123"}'
```

2. **Login to get tokens**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "TestPass123"}'
```

Save the `access` token from the response.

3. **Create a task**
```bash
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"title": "Test Task", "description": "Testing API", "completed": false}'
```

4. **List tasks**
```bash
curl -X GET http://127.0.0.1:8000/api/tasks/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

5. **Update task**
```bash
curl -X PATCH http://127.0.0.1:8000/api/tasks/TASK_ID/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"completed": true}'
```

6. **Delete task**
```bash
curl -X DELETE http://127.0.0.1:8000/api/tasks/TASK_ID/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

7. **Logout**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/logout/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
```

---

## Configuration

### JWT Settings (in `core/settings.py`)

```python
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}
```

### Pagination Settings

```python
REST_FRAMEWORK = {
    "PAGE_SIZE": 10,  # Default page size
}
```

Custom pagination in views:
- Default: 10 items per page
- Configurable: `?page_size=20`
- Maximum: 100 items per page

---

## Development

### Running Tests

The project includes comprehensive test coverage with **66 test cases** covering all aspects of the API.

**Test Coverage:**
- **Users App (24 tests):**
  - User registration (8 tests)
  - User login (5 tests)
  - Token refresh (3 tests)
  - User logout (3 tests)
  - User model (5 tests)

- **Task App (42 tests):**
  - Task list and create (7 tests)
  - Task detail operations (11 tests)
  - Filtering (2 tests)
  - Searching (3 tests)
  - Ordering (3 tests)
  - Pagination (6 tests)
  - Combined filters (2 tests)
  - Task model (8 tests)

**Run all tests:**
```bash
python manage.py test
```

**Run tests for specific app:**
```bash
# Test only users app
python manage.py test users

# Test only task app
python manage.py test task
```

**Run specific test class:**
```bash
python manage.py test users.tests.UserRegistrationTests
python manage.py test task.tests.TaskFilterTests
```

**Run tests with verbosity:**
```bash
python manage.py test --verbosity=2
```

**Run tests with coverage (optional):**
```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run --source='.' manage.py test

# View coverage report
coverage report

# Generate HTML coverage report
coverage html
# Open htmlcov/index.html in browser
```

**Test Categories:**

1. **Authentication Tests:**
   - User registration with validation
   - Login/logout workflows
   - JWT token generation and refresh
   - Token blacklisting

2. **Authorization Tests:**
   - Role-based access control (Admin vs User)
   - Permission enforcement
   - Owner-only access validation

3. **CRUD Operation Tests:**
   - Create, Read, Update, Delete tasks
   - Field validation
   - Error handling

4. **Advanced Feature Tests:**
   - Filtering by completion status
   - Full-text search in title/description
   - Multi-field ordering
   - Pagination with size limits

5. **Model Tests:**
   - Database constraints
   - Default values
   - Auto-generated fields
   - Model relationships

**Expected Output:**
```
Found 66 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..................................................................
----------------------------------------------------------------------
Ran 66 tests in X.XXXs

OK
Destroying test database for alias 'default'...
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Access Admin Panel
```
http://127.0.0.1:8000/admin/
```

### Making Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Production Deployment

### Important Security Settings

Before deploying to production, update `core/settings.py`:

```python
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')  # Use environment variable
ALLOWED_HOSTS = ['yourdomain.com']

# Add HTTPS settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Database

For production, consider using PostgreSQL instead of SQLite:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'taskmanager',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## Dependencies

All dependencies are listed in `requirements.txt`. Install them with:
```bash
pip install -r requirements.txt
```

**Main Dependencies:**
- **Django 6.0.2** - Web framework
- **djangorestframework 3.16.1** - REST API toolkit
- **djangorestframework-simplejwt 5.5.1** - JWT authentication
- **django-filter 25.2** - Filtering support
- **drf-spectacular 0.29.0** - OpenAPI 3.0 schema & documentation
- **PyJWT 2.11.0** - JSON Web Token implementation
- **cryptography 46.0.5** - Cryptographic recipes and primitives

---

## Troubleshooting

### Virtual Environment Activation Issues

**Windows PowerShell:**
If you get an execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\env\Scripts\Activate.ps1
```

### Migration Issues

If you encounter migration conflicts:
```bash
# Windows PowerShell - Delete database and start fresh (development only!)
Remove-Item db.sqlite3 -ErrorAction SilentlyContinue
python manage.py migrate

# Linux/Mac
rm -f db.sqlite3
python manage.py migrate
```

### Token Invalid/Expired

If you get authentication errors:
- Check if access token has expired (60 minutes lifetime)
- Use refresh token to get a new access token
- If refresh token is expired, login again

### Test Failures

**If tests are failing:**

1. **Database issues:**
   ```bash
   # Django creates a test database automatically
   # If issues persist, delete the main database and recreate
   python manage.py flush
   python manage.py migrate
   ```

2. **Import errors:**
   ```bash
   # Ensure all dependencies are installed
   pip install -r requirements.txt
   ```

3. **Run specific failing test for debugging:**
   ```bash
   python manage.py test users.tests.UserRegistrationTests.test_user_registration_success --verbosity=2
   ```

4. **Clear Python cache:**
   ```bash
   # Windows
   Get-ChildItem -Include __pycache__ -Recurse -Force | Remove-Item -Force -Recurse
   
   # Linux/Mac
   find . -type d -name __pycache__ -exec rm -r {} +
   ```

### API Response Issues

**If middleware is not formatting responses correctly:**
- Check that `core.middleware.StandardizeResponseMiddleware` is in MIDDLEWARE settings
- Ensure middleware is positioned after authentication middleware
- Verify content type is `application/json`

**If pagination validation is not working:**
- Check that `TaskPagination` class is set in the view
- Verify `page_size_query_param` is configured correctly

### Schema Generation Warnings

When running the development server, you may see warnings like:
```
Warning [LogoutView]: unable to guess serializer...
Warning [TaskListCreateView]: Failed to obtain model through view's queryset...
```

**These warnings are harmless and can be safely ignored.** They occur because:
- `drf-spectacular` tries to auto-generate API documentation schemas
- Some views (like `LogoutView` using `APIView`) don't expose enough metadata for automatic schema generation
- The schema generator inspects views without authentication context

**The warnings do not affect:**
- API functionality
- Test execution
- Production performance
- Interactive documentation (Swagger/ReDoc still works perfectly)

To suppress these warnings, you can exclude the schema generation output when running the server, or use `@extend_schema` decorators in views for explicit schema definitions.

---

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For questions or support, please open an issue in the repository.

---

**Happy Coding! 🚀**