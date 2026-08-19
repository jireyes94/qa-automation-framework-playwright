# QA Automation Framework with Playwright

A Python test automation framework built with Playwright and Pytest.

This repository is developed both as a professional portfolio project and as a practical environment for learning how to design a maintainable, scalable and defensible QA automation architecture.

The goal is not to maximize the number of automated cases, but to make deliberate decisions about test design, responsibilities, data, isolation, reproducibility and failure diagnosis.

> **Project status:** Active development. The framework currently includes UI and API coverage, Page Objects, reusable UI components, API-driven test preconditions and cleanup, parametrized scenarios, catalog filtering flows, third-party request isolation, GitHub Actions continuous integration and automatic failure evidence for UI tests. The next engineering stage focuses on structured reporting with Allure and automated code-quality checks.

## Current implementation

- Python 3.13 project and dependency management with `uv`
- Pytest with strict marker validation and separate `ui` / `api` markers
- Playwright integration through `pytest-playwright`
- Page Object Model for page-level behavior
- Reusable Component Objects for product cards, cart items, modals, header, categories and brands
- API client abstraction for user lifecycle operations
- Test-data generation through a user factory
- API-driven UI preconditions and cleanup through Pytest fixtures
- Positive and negative authentication coverage
- Product catalog, search, details, category and brand coverage
- Cart flow with UI feedback and product consistency validation
- Parametrized case-insensitive substring search coverage
- Third-party advertisement request blocking to isolate external flakiness
- GitHub Actions continuous integration on pull requests targeting `main`
- Independent API and UI CI jobs running on Ubuntu
- Reproducible CI dependency installation through `uv sync --locked`
- Chromium installation isolated to the UI CI job
- Automatic screenshots for failed UI tests
- Automatic Playwright traces for failed UI tests
- GitHub Actions artifacts preserving failure evidence after CI execution
- Feature-branch and pull-request workflow with milestone-based commits

## Current test coverage

The automated suite currently exercises the following behavior:

### Authentication

- Invalid credentials are rejected
- Valid users created through the API can authenticate through the UI
- Test users are cleaned up after execution

### Products and search

- Expected products are exposed by the catalog
- Search results are validated as a collection rather than by a single hardcoded result
- Substring matching is exercised with lower- and upper-case queries
- Searches with no matches return no product cards
- Empty searches remain in the `All Products` state
- Product information remains consistent when navigating from a card to its detail page

### Categories and brands

- Selecting a category enters the expected category state and returns results
- A representative category result is validated against the category exposed by Product Details
- Selecting a brand validates its semantic URL, page state and returned results
- A representative brand result is validated against the brand exposed by Product Details

### Cart

- Products can be added from the catalog
- The add-to-cart confirmation modal is validated before continuing
- Product name and price remain consistent between the catalog and cart

### API

- User creation is exercised through the public API
- API clients are reused as infrastructure for UI preconditions and cleanup

## Architecture

```text
.
├── .github/
│   └── workflows/             # GitHub Actions CI workflows
├── api/                       # API clients and service-level helpers
├── config/                    # Environment and framework configuration
├── pages/
│   ├── components/            # Reusable Component Objects
│   └── *_page.py              # Page Objects
├── test_data/                 # Test-data builders / factories
├── tests/
│   ├── api/                   # API scenarios
│   └── ui/
│       ├── conftest.py        # UI-specific fixtures, hooks and failure evidence
│       └── test_*.py          # UI scenarios
├── utils/                     # Shared utilities
├── conftest.py                # Shared Pytest fixtures and API infrastructure
└── pyproject.toml             # Dependencies and Pytest configuration
```

### Responsibility boundaries

The framework deliberately separates responsibilities:

- **Tests** own scenario intent and assertions.
- **Page Objects** expose page-level state and interactions without deciding business expectations.
- **Component Objects** encapsulate reusable UI regions such as product cards and category/brand navigation.
- **API clients** encapsulate service-level communication.
- **Fixtures** manage reusable setup, teardown and infrastructure concerns.
- **Pytest hooks** observe execution outcomes without placing reporting logic inside individual tests.
- **GitHub Actions** orchestrates clean CI execution and persists generated evidence, but does not generate browser evidence itself.

A component may return another Page Object when an interaction causes navigation. For example, a product card can navigate to `ProductDetailsPage`, while the test remains responsible for deciding what must be asserted there.

## Testing decisions

Several choices in this repository are intentionally documented because they represent test-design decisions rather than coding constraints.

### Assert only known behavior

Tests do not become stronger merely by adding assertions. Assertions should represent known or observed behavior that can be defended as part of the current contract.

For example, the empty-search scenario deliberately verifies only that the application remains in the `All Products` state.

It does **not** assert that product identity, ordering or catalog size remain unchanged because those properties are not established as invariants.

Adding them would turn assumptions into test oracles and could create false failures if the catalog later becomes dynamic.

### Validate collections when the contract applies to every result

Product search is treated as substring matching.

Instead of checking that one expected card appears, the test obtains the returned `ProductCard` collection and verifies that every returned product satisfies the search condition.

This prevents an invalid result from being hidden by the presence of one correct product.

The search test is parametrized with lower- and upper-case input to exercise case-insensitive behavior without creating separate scenarios for equivalent input partitions.

### Avoid exhaustive UI validation without a reliable oracle

Category and brand membership are not exposed by product cards. The detail page does expose those attributes.

The UI suite therefore validates navigation/state plus one representative returned product through its detail page.

It does not navigate through every result merely to simulate exhaustive coverage.

A complete validation of every returned product would be better supported by an API or data-layer oracle when such a source of truth is available.

### Isolate irrelevant third parties

Automation Exercise serves third-party advertising that can display interstitials and block functional navigation.

Because advertisement behavior is not part of the system behavior this project intends to test, known ad requests are blocked centrally at the `BrowserContext` level.

This keeps third-party handling out of Page Objects and test scenarios and avoids masking the problem with forced clicks, arbitrary waits or navigation workarounds.

In a production system where advertising were part of the product requirements, this isolation decision would need to be reconsidered.

### Distinguish test failures from environment failures

A timeout is not automatically treated as a reason to increase timeouts or add retries.

During development, Automation Exercise was observed to become severely degraded even under manual browser navigation.

The framework was intentionally not modified to compensate for temporary external conditions.

Retries and timeout changes should be introduced only when their purpose and failure mode are understood.

### Capture evidence at the execution layer

Failure evidence is generated by Pytest and Playwright rather than by GitHub Actions.

This reflects the responsibility boundary between execution and orchestration:

```text
Pytest / Playwright
        ↓
detect UI failure
        ↓
generate screenshot + trace
        ↓
filesystem
        ↓
GitHub Actions
        ↓
upload artifact
```

GitHub Actions does not know which browser page, locator or assertion caused a failure. Its responsibility is to preserve files produced by the test execution before the runner is destroyed.

### Preserve evidence only when it is useful

UI tracing starts before each test so execution history is available if the scenario fails.

After execution:

```text
PASS
→ tracing stops
→ trace is discarded
→ no screenshot is persisted

FAIL
→ screenshot is persisted
→ Playwright trace is persisted
→ GitHub Actions uploads the evidence
```

This avoids generating unnecessary evidence for successful scenarios while preserving diagnostic information when it is actually needed.

### Screenshot and trace serve different purposes

A screenshot provides fast visual triage of the browser state at the time of failure.

A Playwright trace provides deeper investigation capabilities including actions, DOM snapshots, timing, network activity and execution context.

They intentionally coexist:

```text
Screenshot
→ quick visual diagnosis

Trace
→ execution reconstruction and deeper debugging
```

The failure-evidence pipeline was validated both with a deliberately failing test and with a real external failure where Automation Exercise returned an HTTP `503 Service Unavailable` response during CI execution.

### Prefer domain-oriented component APIs

Components expose interactions using the language of the UI/domain:

```python
products_page.category.select("Kids", "Dress")
products_page.brand.select("Polo")
```

Categories and brands remain separate components even though both appear in the same sidebar because their interaction models and intent differ.

The framework avoids generic abstractions when they would erase meaningful behavior.

## Continuous integration

GitHub Actions validates pull requests targeting `main`.

The CI workflow currently contains two independent jobs:

```text
Pull Request → main
        │
        ├── API tests
        │   ├── Ubuntu runner
        │   ├── Python 3.13
        │   ├── uv
        │   ├── uv sync --locked
        │   └── pytest -m api
        │
        └── UI tests
            ├── Ubuntu runner
            ├── Python 3.13
            ├── uv
            ├── uv sync --locked
            ├── Chromium + Linux dependencies
            └── pytest -m ui
```

API and UI jobs are intentionally independent and can execute in parallel.

The API job does not install a browser.

This separation exposed and helped remove an accidental browser dependency that previously existed because a global UI fixture required `BrowserContext` even during API-only execution.

CI therefore validates more than test correctness: it also verifies that the repository can reconstruct its environment and execute outside the developer machine.

## Failure evidence

Failed UI tests automatically generate evidence inside:

```text
test-results/
```

A failed test produces files similar to:

```text
test-results/
├── test_name[chromium]-screenshot.png
└── test_name[chromium]-trace.zip
```

The screenshot captures the browser viewport at failure time.

The trace records deeper Playwright execution information and can be opened with:

```bash
uv run playwright show-trace "test-results/<trace-file>.zip"
```

When the UI CI job fails, GitHub Actions uploads `test-results/` as an artifact named:

```text
ui-failure-evidence
```

This allows CI-only failures to be investigated without first reproducing them locally.

The runner itself remains disposable; GitHub Actions artifacts provide the persistence layer for the generated evidence.

## Test identifiers

Scenario comments use domain-based identifiers as lightweight traceability while the project does not yet integrate with a dedicated test-management system.

Examples:

- `PROD-xxx` — product catalog and search
- `CATEGORY-xxx` — category filtering
- `BRAND-xxx` — brand filtering
- `CART-xxx` — shopping cart

The identifier does not replace a descriptive test function name.

If the project later integrates reporting or test-management tooling, these identifiers can evolve into structured metadata.

## Requirements

- Python 3.13 or later
- `uv`
- A Playwright-supported browser

## Installation

Clone the repository:

```bash
git clone https://github.com/jireyes94/qa-automation-framework-playwright.git
cd qa-automation-framework-playwright
```

Install dependencies:

```bash
uv sync --dev
```

Install Playwright browser binaries:

```bash
uv run playwright install
```

## Running the tests

Run the complete suite:

```bash
uv run pytest -v
```

Run only UI tests:

```bash
uv run pytest -m ui -v
```

Run only API tests:

```bash
uv run pytest -m api -v
```

Run with a visible browser:

```bash
uv run pytest --headed
```

Open a saved Playwright trace:

```bash
uv run playwright show-trace "test-results/<trace-file>.zip"
```

## Test target

The UI scenarios use Automation Exercise, a public practice application created for automation testing.

The target application is external to this repository and can change, become degraded or become unavailable independently.

External instability should be diagnosed separately from framework defects.

## Engineering principles

This project prioritizes:

- Readability over unnecessary abstraction
- Assertions backed by known behavior rather than assumptions
- Independent and repeatable tests
- Clear separation between test intent and UI implementation
- API-driven setup when UI setup would add irrelevant cost
- Explicit component and page responsibility boundaries
- Deterministic execution where external dependencies can reasonably be isolated
- Useful failure diagnosis instead of indiscriminate retries
- Reproducible execution outside the developer machine
- Failure evidence that survives disposable CI runners
- Architecture decisions that can be explained and defended

## Milestones

- [x] Bootstrap Python, Pytest, Playwright and `uv`
- [x] Configure markers and browser health coverage
- [x] Add API client and user lifecycle coverage
- [x] Introduce API-driven UI preconditions and cleanup
- [x] Introduce Page Object Model
- [x] Introduce reusable Component Objects
- [x] Build authentication flows
- [x] Build product catalog and search coverage
- [x] Add cart flow and cross-page consistency checks
- [x] Add category and brand filtering coverage
- [x] Parametrize representative search input partitions
- [x] Isolate third-party advertisement interference
- [x] Adopt feature-branch / pull-request workflow
- [x] Add GitHub Actions continuous integration
- [x] Separate API and UI CI jobs
- [x] Capture screenshots on failed UI tests
- [x] Capture Playwright traces on failed UI tests
- [x] Upload UI failure evidence as GitHub Actions artifacts
- [ ] Add Allure reporting
- [ ] Add linting and static analysis
- [ ] Add browser matrix execution
- [ ] Evaluate parallel execution
- [ ] Expand API/UI integration scenarios
- [ ] Define documented retry criteria

## Next engineering stage

The framework has moved beyond basic scenario automation and now includes reproducible CI execution and failure observability.

The next phase focuses on structured reporting and automated engineering quality.

1. **Allure reporting** — introduce structured test reports, execution history, suites/features and richer presentation of test evidence.
2. **Linting and static analysis** — automate formatting and code-quality checks instead of relying on manual whitespace/import cleanup.
3. **Browser matrix execution** — validate UI behavior across additional Playwright-supported browsers once the cost and value are understood.
4. **Parallel execution** — evaluate execution parallelism after browser strategy and CI behavior are stable.
5. **API/UI integration expansion** — use service-level data and API responses to strengthen selected UI scenarios where cross-layer validation adds meaningful value.
6. **Retry criteria** — document explicit conditions under which retries are justified without masking real SUT or environment instability.

## Author

**José Ignacio Reyes Lima**

[![GitHub](https://shields.io)](https://github.com/jireyes94)
[![LinkedIn](https://shields.io)](https://www.linkedin.com/in/ignacio-reyes-lima/)