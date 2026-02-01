from pathlib import Path

import pytest

# Project root: tests/conftest.py is always 1 level deep
PROJECT_ROOT = Path(__file__).parent.parent
TEST_RESULT_DIR = PROJECT_ROOT / "test-result"


def pytest_configure(config: pytest.Config) -> None:
    """Set report path dynamically to always be in project root."""
    if config.option.htmlpath:
        config.option.htmlpath = str(TEST_RESULT_DIR / "report.html")


pytest_plugins = [
    "tests.fixtures.config",
    "tests.fixtures.playwright",
    "tests.fixtures.app",
    "tests.fixtures.api",
    "tests.fixtures.selenium",
]
