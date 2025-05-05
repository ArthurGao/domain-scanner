## 🔧 Structure

    ├── alembic/                   # Database migration scripts
    ├── alembic.ini                # Alembic config
    ├── app/
    │   ├── core/                  # Security, dependencies, configuration
    │   ├── db/                    # Session and base metadata
    │   ├── jobs/                  # Task execution logic (e.g. ScanTask)
    │   ├── models/                # SQLAlchemy models (User, Org, Scan, Schedule)
    │   ├── repositories/          # Repositories for each entity
    │   ├── routers/               # FastAPI routes (auth, users, scan, etc.)
    │   ├── schemas/               # Pydantic schemas (request/response)
    │   ├── services/              # Business logic layer
    │   ├── uow/                   # Unit of Work implementation
    │   └── main.py                # FastAPI application entrypoint
    ├── scripts/                   # CLI scripts (create admin, create tables)
    ├── requirements.txt           # Python dependencies
    └── README.md (to be generated)                                             

This project is a SaaS-style FastAPI application that allows users to register domains and schedule vulnerability scans. It supports multi-tenant architecture, JWT authentication, and scan scheduling via APScheduler.

## 🔧 Features

- 🏢 Multi-tenant organization and user management
- 🔐 JWT-based auth with role-based access (admin, user)
- 🖥 Domain scan scheduling (immediate or recurring: cron, interval, date)
- 📬 Email or dashboard-based result notifications
- 📊 Dashboard-ready endpoints and scan trend storage
- 🧩 Clean architecture: separation of models, services, UoW, and routers

## 📁 Project Structure

```text
{project_structure}
```

## 🚀 Getting Started

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

2. **Setup environment**

```bash
cp .env.example .env
# Edit environment variables (DB, JWT secret, etc.)
```
3. Launch PostgreSQL

```bash
docker-compose up -d
```

3. **Run Alembic migrations**

```bash
alembic upgrade head
```

4. **Run development server**

```bash
 uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5. **(Optional) Create default admin user**

```bash
PYTHONPATH=. python scripts/create_admin_user.py
```

## 🔄 Schedule Example

```json
{
  "name": "Monthly Scan",
  "type": "scheduled",
  "target": "example.com",
  "schedule": {
    "schedule_type": "cron",
    "cron_minute": "0",
    "cron_hour": "12",
    "cron_day": "1",
    "cron_month": "*",
    "cron_day_of_week": "*",
    "enabled": true
  }
}
```

## 📬 Health Check

```bash
GET /health
Response: {{"status": "ok"}}
```

---

## 📚 Tech Stack

- **FastAPI** – Web framework
- **PostgreSQL** – Relational DB
- **SQLAlchemy** – ORM
- **Alembic** – Migrations
- **APScheduler** – Job scheduling
- **Pydantic v2** – Data validation

---

## ✅ TODO (optionally)

- [ ] AI-based result summarization
- [ ] Frontend dashboard (React or Next.js)
- [ ] CI/CD deployment support
"""
