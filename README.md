### FormPilot AI — Agentic Document-to-Form Automation Platform

FormPilot AI is an AI-powered automation system that extracts information from documents such as resumes, academic certificates, and identity documents, and uses the extracted data to automatically fill web forms.

**Key Features:**
- Extracts and classifies information from PDF, image, and text documents.
- Creates a unified user profile and detects conflicting information.
- Automatically analyzes web forms and maps profile data to the appropriate fields.
- Uses **LangGraph** for workflow orchestration and **Playwright** for browser automation.
- Includes human approval before executing form filling.
- Verifies entered data and maintains an audit trail of the process.

**Tech Stack:** Python, FastAPI, LangGraph, Playwright, React, SQLAlchemy, PyMuPDF, Tesseract OCR, Docker, and PostgreSQL/SQLite.

**Impact:** Reduces repetitive manual form-filling work while improving accuracy, transparency, and user control.
how to run this??
Terminal 1: backend

bpython -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
playwright install chromium
Copy-Item ..\.env.example .env
(Get-Content .env) -replace '\./storage','../storage' | Set-Content .env
New-Item -ItemType Directory -Force ..\storage | Out-Null
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Demo form (new PowerShell window, in formpilot-ai\demo_form)
powershell
python -m http.server 3000
Frontend (another new window, in formpilot-ai\frontend)
powershell
npm install
npm run dev

Then open http://localhost:5173.
