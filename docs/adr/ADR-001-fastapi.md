# ADR-001: FastAPI as Backend Framework

**Date:** 2026-04-21
**Status:** Accepted

---

## Context

StepUp requires a backend framework for Python 3.11. The framework needs to handle async database operations (SQLAlchemy 2.0 async), serve a RESTful API consumed by a React frontend, validate request/response data, and auto-generate API documentation for development and portfolio purposes.

Three options were considered: FastAPI, Django REST Framework, and Flask.

---

## Decision

We use **FastAPI**.

---

## Alternatives Considered

**Django REST Framework**
Django is a batteries-included framework with a large ecosystem. However, its ORM is synchronous by default, adding complexity when using async SQLAlchemy. Django's admin and templating system add overhead that is not needed for a pure API backend. Configuration is heavier for a greenfield API project.

**Flask**
Flask is lightweight and flexible but requires assembling many third-party libraries for validation, serialization, and documentation. This increases maintenance surface without providing meaningful benefits over FastAPI for this use case.

---

## Consequences

**Gained:**
- Native async support — aligns with SQLAlchemy 2.0 async and asyncpg driver
- Automatic Swagger UI at `/docs` with zero extra configuration — useful for development and portfolio demos
- Pydantic integration for request/response validation and serialization out of the box
- Type hints throughout the codebase improve IDE support and catch errors early
- Faster to build and iterate compared to Django for a pure API project

**Trade-offs:**
- Smaller ecosystem than Django — fewer built-in solutions for edge cases
- No built-in admin interface — not needed for this project but worth noting
- FastAPI is newer than Django/Flask — slightly less Stack Overflow coverage for obscure issues