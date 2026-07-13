# Ecommerce Microservice API

A learning-oriented ecommerce microservice built with FastAPI, SQLite, SQLAlchemy, Alembic, Redis, and Docker.

The project is being developed incrementally through milestone-based stages, gradually evolving from a simple MVP into a more realistic ecommerce backend while keeping the codebase clean, documented, testable, portable, and easy to extend.

---

## Features

### Products API
- Create products.
- Retrieve all products.
- Retrieve a single product.
- Pydantic validation.
- Seeded demo inventory.
- Redis-backed caching for product list and product detail retrieval.

### Shopping Cart API
- Add products to cart.
- Merge duplicate cart items.
- View cart contents.
- Remove individual items.
- Clear entire cart.
- Validate stock availability.

### Orders API
- Checkout cart items.
- Validate stock during checkout.
- Create order records and order items.
- Persist order history.
- Decrement inventory.
- Clear cart after purchase.
- Retrieve all orders.
- Retrieve individual orders.
- Nested serialization using eager loading.
- Cache invalidation after inventory-changing operations.

### Order Lifecycle API
- Order status support.
- Status transitions.
- Order cancellation rules.
- State-machine style workflow validation.
- Swagger-visible status fields.

### Authentication API
- User registration.
- User login.
- JWT access tokens.
- Password hashing with bcrypt.
- Protected user route.
- Swagger OAuth2 password flow.
- Redis-backed login rate limiting.

### Multi-user Ecommerce API
- User-owned cart items.
- User-owned orders.
- User-scoped cart access.
- User-scoped order access.
- Per-user checkout flow.
- Ownership protection for order retrieval and updates.
- Protected cart and order endpoints.

### Architecture Improvements
- Service-layer extraction for cart logic.
- Service-layer extraction for order logic.
- Thinner route handlers.
- Cleaner separation of concerns.
- Improved maintainability for future scaling.
- Preserved existing API behavior after refactor.
- Dedicated Redis client and cache utility helpers.

### Database Migration Support
- Alembic integration for schema migrations.
- Initial baseline migration.
- SQLite-compatible migration configuration.
- Database revision tracking with `alembic_version`.
- Version-controlled schema evolution for future changes.

### Testing
- Pytest-based automated test suite.
- Shared fixtures with `conftest.py`.
- Isolated SQLite test database.
- FastAPI dependency overrides for test isolation.
- In-memory `FakeRedis` test client for cache and rate-limit isolation.
- Auth, products, cart, and orders endpoint coverage.
- CI-ready test baseline.

### Docker Support
- Dockerized FastAPI application.
- `Dockerfile` for container image builds.
- `docker-compose.yml` for local container orchestration.
- Redis service included in Docker Compose.
- `.dockerignore` for cleaner build context.
- Environment-variable-based configuration.
- Container healthcheck using `/health`.

### Infrastructure
- SQLite database.
- SQLAlchemy ORM.
- Alembic migrations.
- Redis caching.
- Redis-backed rate limiting.
- Pydantic schemas.
- Dependency injection.
- Seed initialization.
- Swagger/OpenAPI documentation.
- Docker.
- Docker Compose.
- Environment variables.
- Container healthchecks.

Swagger UI available at:

```text
/docs
```

---

## Running Tests

Run the full automated test suite with:

```bash
pytest -q
```

Current baseline:
- 9 tests passing.
- Coverage includes authentication, products, cart, and orders.
- Tests run against an isolated SQLite test database using shared fixtures and FastAPI dependency overrides.
- Redis-dependent features are tested with an in-memory `FakeRedis` client.
- The test suite runs against the FastAPI app directly and does not require starting the server manually.

---

## Running with Docker

Build and start the containerized application with:

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

Useful endpoints:
- `/docs`
- `/health`

Current Docker baseline:
- Containerized FastAPI app.
- Redis included as a Compose service.
- Environment variables loaded from `.env`.
- Healthcheck enabled for container validation.

---

## Status

### Completed Milestones

✅ Stage 1 — FastAPI Base Setup  
Completed: 2026-06-18

Implemented:
- FastAPI application.
- SQLite database.
- SQLAlchemy setup.
- Database session dependency.
- Health endpoint.
- Seed mechanism.
- Swagger documentation.

---

✅ Stage 2 — Products API  
Completed: 2026-06-19

Implemented:
- Product model.
- CRUD operations.
- Validation schemas.
- Seeded demo products.

---

✅ Stage 3 — Cart System  
Completed: 2026-06-20

Implemented:
- Add to cart.
- Merge duplicate items.
- View cart.
- Remove item.
- Clear cart.
- Stock validation.

---

✅ Stage 4 — Orders System and Router Refactor  
Completed: 2026-06-26

Implemented:
- Checkout endpoint.
- Order creation.
- Order items.
- Inventory decrement.
- Empty cart after checkout.
- Nested serialization.
- Eager loading.
- Router modularization.
- Products router.
- Cart router.
- Orders router.
- Reduced `main.py` complexity.
- Preserved existing API behavior.
- Preserved OpenAPI compatibility.

---

✅ Stage 5 — Order Lifecycle Management  
Completed: 2026-06-29

Implemented:
- Order status support.
- `PENDING`, `PAID`, `PROCESSING`, `SHIPPED`, `DELIVERED`, `CANCELLED` statuses.
- `PATCH /orders/{id}/status`.
- `POST /orders/{id}/cancel`.
- Transition validation.
- Cancellation rules.
- Swagger verification of order status workflow.

---

✅ Stage 6 — Authentication  
Completed: 2026-07-03

Implemented:
- User model.
- User registration.
- User login.
- Password hashing.
- JWT token generation.
- OAuth2 password flow in Swagger.
- Protected route: `GET /auth/me`.
- Token-based user lookup.

---

✅ Stage 7 — Multi-user Ecommerce  
Completed: 2026-07-07

Implemented:
- User ownership for cart items.
- User ownership for orders.
- Authenticated cart endpoints.
- Authenticated order endpoints.
- User-scoped cart queries.
- User-scoped order queries.
- Per-user checkout behavior.
- Ownership checks for order access and modification.
- Swagger-documented 404 responses for inaccessible orders.

---

✅ Stage 8 — Architecture Refactor  
Completed: 2026-07-08

Implemented:
- Service-layer extraction for cart logic.
- Service-layer extraction for order logic.
- `app/services/cart_service.py`.
- `app/services/order_service.py`.
- Thinner API route handlers.
- Cleaner separation between routing and business logic.
- Preserved Swagger behavior.
- Preserved multi-user ownership isolation.
- Improved maintainability and extensibility.

---

✅ Stage 9 — Alembic  
Completed: 2026-07-09

Implemented:
- Alembic installation and initialization.
- Migration environment setup.
- SQLAlchemy metadata integration.
- Initial baseline migration.
- Database version tracking with `alembic_version`.
- SQLite-compatible migration configuration.

---

✅ Stage 10 — Testing  
Completed: 2026-07-10

Implemented:
- Pytest installation and test setup.
- `httpx` test dependency support.
- Shared fixtures in `tests/conftest.py`.
- Dedicated SQLite test database for isolated test runs.
- FastAPI dependency overrides for database isolation.
- Refactored auth database access to use dependency injection.
- Endpoint tests for authentication flows.
- Endpoint tests for product retrieval.
- Endpoint tests for cart operations.
- Endpoint tests for order creation and retrieval.
- Verified passing test baseline with 9 total tests.

---

✅ Stage 11 — Docker  
Completed: 2026-07-11

Implemented:
- Added `Dockerfile` for containerizing the FastAPI app.
- Added `docker-compose.yml` for local container orchestration.
- Added `.dockerignore` to reduce Docker build context noise.
- Updated `.gitignore` for local environment and cache hygiene.
- Moved database configuration to environment variables.
- Moved auth configuration to environment variables.
- Added `.env`-driven runtime configuration.
- Added Docker healthcheck using the `/health` endpoint.
- Verified successful container build and healthy runtime state.

---

✅ Stage 12 — Redis Caching & Rate Limiting  
Completed: 2026-07-13

Implemented:
- Added Redis integration for application caching.
- Added Redis-backed caching for product list and product detail endpoints.
- Added cache invalidation after inventory-changing operations.
- Added Redis-backed login rate limiting.
- Added Redis service to `docker-compose.yml`.
- Added `app/redis_client.py` for centralized Redis client configuration.
- Added cache utility support for invalidation workflows.
- Updated tests to use an in-memory `FakeRedis` client.
- Verified passing test baseline with Redis-aware test isolation.

---

## Current Architecture

### Application

```text
app/
├── api/                    # API route handlers
│   ├── __init__.py
│   ├── auth.py             # Authentication endpoints
│   ├── products.py         # Product endpoints with caching
│   ├── cart.py             # User-scoped cart endpoints
│   └── orders.py           # User-scoped order endpoints
├── services/               # Business logic layer
│   ├── __init__.py
│   ├── cart_service.py     # Cart business logic
│   └── order_service.py    # Order business logic
├── auth_utils.py           # Password hashing, JWT, auth dependency
├── cache_utils.py          # Cache invalidation helpers
├── database.py             # Database connection/session setup
├── main.py                 # FastAPI application entry point
├── models.py               # SQLAlchemy models
├── redis_client.py         # Redis client setup
├── rate_limiter.py         # Login rate limiting dependency
├── schemas.py              # Pydantic schemas
└── seed.py                 # Seed initial product data

alembic/
├── env.py                  # Alembic environment configuration
├── script.py.mako          # Migration template
└── versions/               # Migration revision files

tests/
├── __init__.py
├── conftest.py             # Shared pytest fixtures, test DB setup, FakeRedis
├── test_auth.py            # Authentication endpoint tests
├── test_products.py        # Product endpoint tests
├── test_cart.py            # Cart endpoint tests
└── test_orders.py          # Order endpoint tests
```

### Root Files

```text
requirements.txt        # Python dependencies
Dockerfile              # Docker image definition
docker-compose.yml      # Local container orchestration
.dockerignore           # Docker build context exclusions
.env                    # Local environment variables (not committed)
alembic.ini             # Alembic configuration
ecommerce.db            # SQLite database (dev only)
README.md               # Project documentation
```

The router modularization was introduced after Stage 4, the service layer was added in Stage 8, Alembic migration support was added in Stage 9, automated testing support was added in Stage 10, Docker support was added in Stage 11, and Redis-backed caching and rate limiting were added in Stage 12 to improve maintainability, separation of concerns, schema evolution workflow, regression safety, portability, performance, and basic abuse protection.

---

## Development Roadmap

| Stage | Description | Status |
| --- | --- | --- |
| 1 | FastAPI Setup | ✅ |
| 2 | Products API | ✅ |
| 3 | Cart System | ✅ |
| 4 | Orders System and Router Refactor | ✅ |
| 5 | Order Lifecycle Management | ✅ |
| 6 | Authentication | ✅ |
| 7 | Multi-user Ecommerce | ✅ |
| 8 | Architecture Refactor | ✅ |
| 9 | Alembic | ✅ |
| 10 | Testing | ✅ |
| 11 | Docker | ✅ |
| 12 | Caching | ✅ |
| 13 | Background Tasks | 🚧 |
| 14 | Mock Payments | 🚧 |
| 15 | Production Readiness | 🚧 |

---

## Next Milestone

### Stage 13 — Background Tasks

Planned focus:
- Introduce background processing for non-blocking tasks.
- Decouple post-request work from synchronous API responses.
- Prepare the project for email, notifications, and async-style workflows.
- Continue improving realism of the ecommerce backend.

Skills expected:
- FastAPI background task patterns.
- Separation of synchronous and deferred work.
- Side-effect handling.
- Backend workflow design.

---

## Last Updated

2026-07-13 – completed Redis caching and login rate limiting (Stage 12)

2026-07-11 – completed Docker containerization (Stage 11)

2026-07-10 – completed testing baseline with pytest (Stage 10)

2026-07-09 – completed Alembic integration (Stage 9)

2026-07-08 – completed architecture refactor (Stage 8)

2026-07-07 – completed multi-user ecommerce (Stage 7)

2026-07-03 – completed Authentication (Stage 6)

2026-06-30 – completed order lifecycle management (Stage 5)

2026-06-26 – completed orders system and router refactor (Stage 4)

2026-06-20 – completed Cart System (Stage 3)

2026-06-19 – completed Products API (Stage 2)

2026-06-18 – completed FastAPI Base Setup (Stage 1)

---

## Tech Stack

- Python.
- FastAPI.
- SQLite.
- SQLAlchemy.
- Alembic.
- Redis.
- Pydantic.
- Dependency injection.
- JWT.
- OAuth2 password flow.
- Password hashing.
- Swagger/OpenAPI.
- Service-layer architecture.
- Pytest.
- HTTPX.
- Automated API testing.
- Docker.
- Docker Compose.
- Environment variables.
- Container healthchecks.
- Caching.
- Rate limiting.