from fastapi import HTTPException
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ResumeCreate(BaseModel):
    """Schema for creating a new resume"""
    file_path: str = Field(..., description="Path to the uploaded resume file")
    parsed_data: Optional[Dict[str, Any]] = Field(None, description="Parsed resume data")


class ResumeUpdate(BaseModel):
    """Schema for updating resume data"""
    parsed_data: Optional[Dict[str, Any]] = Field(None, description="Updated parsed resume data")


class ResumeResponse(BaseModel):
    """Schema for resume response"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    applicant_id: int
    file_path: str
    parsed_data: Optional[Dict[str, Any]] = None
    created_at: datetime

    # Computed fields from parsed_data
    @property
    def name(self) -> Optional[str]:
        return self.parsed_data.get('name') if self.parsed_data else None

    @property
    def email(self) -> Optional[str]:
        return self.parsed_data.get('email') if self.parsed_data else None

    @property
    def field(self) -> Optional[str]:
        return self.parsed_data.get('field') if self.parsed_data else None

    @property
    def skills(self) -> List[str]:
        return self.parsed_data.get('skills', []) if self.parsed_data else []

    @property
    def current_position(self) -> Optional[str]:
        return self.parsed_data.get('current_position') if self.parsed_data else None


class ResumeSearchFilters(BaseModel):
    """Schema for resume search filters"""
    field: Optional[str] = Field(None, description="Filter by professional field")
    skills: Optional[List[str]] = Field(None, description="Filter by skills (any match)")
    education: Optional[str] = Field(None, description="Filter by education keywords")
    experience_years_min: Optional[int] = Field(None, ge=0, description="Minimum years of experience")
    experience_years_max: Optional[int] = Field(None, ge=0, description="Maximum years of experience")
    current_position: Optional[str] = Field(None, description="Filter by current position")
    email_domain: Optional[str] = Field(None, description="Filter by email domain (e.g., @gmail.com)")


class ResumeSearchResponse(BaseModel):
    """Schema for resume search results"""
    resumes: List[ResumeResponse]
    total: int = Field(..., description="Total number of matching resumes")
    page: int = Field(..., description="Current page number")
    pages: int = Field(..., description="Total number of pages")


class ResumeAnalytics(BaseModel):
    """Schema for resume analytics"""
    total_resumes: int = Field(..., description="Total number of resumes in system")
    field_distribution: Dict[str, int] = Field(..., description="Distribution of professional fields")
    top_skills: Dict[str, int] = Field(..., description="Most common skills")
    resume_upload_trend: Dict[str, int] = Field(..., description="Upload trends")


# Schemas for parsed resume data structure
class ParsedExperience(BaseModel):
    """Schema for parsed experience data"""
    current_position: Optional[str] = None
    companies: List[str] = []
    positions: List[str] = []
    years_experience: Optional[int] = None


class ParsedResumeData(BaseModel):
    """Schema for structured parsed resume data"""
    name: Optional[str] = None
    email: Optional[str] = None
    mobile_number: Optional[str] = None
    field: str = "General/Other"
    skills: List[str] = []
    education: List[str] = []
    experience: Optional[ParsedExperience] = None
    current_position: Optional[str] = None
    years_experience: Optional[int] = None
    extracted_text: Optional[str] = None
    no_of_pages: Optional[int] = None
    parsing_error: Optional[str] = None


# Additional schemas for specific use cases
class ResumePreview(BaseModel):
    """Lightweight schema for resume previews"""
    id: int
    name: Optional[str] = None
    field: Optional[str] = None
    current_position: Optional[str] = None
    created_at: datetime


class ResumeStats(BaseModel):
    """Schema for individual resume statistics"""
    id: int
    applicant_id: int
    skills_count: int = 0
    education_count: int = 0
    has_contact_info: bool = False
    parsing_quality: str = "good"  # good, partial, failed


class BulkResumeOperation(BaseModel):
    """Schema for bulk operations on resumes"""
    resume_ids: List[int] = Field(..., min_items=1, max_items=50)
    operation: str = Field(..., pattern="^(delete|reparse|archive)$")


class ResumeUploadResponse(BaseModel):
    """Schema for resume upload response with additional metadata"""
    resume: ResumeResponse
    parsing_success: bool
    parsing_warnings: List[str] = []
    suggestions: List[str] = []


# Validation schemas
class ResumeValidation(BaseModel):
    """Schema for resume validation results"""
    is_valid: bool
    issues: List[str] = []
    suggestions: List[str] = []
    completeness_score: float = Field(..., ge=0.0, le=1.0)


class ResumeComparison(BaseModel):
    """Schema for comparing resumes"""
    resume1_id: int
    resume2_id: int
    similarity_score: float = Field(..., ge=0.0, le=1.0)
    common_skills: List[str] = []
    skill_differences: Dict[str, List[str]] = {}


class ResumeExport(BaseModel):
    """Schema for exporting resume data"""
    format: str = Field(..., pattern="^(csv|json|xlsx)$")
    fields: List[str] = Field(default=["name", "email", "field", "skills", "experience"])
    filters: Optional[ResumeSearchFilters] = None


class ResumeImport(BaseModel):
    """Schema for importing resume data"""
    file_format: str = Field(..., pattern="^(csv|json)$")
    mapping: Dict[str, str] = Field(..., description="Field mapping from import file to resume fields")
    validate_only: bool = Field(False, description="Only validate, don't import")


class ApplicationResponse(BaseModel):
    """Schema for returning application details"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    job_id: int
    applicant_id: int
    resume_file_path: str
    cover_letter: Optional[str] = None
    parsed_resume: Optional[ParsedResumeData] = None
    status: str
    created_at: datetime
    updated_at: datetime


class ApplicationDeleteResponse(BaseModel):
    message: str


class ApplicationSearchFilters(BaseModel):
    """Schema for application search filters"""
    job_id: Optional[int] = None
    applicant_id: Optional[int] = None
    status: Optional[str] = Field(None, pattern="^(pending|reviewed|rejected|accepted)$")
    field: Optional[str] = None
    skills: Optional[List[str]] = None


class ApplicationSearchResponse(BaseModel):
    """Schema for application search results"""
    applications: List[ApplicationResponse]
    total: int
    page: int
    pages: int


class ApplicationCreate(BaseModel):
    """Schema for creating an application"""
    job_id: int
    cover_letter: str
    resume_file_path: Optional[str] = None


class ApplicationUpdateStatus(BaseModel):
    """Schema for updating application status"""
    status: str = Field(..., pattern="^(pending|reviewed|rejected|accepted)$")
