# AdForge

**AI-based product advertisement generator that turns grounded product facts into a complete, audience-adapted campaign package.**

AdForge is a local-first FastAPI application. Phase 1 establishes the typed input/output contract and development tooling; generation and exports arrive in subsequent phases.

## Run locally

### Windows PowerShell

Open PowerShell in the project directory. If `.venv` is already present, do
not recreate it.

```powershell
if (-not (Test-Path .venv\Scripts\python.exe)) {
    python -m venv .venv
}
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m uvicorn adforge.api:app --host 127.0.0.1 --port 8000
```

The API is then available at `http://127.0.0.1:8000`. Open that address for a
small status response, or use:

- `http://127.0.0.1:8000/api/health` for the health check
- `http://127.0.0.1:8000/docs` for the interactive API documentation

Stop the server with `Ctrl+C`.

For development checks, run:

```powershell
python -m pytest
python -m ruff check .
python -m mypy src
```

GNU Make is not installed by default on Windows. You can use the equivalent
PowerShell wrapper commands:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\adforge.ps1 install
powershell -ExecutionPolicy Bypass -File .\scripts\adforge.ps1 run
powershell -ExecutionPolicy Bypass -File .\scripts\adforge.ps1 test
```

### Unix-like shells

```shell
python -m venv .venv
. .venv/bin/activate
make install
make run
```

Then visit `http://127.0.0.1:8000/api/health`.

See `docs/DECISIONS.md` for intentionally scoped implementation choices.
