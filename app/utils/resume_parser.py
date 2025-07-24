import os
import re
from typing import Dict, List, Optional
import PyPDF2
import docx
import pdfplumber
from fastapi import HTTPException


class ResumeParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.text = ""

    def extract_text(self) -> str:
        """Extract text from PDF or DOCX files"""
        try:
            if self.file_path.lower().endswith('.pdf'):
                return self._extract_from_pdf()
            elif self.file_path.lower().endswith(('.docx', '.doc')):
                return self._extract_from_docx()
            else:
                raise ValueError("Unsupported file format")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to extract text: {str(e)}")

    def _extract_from_pdf(self) -> str:
        """Extract text from PDF using pdfplumber (more reliable)"""
        text = ""
        try:
            with pdfplumber.open(self.file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception:
            # Fallback to PyPDF2
            with open(self.file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        return text

    def _extract_from_docx(self) -> str:
        """Extract text from DOCX files"""
        doc = docx.Document(self.file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text

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
        """Extract skills based on common keywords"""
        # Common technical skills - you can expand this list
        common_skills = [
            'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'mysql',
            'postgresql', 'mongodb', 'git', 'docker', 'kubernetes', 'aws', 'azure',
            'machine learning', 'data science', 'html', 'css', 'angular', 'vue.js',
            'django', 'flask', 'fastapi', 'spring boot', 'api', 'rest', 'graphql'
        ]

        found_skills = []
        text_lower = text.lower()

        for skill in common_skills:
            if skill.lower() in text_lower:
                found_skills.append(skill)

        return list(set(found_skills))  # Remove duplicates

    def extract_education(self, text: str) -> List[str]:
        """Extract education information"""
        education_keywords = [
            r'bachelor[\'s]*\s+(?:of\s+)?(?:science|arts|engineering|computer science|business)',
            r'master[\'s]*\s+(?:of\s+)?(?:science|arts|engineering|business)',
            r'phd|doctorate|doctoral',
            r'associate[\'s]*\s+degree',
            r'diploma',
            r'certification',
            r'university|college|institute'
        ]

        education = []
        for pattern in education_keywords:
            matches = re.findall(pattern, text, re.IGNORECASE)
            education.extend(matches)

        return education

    def get_extracted_data(self) -> Dict:
        """Main method to extract all data from resume"""
        try:
            # Extract text
            self.text = self.extract_text()

            if not self.text.strip():
                return {"error": "No text could be extracted from the resume"}

            # Extract various information
            emails = self.extract_emails(self.text)
            phones = self.extract_phone_numbers(self.text)
            skills = self.extract_skills(self.text)
            education = self.extract_education(self.text)

            # Extract name (simple approach - first line that looks like a name)
            lines = self.text.split('\n')
            name = ""
            for line in lines[:5]:  # Check first 5 lines
                line = line.strip()
                if line and len(line.split()) <= 4 and len(line) > 2:
                    # Simple heuristic: likely a name if it's short and at the beginning
                    if not any(char.isdigit() for char in line) and '@' not in line:
                        name = line
                        break

            return {
                "name": name,
                "email": emails[0] if emails else None,
                "mobile_number": phones[0] if phones else None,
                "skills": skills,
                "education": education,
                "total_experience": None,  # Would need more complex parsing
                "extracted_text": self.text[:1000] + "..." if len(self.text) > 1000 else self.text,
                "no_of_pages": len(self.text) // 3000 + 1  # Rough estimate
            }

        except Exception as e:
            return {"error": f"Failed to parse resume: {str(e)}"}