# AdForge

**AI-based product advertisement generator that turns grounded product facts into a complete, audience-adapted campaign package.**

AdForge is a local-first FastAPI application. Phase 1 establishes the typed input/output contract and development tooling; generation and exports arrive in subsequent phases.

## Development

### Windows PowerShell

If `.venv` already exists, do not run `python -m venv .venv` again. Activate
the existing environment and install dependencies directly:

```powershell
if (-not (Test-Path .venv\Scripts\python.exe)) {
    python -m venv .venv
}
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pytest
```

GNU Make is not installed by default on Windows. The equivalent commands are
available through `.\scripts\adforge.ps1 install`, `.\scripts\adforge.ps1 test`,
`.\scripts\adforge.ps1 lint`, `.\scripts\adforge.ps1 typecheck`, and
`.\scripts\adforge.ps1 run`. If PowerShell blocks local scripts, invoke one as
`powershell -ExecutionPolicy Bypass -File .\scripts\adforge.ps1 test`, or use
the direct `python -m ...` commands above without changing execution policy.

### Unix-like shells

```shell
python -m venv .venv
. .venv/bin/activate
make install
make test
```

Run the API with `.\scripts\adforge.ps1 run` or `make run`, then visit
`http://127.0.0.1:8000/api/health`.
See `docs/DECISIONS.md` for intentionally scoped implementation choices.
