# Django Logging & Monitoring System

This project extends a Django backend application with **activity logging** and **error monitoring**, providing secure admin APIs to review logs.

---

## 🚀 Setup & Run Instructions

1. **Clone the repository** (or unzip the provided source):
   ```bash
   git clone https://github.com/your-repo/django-logging-monitoring.git
   cd django-logging-monitoring
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (admin)**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

---

## 📊 Example Log Entries

### Activity Log (stored in `ActivityLog` table)

```json
{
  "id": 1,
  "user": 2,
  "action": "login",
  "method": "POST",
  "path": "/api/login/",
  "ip_address": "127.0.0.1",
  "user_agent": "PostmanRuntime/7.35.0",
  "status_code": 200,
  "timestamp": "2025-09-02T12:34:56Z",
  "extra": {
    "details": "Successful login"
  }
}
```

### Error Log (stored in `ErrorLog` table)

```json
{
  "id": 5,
  "user": 2,
  "message": "no such table: monitoring_item",
  "stack_trace": "Traceback (most recent call last): ...",
  "method": "POST",
  "endpoint": "/api/items/",
  "ip_address": "127.0.0.1",
  "user_agent": "PostmanRuntime/7.35.0",
  "status_code": 500,
  "timestamp": "2025-09-02T12:45:00Z"
}
```

---

## 🔑 Authentication

- All log endpoints are **admin-only**.
- Use JWT or session authentication.
- Include your token in requests:
  ```http
  Authorization: Bearer <your_token>
  ```

---

## 📌 API Endpoints

### ✅ Activity Logs

#### Get all activity logs
```http
GET /api/logs/activities/
```

**Query parameters (optional):**
- `user_id`: filter by user
- `action`: filter by action type (`login`, `logout`, `create`, etc.)
- `start_date`: filter logs created after this date (YYYY-MM-DD)
- `end_date`: filter logs created before this date (YYYY-MM-DD)

**Example:**
```http
GET /api/logs/activities/?user_id=2&action=login&start_date=2025-09-01&end_date=2025-09-02
```

---

### ❌ Error Logs

#### Get all error logs
```http
GET /api/logs/errors/
```

**Query parameters (optional):**
- `status_code`: filter by HTTP status code (e.g., `500`)
- `start_date`: filter logs created after this date (YYYY-MM-DD)
- `end_date`: filter logs created before this date (YYYY-MM-DD)

**Example:**
```http
GET /api/logs/errors/?status_code=500&start_date=2025-09-01
```

---

### 🛠 Example (Postman)

#### Get activity logs
```http
GET http://127.0.0.1:8000/api/logs/activities/
Authorization: Bearer <admin_token>
```

#### Get error logs
```http
GET http://127.0.0.1:8000/api/logs/errors/?status_code=500
Authorization: Bearer <admin_token>
```

---

 ## 📌 API Endpoints
 ## 🔐 Auth Endpoints

POST /api/register/ → Register new user
POST /api/login/ → Login and get token
POST /api/logout/ → Logout user
POST /api/refresh/ → Refresh JWT token

 ## 👤 Profile Endpoints

GET /api/profile/ → Get logged-in user profile
PUT /api/profile/ → Update user profile

 ## 📦 Items CRUD Endpoints

GET /api/items/ → List all items
POST /api/items/ → Create new item
GET /api/items/{id}/ → Get item by ID
PUT /api/items/{id}/ → Update item by ID
DELETE /api/items/{id}/ → Delete item by ID

## 📊 Logs Endpoints (Admin only)

GET /api/logs/activities/ → Get all activity logs
Optional filters: user_id, action, start_date, end_date
GET /api/logs/errors/ → Get all error logs
Optional filters: status_code, start_date, end_date

---

## 📌 Tech Stack

- **Django** (Backend Framework)
- **Django REST Framework** (API)
- **SQLite/PostgreSQL/MySQL** (Database)
- **JWT / Session Auth** (Authentication)

---

## PRJECT-DEMO ##
<img width="1380" height="661" alt="1" src="https://github.com/user-attachments/assets/df910222-92c3-4779-a3f1-bbb84fdce6d9" />
<img width="1382" height="546" alt="2" src="https://github.com/user-attachments/assets/23522993-3d7f-406b-89d9-3ac1c1ca59cb" />
<img width="1375" height="477" alt="3" src="https://github.com/user-attachments/assets/c261e1b9-fdf6-4771-9ec8-ef06df811e06" />
<img width="1384" height="582" alt="4" src="https://github.com/user-attachments/assets/d95147a9-242f-4590-825d-4ff5945cfcab" />
<img width="1383" height="653" alt="5" src="https://github.com/user-attachments/assets/53d99381-8af2-4864-b71b-71567aeeab01" />
<img width="1368" height="861" alt="6" src="https://github.com/user-attachments/assets/e293fd5d-a661-4bee-9d42-679bbc5b8721" />
<img width="1386" height="660" alt="7" src="https://github.com/user-attachments/assets/48028dc2-e934-4ba0-a447-c1b71f57334f" />
<img width="1383" height="490" alt="8" src="https://github.com/user-attachments/assets/c3e45fd9-461c-49f3-a40a-a1b50c816a3c" />
<img width="1388" height="887" alt="9" src="https://github.com/user-attachments/assets/f8afc289-67c2-4382-82c6-4e842bca2af8" />
<img width="1379" height="584" alt="10" src="https://github.com/user-attachments/assets/af5fed7e-7127-4a8b-bc00-547f677e4c7f" />
<img width="1403" height="874" alt="11" src="https://github.com/user-attachments/assets/fd572536-5608-44a1-9d06-c1ec7e4ffa90" />
<img width="1376" height="385" alt="12" src="https://github.com/user-attachments/assets/001fb23d-c20f-460b-95a2-5ae373b7a552" />
<img width="1378" height="819" alt="13" src="https://github.com/user-attachments/assets/478feadd-aca2-44f0-80e3-ac3617b65eb3" />
<img width="1382" height="419" alt="14" src="https://github.com/user-attachments/assets/79a927f8-dbd5-4c58-82df-1624c96ee5c1" />
