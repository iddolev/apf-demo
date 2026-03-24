# Programming Principles

These principles apply to all agents that create code (e.g. backend, frontend, testing, etc.)
and to all agents that review code (e.g. code reviewer, security expert).
Read this file before creating or reviewing code.

## Workflow

### 1. Understand Before Writing

- Read the task requirements completely before touching code.
- Read existing code in the affected areas. Understand current
  patterns, naming conventions, and architectural decisions.
- Identify dependencies, side effects, and integration points.
- If the task plan is ambiguous or incomplete, seek clarification
  before proceeding.

### 2. Implement Incrementally

- Write code in small, testable units.
- Follow existing project patterns rigorously. Place files in
  their correct directories.
- Keep functions focused — each does one thing well.
- Write code that is testable — use dependency injection, avoid
  global state, make components mockable.

### 3. Self-Review Before Presenting

Before considering a task complete, verify:

- [ ] Code follows existing project patterns and conventions
- [ ] All functions have type hints / type annotations
- [ ] Public classes and functions have docstrings
- [ ] Error handling is comprehensive and secure
- [ ] No hardcoded secrets, API keys, or credentials
- [ ] No debug statements or console.log left in code
- [ ] Edge cases are handled (empty inputs, timeouts, failures)
- [ ] Code is in the correct project structure

## Code Quality

- Write clean, readable, self-documenting code with meaningful names.
- DRY — extract shared logic into reusable utilities or services.
- Use proper typing / type annotations throughout.
- Add comments only where the "why" isn't obvious from the code.
- Public classes and functions get docstrings.

## Code Organization

- Follow the existing project structure rigorously. Place files in
  their correct directories.
- Separate concerns: business logic never lives in controllers
  or route handlers.
- Keep configuration separate from logic. Use environment variables
  and config files.
- Use dependency injection for testability and decoupling.
- Create well-defined interfaces / contracts between modules.

## Error Handling

- Use a consistent error handling strategy across the codebase.
- Create custom error types for different error categories
  (ValidationError, NotFoundError, AuthorizationError, etc.).
- Catch exceptions at module boundaries — never let raw library
  exceptions propagate to the API layer.
- Log errors with sufficient context for debugging (request ID,
  user context, operation details).
- Return generic error messages to clients; log details server-side.

## Security

This is a local-only solo MVP with no user data, no authentication, and no external input.
Apply STANDARD security practices:

- **Secrets management**: Never hardcode secrets, API keys, or credentials.
  Use environment variables or secret management. *(No secrets in this project, but
  maintain the habit.)*
- **Input validation**: Validate and sanitize external input at the boundary.
  *(This project has no user-supplied input to the backend, but apply if any is added.)*
- **Error exposure**: Never expose internal stack traces or system information to clients.
- **Injection prevention, auth checks, data protection**: Not applicable to this project
  scope (no DB, no auth, no PII). Apply if scope changes.

## Performance

- Use async / non-blocking operations for I/O-bound tasks.
- Minimize unnecessary data transfer — return only what the
  client needs.
- No premature optimization — write correct, clear code first.
  Optimize only with evidence.
- Avoid N+1 query problems. Use proper indexing strategies.
  Use pagination for list endpoints.
- Consider connection pooling for database and external service
  connections.
