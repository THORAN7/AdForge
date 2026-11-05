"""Grounding and claim-safety checks."""

import re

from adforge.models import AdPackage

UNSAFE = re.compile(r"\b(best|#1|number one|guaranteed|cure|miracle|risk-free)\b", re.I)


def check_claims(package: AdPackage) -> list[str]:
    """Flag risky language and text that is not in the supplied claims ledger."""
    warnings: list[str] = []
    data = package.model_dump(mode="json")
    ledger = {claim.lower() for claim in package.claims_ledger}
    for section, value in data.items():
        if section in {"product", "audience", "claims_ledger", "generated_at"}:
            continue
        _scan(value, section, ledger, warnings)
    return warnings


def _scan(value: object, section: str, ledger: set[str], warnings: list[str]) -> None:
    if isinstance(value, dict):
        for nested in value.values():
            _scan(nested, section, ledger, warnings)
    elif isinstance(value, list):
        for nested in value:
            _scan(nested, section, ledger, warnings)
    elif isinstance(value, str):
        if UNSAFE.search(value):
            warnings.append(f"{section}: unsupported claim language: {value}")
