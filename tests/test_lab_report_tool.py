import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from lab_report_tool.cli import main
from lab_report_tool.core import LabResult, analyze_results, format_report


class LabResultTests(unittest.TestCase):
    def test_status_is_normal_at_range_boundaries(self):
        self.assertEqual(LabResult("Glucose", 70, "mg/dL", 70, 99).status, "NORMAL")
        self.assertEqual(LabResult("Glucose", 99, "mg/dL", 70, 99).status, "NORMAL")

    def test_status_is_low_or_high_outside_range(self):
        self.assertEqual(LabResult("Glucose", 69, "mg/dL", 70, 99).status, "LOW")
        self.assertEqual(LabResult("Glucose", 100, "mg/dL", 70, 99).status, "HIGH")

    def test_analyze_results_preserves_order(self):
        results = [
            LabResult("Glucose", 88, "mg/dL", 70, 99),
            LabResult("Platelets", 220, "10^9/L", 150, 450),
        ]
        self.assertEqual(analyze_results(results), results)

    def test_analyze_results_rejects_empty_results(self):
        with self.assertRaisesRegex(ValueError, "at least one"):
            analyze_results([])

    def test_analyze_results_rejects_invalid_reference_range(self):
        result = LabResult("Glucose", 88, "mg/dL", 100, 70)
        with self.assertRaisesRegex(ValueError, "low value"):
            analyze_results([result])


class ReportTests(unittest.TestCase):
    def test_format_report_contains_patient_and_status(self):
        result = LabResult("Glucose", 112, "mg/dL", 70, 99)

        report = format_report("Asha", [result])

        self.assertIn("LABORATORY REPORT", report)
        self.assertIn("Patient: Asha", report)
        self.assertIn("Glucose", report)
        self.assertIn("HIGH", report)
        self.assertIn("For informational use only", report)

    def test_format_report_rejects_empty_patient(self):
        with self.assertRaisesRegex(ValueError, "patient name"):
            format_report("   ", [LabResult("Glucose", 88, "mg/dL", 70, 99)])


class CommandLineTests(unittest.TestCase):
    def test_cli_prints_custom_result(self):
        output = io.StringIO()
        arguments = [
            "lab-report",
            "--patient",
            "Asha",
            "--result",
            "Glucose=112:mg/dL:70-99",
        ]

        with patch.object(sys, "argv", arguments), redirect_stdout(output):
            main()

        self.assertIn("Patient: Asha", output.getvalue())
        self.assertIn("Glucose", output.getvalue())
        self.assertIn("HIGH", output.getvalue())

    def test_cli_rejects_malformed_result(self):
        arguments = ["lab-report", "--result", "not-valid"]

        with patch.object(sys, "argv", arguments):
            with self.assertRaises(SystemExit):
                main()


if __name__ == "__main__":
    unittest.main()
