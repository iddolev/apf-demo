# Color Button Demo

A minimal full-stack web app: click a button to fetch a random named color from a local Flask API —
the button updates its background color and a popup displays the color name.
Built as a demo to validate the [Agentic Programming Framework (APF)](https://github.com/iddolev/apf) end-to-end.

## Prerequisites

- Python 3.11+
- A modern desktop browser (Chrome recommended)

## Installation

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the App

```bash
python app.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

The port can be overridden via the `PORT` environment variable.

## Testing

- **Automated (backend):** `pytest`
- **Manual (integration):** See `docs/plans/test-plan_v0.1.md` for the full manual test checklist
  (TC-05 through TC-10 cover the end-to-end button-click flow and error path).

## Project Structure

See `docs/PROJECT-STRUCTURE.md`.

## Documentation

- **PRD:** `docs/specs/PRD_v0.1.md`
- **TSD:** `docs/specs/TSD_v0.1.md`
- **Implementation Plan:** `docs/plans/implementation-plan_v0.1.md`
- **Test Plan:** `docs/plans/test-plan_v0.1.md`

## Agentic Programming

This project is built using the Agentic Programming Framework (APF) —
a methodology toolkit that guides AI-assisted development through a structured pipeline:
PRD, TSD, Implementation Plan, Test Plan, and agent setup,
and then an orchestration of the agents.

Look at `README.apf.md` for more information on how APF is used in this project.

The general framework lives here: [APF on GitHub](https://github.com/iddolev/apf/tree/main).
It contains:

- Templates and instructions for creating spec and planning documents
- Agent definitions for Claude Code (tech lead, backend specialist, etc.)
- Shared context, rules, and knowledge files that keep all agents aligned

For details on the framework itself, see [APF's README](https://github.com/iddolev/apf/blob/main/README.md).
