# Testing Strategy

## Purpose

This document describes the testing decisions behind the QA Automation Framework.

The strategy intentionally prioritizes meaningful validation, reproducibility and diagnosability over raw test count.

Automation is treated as an engineering system rather than a collection of browser scripts.

## Testing layers

The framework currently exercises two primary layers:

```text
API
UI
```

These layers are not treated as isolated worlds.

API operations can support UI scenarios when service-level setup is faster and more deterministic than reproducing the same precondition through the browser.

## UI testing

UI tests validate behavior where browser interaction or rendered application state is relevant.

Current UI coverage includes:

- Authentication
- Product catalog
- Search
- Product details
- Category filtering
- Brand filtering
- Shopping cart behavior
- Cross-page consistency

UI tests are intentionally not used for every possible validation.

When a behavior can be established more reliably below the UI, a service or data-layer oracle would generally be preferred.

## API testing

API tests validate service behavior directly and provide reusable infrastructure for higher-level scenarios.

The current framework exercises user lifecycle operations and uses the same API abstraction to support UI preconditions and cleanup.

This avoids duplicating communication logic between API tests and UI fixtures.

## API-driven setup

UI setup should not automatically be performed through the UI.

For example:

```text
Behavior under test
→ Login

Required precondition
→ Existing user
```

Registering that user through multiple UI screens would increase execution time and introduce unrelated failure points.

The framework therefore creates the user through the API before the login scenario and removes it afterward.

The principle is:

> Use the lowest practical layer for setup while exercising the behavior under test at the layer where it matters.

## Assertions and test oracles

More assertions do not automatically create stronger tests.

An assertion should represent behavior that is known, observed and defensible as part of the expected contract.

The framework avoids converting assumptions into test oracles.

### Empty search example

The empty-search scenario verifies that the application remains in the `All Products` state.

It does not automatically assert that:

- Catalog size is identical
- Product ordering is identical
- Every product identity remains identical

Those properties have not been established as invariants.

If the catalog later becomes dynamic, such assertions could produce false failures despite correct application behavior.

## Collection validation

When a requirement applies to every returned result, validating one hardcoded result is insufficient.

Product search is treated as substring matching.

The framework obtains the returned product collection and verifies that every result satisfies the search condition.

Conceptually:

```text
search("blue")
      ↓
returned ProductCards
      ↓
for every card
      ↓
"blue" must exist in normalized product name
```

This prevents an incorrect result from being hidden by the presence of one expected product.

## Input partitioning and parametrization

Equivalent input variations should not require duplicated scenario implementations.

Search behavior is exercised with lower- and upper-case inputs using parametrization.

This validates case-insensitive behavior while preserving one test definition for the same behavioral partition.

Parametrization is used when inputs represent meaningful variations of the same scenario rather than unrelated behaviors.

## Representative validation

Not every collection should be exhaustively traversed through the UI.

Category and brand membership are not exposed directly by product cards, while Product Details exposes those attributes.

The framework therefore validates:

1. Correct navigation/state
2. Returned results exist
3. A representative result exposes the expected category or brand through Product Details

It does not navigate through every returned product solely to simulate exhaustive coverage.

If complete collection membership needed to be proven, a reliable API or data-layer oracle would be preferable.

## Cross-page consistency

Some scenarios validate that data remains consistent while moving between application surfaces.

For example:

```text
Product catalog
    ↓
name + price
    ↓
add to cart
    ↓
Cart
    ↓
same name + price
```

This provides more meaningful validation than checking only whether a button was clickable or navigation occurred.

## Third-party isolation

Automation Exercise includes third-party advertising that can interfere with functional navigation.

Known advertising requests are blocked centrally through the Playwright `BrowserContext`.

This decision is based on scope:

```text
Application behavior under test
≠
third-party advertising behavior
```

Central isolation is preferred over:

- Forced clicks
- Arbitrary sleeps
- Test-specific ad handling
- Navigation workarounds

Those approaches would spread an infrastructure problem throughout the test suite.

If advertising behavior were part of the actual product requirements, this isolation strategy would need to be reconsidered.

## External environment failures

The target application is external to the repository.

It can become overloaded, unavailable or degraded independently of framework changes.

Observed failures during development have included service overload responses and Cloudflare/origin errors.

A failed automated test therefore does not automatically imply:

```text
framework defect
or
application defect
```

Diagnosis is required.

The framework deliberately avoids responding to temporary environmental instability by immediately increasing timeouts or adding retries.

## Retry philosophy

Retries can improve resilience when they address a known transient failure mode.

They can also hide real instability.

The current strategy is therefore conservative:

```text
failure
   ↓
diagnose
   ↓
classify
   ↓
only then consider retry behavior
```

A timeout alone is not sufficient justification for a retry.

Formal retry criteria remain a future engineering decision.

## Failure observability

A failure should provide enough evidence to distinguish:

- Test defect
- Framework defect
- Application defect
- External/environmental failure

Failed UI tests therefore generate two complementary forms of evidence.

### Screenshot

Provides fast visual triage of the final browser state.

Useful for identifying conditions such as:

- Unexpected page
- Error page
- Missing UI
- Overlay
- External service failure

### Playwright trace

Provides deeper execution reconstruction.

A trace can expose:

- Browser actions
- DOM snapshots
- Timing
- Network activity
- Navigation
- Execution context

The screenshot answers:

```text
What did the browser look like?
```

The trace helps answer:

```text
How did execution reach that state?
```

## Evidence lifecycle

Tracing starts before UI execution so history exists if the scenario fails.

Evidence is persisted selectively:

```text
PASS
→ stop tracing
→ discard trace
→ no failure screenshot

FAIL
→ capture screenshot
→ persist trace
→ attach evidence to Allure
→ make files available to CI
```

This avoids storing unnecessary diagnostic data for successful executions.

## Allure reporting

Allure provides a structured view over test execution.

Tests are enriched with business-oriented metadata such as:

```text
Feature
Story
```

For example:

```text
Feature → Product Catalog
Story   → Search
```

Technical markers such as `ui` and `api` remain useful for execution selection but do not replace business-oriented reporting metadata.

Allure results expose:

- Test status
- Execution duration
- Setup / test / teardown phases
- Labels
- Environment information
- Failure information
- Attachments

Failure screenshots and traces are attached directly to the failed test result.

This keeps evidence close to the scenario that produced it.

## GitHub Actions artifacts

CI runners are disposable.

Files that must survive execution therefore need an external persistence mechanism.

GitHub Actions artifacts preserve generated reports and failure evidence after a runner has been destroyed.

Allure reports are uploaded for every UI browser execution.

Browser-specific naming prevents ambiguity:

```text
allure-report-ui-chromium
allure-report-ui-firefox
allure-report-ui-webkit
```

Failure evidence is similarly associated with its browser execution.

## Cross-browser strategy

The complete UI suite currently runs against:

- Chromium
- Firefox
- WebKit

The purpose is not merely to demonstrate that Playwright supports multiple browsers.

The browser matrix validates that framework abstractions and scenarios are not accidentally coupled to one browser engine.

### Local development

Chromium can remain the primary fast feedback browser during ordinary development.

Specific engines can be selected when validating compatibility or investigating engine-specific behavior.

### Continuous integration

CI expands one UI job definition through a GitHub Actions matrix:

```text
browser:
├── chromium
├── firefox
└── webkit
```

This avoids maintaining three duplicated workflows.

`fail-fast` is disabled.

If WebKit fails, Chromium and Firefox are still allowed to finish.

For QA, the complete compatibility picture is more useful than stopping immediately after the first matrix failure.

## CI strategy

Pull requests targeting `main` are validated through independent responsibilities:

```text
api-tests
code-quality
ui-tests (chromium)
ui-tests (firefox)
ui-tests (webkit)
```

These jobs can execute independently.

The API job does not install browsers.

The UI jobs install only their selected browser engine.

The code-quality job does not execute functional scenarios.

This separation improves both execution clarity and failure diagnosis.

## Code-quality gates

Functional correctness is not the only property validated before integration.

The pipeline also checks:

```text
Ruff lint
Ruff formatting
mypy
```

CI does not apply automatic fixes.

The expected workflow is:

```text
developer writes code
        ↓
local tooling can fix/format
        ↓
commit
        ↓
CI validates exact commit
        ↓
PASS or FAIL
```

Allowing CI to silently repair submitted code would mean the pipeline was evaluating a modified state that was never committed.

## Test identifiers

Scenario comments use lightweight domain identifiers.

Examples include:

- `PROD-xxx`
- `CATEGORY-xxx`
- `BRAND-xxx`
- `CART-xxx`

These identifiers provide basic traceability without replacing descriptive test function names.

If a dedicated test-management system is introduced later, the identifiers can evolve into structured external references.

## Current strategy boundaries

The framework deliberately does not attempt to solve every testing problem.

Current boundaries include:

- No indiscriminate retry policy
- No artificial expansion of UI test count
- No exhaustive UI traversal when a better oracle would be required
- No abstraction introduced solely to remove small amounts of duplication
- No CI-side automatic code modification

Potential future work includes:

1. Selected API/UI cross-layer scenarios where service data provides a stronger UI oracle
2. Evaluation of parallel test execution
3. Formal documented retry criteria

Each addition should be justified by a concrete testing or engineering need rather than by tool availability.

## Guiding principle

The framework treats automation as a system for producing trustworthy information.

A useful automated test should not merely fail.

It should make it possible to understand:

```text
what behavior was expected
what actually happened
where the failure occurred
what evidence exists
whether the problem belongs to the test, framework, application or environment
```

That principle guides test design, architecture, reporting and CI decisions throughout the project.