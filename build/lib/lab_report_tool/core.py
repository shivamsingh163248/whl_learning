"""Core laboratory report analysis."""

from dataclasses import dataclass
from typing import Iterable, List


@dataclass(frozen=True)
class LabResult:
    """A single measured laboratory result."""

    test_name: str
    value: float
    unit: str
    low: float
    high: float

    @property
    def status(self) -> str:
        """Return NORMAL, LOW, or HIGH based on the reference range."""
        if self.value < self.low:
            return "LOW"
        if self.value > self.high:
            return "HIGH"
        return "NORMAL"


def analyze_results(results: Iterable[LabResult]) -> List[LabResult]:
    """Validate and return laboratory results in input order."""
    analyzed = list(results)
    if not analyzed:
        raise ValueError("at least one laboratory result is required")
    for result in analyzed:
        if not result.test_name.strip():
            raise ValueError("test names must not be empty")
        if result.low > result.high:
            raise ValueError("reference range low value must not exceed high value")
    return analyzed


def format_report(patient: str, results: Iterable[LabResult]) -> str:
    """Create a readable report; this is not a medical diagnosis."""
    if not patient.strip():
        raise ValueError("patient name must not be empty")
    analyzed = analyze_results(results)
    lines = [
        "LABORATORY REPORT",
        f"Patient: {patient.strip()}",
        "",
        f"{'Test':<22} {'Result':>10} {'Unit':<12} {'Reference':<18} Status",
        "-" * 75,
    ]
    for result in analyzed:
        reference = f"{result.low:g} - {result.high:g}"
        lines.append(
            f"{result.test_name:<22} {result.value:>10g} "
            f"{result.unit:<12} {reference:<18} {result.status}"
        )
    lines.extend(["", "For informational use only; review results with a qualified clinician."])
    return "\n".join(lines)
