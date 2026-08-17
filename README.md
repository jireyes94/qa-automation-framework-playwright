# QA Automation Framework with Playwright

A Python test automation framework built with Playwright and Pytest.

This repository is developed both as a professional portfolio project and as a practical environment for learning how to design a maintainable, scalable and defensible QA automation architecture. The goal is not to maximize the number of automated cases, but to make deliberate decisions about test design, responsibilities, data, isolation and failure diagnosis.

> **Project status:** Active development. The framework currently includes UI and API coverage, Page Objects, reusable UI components, API-driven test preconditions and cleanup, parametrized search scenarios, catalog filtering flows and third-party request isolation. The next stage focuses on engineering infrastructure: CI, reporting, failure artifacts and code-quality tooling.

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
├── api/                    # API clients and service-level helpers
├── config/                 # Environment and framework configuration
├── pages/
│   ├── components/         # Reusable Component Objects
│   └── *_page.py           # Page Objects
├── test_data/              # Test-data builders / factories
├── tests/
│   ├── api/                # API scenarios
│   └── ui/                 # UI scenarios
├── utils/                  # Shared utilities
├── conftest.py             # Shared Pytest fixtures and test infrastructure
└── pyproject.toml          # Dependencies and Pytest configuration
```

### Responsibility boundaries

The framework deliberately separates responsibilities:

- **Tests** own scenario intent and assertions.
- **Page Objects** expose page-level state and interactions without deciding business expectations.
- **Component Objects** encapsulate reusable UI regions such as product cards and category/brand navigation.
- **API clients** encapsulate service-level communication.
- **Fixtures** manage reusable setup, teardown and infrastructure concerns.

A component may return another Page Object when an interaction causes navigation. For example, a product card can navigate to `ProductDetailsPage`, while the test remains responsible for deciding what must be asserted there.

## Testing decisions

Several choices in this repository are intentionally documented because they represent test-design decisions rather than coding constraints.

### Assert only known behavior

Tests do not become stronger merely by adding assertions. Assertions should represent known or observed behavior that can be defended as part of the current contract.

For example, the empty-search scenario deliberately verifies only that the application remains in the `All Products` state. It does **not** assert that product identity, ordering or catalog size remain unchanged because those properties are not established as invariants. Adding them would turn assumptions into test oracles and could create false failures if the catalog later becomes dynamic.

### Validate collections when the contract applies to every result

Product search is treated as substring matching. Instead of checking that one expected card appears, the test obtains the returned `ProductCard` collection and verifies that every returned product satisfies the search condition. This prevents an invalid result from being hidden by the presence of one correct product.

The search test is parametrized with lower- and upper-case input to exercise case-insensitive behavior without creating separate scenarios for equivalent input partitions.

### Avoid exhaustive UI validation without a reliable oracle

Category and brand membership are not exposed by product cards. The detail page does expose those attributes.

The UI suite therefore validates navigation/state plus one representative returned product through its detail page. It does not navigate through every result merely to simulate exhaustive coverage. A complete validation of every returned product would be better supported by an API or data-layer oracle when such a source of truth is available.

### Isolate irrelevant third parties

Automation Exercise serves third-party advertising that can display interstitials and block functional navigation. Because advertisement behavior is not part of the system behavior this project intends to test, known ad requests are blocked centrally at the BrowserContext level.

This keeps third-party handling out of Page Objects and test scenarios and avoids masking the problem with forced clicks, arbitrary waits or navigation workarounds.

In a production system where advertising were part of the product requirements, this isolation decision would need to be reconsidered.

### Distinguish test failures from environment failures

A timeout is not automatically treated as a reason to increase timeouts or add retries. During development, Automation Exercise was observed to become severely degraded even under manual browser navigation. The framework was intentionally not modified to compensate for that temporary external condition.

Retries and timeout changes should be introduced only when their purpose and failure mode are understood.

### Prefer domain-oriented component APIs

Components expose interactions using the language of the UI/domain:

```python
products_page.category.select("Kids", "Dress")
products_page.brand.select("Polo")
```

Categories and brands remain separate components even though both appear in the same sidebar because their interaction models and intent differ. The framework avoids generic abstractions when they would erase meaningful behavior.

## Test identifiers

Scenario comments use domain-based identifiers as lightweight traceability while the project does not yet integrate with a dedicated test-management system.

Examples:

- `PROD-xxx` — product catalog and search
- `CATEGORY-xxx` — category filtering
- `BRAND-xxx` — brand filtering
- `CART-xxx` — shopping cart

The identifier does not replace a descriptive test function name. If the project later integrates reporting or test-management tooling, these identifiers can evolve into structured metadata.

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

## Test target

The UI scenarios use Automation Exercise, a public practice application created for automation testing.

The target application is external to this repository and can change or become unavailable independently. External instability should be diagnosed separately from framework defects.

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
- [ ] Add GitHub Actions continuous integration
- [ ] Add Allure reporting and failure evidence
- [ ] Add linting and static analysis
- [ ] Add browser matrix execution
- [ ] Evaluate parallel execution
- [ ] Expand API/UI integration scenarios
- [ ] Define documented retry criteria

## Next engineering stage

The next phase shifts deliberately from adding more functional scenarios to improving the framework as an engineering system.

1. **GitHub Actions CI** — execute the suite automatically on pushes and pull requests, install dependencies and browser binaries in a clean runner, and make test health visible outside the developer machine.
2. **Failure artifacts** — preserve Playwright traces, screenshots and/or videos for failed CI executions so failures can be diagnosed without reproducing them locally.
3. **Allure reporting** — introduce structured reporting, suites/features and richer execution evidence. Existing lightweight scenario identifiers can later be mapped into reporting metadata where useful.
4. **Linting and static analysis** — automate formatting and code-quality checks instead of relying on manual whitespace/import cleanup.
5. **Execution strategy** — once CI is stable, evaluate browser matrices and parallel execution based on measured cost and value rather than enabling them by default.

## Author

**José Ignacio Reyes Lima**

- GitHub: `jireyes94`
- LinkedIn: `ignacio-reyes-lima`
