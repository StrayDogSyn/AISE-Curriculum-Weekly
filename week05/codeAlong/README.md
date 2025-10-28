# AISE26 — W5D2 In-Class Material
**Domain-Driven Design + Hexagonal (Ports & Adapters) — FastAPI**

This repo demonstrates clean boundaries with **domain / application / infrastructure** layers and a **FastAPI** HTTP adapter, plus unit tests for core logic.

---

## Prerequisites
- **Python** 3.10+ (3.11 recommended)
- **pip** (bundled with Python)
- **Git** and (Optional) **VS Code**


## Quickstart — Mac/Linux (bash/zsh)

# 1) Go to the project folder
cd /path/to/AISE26-W5D2-inclassmaterial

# 2) Create & activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3) Install dependencies
pip install -r requirements.txt

# 4) Run unit tests
pytest -q

# 5) Start the API (FastAPI + Uvicorn)
uvicorn app:app --reload
# → Open http://127.0.0.1:8000/docs (Swagger UI)

## Quickstart — Windows (PowerShell)

# 1) Go to the project folder
cd C:\path\to\AISE26-W5D2-inclassmaterial

# 2) Create & activate virtual environment
python -m venv .venv
.venv\Scripts\Activate    # (note the capital A in PowerShell)

# 3) Install dependencies
pip install -r requirements.txt

# 4) Run unit tests
pytest -q

# 5) Start the API
uvicorn app:app --reload

# → Open http://127.0.0.1:8000/docs

## Windows (Command Prompt alternative)

cd C:\path\to\AISE26-W5D2-inclassmaterial
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
pytest -q
uvicorn app:app --reload

If uvicorn isn’t recognized, use:
python -m uvicorn app:app --reload

## Deactivate the virtual environment
Mac/Linux: deactivate
Windows (PowerShell/CMD): deactivate