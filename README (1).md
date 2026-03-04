
# JobPlatformFastAPI

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Redis](https://img.shields.io/badge/Redis-Cache-red)
![Docker](https://img.shields.io/badge/Docker-Container-blue)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

An **AI‑powered job platform API** built with **FastAPI** that connects **applicants and employers** with intelligent resume analysis using **OpenAI GPT**.

This repository demonstrates a **production‑style backend architecture** with:

- FastAPI REST API
- PostgreSQL database
- Redis rate limiting
- Docker containerization
- Alembic migrations
- GitHub Actions CI
- Ruff + Black linting
- Pytest testing
- Pre‑commit hooks

---

# Architecture

```
Client (Web/Mobile)
        |
        v
     FastAPI API
        |
   +----+----+
   |         |
PostgreSQL  Redis
   |         |
   +----+----+
        |
       OpenAI
```

---

# Features

## Authentication
- JWT authentication
- Google OAuth login
- Role‑based access control

## Job Platform
Employers can:
- Create jobs
- Manage applicants

Applicants can:
- Browse jobs
- Upload resumes
- Apply for jobs

## AI Resume Parsing
Powered by **OpenAI GPT**.

Supported formats:
- PDF
- DOCX

Extracted information:
- Skills
- Experience
- Education
- Summary

## Reviews
Users can leave **1–5 star reviews**.

## Rate Limiting
Implemented with **Redis + fastapi‑limiter**.

## Database Migrations
Handled with **Alembic**.

---

# Tech Stack

| Layer | Technology |
|------|-------------|
| Backend | FastAPI |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Cache | Redis |
| AI | OpenAI |
| Migrations | Alembic |
| Containerization | Docker |
| Testing | Pytest |
| Linting | Ruff |
| Formatting | Black |
| CI | GitHub Actions |

---

# Project Structure

```
jobplatformfastapi/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── repository/
│   ├── routes/
│   ├── schemas/
│   ├── config/
│   ├── utils/
│   ├── uploads/
│   └── main.py
│
├── tests/
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── lint.yml
│
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── .pre-commit-config.yaml
├── CONTRIBUTING.md
├── .env.example
└── README.md
```

---

# Running the Project

## Run with Docker (Recommended)

### Clone the repo

```
git clone https://github.com/kimenyu/jobplatform-fastapi.git
cd jobplatform-fastapi
```

### Create environment file

```
cp .env.example .env
```

Edit `.env` with your credentials.

### Start services

```
docker compose up --build
```

Services started:
- FastAPI
- PostgreSQL
- Redis
- Alembic migration container

### Access

API:
```
http://localhost:8000
```

Docs:
```
http://localhost:8000/docs
```

Health check:
```
http://localhost:8000/health
```

Stop services:

```
docker compose down
```

---

# Local Development

Create virtual environment:

```
python -m venv env
source env/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
pip install -e ".[dev]"
```

Run migrations:

```
alembic upgrade head
```

Start API:

```
uvicorn app.main:app --reload
```

---

# Testing

Run:

```
pytest
```

---

# Code Quality

Tools used:
- Ruff
- Black
- Pre‑commit

Install hooks:

```
pre-commit install
```

Run checks:

```
ruff check .
black --check .
```

---

# CI

GitHub Actions runs:

- Tests
- Linting
- Formatting checks

Workflows:

```
.github/workflows/ci.yml
.github/workflows/lint.yml
```

---

# Contributing

Please see:

```
CONTRIBUTING.md
```

---

# Author

Joseph Njoroge  
Backend Software Engineer

GitHub:
https://github.com/kimenyu

---

# License

MIT
