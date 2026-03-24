# Technical Specifications Document (TSD)

---

<a id="document-control"/>

## 1. Document Control

- **Product / Feature Name:** Color Button Demo
- **Technical One-liner:** Single-page frontend calling a local Python/Flask REST API that returns a
  random named color; the button updates its background color and shows a popup.
- **Version:** 0.1
- **Status:** Approved
- **Author(s):** Iddo Lev
- **Reviewers:** Iddo Lev
- **Last Updated:** 2026-03-24 19:09
- **Primary Engineer / Tech Lead:** Iddo Lev
- **Target Release Date:** TBD
- **Related PRD:** [PRD v0.1](PRD_v0.1.md)
- **Related Docs / Links:** N/A

---

## Table of Contents

- [1. Document Control](#document-control)
- [2. Executive Summary & Scope](#executive-summary-scope)
- [3. PRD Traceability](#prd-traceability)
- [4. System Architecture](#system-architecture)
- [5. Technology Stack & Environments](#technology-stack-environments)
- [6. API & Interface Contracts](#api-interface-contracts)
- [7. Core Technical Flows & Logic](#core-technical-flows-logic)
- [8. Business Rules & Validation](#business-rules-validation)
- [9. Security](#security)
- [10. Risks & Open Questions](#risks-open-questions)
- [11. Decision Log](#decision-log)
- [12. Appendix](#appendix)

---

<a id="executive-summary-scope"/>

## 2. Executive Summary & Scope

### 2.1 Technical Summary

- **Objective:** Build a minimal full-stack web app (frontend + backend) to validate the APF agentic
  workflow end-to-end.
- **High-Level Solution:** A Flask application serves a static `index.html` at `GET /` and exposes
  `GET /random-color`. The page contains a centered button; clicking it fetches a random named color
  from the backend, updates the button's background, and shows a browser `alert` with the color
  name.
- **Key Trade-offs / Decisions:** Serving the frontend from Flask (same origin) eliminates CORS
  complexity. Plain HTML/JS (no framework) minimizes dependencies. Browser `alert()` for the popup
  avoids any UI component library.

### 2.2 Scope & Assumptions

- **In Scope:** Flask backend with one API endpoint; static HTML/CSS/JS frontend; single local-dev
  environment.
- **Out of Scope:** Persistent storage, user authentication, color history, animated transitions,
  native mobile, color picker.
- **Assumptions:** Developer runs Python 3.11+ locally; app is accessed in a modern desktop browser.
- **Constraints:** All dependencies installable via pip; startup via `python app.py`; no external
  services.

---

<a id="prd-traceability"/>

## 3. PRD Traceability

| PRD Ref | Requirement Summary | Implementation Surface | TSD Section(s) | Notes |
|--------:|---------------------|------------------------|----------------|-------|
| FR-01 | Display a centered button on the page | `static/index.html` — CSS flexbox centering | §4, §7 | |
| FR-02 | `GET /random-color` returns `{ name, code }` | `app.py` — Flask route | §6 | |
| FR-03 | Frontend calls `/random-color` on button click | `static/index.html` — JS `fetch()` | §7 | |
| FR-04 | Button background changes to returned color code | `static/index.html` — JS DOM update | §7 | |
| FR-05 | Popup shows "Changed the color to \<color_name\>" | `static/index.html` — `window.alert()` | §7, §8 | |
| FR-06 | Repeated clicks fetch a new color each time | Stateless API + JS event listener | §7 | |

---

<a id="system-architecture"/>

## 4. System Architecture

### 4.1 System Context

A single Python process runs Flask locally. The browser loads the page from Flask and makes
XHR/fetch calls to the same Flask process. No external services, no database, no CDN.

```
Browser
  │  GET /          → index.html (static)
  │  GET /random-color → { name, code }
  └──────────────────────────────────────
              Flask (localhost:5000)
                 app.py
```

### 4.2 Component Overview

| Component | Type | Responsibility | Tech | Statefulness |
|-----------|------|----------------|------|--------------|
| Flask app | Backend process | Serves static frontend; exposes `/random-color` API | Python 3.11, Flask 3.x | Stateless (color list in memory as constant) |
| Frontend page | Static HTML/JS/CSS | Renders button; calls API; updates DOM; shows popup | HTML5, CSS3, Vanilla JS (ES6) | Ephemeral (button color held in DOM only) |

### 4.3 Data Flow

1. Developer runs `python app.py`; Flask starts on `localhost:5000`.
2. Browser navigates to `http://localhost:5000/` → Flask serves `static/index.html`.
3. User clicks the button → JS calls `fetch('/random-color')`.
4. Flask selects a random color from its in-memory list → returns `{ "name": "Coral", "code":
   "#FF7F50" }`.
5. JS sets `button.style.backgroundColor = code` → calls `alert("Changed the color to Coral")`.

### 4.4 Key Design Decisions

| Decision | Options Considered | Chosen Option | Rationale |
|----------|--------------------|---------------|-----------|
| File serving | Flask serves frontend vs. separate file server vs. open HTML directly | Flask serves `static/index.html` | Same origin eliminates CORS; single `python app.py` starts everything |
| Popup implementation | Browser `alert()` vs. custom modal | `alert()` | Zero dependencies; simplest; PRD allows it |
| Color storage | Hardcoded list vs. file vs. DB | Hardcoded Python list in `app.py` | No persistence needed; trivial to change |

---

<a id="technology-stack-environments"/>

## 5. Technology Stack & Environments

### 5.1 Languages, Frameworks, and Libraries

| Layer | Technology | Version | Rationale |
|-------|------------|---------|-----------|
| Backend | Python | 3.11+ | Widely available; matches `python app.py` startup constraint |
| Backend framework | Flask | 3.x | Minimal boilerplate; single-file app; `pip install flask` |
| Frontend | HTML5 / CSS3 / Vanilla JavaScript | ES6+ | No framework needed; PRD requires no third-party libraries |

### 5.2 Runtime Environments

| Environment | Purpose | Notes |
|-------------|---------|-------|
| Local Dev | Development and manual testing | `python app.py`; browser at `http://localhost:5000` |

### 5.3 Configuration Management

- Flask `debug=True` for local dev (hot reload).
- Port defaults to `5000`; can be overridden via `PORT` environment variable.
- No secrets or external config required.

---

<a id="api-interface-contracts"/>

## 6. API & Interface Contracts

### 6.1 Endpoint: `GET /random-color`

- **Purpose:** Return one randomly selected named color from the backend's color list.
- **Authorization:** None.
- **Request:** No body or query parameters.
- **Response (200 OK):**

```json
{
  "name": "Coral",
  "code": "#FF7F50"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Human-readable color name (e.g. `"Coral"`) |
| `code` | string | CSS-compatible hex color value (e.g. `"#FF7F50"`) |

- **Error Cases:** Flask returns HTTP 500 only on an unhandled exception (should never occur given a
  hardcoded list). The frontend treats any non-200 response as an error.
- **CORS:** Not required — frontend is served from the same Flask origin.

### 6.2 Endpoint: `GET /`

- **Purpose:** Serve the frontend page.
- **Response:** `static/index.html` with `Content-Type: text/html`.

---

<a id="core-technical-flows-logic"/>

## 7. Core Technical Flows & Logic

### 7.1 Flow: Button Click → Color Change

- **Trigger:** User clicks the button element.
- **Steps:**
  1. JS `click` event listener fires.
  2. `fetch('/random-color')` is called (async).
  3. While the request is in flight, the button remains interactive (no loading state required —
     response is near-instant on localhost).
  4. On success (HTTP 200): parse JSON → set `button.style.backgroundColor = data.code` → call
     `window.alert("Changed the color to " + data.name)`.
  5. On failure (non-200 or network error): call `window.alert("Error: could not fetch color. Please
     try again.")`.
- **Failure Modes:**
  - Backend unreachable (not started): `fetch` rejects → error branch → alert shown.
  - Backend returns non-200: response check fails → error branch → alert shown.

---

<a id="business-rules-validation"/>

## 8. Business Rules & Validation

### 8.1 Random Color Selection

- The backend selects one color uniformly at random from its color list using Python's
  `random.choice()`.
- No de-duplication: the same color may be returned on consecutive clicks (PRD UC-1 explicitly
  allows this).

### 8.2 Color Palette

The backend holds the following hardcoded named colors:

| Name | Hex Code |
|------|----------|
| Coral | #FF7F50 |
| Teal | #008080 |
| Crimson | #DC143C |
| Goldenrod | #DAA520 |
| SlateBlue | #6A5ACD |
| OrangeRed | #FF4500 |
| MediumSeaGreen | #3CB371 |
| DeepSkyBlue | #00BFFF |
| HotPink | #FF69B4 |
| DarkOrange | #FF8C00 |
| MediumOrchid | #BA55D3 |
| LimeGreen | #32CD32 |
| DodgerBlue | #1E90FF |
| Tomato | #FF6347 |
| SteelBlue | #4682B4 |
| Gold | #FFD700 |
| MediumVioletRed | #C71585 |
| DarkTurquoise | #00CED1 |
| Chocolate | #D2691E |
| ForestGreen | #228B22 |

Colors are chosen to be visually distinct and have high contrast with white button text.

---

<a id="security"/>

## 9. Security

- No user data is collected or transmitted.
- No cookies, sessions, or authentication.
- Backend exposes no sensitive information — only color names and hex codes.
- API keys: none required.
- Local-only: the app is not intended to be exposed to a network; `debug=True` is acceptable for
  this scope.

---

<a id="risks-open-questions"/>

## 10. Risks & Open Questions

### 10.1 Risks

| Risk | Likelihood | Impact | Mitigation | Owner |
|------|-----------|--------|------------|-------|
| Flask debug mode exposed on a network | L | M | App is local-only; document in README that debug mode must be disabled before any network exposure | Iddo Lev |
| Browser blocks `alert()` (e.g. in iframes) | L | L | App is served as a top-level page; `alert()` works in all modern browsers in this context | Iddo Lev |

### 10.2 Open Questions

No open questions — all PRD-deferred technical decisions resolved in this TSD.

---

<a id="decision-log"/>

## 11. Decision Log

| ID | Timestamp | Decision | Rationale | Owner |
|----|-----------|----------|-----------|-------|
| D-001 | 2026-03-24 19:09 | Flask serves frontend from `static/` (same origin) | Avoids CORS; single startup command | Iddo Lev |
| D-002 | 2026-03-24 19:09 | Browser `alert()` for popup | Simplest; no dependencies; PRD allows it | Iddo Lev |
| D-003 | 2026-03-24 19:09 | Hardcoded 20-color palette in `app.py` | No DB needed; easily extensible | Iddo Lev |
| D-004 | 2026-03-24 19:09 | Vanilla JS — no frontend framework | PRD: no third-party libraries; app is too small to warrant a framework | Iddo Lev |

---

<a id="appendix"/>

## 12. Appendix

### Glossary

| Term | Definition |
|------|------------|
| TSD | Technical Specifications Document — the detailed technical blueprint for implementing a product feature or system. |
| PRD | Product Requirements Document — defines what is being built and why. |
| CORS | Cross-Origin Resource Sharing — a browser security mechanism that controls which origins can make HTTP requests to a server. |
| Flask | A lightweight Python web framework for building web applications and APIs. |
| ES6 | ECMAScript 2015 — a version of JavaScript that introduced `fetch`, arrow functions, `const`/`let`, and template literals. |
| DOM | Document Object Model — the browser's in-memory representation of an HTML page, manipulated by JavaScript. |
| Vanilla JS | Plain JavaScript with no external libraries or frameworks. |
| APF | Agentic Programming Framework — the workflow this project is designed to demonstrate. |

### Change Log

| Version | Timestamp | Author | Changes |
|---------|-----------|--------|---------|
| 0.1 | 2026-03-24 18:56 | Iddo Lev | Initial skeleton |
| 0.1 | 2026-03-24 19:09 | Iddo Lev | Full draft — all sections written |
