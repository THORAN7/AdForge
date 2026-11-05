[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateSet("install", "run", "test", "lint", "format", "typecheck")]
    [string] $Command
)

$ErrorActionPreference = "Stop"
$python = Join-Path $PSScriptRoot "..\.venv\Scripts\python.exe"

if (-not (Test-Path $python)) {
    throw "No project virtual environment found. Run: python -m venv .venv"
}

switch ($Command) {
    "install" {
        & $python -m pip install --upgrade pip
        & $python -m pip install -e ".[dev]"
    }
    "run" {
        & $python -m uvicorn adforge.api:app --host 127.0.0.1 --port 8000
    }
    "test" {
        & $python -m pytest
    }
    "lint" {
        & $python -m ruff check .
    }
    "format" {
        & $python -m ruff format .
    }
    "typecheck" {
        & $python -m mypy src
    }
}

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
