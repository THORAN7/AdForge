# AdForge

**AI-based product advertisement generator that turns grounded product facts into a complete, audience-adapted campaign package.**

AdForge is a local-first FastAPI application with deterministic offline
generation, audience adaptation, automated claim/consistency checks, local SVG
previews, and JSON/Markdown/DOCX/PDF/ZIP exports. No API key is required.

## Run and test locally

### Windows PowerShell

Open PowerShell in the project directory:

```powershell
# Create the environment only if it does not already exist.
if (-not (Test-Path .venv\Scripts\python.exe)) {
    python -m venv .venv
}

.venv\Scripts\Activate.ps1

# Install the application and development tools.
python -m pip install -e ".[dev]"
# Optional DOCX and PDF support:
python -m pip install -e ".[documents]"
```

Start the development server in the same activated PowerShell window:

```powershell
python -m uvicorn adforge.api:app --host 127.0.0.1 --port 8000
```

Open these URLs in your browser:

- `http://127.0.0.1:8000/` — interactive campaign wizard
- `http://127.0.0.1:8000/api/health` — health check
- `http://127.0.0.1:8000/docs` — interactive API documentation

Stop the server with `Ctrl+C`.

Enter a product name, category, three to eight features, USP, brand details,
and an audience in the wizard. The generated tabs show descriptions, promo,
social, visual, and video sections. Use the export buttons to download the
canonical package. The API can also be called directly:

```powershell
@'
{"product":{"name":"Desk Lamp","category":"lighting","key_features":["adjustable","portable","USB-C"],"price_offer":"$19.99","unique_selling_point":"Focused light.","brand_name":"BrightCo","brand_tone":"trustworthy","language":"English"},"audiences":[{"preset":"young_professionals"}]}
'@ | Set-Content request.json
curl.exe -X POST http://127.0.0.1:8000/api/generate `
  -H "Content-Type: application/json" --data-binary "@request.json"
```

Hosted LLM mode is opt-in only. Set `ADFORGE_ALLOW_EXTERNAL_LLM=true`,
`ADFORGE_LLM_PROVIDER=openai` or `anthropic`, and the corresponding API key.
Product data is otherwise kept local; generated content should still be
reviewed by a human before publication.

In a second PowerShell window, activate the environment and run the checks:

```powershell
.venv\Scripts\Activate.ps1
python -m pytest
python -m ruff check .
python -m ruff format --check .
python -m mypy src
```

GNU Make is not installed by default on Windows. The equivalent wrapper
commands are:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\adforge.ps1 install
powershell -ExecutionPolicy Bypass -File .\scripts\adforge.ps1 run
powershell -ExecutionPolicy Bypass -File .\scripts\adforge.ps1 test
powershell -ExecutionPolicy Bypass -File .\scripts\adforge.ps1 lint
powershell -ExecutionPolicy Bypass -File .\scripts\adforge.ps1 format-check
powershell -ExecutionPolicy Bypass -File .\scripts\adforge.ps1 typecheck
```

### Docker

Docker Desktop must be installed and running:

```powershell
docker compose up --build
```

The host remains bound to `127.0.0.1:8000`. Check the container with
`http://127.0.0.1:8000/api/health`. Stop it with:

```powershell
docker compose down
```

### Unix-like shells

```shell
python -m venv .venv
. .venv/bin/activate
make install
make run
```

Run the checks with `make test`, `make lint`, `make format-check`, and
`make typecheck`.

See `docs/DECISIONS.md` for intentionally scoped implementation choices.
