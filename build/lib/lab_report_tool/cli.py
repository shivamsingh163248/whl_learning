"""Command-line interface for the laboratory report tool."""

import argparse

from .core import LabResult, format_report


def demo_results():
    return [
        LabResult("Hemoglobin", 13.8, "g/dL", 12.0, 17.5),
        LabResult("Glucose", 112, "mg/dL", 70, 99),
        LabResult("Platelets", 220, "10^9/L", 150, 450),
    ]


def main() -> None:
    """Print a sample report or analyze supplied results."""
    parser = argparse.ArgumentParser(description="Analyze laboratory results.")
    parser.add_argument("--patient", default="Demo Patient", help="patient label")
    parser.add_argument(
        "--result",
        action="append",
        metavar="TEST=VALUE:UNIT:LOW-HIGH",
        help="result specification; repeat for multiple tests",
    )
    args = parser.parse_args()

    results = demo_results()
    if args.result:
        results = []
        for specification in args.result:
            try:
                test, measurement = specification.split("=", 1)
                value_text, unit, reference = measurement.split(":", 2)
                low_text, high_text = reference.split("-", 1)
                results.append(
                    LabResult(
                        test.strip(),
                        float(value_text),
                        unit.strip(),
                        float(low_text),
                        float(high_text),
                    )
                )
            except ValueError as error:
                raise SystemExit(
                    f"Invalid result '{specification}'. Use TEST=VALUE:UNIT:LOW-HIGH."
                ) from error

    print(format_report(args.patient, results))


if __name__ == "__main__":
    main()
