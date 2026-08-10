# QA Automation Framework with Playwright

A Python test automation project built with Playwright and Pytest.

This repository is being developed as both a professional portfolio project and a practical environment for designing a maintainable automation framework for UI and API testing.

> **Project status:** Active development — the initial project structure, dependency management and browser health test are currently implemented. The architecture and test suites described in the roadmap are being added incrementally.

## Current implementation

- Python project and dependency management with `uv`
- Pytest configuration with strict marker validation
- Playwright integration through `pytest-playwright`
- Initial package structure for pages, API clients, configuration and utilities
- Browser-based health test against [Automation Exercise](https://automationexercise.com/)
- Environment configuration template

## Planned scope

The framework is intended to include:

- Page Object Model for reusable UI interactions
- UI and API test suites
- Shared fixtures with deliberate Pytest scopes
- Environment-based configuration
- Test data builders and parametrized scenarios
- Positive, negative and boundary test cases
- Authentication and session reuse
- Screenshots, traces and videos for failed tests
- HTML or Allure reporting
- Parallel execution
- Test markers and selective suite execution
- Linting and static analysis
- Continuous integration with GitHub Actions
- Flaky-test prevention and documented retry criteria

## Project structure

```text
.
├── api/            # API clients and service-level helpers
├── config/         # Environment and framework configuration
├── pages/          # Page Objects and reusable UI interactions
├── tests/          # Automated test suites
├── utils/          # Shared utilities
├── conftest.py     # Pytest fixtures and hooks
└── pyproject.toml  # Project dependencies and Pytest configuration
```

Some packages are currently placeholders and will be implemented as the framework evolves.

## Requirements

- Python 3.13 or later
- [uv](https://docs.astral.sh/uv/)
- A Playwright-supported browser

## Installation

Clone the repository:

```bash
git clone https://github.com/jireyes94/qa-automation-framework-playwright.git
cd qa-automation-framework-playwright
```

Install the project dependencies:

```bash
uv sync --dev
```

Install the Playwright browser binaries:

```bash
uv run playwright install
```

## Running the tests

Run the complete test suite:

```bash
uv run pytest
```

Run with visible browser execution:

```bash
uv run pytest --headed
```

## Test target

The initial UI scenarios use [Automation Exercise](https://automationexercise.com/), a public practice application created for automation testing.

The target application is external to this repository and may change independently.

## Engineering goals

This project prioritizes:

- Readability over unnecessary abstraction
- Independent and repeatable tests
- Clear separation between test intent and UI implementation
- Useful failure evidence
- Configuration that can evolve across environments
- Architecture decisions that can be explained and defended

## Roadmap

- [x] Bootstrap Python, Pytest and Playwright
- [x] Add an initial browser health test
- [ ] Implement typed configuration
- [ ] Add shared fixtures
- [ ] Introduce the first Page Object
- [ ] Build authentication and user-flow scenarios
- [ ] Add API clients and API tests
- [ ] Add reporting and failure artifacts
- [ ] Configure linting and static analysis
- [ ] Add GitHub Actions CI
- [ ] Document the complete testing strategy

## Author

**José Ignacio Reyes Lima**

- [GitHub](https://github.com/jireyes94)
- [LinkedIn](https://www.linkedin.com/in/ignacio-reyes-lima/)
