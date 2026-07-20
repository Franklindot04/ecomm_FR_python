# Contributing Guidelines

Thank you for your interest in contributing to the Ecommerce Microservice API.

This project is a learning-oriented FastAPI ecommerce backend developed incrementally through milestone-based stages. Contributions, feedback, and constructive discussion are welcome.

## Before You Start

Before making a contribution:

1. Read the project `README.md`.
2. Check the existing issues and pull requests to avoid duplicating work.
3. For larger changes, open or discuss an issue first so the proposed direction is clear.
4. Keep contributions focused and aligned with the project's current architecture and development goals.

## Development Setup

### Requirements

The project currently uses:

* Python
* FastAPI
* SQLite
* SQLAlchemy
* Alembic
* Redis
* Docker
* Docker Compose
* Pytest

### Local Setup

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd ecommerce-api
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create the local environment file from the committed example:

```bash
cp .env.example .env
```

Adjust the values in `.env` as needed for your local environment.

## Running the Application

Start the FastAPI application with:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Swagger UI is available at:

```text
http://localhost:8000/docs
```

## Running with Docker

The application can also be started with Docker Compose:

```bash
docker compose up --build
```

Redis is included as a Compose service.

The API service uses the Redis healthcheck to improve startup readiness.

## Database Migrations

Apply the current database schema with:

```bash
alembic upgrade head
```

Check the current migration revision with:

```bash
alembic current
```

If your contribution changes the database schema, include the appropriate Alembic migration with the change.

Do not manually edit existing migration history unless the change is specifically intended to correct migration history and has been discussed beforehand.

## Running Tests

Run the full test suite with:

```bash
pytest -q
```

All contributions should preserve the existing test suite.

When adding or changing functionality, add or update tests where appropriate.

The project uses:

* An isolated SQLite test database.
* FastAPI dependency overrides.
* Shared pytest fixtures.
* An in-memory `FakeRedis` test client for Redis-dependent tests.

## Branching and Pull Requests

Create a focused branch for each change:

```bash
git checkout main
git pull origin main
git checkout -b <type>/<short-description>
```

Examples:

```text
feature/payment-webhook
fix/cart-stock-validation
docs/update-readme
refactor/order-service
```

Keep branches focused on one logical change whenever possible.

### Pull Request Expectations

Pull requests should:

* Clearly describe what changed.
* Explain why the change was made.
* Include relevant testing or verification details.
* Keep unrelated changes out of the pull request.
* Update documentation when behavior or project structure changes.
* Include database migrations when schema changes are introduced.

Before opening a pull request, verify:

```bash
git status
pytest -q
```

Review the final diff:

```bash
git diff main...HEAD
```

## Commit Messages

Use clear and descriptive commit messages.

The project generally follows a conventional style such as:

```text
feat: add payment workflow
fix: correct cart stock validation
docs: update contributing guide
refactor: extract order service
test: add payment endpoint coverage
```

Keep the commit message focused on the actual change.

## Code Style and Design

When contributing code:

* Prefer clear and readable Python.
* Keep route handlers focused on HTTP concerns.
* Place reusable business logic in the service layer where appropriate.
* Use existing project patterns before introducing new abstractions.
* Preserve existing API behavior unless a breaking change is intentional and documented.
* Avoid unnecessary dependencies.
* Keep configuration environment-driven.
* Do not commit secrets or local environment files.

## Documentation

Documentation is part of the project.

Update the relevant documentation when a contribution changes:

* API behavior.
* Configuration.
* Database migrations.
* Docker or local setup.
* Project architecture.
* Development workflows.

## Issues and Feature Requests

When opening an issue, provide as much useful context as possible.

For bug reports, include:

* A clear description of the problem.
* Steps to reproduce the issue.
* Expected behavior.
* Actual behavior.
* Relevant error messages or logs.
* Environment details where relevant.

For feature requests, explain the problem the feature would solve and describe the proposed behavior.

## Review Process

Pull requests may be reviewed for:

* Correctness.
* Maintainability.
* Test coverage.
* Architectural consistency.
* Documentation quality.
* Scope and clarity.

Constructive review feedback is encouraged. Contributors are expected to respond to review discussions professionally and make reasonable adjustments where appropriate.

## Thank You

Thank you for contributing to the Ecommerce Microservice API and helping improve the project.
