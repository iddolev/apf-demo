# Test Plan — Color Button Demo

---

<a id="document-control"/>

## 1. Document Control

- **Product / Feature Name:** Color Button Demo
- **Version:** 0.1
- **Status:** Approved
- **Author(s):** Iddo Lev
- **Last Updated:** 2026-03-24 21:40
- **Related TSD:** [TSD v0.1](../specs/TSD_v0.1.md)
- **Related PRD:** [PRD v0.1](../specs/PRD_v0.1.md)
- **Related Implementation Plan:** [Implementation Plan v0.1](implementation-plan_v0.1.md)

---

## Table of Contents

- [1. Document Control](#document-control)
- [2. Scope & Objectives](#scope-objectives)
- [3. Requirements Traceability](#requirements-traceability)
- [4. Test Strategy](#test-strategy)
- [5. Test Cases](#test-cases)
- [6. Open Questions](#open-questions)

---

<a id="scope-objectives"/>

## 2. Scope & Objectives

### 2.1 In Scope

- Flask backend: `GET /` and `GET /random-color` endpoints
- Frontend: button rendering, click handler, DOM update, `alert()` popup
- Integration: full button-click flow (browser → Flask → browser)
- Error path: frontend behaviour when backend is unreachable
- Non-functional: keyboard accessibility (FR keyboard NFR), response latency (manual)

### 2.2 Out of Scope

- Color history, transitions, or any feature listed as out of scope in PRD §7.2
- Browser compatibility beyond Chrome (manual) — PRD lists Chrome/Firefox/Safari but this
  is a solo MVP; Chrome is the primary target
- Performance load testing (single local user, no SLOs requiring automation)
- Security testing (no auth, no user data, no network exposure)
- Accessibility compliance beyond "button is keyboard-focusable and activatable"

### 2.3 Objectives

- Verify all six PRD functional requirements (FR-01–FR-06) pass
- Verify the TSD API contract (`GET /random-color` → `{ name, code }`) is correctly implemented
- Confirm the frontend error path (backend offline → user-visible alert)
- Confirm the button is keyboard-accessible (PRD NFR)

---

<a id="requirements-traceability"/>

## 3. Requirements Traceability

| PRD Ref | Requirement Summary | Test Case ID(s) | Type | Status |
|--------:|---------------------|-----------------|------|--------|
| FR-01 | Centered button on page load | TC-05 | Manual | — |
| FR-02 | `GET /random-color` returns `{ name, code }` JSON | TC-01, TC-02, TC-03 | Automated | — |
| FR-03 | Click triggers fetch to `/random-color` | TC-06 | Manual | — |
| FR-04 | Button background updates to returned color code | TC-07 | Manual | — |
| FR-05 | Popup shows "Changed the color to \<color_name\>" | TC-08 | Manual | — |
| FR-06 | Repeated clicks each fetch a new color | TC-09 | Manual | — |

### 3.1 Risk-Based Focus Areas

- **Error path (TC-10):** Backend offline → frontend must show the correct alert text. This is
  the only "failure mode" in the TSD (§7.1) and is explicitly required by PRD §8.2 and §9.3.
- **Alert text exactness (TC-08):** The PRD requires the exact string
  `"Changed the color to <color_name>"`. A subtle wording difference would be a FR-05 failure.

---

<a id="test-strategy"/>

## 4. Test Strategy

### 4.1 Approach

The project has two independently testable components (TSD §4.2): the Flask backend and the
static frontend. Backend logic is covered by automated tests using the Flask test client (no
live server required). Frontend and integration behaviour — DOM updates, `alert()` calls,
user interaction — requires a real browser and is covered by a manual checklist.

### 4.2 Test Levels & Coverage

| Level | Scope | Tool(s) | What is Mocked / Isolated | Coverage Target |
|-------|-------|---------|---------------------------|-----------------|
| Automated (integration) | Flask routes (`GET /`, `GET /random-color`) | pytest, Flask test client (`app.test_client()`) | Nothing — real Flask app, in-memory color list | All backend endpoints; color palette validation |
| Manual E2E | Full button-click flow in browser | Chrome (manual) | Nothing — real Flask server running locally | All FR-01–FR-06; error path; keyboard NFR |

### 4.3 Mocking & Test Isolation

- **Automated tests:** No mocking needed. The Flask test client exercises the real route
  handlers against the real in-memory color list. `random.choice()` is not mocked — instead,
  tests assert that the response is *a member of the known palette* rather than a specific value.
- **Manual tests:** Run against a live `python app.py` instance on `localhost:5000`.

### 4.4 Test Infrastructure & Tooling

| Tool | Purpose | Version |
|------|---------|---------|
| pytest | Test runner for automated backend tests | latest (via pip) |
| Flask test client | In-process HTTP client for Flask routes | bundled with Flask 3.x |
| Chrome | Manual E2E browser testing | latest stable |

---

<a id="test-cases"/>

## 5. Test Cases

### 5.1 Flask Backend

> `app.py` — Flask routes. Ref TSD §6.1, §6.2. Depends on WP-02, WP-03.

| ID | Test Case | Category | Type | Priority | Expected Result | Depends On | Automated |
|----|-----------|----------|------|----------|-----------------|------------|-----------|
| TC-01 | `GET /random-color` returns HTTP 200 | core | automated | P1 | Status code is 200; `Content-Type` is `application/json` | WP-02, WP-03 | Yes |
| TC-02 | Response body has `name` (non-empty string) and `code` (valid CSS hex) | core | automated | P1 | JSON contains `name` (non-empty `str`) and `code` matching regex `^#[0-9A-Fa-f]{6}$` | WP-03 | Yes |
| TC-03 | Returned color is from the defined 20-color palette (TSD §8.2) | core | automated | P1 | `name` and `code` match one of the 20 palette entries exactly | WP-03 | Yes |
| TC-04 | `GET /` returns `index.html` with HTML content-type | core | automated | P1 | Status code is 200; `Content-Type` starts with `text/html`; body is non-empty | WP-02 | Yes |

### 5.2 Frontend / JavaScript

> `static/index.html` — button rendering, click handler, DOM updates, `alert()`. Ref TSD §7.1.
> Depends on WP-04.

| ID | Test Case | Category | Type | Priority | Expected Result | Depends On | Automated |
|----|-----------|----------|------|----------|-----------------|------------|-----------|
| TC-05 | Button is visually centered on page load | core | manual | P1 | Button appears horizontally and vertically centered in the viewport on a default-size Chrome window | WP-04 | No |
| TC-06 | Clicking the button triggers a `GET /random-color` network request | core | manual | P1 | Chrome DevTools Network tab shows a `GET /random-color` request fired on each button click | WP-03, WP-04 | No |
| TC-07 | Button background changes to the returned color code | core | manual | P1 | Button's background color visibly changes to the color returned by the API; `button.style.backgroundColor` matches the hex code | WP-03, WP-04 | No |
| TC-08 | Popup shows exact message "Changed the color to \<color_name\>" | core | manual | P1 | `alert()` dialog text is exactly `"Changed the color to Coral"` (or whichever color was returned); no extra words or punctuation | WP-03, WP-04 | No |
| TC-09 | Repeated clicks each fetch a new color and show the popup | core | manual | P1 | Three consecutive clicks each trigger a network request, update the button color, and show the alert | WP-03, WP-04 | No |
| TC-10 | Backend offline → error alert displayed | error | manual | P1 | With Flask stopped, clicking the button shows `alert("Error: could not fetch color. Please try again.")` and does **not** crash or silently fail | WP-04 | No |
| TC-11 | Button is keyboard-focusable and activatable | edge | manual | P2 | Tab key focuses the button (visible focus ring); pressing Enter or Space triggers the same color-change and alert behaviour as a mouse click | WP-04 | No |

### 5.3 Manual E2E Checklist

> Run with `python app.py` on `localhost:5000`, Chrome (latest stable).

- [ ] **TC-05** — Page loads; button is centered. No console errors on load.
- [ ] **TC-06** — Click button; Network tab shows `GET /random-color` request.
- [ ] **TC-07** — Button background changes to a color from the palette.
- [ ] **TC-08** — Alert text is exactly `"Changed the color to <name>"`.
- [ ] **TC-09** — Click 3 more times; each click changes color and shows alert.
- [ ] **TC-10** — Stop Flask (`Ctrl+C`); click button; alert shows error message.
- [ ] **TC-11** — Tab to button; press Enter; color changes and alert appears.
- [ ] **Performance** — Visually, color change and alert appear near-instantly (< 1s subjectively on
  localhost).

---

<a id="open-questions"/>

## 6. Open Questions

No open questions — all testing concerns are resolved by the TSD and PRD.

---

## Change Log

- *v0.1 - 2026-03-24 21:40* - Initial skeleton by Iddo Lev
