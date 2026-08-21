# Framework Architecture

## Purpose

This document describes the architectural boundaries of the QA Automation Framework and the reasoning behind them.

The framework is intentionally structured so test scenarios express business intent while browser mechanics, service communication, test-data generation and execution infrastructure remain isolated behind dedicated abstractions.

The architecture is not intended to maximize abstraction. New layers are introduced only when they provide a clear responsibility boundary or meaningful reuse.

## High-level structure

```text
Tests
  │
  ├── Page Objects
  │       │
  │       └── Component Objects
  │
  ├── API Clients
  │
  └── Fixtures
          │
          ├── Test Data / Factories
          └── Execution Infrastructure
```

Supporting those layers:

```text
Pytest hooks
→ execution observation and failure lifecycle

Playwright
→ browser and HTTP automation

GitHub Actions
→ CI orchestration and artifact persistence
```

## Responsibility boundaries

### Tests

Tests own:

- Scenario intent
- Test-specific input
- Assertions
- Expected business behavior

Tests should describe what is being validated without containing unnecessary browser implementation details.

For example, a test may request a category selection and then assert the resulting state. It should not need to understand how the category accordion is located or expanded.

Tests are also responsible for deciding what constitutes success. Page Objects and Components do not make business assertions on behalf of scenarios.

## Page Objects

Page Objects represent page-level behavior and state.

They encapsulate:

- Page navigation
- Page-level locators
- Page-specific interactions
- Access to reusable components
- Navigation toward other page abstractions

They do not own test expectations.

A Page Object can expose a `Locator` or another domain-relevant object so the test remains responsible for the assertion.

## Component Objects

Component Objects represent reusable or independently meaningful UI regions.

Examples in the framework include:

- Product cards
- Cart items
- Cart modal
- Header
- Category navigation
- Brand navigation

Components are preferred over continuously expanding Page Objects when a region has its own behavior or reusable responsibility.

A component can return another Page Object when its interaction causes navigation.

For example:

```text
ProductCard
    ↓
view details
    ↓
ProductDetailsPage
```

The component owns the interaction.

The resulting Page Object owns the destination interface.

The test owns the expectation.

## Domain-oriented component APIs

Components expose behavior using terminology meaningful to the interface rather than exposing generic browser mechanics.

For example:

```python
products_page.category.select("Kids", "Dress")
products_page.brand.select("Polo")
```

Categories and brands remain separate components even though they occupy a similar area of the application.

Their intent and interaction models are distinct, and merging them into a generic abstraction would reduce clarity merely to remove code.

The framework favors meaningful duplication over abstractions that erase domain behavior.

## API clients

API clients isolate service-level communication from tests and fixtures.

For example, user lifecycle operations are exposed through `UsersClient`.

Tests and fixtures therefore work with operations such as:

```text
create user
delete user
```

without repeatedly defining request URLs, HTTP methods or payload mechanics.

API clients can serve two purposes:

1. Direct API test coverage
2. Infrastructure supporting UI scenarios

The second use is particularly important for efficient setup and cleanup.

## API-driven UI preconditions

A UI scenario should not necessarily create all of its preconditions through the UI.

For authentication coverage, the behavior under test is login.

User registration is therefore setup rather than the scenario itself.

The framework creates the required user through the API:

```text
Fixture
   ↓
UserFactory
   ↓
UsersClient
   ↓
create account
   ↓
yield UserData
   ↓
UI login test
   ↓
fixture teardown
   ↓
delete account
```

This reduces execution cost and isolates the UI scenario around the behavior it actually intends to validate.

## Test-data factories

Test-data generation is separated from service communication.

The user factory owns creation of valid user data.

The API client owns communication with the target service.

This distinction prevents the client from becoming responsible for deciding what test data should exist and prevents tests from manually constructing large payloads.

The resulting flow is:

```text
UserFactory
→ creates data

UsersClient
→ sends data

Fixture
→ coordinates lifecycle

Test
→ consumes prepared state
```

## Fixtures

Fixtures coordinate reusable test lifecycle and infrastructure.

Examples include:

- Playwright request contexts
- API clients
- Registered users
- Browser-level setup
- Test cleanup

Fixtures are used when setup or teardown represents reusable execution infrastructure rather than scenario intent.

They should not become containers for arbitrary business assertions.

Infrastructure assertions can still exist where required to guarantee that a precondition was successfully created before a test continues.

## Shared and UI-specific configuration

Framework fixtures are separated according to scope.

The root `conftest.py` contains shared infrastructure such as API-related fixtures.

UI-specific execution behavior lives under:

```text
tests/ui/conftest.py
```

This distinction became particularly important in CI.

A previous global UI dependency could force browser infrastructure to exist even when only API tests were running.

Separating UI-specific fixtures prevents API execution from accidentally depending on a browser.

## Pytest hooks and failure lifecycle

Pytest hooks observe test execution when behavior must react to the final test outcome.

Failure evidence is one example.

The framework needs to know whether a test failed before deciding whether its trace and screenshot should be persisted.

That responsibility does not belong inside every test.

The execution lifecycle is therefore coordinated centrally:

```text
test starts
    ↓
Playwright tracing starts
    ↓
test executes
    ↓
pytest report determines outcome
    ↓
PASS ───────────────→ stop trace / discard evidence
    │
    └── FAIL ───────→ capture screenshot
                      persist trace
                      attach evidence
```

This keeps reporting and observability concerns out of scenario implementations.

## Failure evidence responsibility

Failure evidence is produced by the execution layer:

```text
Pytest + Playwright
```

GitHub Actions does not generate screenshots or traces.

The separation is:

```text
Pytest / Playwright
        ↓
detect failure
        ↓
generate evidence
        ↓
filesystem
        ↓
GitHub Actions
        ↓
persist artifact
```

This matters because the CI runner understands jobs and files, but it does not understand which page, locator, browser action or assertion caused a scenario failure.

## CI architecture

GitHub Actions provides orchestration rather than test behavior.

The pipeline separates:

```text
api-tests
code-quality
ui-tests
```

The UI job uses a browser matrix:

```text
ui-tests
    ├── chromium
    ├── firefox
    └── webkit
```

Each matrix execution receives an isolated runner and installs only the required browser.

This structure provides several benefits:

- API execution remains independent from browsers
- Browser compatibility is explicit
- Browser failures are independently visible
- Browser-specific evidence can be preserved
- Matrix jobs can execute concurrently
- A single UI job definition avoids YAML duplication

`fail-fast` is disabled for the browser matrix.

If one browser fails, the remaining engines continue executing so the pipeline retains the maximum diagnostic information.

## Code-quality architecture

Static analysis is separated into complementary responsibilities.

### Ruff lint

Detects code-quality issues such as unused imports and import organization problems.

### Ruff formatter

Provides deterministic Python formatting.

### mypy

Validates static type contracts between framework components and external APIs.

These checks run locally and in CI.

CI deliberately performs validation only:

```text
ruff check .
ruff format --check .
mypy .
```

It does not automatically modify submitted code.

A CI run should evaluate the exact commit proposed for integration rather than silently create a different version of that code.

## Architectural principles

The framework follows several general rules:

1. Test intent remains visible in tests.
2. Browser mechanics belong behind page or component abstractions.
3. Service communication belongs behind API clients.
4. Data generation and data transport remain separate responsibilities.
5. Fixtures coordinate reusable lifecycle rather than scenario behavior.
6. Execution-level concerns are centralized rather than repeated in tests.
7. CI orchestrates and persists; it does not own test behavior.
8. Abstractions are introduced to clarify responsibilities, not merely to reduce line count.
9. External instability should not be hidden through framework complexity.
10. Architectural decisions should remain explainable and defensible.