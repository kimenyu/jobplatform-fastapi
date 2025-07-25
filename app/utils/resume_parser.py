import os
import re
from typing import Dict, List, Optional
import PyPDF2
import docx
from fastapi import HTTPException


class ResumeParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.text = ""

    def extract_text(self) -> str:
        """Extract text from PDF or DOCX files using only PyPDF2 and python-docx"""
        try:
            if self.file_path.lower().endswith('.pdf'):
                return self._extract_from_pdf_simple()
            elif self.file_path.lower().endswith(('.docx', '.doc')):
                return self._extract_from_docx()
            else:
                raise ValueError("Unsupported file format")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to extract text: {str(e)}")

    def _extract_from_pdf_simple(self) -> str:
        """Extract text from PDF using only PyPDF2"""
        text = ""
        try:
            with open(self.file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to read PDF: {str(e)}")

        return text

    def _extract_from_docx(self) -> str:
        """Extract text from DOCX files"""
        try:
            doc = docx.Document(self.file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to read DOCX: {str(e)}")

    def extract_emails(self, text: str) -> List[str]:
        """Extract email addresses from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(email_pattern, text)

    def extract_phone_numbers(self, text: str) -> List[str]:
        """Extract phone numbers from text"""
        phone_patterns = [
            r'\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}',
            r'\+?[0-9]{1,3}[-.\s]?[0-9]{3,4}[-.\s]?[0-9]{3,4}[-.\s]?[0-9]{3,4}'
        ]
        phones = []
        for pattern in phone_patterns:
            phones.extend(re.findall(pattern, text))
        return phones

    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from any field using multiple approaches"""

        # Predefined skills from various fields
        skill_categories = {
            'tech': [
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby',
                'react', 'vue.js', 'angular', 'node.js', 'express', 'django', 'flask',
                'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'git', 'docker', 'aws'
            ],
            'business': [
                'project management', 'leadership', 'excel', 'powerpoint', 'accounting',
                'financial analysis', 'budgeting', 'strategic planning'
            ],
            'marketing': [
                'digital marketing', 'social media', 'seo', 'content marketing', 'analytics'
            ],
            'general': [
                'communication', 'problem solving', 'teamwork', 'microsoft office'
            ]
        }

        # Flatten all skills
        all_skills = []
        for category_skills in skill_categories.values():
            all_skills.extend(category_skills)

        # Find skills in text
        found_skills = []
        text_lower = text.lower()

        for skill in all_skills:
            if skill.lower() in text_lower:
                found_skills.append(skill)

        # Extract from skills sections
        skills_patterns = [
            r'(?:TECHNICAL\s+)?SKILLS?[:\s]*\n(.*?)(?:\n[A-Z][A-Z\s]+:|$)',
            r'(?:CORE\s+)?COMPETENCIES[:\s]*\n(.*?)(?:\n[A-Z][A-Z\s]+:|$)'
        ]

        for pattern in skills_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                skill_items = re.split(r'[,;•\-\n\|]', match)
                for item in skill_items:
                    cleaned = re.sub(r'^[-•\s]+', '', item.strip())
                    if cleaned and len(cleaned) > 2 and len(cleaned) < 50:
                        found_skills.append(cleaned)

        found_skills = list(set([skill.strip() for skill in found_skills if skill.strip()]))

        if not found_skills:
            return ["No specific skills identified - please review manually"]

        return found_skills

    def extract_education(self, text: str) -> List[str]:
        """Extract education information"""
        education_info = []

        # Look for degree patterns
        degree_patterns = [
            r'bachelor[\'s]*\s+(?:degree\s+)?(?:of\s+|in\s+)?([^.\n]+)',
            r'master[\'s]*\s+(?:degree\s+)?(?:of\s+|in\s+)?([^.\n]+)',
            r'([A-Z][a-zA-Z\s]+)\s+(?:University|College)',
            r'ALX\s+Software\s+Engineering\s+Program'
        ]

        for pattern in degree_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0] if match[0] else match[1]
                education_info.append(match.strip())

        return list(set([edu for edu in education_info if edu and len(edu.strip()) > 2]))

    def get_extracted_data(self) -> Dict:
        """Main method to extract all data from resume"""
        try:
            # Extract text
            self.text = self.extract_text()

            if not self.text.strip():
                return {"error": "No text could be extracted from the resume"}

            # Extract information
            emails = self.extract_emails(self.text)
            phones = self.extract_phone_numbers(self.text)
            skills = self.extract_skills(self.text)
            education = self.extract_education(self.text)

            # Extract name (simple approach)
            lines = self.text.split('\n')
            name = ""
            for line in lines[:5]:
                line = line.strip()
                if line and len(line.split()) <= 4 and len(line) > 2:
                    if not any(char.isdigit() for char in line) and '@' not in line:
                        name = line
                        break

            return {
                "name": name,
                "email": emails[0] if emails else None,
                "mobile_number": phones[0] if phones else None,
                "skills": skills,
                "education": education,
                "extracted_text": self.text[:1000] + "..." if len(self.text) > 1000 else self.text,
                "no_of_pages": len(self.text) // 3000 + 1
            }

        except Exception as e:
            return {"error": f"Failed to parse resume: {str(e)}"}
