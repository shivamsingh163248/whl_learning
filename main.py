from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from lab_report_tool.cli import main
from build_wheel import build_wheel


def run() -> None:
    """Build a fresh wheel, then run the application."""
    skip_build = "--no-build" in sys.argv
    if skip_build:
        sys.argv.remove("--no-build")
    else:
        build_wheel()

    main()


if __name__ == "__main__":
#this is the calling the run fucation
    run()
