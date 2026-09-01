# Project instructions

## Environment variables

This repo has two subprojects, each with its own env files: [back_movie_review/](back_movie_review/) and [front_movie_review/](front_movie_review/).

- `.env` — local values, gitignored, never committed.
- `.env.example` — committed, mirrors every key in `.env` with a safe/default value.

When adding any configuration value that varies by environment or deployment (secrets, hostnames, URLs, ports, feature flags, API keys, allowed origins, etc.):

1. Read it from an environment variable in code instead of hardcoding it (backend: via `django-environ`, already wired in `settings.py`; frontend: via Vite's `import.meta.env`, requires a `VITE_` prefix).
2. Add the variable to that subproject's `.env` with the working local value.
3. Add the same key to that subproject's `.env.example` with a safe placeholder/default.
4. Never commit real secrets in `.env.example`.

Do not add env vars for values that are architectural/code-level (installed apps, middleware order, URL routes, component structure) — only for things that differ between environments or machines.
