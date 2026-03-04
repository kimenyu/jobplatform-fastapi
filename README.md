# JobPlatformFastAPI

> An intelligent, full-featured job platform built with **FastAPI** that connects **applicants** and **employers**, powered by AI-driven resume parsing using **OpenAI's GPT**.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Run with Docker (Recommended)](#run-with-docker-recommended)
  - [Run Locally (Without Docker)](#run-locally-without-docker)
- [API Endpoints](#api-endpoints)
- [Database Migrations](#database-migrations)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [Author](#author)
- [License](#license)

---

## Features

### Authentication & Authorization

- JWT-based login & registration
- **Google OAuth 2.0** integration for seamless sign-in
- Automatic user creation for new Google users
- Role-based access control: **Admin**, **Employer**, **Applicant**

### Job Management

- Employers can create, update, delete, and manage job listings
- Applicants can browse and apply to jobs
- Advanced job filtering and search capabilities

### Resume Upload & AI Parsing

Applicants upload resumes in `.docx` or `.pdf` format. A hybrid parsing approach is used:

- **OpenAI GPT** for intelligent content extraction
- `python-docx` and `pdfplumber` as fallback parsers

Extracted insights include:

- Skills & experience
- Education & achievements
- Career summary
- Job–skill match recommendations

### Application Tracking

- Admins and employers can view and manage applications
- Applicants track submission status in real time

### Notifications

- System-generated notifications for application events
- Email integration for important updates

### Reviews & Ratings

Users can leave reviews (1–5 stars) to build transparency and trust.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python) |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Migrations | Alembic |
| Authentication | JWT + OAuth2 + Google OAuth |
| AI Integration | OpenAI GPT |
| Resume Parsing | GPT + python-docx / pdfplumber |
| Containerization | Docker + Docker Compose |
| Caching / Rate Limiting | Redis |

---

## Project Structure

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
```

---

## Getting Started

### Run with Docker (Recommended)

Docker automatically starts the FastAPI server, PostgreSQL, and Redis.

**1. Clone the repository**

```bash
git clone https://github.com/kimenyu/jobplatform-fastapi.git
cd jobplatform-fastapi
```

**2. Create a `.env` file**

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

**3. Build and start the containers**

```bash
docker compose up --build
```

**4. Access the application**

| Service | URL |
|---|---|
| API | http://localhost:8000 |
| Swagger Docs | http://localhost:8000/docs |

**5. Stop containers**

```bash
docker compose down
```

---

### Run Locally (Without Docker)


**1. Create and activate a virtual environment**

```bash
python -m venv env
source env/bin/activate       # macOS/Linux
env\Scripts\activate          # Windows
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Start PostgreSQL and Redis locally**

Ensure both services are running on your machine before proceeding.

**4. Configure `.env`**

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/jobboard
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your_secret_key
OPENAI_API_KEY=your_openai_key
```

**5. Run database migrations**

```bash
alembic upgrade head
```

**6. Start the server**

```bash
# Development
uvicorn app.main:app --reload

# Production
gunicorn -k uvicorn.workers.UvicornWorker app.main:app
```

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login/user` | Email/password login |
| GET | `/auth/login` | Initiate Google OAuth login |
| GET | `/auth/callback` | Google OAuth callback |
| GET | `/auth/protected` | Test protected endpoint |

### Jobs & Applications

| Method | Endpoint | Description |
|---|---|---|
| POST | `/jobs/create` | Create a job listing |
| GET | `/jobs/all` | List all jobs |
| POST | `/applications/submit` | Apply for a job |
| GET | `/applications/{id}` | Get application details |

### Reviews

| Method | Endpoint | Description |
|---|---|---|
| POST | `/reviews` | Submit a review |

---

## Database Migrations

Alembic manages all schema changes.

```bash
# Create a new migration
alembic revision --autogenerate -m "Add table"

# Apply all pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

---

## Future Enhancements

- AI-powered job matching
- Real-time notifications via WebSockets
- Email notification system
- Admin analytics dashboard
- Multi-language support
- Video interview scheduling
- Skills testing platform

---

## Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit your changes: `git commit -m "Add new feature"`
4. Push to the branch: `git push origin feature/new-feature`
5. Open a Pull Request

---

## Author

**Joseph Njoroge** — Backend / Full-Stack Software Engineer focused on scalable backend systems and AI-powered platforms.

- GitHub: [github.com/kimenyu](https://github.com/kimenyu)
- Email: [njorogekimenyu@gmail.com](mailto:njorogekimenyu@gmail.com)

---

## License

This project is licensed under the [MIT License](LICENSE).