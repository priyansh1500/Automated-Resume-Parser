# app/parser.py
#
# This file handles all resume text extraction and NLP parsing logic.
# - Stage 3: Uses PDFPlumber to extract raw text from PDFs.
# - Stage 4: Uses spaCy and Regex to parse structured details
#            (name, email, phone, skills, education, experience).

import re
import pdfplumber
import spacy

# Load the spaCy English language model once when the module is imported
try:
    nlp = spacy.load('en_core_web_sm')
except Exception:
    nlp = None


def extract_text_from_pdf(filepath):
    """
    Opens a PDF file and extracts all readable text from it using PDFPlumber.
    """
    extracted_pages = []

    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_pages.append(page_text.strip())

    full_text = "\n\n--- Page Break ---\n\n".join(extracted_pages)
    return full_text


def extract_email(text):
    """
    Extracts the first email address found in the text using Regular Expressions.
    """
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_pattern, text)
    return match.group(0) if match else "Not found"


def extract_phone(text):
    """
    Extracts the first phone number found in the text using Regular Expressions.
    Matches various formats (+91 9876543210, (123) 456-7890, 9876543210, etc.)
    """
    phone_pattern = r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}'
    matches = re.findall(phone_pattern, text)
    
    for match in matches:
        digits_only = re.sub(r'\D', '', match)
        if 10 <= len(digits_only) <= 13:
            return match.strip()
            
    return "Not found"


def extract_name(text):
    """
    Extracts the candidate's name using spaCy Named Entity Recognition (NER)
    and fallback heuristic rules.
    """
    lines = [line.strip() for line in text.split('\n') if line.strip() and not line.startswith("--- Page Break ---")]

    if not lines:
        return "Not found"

    # Strategy 1: Check early individual lines using spaCy for a PERSON entity
    for line in lines[:5]:
        if "@" in line or re.search(r'\d{7,}', line):
            continue
        if any(keyword in line.lower() for keyword in ["resume", "curriculum", "cv", "profile", "contact"]):
            continue
            
        if nlp:
            doc = nlp(line)
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    clean_ent = ent.text.strip()
                    if 1 <= len(clean_ent.split()) <= 4:
                        return clean_ent

    # Strategy 2: Fallback to the first clean non-header line
    for line in lines[:3]:
        if any(keyword in line.lower() for keyword in ["resume", "curriculum vitae", "cv", "profile", "summary", "contact"]):
            continue
        if not re.search(r'[\d@#$:=]', line) and 1 <= len(line.split()) <= 4:
            return line

    return "Not found"


def extract_skills(text):
    """
    Extracts technical and soft skills by matching against a curated skills dictionary.
    """
    SKILLS_DATABASE = [
        # Programming & Web
        "Python", "Java", "C++", "C#", "C", "JavaScript", "TypeScript", "HTML", "CSS",
        "PHP", "Ruby", "Go", "Rust", "SQL", "R", "MATLAB", "Swift", "Kotlin",
        
        # Frameworks & Libraries
        "Flask", "Django", "FastAPI", "React", "Node.js", "Angular", "Vue.js",
        "Express", "Bootstrap", "Tailwind", "jQuery", "Spring", "ASP.NET",
        
        # AI, Data Science & ML
        "Machine Learning", "Data Science", "Artificial Intelligence", "Deep Learning",
        "NLP", "Natural Language Processing", "spaCy", "NLTK", "OpenCV",
        "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "Keras", "PyTorch",
        "Data Analysis", "Data Visualization", "Power BI", "Tableau", "Excel",
        
        # Databases & Tools
        "PostgreSQL", "MySQL", "SQLite", "MongoDB", "Redis", "Oracle",
        "Git", "GitHub", "GitLab", "Docker", "Kubernetes", "Linux", "Unix",
        "AWS", "Azure", "GCP", "Google Cloud", "VS Code", "Postman",
        
        # Soft Skills
        "Communication", "Leadership", "Teamwork", "Problem Solving",
        "Time Management", "Critical Thinking", "Adaptability", "Project Management"
    ]

    found_skills = []
    text_lower = text.lower()

    for skill in SKILLS_DATABASE:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return found_skills if found_skills else ["No skills identified"]


def extract_education(text):
    """
    Extracts lines mentioning education, degrees, or academic institutions.
    """
    DEGREE_KEYWORDS = [
        "b.sc", "bsc", "b.tech", "btech", "b.e", "be", "bachelor", "bachelors",
        "m.sc", "msc", "m.tech", "mtech", "m.e", "me", "master", "masters",
        "ph.d", "phd", "doctorate", "diploma", "degree",
        "university", "college", "institute", "school", "academy"
    ]

    lines = text.split('\n')
    education_lines = []

    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue
        line_lower = line_str.lower()
        if any(keyword in line_lower for keyword in DEGREE_KEYWORDS):
            if len(line_str) < 120 and line_str not in education_lines:
                education_lines.append(line_str)

    return education_lines if education_lines else ["Education details not explicitly found"]


def extract_experience(text):
    """
    Extracts lines mentioning work experience, job titles, or internships.
    """
    EXPERIENCE_KEYWORDS = [
        "intern", "internship", "developer", "engineer", "assistant",
        "manager", "analyst", "consultant", "specialist", "associate",
        "trainee", "software engineer", "data analyst", "web developer",
        "experience", "work history", "employment", "responsibilities"
    ]

    lines = text.split('\n')
    experience_lines = []

    for line in lines:
        line_str = line.strip()
        if not line_str:
            continue
        line_lower = line_str.lower()
        if any(keyword in line_lower for keyword in EXPERIENCE_KEYWORDS):
            if len(line_str) < 120 and line_str not in experience_lines:
                experience_lines.append(line_str)

    return experience_lines if experience_lines else ["Work experience details not explicitly found"]


def parse_resume_text(text):
    """
    Master function that parses raw extracted resume text into a structured dictionary.

    Returns:
      dict: Structured candidate profile containing name, email, phone,
            skills, education, and experience.
    """
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text)
    }
