"""Package review and documented quality score."""

from adforge.models import AdPackage

from .claims import check_claims
from .consistency import check_consistency
from .platforms import check_platforms


def review_package(package: AdPackage) -> AdPackage:
    """Apply deterministic checks and score 100 minus five points per warning."""
    warnings = (
        check_claims(package) + check_consistency(package) + check_platforms(package)
    )
    package.compliance_warnings = check_claims(package)
    package.consistency_warnings = check_consistency(package)
    package.quality_score = max(0, 100 - (len(warnings) * 5))
    return package
