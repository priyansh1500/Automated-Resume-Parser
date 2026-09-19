# 📄 Automated Resume Parser

A full-stack AI application built with **Python**, **Flask**, **PDFPlumber**, **spaCy NLP**, and **PostgreSQL**. 

This application automatically extracts, structures, and stores candidate information from uploaded PDF resumes — built as a BSc Artificial Intelligence and Data Science internship project.

---

## 🎯 Internship Objectives & Overview

The objective of this project is to build an end-to-end Automated Resume Parser that converts unstructured PDF resumes into structured, searchable candidate data.

### Key Capabilities:
* 📤 **PDF Upload**: Upload resume files in `.pdf` format.
* 📖 **Text Extraction**: Uses **PDFPlumber** to read and extract text page by page.
* 🧠 **NLP & Regex Extraction**: Uses **spaCy Named Entity Recognition (`PERSON`)** and **Regular Expressions** to extract candidate Name, Email, Phone Number, Skills, Education, and Work Experience.
* 🗄️ **Persistent Storage**: Stores parsed candidate records permanently in a **PostgreSQL** database via **Flask-SQLAlchemy**.
* 👥 **Recruiter Dashboard**: Browse all parsed candidates in a dashboard view (`/candidates`) and view individual candidate profiles (`/candidate/<id>`).
* 🔒 **Secure Configuration**: Uses local `.env` files via `python-dotenv` so database credentials and passwords are never hardcoded or committed to version control.

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Backend Framework** | Python 3.13 + Flask 3.1 | Web application server and API routing |
| **PDF Extraction** | PDFPlumber | Extracts raw text from PDF files |
| **NLP Engine** | spaCy (`en_core_web_sm`) | Named Entity Recognition (NER) for candidate names |
| **Pattern Matching** | Python Regex (`re`) | Extracts email addresses, phone numbers, and skills |
| **Database** | PostgreSQL 18 | Permanent relational database storage |
| **Database ORM** | Flask-SQLAlchemy + `psycopg2-binary` | Python object-relational mapping |
| **Environment Mgmt** | `python-dotenv` | Securely loads credentials from `.env` |
| **Frontend** | HTML5, CSS3, Vanilla JS | Clean, responsive user interface |

---

## 🗂️ Project Structure

```
Automated_Resume_Parser/
│
├── app/                        ← Main Flask application package
│   ├── __init__.py             ← Initializes Flask app & SQLAlchemy database
│   ├── routes.py               ← App routes (/ , /candidates, /candidate/<id>, error handlers)
│   ├── parser.py               ← Text extraction (PDFPlumber) & NLP parsing (spaCy)
│   ├── models.py               ← Candidate SQLAlchemy database model
│   │
│   ├── templates/              ← HTML templates
│   │   ├── index.html          ← Upload page & navbar
│   │   ├── results.html        ← Parsed resume profile view
│   │   ├── candidates.html     ← Candidates dashboard grid
│   │   └── candidate_detail.html ← Individual candidate record view
│   │
│   └── static/                 ← Frontend assets
│       ├── css/
│       │   └── style.css       ← Styling & responsive design
│       └── js/
│           └── main.js          ← File upload UX & loading state
│
├── uploads/                    ← Uploaded resume PDFs (temporary storage)
├── venv/                       ← Isolated Python virtual environment
├── .env                        ← Private local environment variables (Git-ignored)
├── .gitignore                  ← Prevents committing .env, venv/, and uploads/
├── config.py                   ← Application configuration class
├── run.py                      ← Application entry point (python run.py)
├── requirements.txt            ← Python package dependencies list
└── README.md                   ← Project documentation
```

---

## 🚀 Completed Development Roadmap

* ✅ **Stage 1 — Project Setup**: Scaffolding folder structure, placeholder files, and README.
* ✅ **Stage 2 — Basic Flask Web Application**: Minimal Flask application, homepage routing, HTML/CSS layout.
* ✅ **Stage 3 — PDF Upload & Text Extraction**: Integrated PDFPlumber for reading PDF text, error validation, and text display.
* ✅ **Stage 4 — NLP & Entity Extraction**: Integrated spaCy (`en_core_web_sm`) and Regex for Name, Email, Phone, Skills, Education, and Experience.
* ✅ **Stage 5 — PostgreSQL Database Integration**: Defined SQLAlchemy `Candidate` model, set up secure `.env` credentials, and saved parsed resumes to PostgreSQL.
* ✅ **Stage 6 — Candidate Dashboard & Profile View**: Built `/candidates` dashboard grid and `/candidate/<id>` profile view routes.
* ✅ **Stage 7 — Custom Error Handling & Documentation**: Added custom HTTP 404, 413, and 500 error handlers and finalized complete documentation.

---

## ⚙️ Setup & Installation Guide

### 1. Environment Setup

Clone or open the project folder and create a Python virtual environment:

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt

# Download spaCy English NLP model
python -m spacy download en_core_web_sm
```

---

### 2. PostgreSQL & `.env` Configuration

1. Install PostgreSQL on your computer (Port `5432`).
2. Create a local `.env` file in the project root:
   ```env
   DATABASE_URL=postgresql://postgres:YOUR_POSTGRES_PASSWORD@localhost:5432/resume_parser_db
   SECRET_KEY=dev-secret-key-change-in-production
   ```
3. Replace `YOUR_POSTGRES_PASSWORD` with your local PostgreSQL password.

*(The database `resume_parser_db` and candidate table will be created automatically when you start the app).*

---

## ▶️ Running the Application

Ensure your virtual environment is active, then run:

```powershell
python run.py
```

Open your browser and visit:
👉 **`http://127.0.0.1:5000`**

---

## 🧪 Testing the Application

1. **Upload Resume**: Go to `http://127.0.0.1:5000`, choose a PDF resume, and click **Upload Resume**.
2. **Parsed Profile View**: Inspect the extracted Candidate Name, Email, Phone, Skill Badges, Education, Experience, and raw PDF text. Note the **Saved Candidate ID: #1**.
3. **Candidates Dashboard**: Click **Candidates Dashboard** in the navigation bar (`http://127.0.0.1:5000/candidates`) to view all saved candidates.
4. **Candidate Profile View**: Click **View Full Profile →** on any candidate card to view their database record.

---

## 👨‍💻 Author

**BSc Artificial Intelligence and Data Science Student**  
Automated Resume Parser — Internship Project 2026
