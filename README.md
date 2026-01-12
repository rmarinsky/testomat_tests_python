# Testomat E2E Tests

Playwright-based end-to-end testing framework for [Testomat](https://testomat.io) application.

## Project Structure

```
testomat_tests/
├── src/                          # Source code
│   └── web/                      # Web UI automation
│       ├── application.py        # Application facade (entry point)
│       ├── pages/                # Page Object Models
│       │   ├── base_page.py      # Abstract base class for pages
│       │   ├── home_page.py
│       │   ├── login_page.py
│       │   ├── projects_page.py
│       │   ├── new_projects_page.py
│       │   └── project_page.py
│       └── components/           # Reusable UI components
│           ├── project_card.py
│           ├── projects_page_header.py
│           └── side_bar.py
│
├── tests/                        # Test suite
│   ├── conftest.py               # Pytest fixtures
│   └── web/                      # Web UI tests
│       ├── login_page_test.py
│       ├── projects_page_test.py
│       └── project_creation_tests.py
│
├── test-result/                  # Test execution results
│   └── videos/                   # Video recordings
│
├── .env                          # Environment configuration
├── pyproject.toml                # Project configuration
└── uv.lock                       # Dependency lock file
```

## Requirements

- Python >= 3.14
- [uv](https://github.com/astral-sh/uv) package manager (recommended)

## Installation

### Using uv (Recommended)

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
uv sync

# Install Playwright browsers
uv run playwright install
```

### Using pip

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
playwright install
```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
BASE_URL=https://testomat.io
BASE_APP_URL=https://app.testomat.io
EMAIL=your_email@example.com
PASSWORD=your_password
```

## Running Tests

```bash
# Run all tests
pytest

# Run smoke tests
pytest -m smoke

# Run regression tests
pytest -m regression

# Run web UI tests
pytest -m web

# Run specific test file
pytest tests/web/login_page_test.py

# Run with verbose output
pytest -v

# Run tests in headed mode (browser visible) - default
pytest --headed

# Generate HTML report (default: test-result/report.html)
pytest --html=test-result/report.html
```

## Test Markers

| Marker | Description |
|--------|-------------|
| `smoke` | Quick validation tests |
| `regression` | Full test suite |
| `web` | Web UI specific tests |
| `slow` | Long-running tests |

## Architecture

### Page Object Model (POM)

All pages inherit from `BasePage` which provides common functionality:
- `is_loaded()` - Verify page is loaded
- `wait_for_load()` - Wait for page to fully load
- `get_current_url()` - Get current page URL
- `take_screenshot()` - Capture screenshot
- `scroll_to_top()` / `scroll_to_bottom()` - Page scrolling

### Fluent Interface Pattern

Methods return `Self` for method chaining:

```python
app.login_page.open().is_loaded().login_user(email, password)
```

### Application Facade

The `Application` class provides a unified entry point to all pages:

```python
class Application:
    def __init__(self, page: Page):
        self.page = page
        self.home_page = HomePage(page)
        self.login_page = LoginPage(page)
        self.projects_page = ProjectsPage(page)
        # ...
```

### Fixture Strategy

| Fixture | Scope | Purpose |
|---------|-------|---------|
| `configs` | session | Load environment variables |
| `browser_instance` | session | Reuse browser across tests |
| `app` | function | Fresh page per test |
| `logged_app` | function | Pre-authenticated page per test |
| `logged_context` | session | Reused authenticated session |
| `shared_page` | module | Shared page for parametrized tests |

## Code Quality

The project uses [Ruff](https://github.com/astral-sh/ruff) for linting and formatting.

```bash
# Check for linting issues
ruff check .

# Fix linting issues automatically
ruff check --fix .

# Format code
ruff format .
```

## Browser Configuration

Default browser settings (configured in `conftest.py`):
- Resolution: 1920x1080
- Locale: uk-UA
- Timezone: Europe/Kyiv
- Video recording: Enabled
- Headless: False

## Dependencies

### Runtime
- **playwright** - Browser automation
- **pytest** - Test framework
- **pytest-html** - HTML reporting
- **faker** - Test data generation
- **python-dotenv** - Environment variable management

### Development
- **ruff** - Linter and formatter
