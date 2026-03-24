# Project Rules

## Purpose

This document defines project-specific coding and design conventions that all agents must follow.
These rules complement the general `PROGRAMMING-PRINCIPLES.md` —
they capture conventions unique to this project that emerge from the TSD's technology
choices, design principles, and API contracts.

---

## 1. Language & Framework Conventions

- Backend: Python 3.11+, Flask 3.x. Follow PEP 8 (snake_case for functions/variables,
  UPPER_CASE for constants, PascalCase for classes).
- Frontend: Vanilla JS (ES6+). Use `fetch()` with `async/await`. No third-party libraries
  or frameworks.
- Never add a frontend framework or JS build step — the project must remain plain HTML/JS.

## 2. API & Interface Conventions

- `GET /random-color` must always return `{ "name": string, "code": string }` with HTTP 200.
  No other fields. No query parameters.
- The frontend treats any non-200 response or network error as a failure; show the exact
  error alert text from TSD §7.1.
- No new endpoints unless explicitly added to the TSD.

## 3. Data & Storage Conventions

- The color palette is a hardcoded constant in `app.py`. Never read it from a file,
  database, or environment variable.
- Never mutate the color list at runtime.

## 4. Error Handling Conventions

- Frontend: on fetch failure (any exception or non-200), always call
  `window.alert("Error: could not fetch color. Please try again.")` — exact text, no variations.
- Never silently swallow errors on either the frontend or backend.

## 5. Naming Conventions

- Python files: `snake_case.py`. Flask route paths: `kebab-case` (e.g., `/random-color`).
  JSON fields: lowercase (`name`, `code`).
- JS variables/functions: `camelCase`. HTML IDs/classes: `kebab-case`.
- Test files: `test_<module>.py` in the project root or a `tests/` directory.

## 6. Testing Conventions

- Automated tests use pytest + Flask test client (`app.test_client()`). Never spin up a
  live server for automated tests.
- Do not mock `random.choice()` — assert that the result is a member of the known palette
  instead.
- Each test must be independent (no shared mutable state between tests).

## 7. Security Conventions

See `rules/SECURITY-CONVENTIONS.md` (if applicable).
