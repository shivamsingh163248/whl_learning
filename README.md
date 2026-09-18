# lab-report-tool

A small, reusable laboratory result analyzer. It compares measurements with
the reference range supplied by the laboratory and labels each result
`NORMAL`, `LOW`, or `HIGH`. It does not diagnose medical conditions.

## Build and run

Running `main.py` builds a fresh wheel and prints a sample report:

```powershell
python main.py
```

The wheel is created at:

```text
dist\lab_report_tool-0.1.0-py3-none-any.whl
```

To run without rebuilding:

```powershell
python main.py --no-build --patient "Test Patient" `
  --result "Hemoglobin=13.8:g/dL:12-17.5" `
  --result "Glucose=112:mg/dL:70-99"
```

## Install and use the wheel

```powershell
python -m pip install dist\lab_report_tool-0.1.0-py3-none-any.whl
lab-report --patient "Test Patient"
```

## Use as a library

```python
from lab_report_tool import LabResult, format_report

results = [
    LabResult("Glucose", 112, "mg/dL", 70, 99),
]
print(format_report("Test Patient", results))
```
# whl_learning
