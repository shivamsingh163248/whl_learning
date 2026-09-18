"""Build the distributable wheel for this project."""

from pathlib import Path
import shutil
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parent
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"
EGG_INFO_DIRS = list((PROJECT_ROOT / "src").glob("*.egg-info"))


def build_wheel() -> None:
    """Build the project wheel into the dist directory."""
    for path in [BUILD_DIR] + EGG_INFO_DIRS:
        if path.exists():
            shutil.rmtree(path)
    DIST_DIR.mkdir(exist_ok=True)
    for wheel in DIST_DIR.glob("*.whl"):
        wheel.unlink()

    command = [
        sys.executable,
        "-m",
        "build",
        "--wheel",
        "--outdir",
        str(DIST_DIR),
        str(PROJECT_ROOT),
    ]
    subprocess.run(command, cwd=PROJECT_ROOT.parent, check=True)
    print(f"Wheel created in: {DIST_DIR}")


if __name__ == "__main__":
    build_wheel()
