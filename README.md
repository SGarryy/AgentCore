# AgentCore

AgentCore is a local multi-agent orchestration demo. It accepts a natural-language task, extracts intent/entities, routes the task to a specialized agent, runs a simulated workflow, and optionally summarizes the result with a local Ollama LLM.

This is a phase-1 portfolio/MVP project. It has a working FastAPI backend, a Streamlit dashboard, tests, input validation, model integrity handling, optional API-key protection, and local-only LLM support. Database persistence and real third-party integrations are intentionally not connected yet.

## Features

- FastAPI backend with `/health`, `/health/detailed`, and `/process`
- Streamlit dashboard in `app/dashboard.py`
- NLP entity extraction with spaCy
- ML intent routing with scikit-learn TF-IDF + Logistic Regression
- Five agents: HR, Finance, IT, Sales, and Operations
- Local LLM summary generation through Ollama
- Request validation with Pydantic schemas
- Rate limiting on `/process`
- Optional bearer API key protection
- Signed model integrity check with automatic trusted retraining when needed
- Pytest suite: currently `41 passed`

## Project Status

Current phase: local MVP / phase-1 baseline.

Not included yet:

- Real database persistence
- Real email/Jira/Slack/CRM integrations
- Production auth flow
- Deployment pipeline
- Centralized observability

## Requirements

- Python 3.10+
- Ollama, optional but recommended for LLM summaries
- spaCy model `en_core_web_sm`
- Windows PowerShell examples are shown below because this project is currently being run on Windows.

## Setup

From the project root:

```powershell
cd C:\Users\asus\Desktop\AgentCore\AgentCore
```

Activate the virtual environment:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

Install dependencies when package/network access is working:

```powershell
python -m pip install -r requirements.txt
```

If `pip` is corrupted inside the venv, repair it:

```powershell
.\venv\Scripts\python.exe -m ensurepip --upgrade
```

If your network/proxy blocks the spaCy model wheel from GitHub, dependency installation may fail on `en_core_web_sm`. Fix proxy/network access, then rerun:

```powershell
python -m pip install -r requirements.txt
```

## Environment

Copy the template if needed:

```powershell
Copy-Item .env.example .env
```

Important variables:

```env
OLLAMA_URL=http://localhost:11434/api/generate
LLM_MODEL=mistral
LLM_TIMEOUT=60

MODEL_PATH=./models/router_model.pkl
MODEL_SIGNATURE_PATH=./models/router_model.pkl.sig

API_KEY=
API_HOST=0.0.0.0
API_PORT=8000
ALLOWED_ORIGINS=http://localhost:8000,http://localhost:8501

ENVIRONMENT=development
AGENTCORE_DEBUG=false
```

`.env` must stay local and untracked. Use `.env.example` for shared defaults.

## Run The Backend

In terminal 1:

```powershell
cd C:\Users\asus\Desktop\AgentCore\AgentCore
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open:

```text
http://127.0.0.1:8000/docs
```

The root URL returns `404` because no `/` route is defined. Use `/docs`, `/health`, or `/process`.

Health endpoints:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/health/detailed
```

## Run The Streamlit Dashboard

Keep the backend terminal running. Open terminal 2.

If the venv has complete Streamlit dependencies:

```powershell
cd C:\Users\asus\Desktop\AgentCore\AgentCore
.\venv\Scripts\Activate.ps1
python -m streamlit run app/dashboard.py --server.port 8501
```

If the venv Streamlit install is incomplete, use the system Python that has Streamlit installed:

```powershell
cd C:\Users\asus\Desktop\AgentCore\AgentCore
C:\Users\asus\AppData\Local\Programs\Python\Python313\python.exe -m streamlit run app/dashboard.py --server.port 8501
```

Open:

```text
http://localhost:8501
```

## Ollama

For local LLM summaries:

```powershell
ollama pull mistral
ollama serve
```

Ollama should be available at:

```text
http://localhost:11434
```

If Ollama is unavailable, the API falls back to the agent output instead of failing the whole request.

## API Usage

Example request:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri "http://127.0.0.1:8000/process" `
  -ContentType "application/json" `
  -Body '{"text":"Onboard new developer John to engineering","priority":"high"}'
```

If `API_KEY` is set, include:

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri "http://127.0.0.1:8000/process" `
  -Headers @{ Authorization = "Bearer your-api-key" } `
  -ContentType "application/json" `
  -Body '{"text":"Fix the login bug urgently","priority":"high"}'
```

In `development`, `/process` is open unless `API_KEY` is configured. In non-development environments, `/process` requires `API_KEY`.

## Testing

Run all tests:

```powershell
pytest -q
```

Current verification:

```text
41 passed
```

The tests mock external Ollama/LLM calls so they run quickly and do not require the local LLM service.

## Security Notes

- `.env` is ignored and should not be committed.
- Rotate any secret that was previously committed.
- `API_KEY` enables bearer-token protection for `/process`.
- CORS is restricted to configured local origins by default.
- Model files are loaded through `ModelManager`.
- Unsigned model files are not blindly loaded. If a signature is missing, the router retrains from trusted local training data and writes a new signature.
- `joblib`/pickle model files should never be accepted from untrusted sources.

## Architecture

```text
User input
  -> app.nlp.extractor.extract_intent
  -> app.ml.router.route_task
  -> app.agents.dispatcher.dispatch
  -> specialized agent
  -> app.llm.generate_response
  -> API/dashboard response
```

## Project Structure

```text
AgentCore/
├── app/
│   ├── agents/
│   │   ├── base_agent.py
│   │   ├── dispatcher.py
│   │   ├── finance_agent.py
│   │   ├── hr_agent.py
│   │   ├── it_agent.py
│   │   ├── operations_agent.py
│   │   └── sales_agent.py
│   ├── ml/
│   │   ├── model_manager.py
│   │   └── router.py
│   ├── nlp/
│   │   └── extractor.py
│   ├── utils/
│   │   └── ids.py
│   ├── config.py
│   ├── constants.py
│   ├── dashboard.py
│   ├── llm.py
│   ├── logging_config.py
│   ├── main.py
│   ├── router.py
│   └── schemas.py
├── data/
│   └── training_data.py
├── models/
├── tests/
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

## Example Tasks

| Input | Routed Agent |
|---|---|
| Onboard new employee Sarah to HR on Monday | HR Agent |
| Reconcile duplicate invoices from last month | Finance Agent |
| Triage bug on login page crashing on mobile | IT Agent |
| Generate leads from retail sector urgently | Sales Agent |
| Schedule vendor meeting for procurement | Operations Agent |

## Roadmap

- Add SQLite/Postgres persistence for task runs
- Add real auth and user sessions
- Add audit logs
- Add CI for tests and dependency scanning
- Add real integrations such as email, Slack, Jira, or CRM
- Expand training data and improve routing confidence
- Add production deployment configuration
