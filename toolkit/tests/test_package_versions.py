"""Toolkit release metadata tests."""

from scripts.check_versions import PACKAGE_NAMES, read_version


def test_package_versions_are_synchronized() -> None:
    """All toolkit distributions use one release version."""
    assert {read_version(package_name) for package_name in PACKAGE_NAMES} == {"0.2.1"}
