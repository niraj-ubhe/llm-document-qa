# LLM Document Q&A API

A small FastAPI project for learning how to build a document question-and-answer API. Day 2 stores document metadata in PostgreSQL. It does not upload or extract PDF content, or connect to an LLM yet.

## Set up on Windows PowerShell

Run these commands from the project folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Open `.env` and replace `YOUR_PASSWORD` with the password for the PostgreSQL user. Keep `.env` private; it is listed in `.gitignore`. The example URL uses the local Docker port mapping `localhost:5433` and database `llm_documents`.

If PowerShell blocks virtual environment activation, install dependencies and run the server without activating it:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Edit `.env` to replace `YOUR_PASSWORD` before starting the API.

## Run the API

With the virtual environment activated:

```powershell
uvicorn app.main:app --reload
```

Or, without activating it:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Press `Ctrl+C` to stop the server.

The app reads `DATABASE_URL` from `.env`. At startup, SQLAlchemy creates the `documents` table if it does not exist. This is a simple development setup; schema migrations are not configured.

## Try the endpoints

In a second PowerShell window, run:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/
Invoke-RestMethod http://127.0.0.1:8000/health
```

The first request returns `message: LLM Document Q&A API`; the second returns `status: ok`. FastAPI's interactive API docs are at `http://127.0.0.1:8000/docs`.

Create a metadata row by sending JSON:

```powershell
$document = @{
    filename = "notes.pdf"
    content_type = "application/pdf"
} | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/documents -ContentType "application/json" -Body $document
```

`status` is optional and defaults to `pending`. List saved metadata with:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/documents
```
