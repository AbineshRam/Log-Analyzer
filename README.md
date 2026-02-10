# AI Log Analyzer

AI Log Analyzer is a **FastAPI-based web application** that automatically analyzes job failure logs using **rule-based logic and Large Language Models (LLMs)** like **OpenAI GPT** or **Ollama LLaMA**. It supports logs from local files or S3 buckets, classifies failures, explains the root cause, and provides remediation suggestions.

This project demonstrates **Python backend development, AI integration, MongoDB storage, and a web GUI**, making it a strong portfolio piece for DevOps, Backend, or AI-focused roles.

---

## 🏗 Features

- **Automated Failure Classification**
  - Rule-based detection for Database, Memory, File System, Network, Application errors
  - Confidence scoring

- **LLM-based Explanation**
  - Integrates OpenAI GPT or local Ollama LLaMA
  - Explains why a job failed and suggests remediation steps

- **Log Sources**
  - Local log files
  - AWS S3 buckets

- **Web GUI**
  - Paste stdout/stderr logs and exit code
  - Get real-time AI-powered analysis

- **Persistence**
  - MongoDB for storing job logs and AI analysis results
  - Allows historical log analysis and summaries

- **Background Processing**
  - Optional Celery + Redis integration for asynchronous log analysis

- **Summarization**
  - Combine multiple job failures and get a single AI-generated summary

---

## 📁 Folder Structure

Log Analyzer/  
├─ app/  
│ ├─ ai/ # AI logic (rules, LLM, engine, summarizer)  
│ ├─ api/ # FastAPI routes  
│ ├─ core/ # Configuration  
│ ├─ db/ # MongoDB models & connection  
│ ├─ schemas/ # Pydantic schemas  
│ ├─ utils/ # Helpers (log parsing, S3 reader, file watcher)  
│ └─ main.py # FastAPI entrypoint  
├─ gui/ # Frontend files (HTML/CSS/JS)  
├─ tests/ # Unit tests  
├─ requirements.txt  
└─ README.md


---

## ⚡ Tech Stack

- **Backend:** FastAPI, Python 3.11+
- **Database:** MongoDB
- **AI:** OpenAI GPT or Ollama LLaMA
- **File Handling:** Watchdog, Boto3 (for S3)
- **Frontend:** HTML, CSS, JavaScript
- **Testing:** Pytest
- **Optional:** Celery + Redis for async tasks

---

## 🚀 Setup & Installation

1. Clone this repo:

2. Create virtual environment & install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate       # Linux/Mac
.venv\Scripts\activate          # Windows

pip install --upgrade pip
pip install -r requirements.txt
```
3. Set environment variables:
````bash
export LLM_PROVIDER="openai"             # or "ollama"
export OPENAI_API_KEY="your_openai_key"
export OPENAI_MODEL="gpt-4o-mini"
export OLLAMA_BASE_URL="http://localhost:11434"
export OLLAMA_MODEL="llama3"
export CONFIDENCE_THRESHOLD=80
export MONGO_URI="mongodb://localhost:27017"

````
4. Start FastAPI server:
````bash
uvicorn app.main:app --reload
````
5. Open GUI in browser:

````bash
http://127.0.0.1:8000/gui/index.html
````
---

## 🛠 Usage

### Analyze a Single Job

- Enter `stderr`, `stdout`, and `exit_code` in the GUI
    
- Click **Analyze Failure**
    
- Get **category, confidence, and AI explanation**
    

### Summarize Multiple Failures

- API endpoint `/summarize` accepts a list of failures
    
- Returns combined AI-generated summary
Summarize Multiple Failures

API endpoint /summarize accepts a list of failures

Returns combined AI-generated summary

---
## 🧠 AI Reasoning Flow

1. **Rule-based classification**: Quick checks for common errors
    
2. **Confidence scoring**: Determines if LLM is required
    
3. **LLM explanation**: OpenAI or Ollama generates:
    
    - Why the job failed
        
    - Root cause
        
    - Remediation steps
        

---

## 📝 Example API Requests

**Analyze Single Job**
````bash
`POST /analyze Content-Type: application/json  {   "stderr": "ORA-12541: TNS:no listener",   "stdout": "",   "exit_code": 1 }`
````
**Response**

````bash
`{   "category": "Database Error",   "confidence": 85,   "exit_code": 1,   "result": {     "analysis": "The job failed due to database connectivity issues...",     "llm_used": true   } }`
````
---

## ✅ Future Improvements

- File upload support in GUI
    
- Async background processing for large logs
    
- Enhanced embeddings & semantic search for historical failures
    
- Docker + docker-compose for one-command deployment
    
- React frontend for richer UI
---
## 📜 License

MIT License © 2026