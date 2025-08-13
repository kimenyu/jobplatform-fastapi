# JobPlatformFastAPI

An intelligent, full-featured job platform built with **FastAPI** that connects **applicants** and **employers**, powered by AI-driven resume parsing using **OpenAI's GPT**. It features robust role-based authentication with **Google OAuth**, job posting, application management, resume analysis, notifications, and user reviews.

---

## Features

### Authentication & Authorization
- **Multiple Login Options:**
  - Traditional JWT-based login & registration
  - **Google OAuth 2.0 integration** for seamless sign-in
  - Automatic user creation for new Google users
- **Role-specific access** (Admin, Employer, Applicant)
- **Secure token-based authentication**

### Job Management
- Employers can create, update, delete, and manage jobs
- Applicants can browse and apply to jobs
- Advanced job filtering and search capabilities

### Resume Upload & AI Parsing
- Applicants upload resumes in `.docx`/`.pdf` formats
- **Hybrid parsing approach:**
  - Uses **OpenAI GPT** for intelligent content extraction
  - Traditional parsing with PyPDF2/python-docx as fallback
- Extracts skills, experience, education, and career insights

### Application Tracking
- Admins and Employers can view all applications
- Applicants can track and manage their submissions
- Real-time application status updates

### Notifications
- System-generated notifications for application events
- Email integration for important updates

### Reviews & Ratings
- Users can leave reviews for each other (1–5 star rating)
- Builds trust and transparency in the platform

###  Database Management
- **Alembic migrations** for seamless database schema updates
- Robust data modeling with SQLAlchemy ORM

---

## Powered by AI

This platform integrates **OpenAI's GPT API** to parse and understand resumes using natural language understanding. Traditional keyword extraction is replaced with contextual insights such as:

- Experience level assessment
- Skill proficiency evaluation
- Career summary generation
- Education and achievements analysis
- Job-skill matching recommendations

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | FastAPI (Python) |
| **ORM** | SQLAlchemy |
| **Database** | PostgreSQL (SQLite for dev) |
| **Migrations** | Alembic |
| **Authentication** | JWT + OAuth2 + Google OAuth |
| **AI Integration** | OpenAI (GPT-4) |
| **File Processing** | FastAPI UploadFile |
| **Resume Parsing** | GPT + `python-docx`/`pdfplumber` |
| **Container** | Docker |

---

## Project Structure

```
app/
├── api/                # Authentication routes
├── core/               # Security & dependencies
├── database/           # Database session and base models
├── models/             # SQLAlchemy models
├── repository/         # Business logic layer
├── routes/             # API route definitions
├── schemas/            # Pydantic schemas
├── uploads/            # Uploaded resume files
├── alembic/            # Database migration files
├── alembic.ini         # Alembic configuration
├── main.py             # Application entry point
└── requirements.txt    # Python dependencies
```

---

## API Endpoints

### Authentication
- `POST /auth/register` – Traditional user registration
- `POST /auth/login/user` – Email/password authentication
- `GET /auth/login` – **Google OAuth login redirect**
- `GET /auth/callback` – **Google OAuth callback handler**
- `GET /auth/protected` – Test protected endpoint

### Jobs & Applications
- `POST /jobs/create` – Employer creates job (auth required)
- `GET /jobs/all` – List all available jobs
- `POST /applications/submit` – Apply for job (with resume upload)
- `GET /applications/{id}` – View application details

### Reviews
- `POST /reviews/` – Submit user review

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/kimenyu/jobplatform-fastapi.git
cd jobplatform-fastapi
```

### 2. Set Up Virtual Environment
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost/jobplatform
# or for SQLite: DATABASE_URL=sqlite:///./app.db

# JWT Security
SECRET_KEY=your_super_secure_jwt_secret_key_here

# OpenAI Integration
OPENAI_API_KEY=your_openai_api_key

# Google OAuth Configuration
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
```

### 4. Google OAuth Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add `http://localhost:8000/auth/callback` to authorized redirect URIs

### 5. Database Setup
```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 6. Run the Application
```bash
# Development
uvicorn app.main:app --reload

# Production
gunicorn -c app/config/gunicorn_conf.py app.main:app
```

The API will be available at: `http://localhost:8000`
Interactive docs at: `http://localhost:8000/docs`

---

## Google OAuth Flow

### How it works:
1. **User initiates login:** `GET /auth/login`
2. **Redirects to Google:** User authenticates with Google
3. **Google callback:** `GET /auth/callback` receives user data
4. **User creation/login:** Automatically creates new users or logs in existing ones
5. **JWT token:** Returns access token for API authentication

### Sample OAuth Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 123,
    "email": "user@gmail.com",
    "name": "John Doe",
    "profile_picture": "https://lh3.googleusercontent.com/...",
    "role": "applicant"
  }
}
```

---

## AI Resume Parsing Example

Sample OpenAI resume analysis output:

```json
{
  "name": "John Doe",
  "skills": ["Python", "FastAPI", "PostgreSQL", "Machine Learning"],
  "experience": "5 years as a Senior Backend Developer at Tech Corp",
  "education": "MSc in Computer Science, Stanford University",
  "summary": "Experienced backend engineer specializing in scalable APIs and AI integration.",
  "experience_level": "Senior",
  "key_achievements": [
    "Led development of microservices architecture",
    "Improved API performance by 300%"
  ]
}
```

---

## Database Migrations

Using Alembic for database schema management:

```bash
# Create a new migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback to previous version
alembic downgrade -1

# Check current migration status
alembic current
```

---

## Future Enhancements

- [ ] **Advanced AI matching** algorithm for job-candidate pairing
- [ ] **Real-time notifications** with WebSocket support
- [ ] **Email notification system** for job updates
- [ ] **Advanced admin dashboard** with analytics
- [ ] **Multi-language support**
- [ ] **Mobile app integration**
- [ ] **Video interview scheduling**
- [ ] **Skills assessment tests**

---

##  Author

**Joseph Njoroge**  
Full-stack Software Developer – Passionate about backend systems, AI-powered applications, and solving real-world problems with innovative technology.

> "Building the future of recruitment with AI and seamless user experiences."

### Connect with me:
- GitHub: [@kimenyu](https://github.com/kimenyu)
- Email: [njorogekimenyu@gmail.com](mailto:njorogekimenyu@gmail.com)

---

## License

MIT License – Feel free to build upon this project and make it even better!

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

