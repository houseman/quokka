"""Nox configuration."""
import enum
import os

import nox

# Set to True if Nox is running in CI (GitHub Actions)
CI = os.environ.get("CI") is not None

# Supported Python versions
PYTHON_VERSIONS = ["3.11", "3.12"]


class Tag(str, enum.Enum):
    """Define acceptable tag values."""

    TEST = "test"
    LINT = "lint"


@nox.session(python=PYTHON_VERSIONS, tags=[Tag.TEST])
def pytest(session):
    """Run all unit tests."""
    session.install(".[test]")  # install library and test dependencies
    session.run("python", "-m", "pytest")  # Runs pytest


@nox.session(python=PYTHON_VERSIONS, tags=[Tag.LINT])
def format(session):
    """Run the ruff formatter."""
    args = ["ruff", "format", "."]

    if CI:
        # If running in CI, check only
        args.append("--check")

    session.install("ruff")
    session.run(*args)


@nox.session(python=PYTHON_VERSIONS, tags=[Tag.LINT])
def ruff(session):
    """Run the ruff linter."""
    args = ["ruff", "check", "."]

    if not CI:
        # If not in CI, fix errors that are fixable
        args.append("--fix")

    session.install(".[dev]")
    session.run(*args)


@nox.session(python=PYTHON_VERSIONS, tags=[Tag.LINT])
def mypy(session):
    """Run the mypy type checker."""
    args = ["mypy", "."]

    if CI:
        # If running in CI, check only
        args.append("--check")

    session.install(".[dev]")
    session.run(*args)
