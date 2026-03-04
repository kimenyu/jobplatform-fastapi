```markdown
# JobPlatformFastAPI

An intelligent, full-featured job platform built with **FastAPI** that connects **applicants** and **employers**, powered by AI-driven resume parsing using **OpenAI's GPT**. It features robust role-based authentication with **Google OAuth**, job posting, application management, resume analysis, notifications, and user reviews.

---

# Features

## Authentication & Authorization

- **Multiple Login Options**
  - Traditional JWT-based login & registration
  - **Google OAuth 2.0 integration** for seamless sign-in
  - Automatic user creation for new Google users
- **Role-specific access** (Admin, Employer, Applicant)
- **Secure token-based authentication**

---

## Job Management

- Employers can create, update, delete, and manage jobs
- Applicants can browse and apply to jobs
- Advanced job filtering and search capabilities

---

## Resume Upload & AI Parsing

Applicants upload resumes in `.docx` or `.pdf` formats.

Hybrid parsing approach:

- **OpenAI GPT** for intelligent content extraction
- Traditional parsing using `python-docx` and `pdfplumber` as fallback

Extracted insights include:

- Skills
- Experience
- Education
- Career summary
- Achievements

---

## Application Tracking

- Admins and employers can view applications
- Applicants track submission status
- Real-time application status updates

---

## Notifications

- System-generated notifications for application events
- Email integration for important updates

---

## Reviews & Ratings

Users can leave reviews (1–5 stars) to build transparency and trust on the platform.

---

## Database Management

- **Alembic migrations** for schema updates
- SQLAlchemy ORM for robust data modeling

---

# Powered by AI

The platform integrates **OpenAI GPT** to analyze resumes using natural language understanding.

It generates insights such as:

- Experience level assessment
- Skill proficiency evaluation
- Career summary generation
- Education and achievements extraction
- Job–skill matching recommendations

---

# Tech Stack

| Layer | Technology |
|------|------------|
| Backend | FastAPI (Python) |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Migrations | Alembic |
| Authentication | JWT + OAuth2 + Google OAuth |
| AI Integration | OpenAI |
| Resume Parsing | GPT + python-docx / pdfplumber |
| Containerization | Docker + Docker Compose |
| Caching / Rate Limiting | Redis |

---

# Project Structure

```

jobplatformfastapi/
│
├── app/
│   ├── api/                # Authentication routes
│   ├── core/               # Security utilities
│   ├── database/           # Database session
│   ├── models/             # SQLAlchemy models
│   ├── repository/         # Business logic layer
│   ├── routes/             # API routes
│   ├── schemas/            # Pydantic schemas
│   ├── uploads/            # Uploaded resume files
│   ├── alembic/            # Database migrations
│   ├── config/             # Logging and config
│   └── main.py             # FastAPI entry point
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

````

---

# Running the Project

The project can be run **using Docker (recommended)** or **locally without Docker**.

---

# Run With Docker (Recommended)

Docker will automatically start:

- FastAPI API server
- PostgreSQL database
- Redis (for rate limiting)

### 1 Clone the repository

```bash
git clone https://github.com/kimenyu/jobplatform-fastapi.git
cd jobplatform-fastapi
````

---

### 2 Create `.env` file

Create a `.env` file in the root directory:

```env
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=jobboard
POSTGRES_HOST=db
POSTGRES_PORT=5432

DATABASE_URL=postgresql://postgres:postgres@db:5432/jobboard

# Redis
REDIS_URL=redis://redis:6379/0

# JWT
SECRET_KEY=your_super_secure_jwt_secret_key_here

# OpenAI
OPENAI_API_KEY=your_openai_api_key

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
```

---

### 3 Build and start the containers

```bash
docker compose up --build
```

This will start:

* FastAPI API server
* PostgreSQL database
* Redis cache

---

### 4 Access the application

API:

```
http://localhost:8000
```

Swagger Docs:

```
http://localhost:8000/docs
```

---

### 5 Stop containers

```bash
docker compose down
```

---

# Running Without Docker (Local Development)

### 1 Create virtual environment

```bash
python -m venv env
source env/bin/activate
```

Windows:

```
env\Scripts\activate
```

---

### 2 Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3 Start PostgreSQL and Redis

Make sure the following services are running locally:

```
PostgreSQL
Redis
```

---

### 4 Configure `.env`

Example:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/jobboard
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your_secret_key
OPENAI_API_KEY=your_openai_key
```

---

### 5 Run database migrations

```bash
alembic upgrade head
```

---

### 6 Start FastAPI

Development:

```bash
uvicorn app.main:app --reload
```

Production:

```bash
gunicorn -k uvicorn.workers.UvicornWorker app.main:app
```

---

# API Endpoints

## Authentication

| Method | Endpoint           | Description             |
| ------ | ------------------ | ----------------------- |
| POST   | `/auth/register`   | Register new user       |
| POST   | `/auth/login/user` | Email/password login    |
| GET    | `/auth/login`      | Google OAuth login      |
| GET    | `/auth/callback`   | Google OAuth callback   |
| GET    | `/auth/protected`  | Test protected endpoint |

---

## Jobs & Applications

| Method | Endpoint               | Description         |
| ------ | ---------------------- | ------------------- |
| POST   | `/jobs/create`         | Create job          |
| GET    | `/jobs/all`            | List jobs           |
| POST   | `/applications/submit` | Apply for job       |
| GET    | `/applications/{id}`   | Application details |

---

## Reviews

| Method | Endpoint   | Description   |
| ------ | ---------- | ------------- |
| POST   | `/reviews` | Submit review |

---

# Database Migrations

Alembic manages schema changes.

Create migration:

```bash
alembic revision --autogenerate -m "Add table"
```

Apply migration:

```bash
alembic upgrade head
```

Rollback:

```bash
alembic downgrade -1
```

---

# Future Enhancements

* AI-powered job matching
* Real-time notifications using WebSockets
* Email notification system
* Admin analytics dashboard
* Multi-language support
* Video interview scheduling
* Skills testing platform

---

# Author

**Joseph Njoroge**

Backend / Full-Stack Software Engineer focused on building scalable backend systems and AI-powered platforms.

GitHub
[https://github.com/kimenyu](https://github.com/kimenyu)

Email
[njorogekimenyu@gmail.com](mailto:njorogekimenyu@gmail.com)

---

# License

MIT License

---

# Contributing

Contributions are welcome.

1 Fork the repository
2 Create a feature branch

```
git checkout -b feature/new-feature
```

3 Commit changes

```
git commit -m "Add new feature"
```

4 Push branch

```
git push origin feature/new-feature
```

5 Open Pull Request

```

---

If you'd like, I can also help you **improve this README to a “senior-level GitHub project” standard** (with badges, architecture diagram, API examples, screenshots, and deployment instructions).
```
