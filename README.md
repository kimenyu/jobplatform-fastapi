# JobPlatformFastAPI

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-blue)
![Redis](https://img.shields.io/badge/Redis-Upstash-red)
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
   |    Neon     |                   |   Upstash   |
   |  PostgreSQL |                   | Redis (TLS) |
   | (Serverless)|                   | Rate Limit  |
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
- Alembic migrations for schema changes against Neon PostgreSQL

### Rate Limiting
- Upstash Redis-backed rate limiting over TLS (FastAPI Limiter)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI |
| ORM | SQLAlchemy + psycopg2 |
| Database | Neon PostgreSQL (serverless) |
| Migrations | Alembic |
| Auth | JWT + Google OAuth |
| AI | OpenAI |
| Resume Parsing | python-docx, pdfplumber |
| Rate Limiting | Upstash Redis + fastapi-limiter |
| Containerization | Docker + Docker Compose |
| Logging | Structlog |

---

## Project Structure

```
jobplatformfastapi/
├── app/
│   ├── api/                # Authentication routes
│   ├── config/             # Gunicorn + logging config
│   ├── core/               # Security utilities
│   ├── database/           # DB session & engine
│   ├── models/             # SQLAlchemy models
│   ├── repository/         # Business logic layer
│   ├── routes/             # API endpoints
│   ├── schemas/            # Pydantic schemas
│   ├── alembic/            # Migration scripts
│   ├── utils/              # Helper utilities
│   ├── uploads/            # Uploaded resumes
│   └── main.py             # FastAPI entrypoint
├── tests/
├── .github/workflows/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Environment Variables

Create a `.env` file at the project root. Use `.env.example` as a template:

```bash
cp .env.example .env
```

Required variables:

```dotenv
# Neon PostgreSQL — get from console.neon.tech
DATABASE_URL=postgresql+psycopg2://neondb_owner:YOUR_PASSWORD@ep-xxx.neon.tech/neondb?sslmode=require

# Upstash Redis — get from console.upstash.com (note: rediss:// with double s for TLS)
REDIS_URL=rediss://default:YOUR_TOKEN@your-instance.upstash.io:6379

# App secret
SECRET_KEY=your-random-secret-key
```

> **Never commit `.env` to git.** It is listed in `.gitignore`.

---

## Running with Docker (Recommended)

Docker runs the API only. Database (Neon) and Redis (Upstash) are external cloud services — no local containers needed for them.

### 1) Clone

```bash
git clone https://github.com/kimenyu/jobplatform-fastapi.git
cd jobplatform-fastapi
```

### 2) Configure `.env`

```bash
cp .env.example .env
# Fill in DATABASE_URL, REDIS_URL, SECRET_KEY
```

### 3) Build and start

```bash
docker compose up --build
```

### 4) Run migrations (first time only)

In a separate terminal while the container is running:

```bash
docker compose run --rm api alembic -c app/alembic.ini upgrade head
```

### 5) URLs

- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`

### 6) Stop

```bash
docker compose down
```

---

## Running Locally (Without Docker)

### 1) Virtualenv

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### 2) Configure `.env`

```dotenv
DATABASE_URL=postgresql+psycopg2://neondb_owner:YOUR_PASSWORD@ep-xxx.neon.tech/neondb?sslmode=require
REDIS_URL=rediss://default:YOUR_TOKEN@your-instance.upstash.io:6379
SECRET_KEY=your-secret-key
```

### 3) Run migrations

```bash
cd app
alembic -c alembic.ini upgrade head
```

### 4) Start server

```bash
uvicorn app.main:app --reload
```

---

## Database Migrations (Alembic)

Migrations run against Neon PostgreSQL using the `DATABASE_URL` from your `.env`.

**Generate a new migration after model changes:**

```bash
docker compose run --rm api alembic -c app/alembic.ini revision --autogenerate -m "describe your change"
```

**Apply migrations:**

```bash
docker compose run --rm api alembic -c app/alembic.ini upgrade head
```

**Check current state:**

```bash
docker compose run --rm api alembic -c app/alembic.ini current
```

**Rollback one step:**

```bash
docker compose run --rm api alembic -c app/alembic.ini downgrade -1
```

> The `docker-compose.yml` includes a volume mount (`. :/code`) so generated migration files are written back to your local filesystem.

---

## Deploying to Render

### Method A — Without Docker (Recommended)

**1. Push to GitHub**

Make sure `.gitignore` includes:
```
.env
jobboard.db
uploads/
client_secret_*.json
```

```bash
git add .
git commit -m "your commit message"
git push origin main
```

**2. Create a Web Service on Render**

- Go to [render.com](https://render.com) → New → Web Service
- Connect your GitHub repo
- Set:

| Field | Value |
|---|---|
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn -k uvicorn.workers.UvicornWorker -c app/config/gunicorn_conf.py app.main:app` |

**3. Add environment variables in Render dashboard**

```
DATABASE_URL=postgresql+psycopg2://...neon.tech/neondb?sslmode=require
REDIS_URL=rediss://...upstash.io:6379
SECRET_KEY=your-secret-key
```

**4. Run migrations after first deploy**

In Render dashboard → your service → Shell tab:

```bash
alembic -c app/alembic.ini upgrade head
```

Render auto-deploys on every `git push` to `main` after this.

### Method B — With Docker

- Go to Render → New → Web Service → connect repo
- Set **Runtime** to **Docker**
- Render auto-detects the `Dockerfile`
- Add the same 3 environment variables
- Run migrations via the Shell tab after first deploy

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

```bash
pip install -e ".[dev]"
pre-commit install

# Run checks
ruff check .
black --check .
pytest -q

# Auto-fix
ruff check . --fix
black .
```

---

## CI

GitHub Actions runs on every push:
- Alembic migrations
- Pytest

Workflow: `.github/workflows/ci.yml`

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