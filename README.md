# QA Automation Framework with Playwright

A Python test automation framework built with Playwright and Pytest.

This repository is developed both as a professional portfolio project and as a practical environment for designing a maintainable, scalable and defensible QA automation architecture.

The goal is not to maximize the number of automated cases, but to make deliberate engineering decisions around test design, responsibilities, data, isolation, reproducibility, observability and failure diagnosis.

## What this project demonstrates

The framework currently includes:

- UI and API automated testing with Pytest
- Playwright-based browser automation
- Page Object Model for page-level behavior
- Reusable Component Objects for shared UI regions
- API client abstractions
- Test-data generation through factories
- API-driven UI preconditions and cleanup
- Parametrized test scenarios
- Cross-page data consistency validation
- Third-party request isolation
- Automatic screenshots and Playwright traces on UI failures
- Allure reporting with structured feature and story metadata
- Failure evidence attached directly to Allure test results
- GitHub Actions continuous integration
- Cross-browser execution on Chromium, Firefox and WebKit
- Browser-specific Allure and failure-evidence artifacts
- Ruff linting and formatting
- mypy static type checking
- Automated code-quality gates in CI
- Reproducible dependency installation with `uv`

## Technology stack

- Python 3.13
- Pytest
- Playwright
- pytest-playwright
- Allure
- Ruff
- mypy
- uv
- GitHub Actions

## Architecture

```text
.
├── .github/
│   └── workflows/             # GitHub Actions CI workflows
├── api/                       # API clients and service-level helpers
├── config/                    # Environment and framework configuration
├── docs/                      # Architecture and testing documentation
├── pages/
│   ├── components/            # Reusable Component Objects
│   └── *_page.py              # Page Objects
├── test_data/                 # Test-data builders / factories
├── tests/
│   ├── api/                   # API scenarios
│   └── ui/
│       ├── conftest.py        # UI-specific fixtures, hooks and evidence
│       └── test_*.py          # UI scenarios
├── utils/                     # Shared utilities
├── conftest.py                # Shared fixtures and API infrastructure
└── pyproject.toml             # Dependencies and Pytest configuration
```

The framework deliberately separates test intent from implementation and infrastructure concerns.

At a high level:

- **Tests** own scenario intent and assertions.
- **Page Objects** expose page-level behavior and state.
- **Component Objects** encapsulate reusable UI regions.
- **API clients** encapsulate service-level communication.
- **Factories** generate test data.
- **Fixtures** manage reusable setup, teardown and infrastructure.
- **Pytest hooks** observe execution outcomes and coordinate failure evidence.
- **GitHub Actions** orchestrates execution and persists generated artifacts.

For the reasoning behind these boundaries, see [`docs/architecture.md`](docs/architecture.md).

## Test coverage

### Authentication

- Invalid credentials are rejected
- Users created through the API can authenticate through the UI
- Test users are cleaned up after execution

### Products and search

- Product catalog validation
- Case-insensitive substring search
- Parametrized search inputs
- No-result search behavior
- Empty-search behavior
- Product detail consistency

### Categories and brands

- Category navigation and state validation
- Representative category membership validation
- Brand navigation and semantic URL validation
- Representative brand membership validation

### Cart

- Products can be added from the catalog
- Add-to-cart confirmation feedback is validated
- Product name and price remain consistent between catalog and cart

### API

- User creation through the public API
- API clients reused for UI setup and cleanup

The suite intentionally favors representative, defensible scenarios over artificial test-count growth.

More detail about test design and oracle decisions is available in [`docs/testing-strategy.md`](docs/testing-strategy.md).

## Cross-browser execution

The UI suite is validated against all three browser engines supported by Playwright:

```text
Chromium
Firefox
WebKit
```

Locally, a specific browser can be selected with:

```bash
uv run pytest -m ui --browser chromium
uv run pytest -m ui --browser firefox
uv run pytest -m ui --browser webkit
```

GitHub Actions uses a browser matrix so the same UI job definition expands into three independent executions:

```text
ui-tests (chromium)
ui-tests (firefox)
ui-tests (webkit)
```

Matrix fail-fast behavior is disabled so a failure in one browser does not prevent the remaining browser executions from providing diagnostic information.

## Continuous integration

Pull requests targeting `main` are validated by independent GitHub Actions jobs.

```text
Pull Request → main
        │
        ├── api-tests
        │   └── Pytest API suite
        │
        ├── code-quality
        │   ├── Ruff lint
        │   ├── Ruff format check
        │   └── mypy
        │
        └── ui-tests matrix
            ├── Chromium
            ├── Firefox
            └── WebKit
```

The jobs are intentionally separated.

API validation does not require browser infrastructure, while each UI matrix execution installs only the browser engine it needs.

CI uses:

```bash
uv sync --locked
```

to reproduce the committed dependency state.

Code-quality checks validate the committed code but do not modify it automatically. Formatting and lint fixes remain explicit developer actions rather than CI-side mutations.

## Reporting and failure observability

UI failures automatically capture:

- Browser screenshot
- Playwright trace

Evidence is generated at the test-execution layer rather than by GitHub Actions.

```text
Pytest / Playwright
        ↓
detect UI failure
        ↓
capture screenshot + trace
        ↓
attach evidence to Allure
        ↓
persist files
        ↓
GitHub Actions
        ↓
upload artifacts
```

Screenshots provide fast visual triage, while Playwright traces provide deeper execution reconstruction through actions, DOM snapshots, network activity and timing information.

Allure provides structured reporting including test status, execution metadata, feature/story labels and failure attachments.

Each browser execution in CI produces its own report artifact:

```text
allure-report-ui-chromium
allure-report-ui-firefox
allure-report-ui-webkit
```

Failure evidence is also preserved per browser when required.

A saved Playwright trace can be opened locally with:

```bash
uv run playwright show-trace "test-results/<trace-file>.zip"
```

For the complete observability and failure-handling strategy, see [`docs/testing-strategy.md`](docs/testing-strategy.md).

## Code quality

The repository uses three complementary static-quality mechanisms:

```text
Ruff lint
→ code-quality and import rules

Ruff formatter
→ deterministic Python formatting

mypy
→ static type-contract validation
```

Run the checks locally with:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy .
```

Developer-side automatic formatting and safe lint fixes can be applied with:

```bash
uv run ruff check . --fix
uv run ruff format .
```

CI only performs validation.

## Requirements

- Python 3.13 or later
- `uv`
- Playwright-supported browser binaries

Allure CLI is required only when generating or opening Allure reports locally.

## Installation

Clone the repository:

```bash
git clone https://github.com/jireyes94/qa-automation-framework-playwright.git
cd qa-automation-framework-playwright
```

Install project dependencies:

```bash
uv sync --dev
```

Install Playwright browser binaries:

```bash
uv run playwright install
```

## Running the tests

Complete suite:

```bash
uv run pytest -v
```

UI tests:

```bash
uv run pytest -m ui -v
```

API tests:

```bash
uv run pytest -m api -v
```

Specific browser:

```bash
uv run pytest -m ui --browser firefox -v
```

Visible browser:

```bash
uv run pytest -m ui --headed
```

Generate Allure results:

```bash
uv run pytest --alluredir=allure-results --clean-alluredir
```

Open a saved Playwright trace:

```bash
uv run playwright show-trace "test-results/<trace-file>.zip"
```

## Test target

The UI scenarios use Automation Exercise, a public practice application created for automation testing.

The target is external to this repository and can change, become degraded or become unavailable independently of the framework.

External instability is therefore diagnosed separately from framework defects. The framework does not automatically treat timeouts, HTTP failures or temporary service degradation as reasons to increase waits or introduce retries.

## Engineering principles

This project prioritizes:

- Readability over unnecessary abstraction
- Assertions backed by known behavior rather than assumptions
- Independent and repeatable tests
- Clear separation between test intent and implementation
- API-driven setup when UI setup would add irrelevant cost
- Explicit component and page responsibility boundaries
- Deterministic execution where external dependencies can reasonably be isolated
- Useful failure diagnosis instead of indiscriminate retries
- Reproducible execution outside the developer machine
- Failure evidence that survives disposable CI runners
- Architecture decisions that can be explained and defended

## Documentation

Detailed engineering documentation is separated from the project overview:

- [`docs/architecture.md`](docs/architecture.md) — framework structure, responsibility boundaries and architectural decisions
- [`docs/testing-strategy.md`](docs/testing-strategy.md) — test design, oracles, isolation, observability, reporting, CI and cross-browser strategy

## Milestones

- [x] Bootstrap Python, Pytest, Playwright and `uv`
- [x] Configure UI and API markers
- [x] Add API client and user lifecycle coverage
- [x] Introduce API-driven UI preconditions and cleanup
- [x] Introduce Page Object Model
- [x] Introduce reusable Component Objects
- [x] Build authentication flows
- [x] Build product catalog and search coverage
- [x] Add cart and cross-page consistency validation
- [x] Add category and brand filtering coverage
- [x] Parametrize representative search partitions
- [x] Isolate third-party advertisement interference
- [x] Adopt feature-branch / pull-request workflow
- [x] Add GitHub Actions continuous integration
- [x] Separate API and UI CI responsibilities
- [x] Capture screenshots on failed UI tests
- [x] Capture Playwright traces on failed UI tests
- [x] Persist CI failure evidence
- [x] Add Allure reporting
- [x] Attach failure evidence to Allure test results
- [x] Add Ruff linting and formatting
- [x] Add mypy static type checking
- [x] Add automated code-quality CI gates
- [x] Add Chromium, Firefox and WebKit browser matrix
- [ ] Evaluate parallel test execution
- [ ] Expand selected API/UI integration scenarios
- [ ] Define formal retry criteria

## Author

**José Ignacio Reyes Lima**

- [Mi Perfil de GitHub](https://github.com/jireyes94)
- [Mi Perfil de LinkedIn](https://www.linkedin.com/in/ignacio-reyes-lima/)