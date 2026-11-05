# AdForge

**AI-based product advertisement generator that turns grounded product facts into a complete, audience-adapted campaign package.**

AdForge is a local-first FastAPI application. Phase 1 establishes the typed input/output contract and development tooling; generation and exports arrive in subsequent phases.

## Development

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
make install
make test
```

Run the API with `make run`, then visit `http://127.0.0.1:8000/api/health`.
See `docs/DECISIONS.md` for intentionally scoped implementation choices.

