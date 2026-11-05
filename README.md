# AdForge

**AI-based product advertisement generator that turns grounded product facts into a complete, audience-adapted campaign package.**

AdForge is a local-first FastAPI application. The current release provides the
typed API contract, validation, security defaults, and browser landing page;
generation and exports are being added incrementally.

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
```

Start the development server in the same activated PowerShell window:

```powershell
python -m uvicorn adforge.api:app --host 127.0.0.1 --port 8000
```

Open these URLs in your browser:

- `http://127.0.0.1:8000/` — AdForge landing page
- `http://127.0.0.1:8000/api/health` — health check
- `http://127.0.0.1:8000/docs` — interactive API documentation

Stop the server with `Ctrl+C`.

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
