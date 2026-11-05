# AdForge

**AdForge turns product facts into a complete, audience-adapted advertising
package.**

It generates product descriptions, promotional copy, social posts, visual
concepts, and video narration. The default mode is deterministic, offline, and
requires **no API key**.

## What it includes

- Audience-aware campaign generation
- Product descriptions, promotion, social media, visuals, and video scripts
- Claim and consistency checks
- Local SVG visual previews
- JSON, Markdown, DOCX, PDF, and ZIP exports
- FastAPI backend and browser-based campaign wizard
- Optional OpenAI or Anthropic provider with explicit opt-in

## Run on Windows PowerShell

### 1. Open the project folder

```powershell
cd "C:\Users\thora\OneDrive\Documents\Agentic AI 2"
```

### 2. Create or activate the virtual environment

Create it only if it does not already exist:

```powershell
if (-not (Test-Path .venv\Scripts\python.exe)) {
    python -m venv .venv
}
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks the script, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\.venv\Scripts\Activate.ps1
```

If `.venv` is already active, do not create it again. The prompt will usually
start with `(.venv)`.

### 3. Install dependencies

For normal development:

```powershell
python -m pip install -e ".[dev]"
```

For DOCX and PDF exports too:

```powershell
python -m pip install -e ".[documents]"
```

### 4. Start AdForge

Keep this PowerShell window open:

```powershell
python -m uvicorn adforge.api:app --host 127.0.0.1 --port 8000
```

### 5. Open the application

Open this URL in your browser:

**<http://127.0.0.1:8000/>**

You can also open:

| URL | Purpose |
|---|---|
| <http://127.0.0.1:8000/> | AdForge campaign wizard |
| <http://127.0.0.1:8000/docs> | Interactive API documentation |
| <http://127.0.0.1:8000/api/health> | Service health check |

To stop the server, press **Ctrl+C**.

## How to use the wizard

1. Enter the product name, category, brand, tone, and unique selling point.
2. Enter **3–8 key features**, one per line.
3. Enter an optional price or offer.
4. Select an audience.
5. Click **Generate campaign**.
6. Review the Descriptions, Promotion, Social, Visual, and Video tabs.
7. Download JSON, Markdown, or a ZIP campaign kit.

## Test and lint the project

Open a second PowerShell window, enter the project folder, and activate the
environment:

```powershell
cd "C:\Users\thora\OneDrive\Documents\Agentic AI 2"
.\.venv\Scripts\Activate.ps1
```

Run the complete validation:

```powershell
python -m pytest
python -m ruff check .
python -m ruff format --check .
python -m mypy src
```

The test suite includes coverage enforcement. The project requires at least
85% coverage.

## API example

With the server running, save this request as `request.json`:

```json
{
  "product": {
    "name": "Desk Lamp",
    "category": "lighting",
    "key_features": ["adjustable", "portable", "USB-C"],
    "price_offer": "$19.99",
    "unique_selling_point": "Focused light for flexible workspaces.",
    "brand_name": "BrightCo",
    "brand_tone": "trustworthy",
    "language": "English"
  },
  "audiences": [
    { "preset": "young_professionals" }
  ]
}
```

Send it to the generation endpoint:

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/generate `
  -H "Content-Type: application/json" `
  --data-binary "@request.json"
```

Available main endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/health` | Check service status |
| `GET` | `/api/audiences` | List audience presets |
| `POST` | `/api/generate` | Generate campaign packages |
| `POST` | `/api/generate/compare` | Generate packages for multiple audiences |
| `POST` | `/api/regenerate/{section}` | Regenerate a campaign section |
| `POST` | `/api/export/{format}` | Export as `json`, `markdown`, `docx`, `pdf`, or `zip` |

## Optional hosted LLM mode

AdForge works without a hosted model. To enable one, set these environment
variables before starting the server:

```powershell
$env:ADFORGE_ALLOW_EXTERNAL_LLM = "true"
$env:ADFORGE_LLM_PROVIDER = "openai"
$env:ADFORGE_LLM_API_KEY = "your-api-key"
```

Use `anthropic` instead of `openai` when appropriate. External generation is
disabled unless `ADFORGE_ALLOW_EXTERNAL_LLM=true` is explicitly set. Never
commit API keys or real customer data.

## Docker

Install and start Docker Desktop, then run:

```powershell
docker compose up --build
```

Open <http://127.0.0.1:8000/>. Stop the container with:

```powershell
docker compose down
```

## Windows command wrapper

GNU Make is not normally installed on Windows. The PowerShell wrapper provides
equivalent commands:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\adforge.ps1 install
powershell -ExecutionPolicy Bypass -File .\scripts\adforge.ps1 run
powershell -ExecutionPolicy Bypass -File .\scripts\adforge.ps1 test
powershell -ExecutionPolicy Bypass -File .\scripts\adforge.ps1 lint
powershell -ExecutionPolicy Bypass -File .\scripts\adforge.ps1 format-check
powershell -ExecutionPolicy Bypass -File .\scripts\adforge.ps1 typecheck
```

## Troubleshooting

**The browser shows JSON instead of the app:** make sure you open
`http://127.0.0.1:8000/`, not `/api/health` or `/docs`.

**Port 8000 is already in use:** stop the old server with `Ctrl+C`, or start
another port:

```powershell
python -m uvicorn adforge.api:app --host 127.0.0.1 --port 8001
```

Then open <http://127.0.0.1:8001/>.

**`make` is not recognized:** use the PowerShell wrapper above or run the
`python -m` commands directly.

**Virtual environment permission error:** do not recreate an existing `.venv`.
Activate it and continue with dependency installation.

## Responsible use

Generated advertising content is a draft. Review every claim, price, offer,
image, and platform-specific asset before publishing. Follow applicable
advertising law, disclosure requirements, and platform policies.

See `docs/DECISIONS.md` for implementation decisions and `docs/COMPLIANCE.md`
for the current compliance rules.
