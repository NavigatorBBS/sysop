"""Setuptools helper for packaging the prebuilt JupyterLab extension assets."""

from collections import defaultdict
from pathlib import Path, PurePosixPath

from setuptools import setup

LABEXTENSION_NAME = "sysop-jupyterlab"
ROOT = Path(__file__).parent.resolve()
LABEXTENSION_DIR = ROOT / "labextension"
INSTALL_JSON = ROOT / "install.json"


def _relative_path(path: Path) -> str:
    """Return a setup.py-relative path using forward slashes."""
    return path.relative_to(ROOT).as_posix()


def build_labextension_data_files() -> list[tuple[str, list[str]]]:
    """Return the data_files entries for the prebuilt JupyterLab extension."""
    data_files: dict[str, list[str]] = defaultdict(list)

    if LABEXTENSION_DIR.exists():
        for file_path in LABEXTENSION_DIR.rglob("*"):
            if not file_path.is_file():
                continue

            relative_parent = file_path.relative_to(LABEXTENSION_DIR).parent
            destination = PurePosixPath("share/jupyter/labextensions") / LABEXTENSION_NAME
            if str(relative_parent) != ".":
                destination /= PurePosixPath(relative_parent.as_posix())

            data_files[str(destination)].append(_relative_path(file_path))

    if INSTALL_JSON.exists():
        destination = PurePosixPath("share/jupyter/labextensions") / LABEXTENSION_NAME
        data_files[str(destination)].append(_relative_path(INSTALL_JSON))

    return sorted(data_files.items())


setup(data_files=build_labextension_data_files())
