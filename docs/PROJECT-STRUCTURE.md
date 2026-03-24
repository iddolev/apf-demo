# Project Structure

```
apf-demo/
├── app.py                     # Flask application entry point; serves static frontend
│                              # and exposes GET /random-color
├── requirements.txt           # Python dependencies (Flask 3.x)
├── README.md                  # Project overview and setup instructions
├── README.apf.md              # APF-specific usage notes
│
├── static/
│   └── index.html             # Single-page frontend: button, CSS, JS fetch logic
│
├── docs/
│   ├── PROJECT-STRUCTURE.md   # This file
│   ├── specs/
│   │   ├── PRD_v0.1.md        # Product Requirements Document
│   │   └── TSD_v0.1.md        # Technical Specifications Document
│   └── plans/
│       ├── implementation-plan_v0.1.md
│       └── test-plan_v0.1.md
│
├── rules/                     # Governance rules for agents and humans
│   ├── PROGRAMMING-PRINCIPLES.md
│   ├── PROJECT-RULES.md
│   └── GIT-RULES.md
│
├── .claude/
│   ├── agents/                # Agent definitions (tech-lead, backend, frontend, etc.)
│   ├── commands/apf/          # APF slash commands
│   └── shared/apf/            # Shared context loaded by agents
│
└── .apf/                      # APF framework files (preparation, templates, state)
    ├── STATE-v0.1.md          # Preparation progress tracker
    ├── CLAUDE.apf.md          # APF-specific Claude instructions
    └── preparation/           # Preparation workflow and templates
```
