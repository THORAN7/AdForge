# Architecture Decisions

## Phase 1

- **Canonical output:** `AdPackage` is the single output boundary. Exporters will
  consume it rather than reconstructing content.
- **Local-first defaults:** the server binds to `127.0.0.1`, uses the offline
  template provider by default, and does not enable external LLM access.
- **Audience limit:** one to three audiences are accepted to support comparison
  without unbounded generation cost.
- **Typed contracts first:** generation stages will be added behind the Pydantic
  models so API, UI, and exporters share one schema.
- **Windows developer path:** because GNU Make is not included with Windows,
  `scripts/adforge.ps1` provides equivalent commands using the project venv.
- **Phase 1.5 static packaging:** the web page is stored in `src/adforge/static`
  and included as package data so editable installs, wheels, and containers use
  the same asset.
- **Audience registry boundary:** Phase 1.5 validates the nine planned preset
  identifiers through `adforge.audiences`; Phase 2 will replace the identifier
  set with JSON-backed profile loading without changing the request contract.
