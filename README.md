#  JobPlatformFastAPI

An intelligent, full-featured job platform built with **FastAPI** that connects **applicants** and **employers**, powered by AI-driven resume parsing using **OpenAI's GPT**. It features robust role-based authentication, job posting, application management, resume analysis, notifications, and user reviews.

---
## 🚀 Features

###  Core Functionality

-  **Authentication & Authorization**
  - Secure JWT-based login & registration
  - Role-specific access (Admin, Employer, Applicant)

-  **Job Management**
  - Employers can create, update, delete, and manage jobs
  - Applicants can browse and apply to jobs

-  **Resume Upload & Parsing**
  - Applicants upload resumes in `.docx`/`.pdf`
  - Uses **OpenAI** to extract skills, experience, education, etc.

-  **Application Tracking**
  - Admins and Employers can view all applications
  - Applicants can track and delete their own submissions

-  **Notifications**
  - System-generated notifications for application events

-  **Reviews**
  - Users can leave reviews for each other (1–5 star rating)

-  **Resume Intelligence(hybrid parsing)**
  - Automatically parses resume content using AI for analysis and searchability
  - Parse resume using PyPDF2/python-docx

---

##  Powered by AI

This platform integrates **OpenAI's GPT API** to parse and understand resumes using natural language understanding. Traditional keyword extraction is replaced with contextual insights such as:

- Experience level
- Skill proficiency
- Career summary
- Education and achievements

---

##  Tech Stack

| Layer         | Technology        |
| ------------- | ----------------- |
| Backend       | FastAPI (Python)  |
| ORM           | SQLAlchemy        |
| Database      | PostgreSQL (or SQLite for dev) |
| Auth          | JWT + OAuth2      |
| AI Integration| OpenAI (GPT-4)    |
| File Uploads  | FastAPI UploadFile |
| Resume Parsing| GPT + `python-docx`/`pdfplumber` |
| Container     | Docker  |

---

##  Project Structure

```
app/
├── api/                # Auth routes
├── core/               # Security & dependencies
├── database/           # Session and base model
├── models/             # SQLAlchemy models
├── repository/         # Business logic
├── routes/             # Route definitions
├── schemas/            # Pydantic schemas
├── uploads/            # Uploaded resumes
├── main.py             # App entry point
└── requirements.txt
```

---

##  API Endpoints

Sample endpoints:

- `POST /auth/register` – Register a new user
- `POST /auth/login` – Authenticate and receive token
- `POST /jobs/create` – Employer creates job (auth required)
- `GET /jobs/all` – List all jobs
- `POST /applications/create` – Apply for job (upload resume)
- `GET /applications/{id}` – View application detail
- `POST /reviews/` – Submit review

---

##  Installation

```bash
git clone https://github.com/kimenyu/jobplatform-fastapi.git
cd jobplatformfastapi
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_key
SECRET_KEY=your_jwt_secret
```

Run the application:

```bash
uvicorn app.main:app --reload
```

---

##  Sample Resume Parsing (AI)

Sample OpenAI resume output (for uploaded file):

```json
{
  "name": "John Doe",
  "skills": ["Python", "FastAPI", "PostgreSQL"],
  "experience": "3 years as a backend developer at Acme Corp",
  "education": "BSc in Computer Science",
  "summary": "Backend engineer with a focus on scalable systems."
}
```

---

##  Future Enhancements

- Advanced job matching algorithm using AI
- Recommendation engine for skills/jobs
- Email notifications for job updates
- Admin dashboard

---

##  Author

**Joseph Njoroge**  
Fullstack Software Developer – Passionate about backend systems, AI-powered applications, and solving real-world problems with code.

> Inspired by innovation. Built with excellence. Driven by learning.

---

##  License

MIT License – feel free to build upon this project and improve it!
