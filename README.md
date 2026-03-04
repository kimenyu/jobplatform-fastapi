# JobPlatformFastAPI

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Redis](https://img.shields.io/badge/Redis-Cache-red)
![Docker](https://img.shields.io/badge/Docker-Container-blue)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

An **AI-powered job platform API** built with **FastAPI** that connects **applicants and employers** with intelligent resume analysis using **OpenAI GPT**.

---

## Architecture

```
                 +-------------------+
                 |      Client       |
                 | (Web / Mobile)    |
                 +---------+---------+
                           |
                           v
                    +-------------+
                    |   FastAPI   |
                    |   Backend   |
                    +------+------+ 
                           |
          +----------------+----------------+
          |                                 |
          v                                 v
   +-------------+                   +-------------+
   | PostgreSQL  |                   |    Redis    |
   |  Database   |                   | Rate Limit  |
   +-------------+                   +-------------+
                           |
                           v
                     +-----------+
                     |  OpenAI   |
                     | Resume AI |
                     +-----------+
```

---

## Features

### Authentication & Authorization
- JWT authentication
- Google OAuth login
- Automatic user creation for OAuth users
- Role-based access control (Admin, Employer, Applicant)

### Job Management
- Employers: create/update/delete jobs, manage applicants
- Applicants: browse jobs, apply with resume upload, track status

### AI Resume Parsing
- Resume formats: `.pdf`, `.docx`
- Uses **OpenAI GPT** for structured extraction (skills, experience, education, summary)
- Falls back to traditional parsing (`python-docx`, `pdfplumber`) where needed

### Reviews & Ratings
- Users can review each other (1–5 stars)

### Migrations
- Alembic migrations for schema changes

### Rate Limiting
- Redis-backed rate limiting (FastAPI Limiter)

---

## Tech Stack

| Layer | Technology |
|------|-------------|
| Backend | FastAPI |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Migrations | Alembic |
| Auth | JWT + Google OAuth |
| AI | OpenAI |
| Resume Parsing | python-docx, pdfplumber |
| Rate Limiting | Redis + fastapi-limiter |
| Containerization | Docker + Docker Compose |
| Logging | Structlog |

---

## Project Structure

```
jobplatformfastapi/
├── app/
│   ├── api/                # Authentication routes
│   ├── core/               # Security utilities
│   ├── database/           # DB session & engine
│   ├── models/             # SQLAlchemy models
│   ├── repository/         # Business logic layer
│   ├── routes/             # API endpoints
│   ├── schemas/            # Pydantic schemas
│   ├── config/             # Logging configuration
│   ├── utils/              # Helper utilities
│   ├── uploads/            # Uploaded resumes
│   └── main.py             # FastAPI entrypoint
├── tests/
├── .github/workflows/
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── .pre-commit-config.yaml
├── requirements.txt
└── README.md
```

---

## Running the Project

### Running with Docker (Recommended)

Docker starts:
- FastAPI API
- PostgreSQL
- Redis
- One-time migration service (Alembic)

#### 1) Clone
```bash
git clone https://github.com/kimenyu/jobplatform-fastapi.git
cd jobplatform-fastapi
```

#### 2) Create `.env`
Use `.env.example` as a template:
```bash
cp .env.example .env
```

Update values in `.env` (OpenAI key, Google OAuth, SECRET_KEY).

#### 3) Start services
```bash
docker compose up --build
```

#### 4) URLs
- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`

#### 5) Stop
```bash
docker compose down
```

> Note: Postgres is mapped to host port **5433** to avoid conflicts with local Postgres.
> Container-to-container connections still use `db:5432`.

---

### Running Locally (Without Docker)

#### 1) Virtualenv
```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

#### 2) Start dependencies
Make sure **PostgreSQL** and **Redis** are running locally.

#### 3) Configure `.env`
Example:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/jobboard
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=change_me
ENABLE_RATE_LIMIT=false
```

#### 4) Run migrations
```bash
alembic upgrade head
```

#### 5) Start server
```bash
uvicorn app.main:app --reload
```

---

## API Examples

### Register
`POST /auth/register`
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

### Login
`POST /auth/login/user`
```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}
```

---

## Formatting, Linting, and Hooks

This repo supports:
- **Ruff** (lint + import sorting)
- **Black** (formatting)
- **Pytest** (tests)
- **Pre-commit hooks** (runs checks before commits)

### Install dev tools
```bash
pip install -r requirements.txt
pip install -e ".[dev]"
pre-commit install
```

### Run checks manually
```bash
ruff check .
black --check .
pytest -q
```

### Auto-fix
```bash
ruff check . --fix
black .
```

---

## Database Migrations (Alembic)

Create migration:
```bash
alembic revision --autogenerate -m "add table"
```

Apply:
```bash
alembic upgrade head
```

Rollback:
```bash
alembic downgrade -1
```

---

## CI

GitHub Actions runs:
- Postgres + Redis services
- Alembic migrations
- Pytest

Workflow file:
- `.github/workflows/ci.yml`

---

## Roadmap
- AI job recommendations
- Real-time notifications (WebSockets)
- Admin analytics dashboard
- Interview scheduling

---

## Author

**Joseph Njoroge**  
Backend Software Engineer focused on scalable backend systems and AI-powered platforms.

- GitHub: https://github.com/kimenyu  
- Email: njorogekimenyu@gmail.com

---

## License
MIT
