"""Verify lockstep versions for Tempo toolkit distributions."""

from pathlib import Path
from tomllib import load

PACKAGE_ROOT = Path(__file__).resolve().parents[1] / "packages"
PACKAGE_NAMES = ("contracts", "application", "infrastructure")


def read_version(package_name: str) -> str:
    """Read a package version from its project metadata."""
    with (PACKAGE_ROOT / package_name / "pyproject.toml").open("rb") as pyproject_file:
        return load(pyproject_file)["project"]["version"]


def main() -> None:
    """Fail when toolkit package versions differ."""
    versions = {package_name: read_version(package_name) for package_name in PACKAGE_NAMES}
    if len(set(versions.values())) != 1:
        raise SystemExit(f"Toolkit package versions differ: {versions}")


if __name__ == "__main__":
    main()
